CC_x64 := x86_64-w64-mingw32-g++
CFLAGS := -c -w -fpermissive
OUT_x64 := ../bof.x64.o

all:
	$(CC_x64) $(CFLAGS) bof.cpp -o $(OUT_x64)

clean:
	rm -f $(OUT_x64)
