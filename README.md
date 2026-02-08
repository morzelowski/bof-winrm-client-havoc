# BOF WinRM Client for Havoc C2

This is a port of the [FalconForceTeam/bof-winrm-client](https://github.com/FalconForceTeam/bof-winrm-client) to Havoc C2. 
It implements a WinRM shell client using Windows APIs via a Beacon Object File (BOF).

## Features

*   Executes commands on remote systems via WinRM using BOF.
*   Supports `x64` architecture.
*   Implements timeout handling (30s) to prevent beacon hanging on unreachable hosts.

## Build

To compile the BOF (requires `x86_64-w64-mingw32-g++`):

```bash
cd bof-winrm-client
make
```

This will generate `bof.x64.o` in the project root.

## Usage

1.  Load the `bof-winrm-client.py` script into Havoc.
2.  Run the command from the Havoc console:

```
winrm-client --host <hostname> --cmd <command>
```

**Example:**

```
winrm-client --host ws.mini.lab --cmd "whoami /all"
```

## Credits

*   Original Author: [FalconForceTeam](https://github.com/FalconForceTeam/bof-winrm-client)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.