# Set the ASUS ScreenPad Brightness via the command line

Brightness Controller for ASUS ScreenPad Pro. This has been tested and works with the ASUS ZenBook Pro Duo UX851.

This program allows you to set the ScreenPad Pro brightness in Windows without the massive bloatware that is ScreenXpert.

Requires Python 3 on Windows.

Run `python .\set_screenpad_brigthness.py <VALUE>` where VALUE is between 0 (backlight off) and 255 (maximum brigthness).

THIS IS 64 BIT ONLY!!

## Technical explanation

ASUS uses the ATKACPI driver to control various devices, including the ScreenPad Pro. These controls, such as the ScreenPad brightness, don't show up in Windows natively.

By opening a handle to `\\.\ATKACPI` using CreateFileW, the device can be controlled.

The `execute_device_command` function is a wrapper around the driver controller functionality. In order to control the device, you need to send it a specially prepared DWORD buffer.

### Magic buffer to control the device

The magic buffer you want is an array of 4 DWORDS (that is, 0x10 bytes) and has the contents: `[0x53564544, 8, Command ID, Command Parameter]`. x64 is little-endian, so if your command ID is 0xdeadbeef and your parameter is 0xcacad0d0 then it will look like this in memory: (smaller addresses) `44 45 56 53 08 00 00 00 EF BE AD DE D0 D0 CA CA` (bigger addresses).

0x53564544 is the string "DEVS" (go figure).

The "8" represents the fact that the command you want to send will be 8 bytes (4 bytes of command ID and 4 bytes of command parameter).

The next 2 values are a command ID and a parameter value. See below for a list.


### Command IDs and parameters

This is a list of Command IDs I found by reverse engineering ASUSLibraService.exe. I have an idea of what they might do but I'm not sure.

Command ID | What the command ID does | What the command parameter does
--- | --- | ---
0x50031 | Touchscreen state? | ???
0x50032 | Set brightness | New brightness value, between 0x00 and 0xFF (bigger values wrap around).
0x50035 | Lid close action? | ???
0x100052 | ??? | ???

For example, to set the brigthness to maximum (0xFF), you want to send: `[0x53564544, 8, 0x50032, 0xFF]`. Which is: `DEVS\x08\x00\x00\x002\x00\x05\x00\xff\x00\x00\x00`

### Limitations and further research

There is little error handling if there are problems communicating with the driver.

To my knowledge there is not a mechanism to obtain the current brightness value, which I imagine is why the first time you launch the ASUS Libra Service (control software), it resets the brightness.

It may be possible to control other ASUS parameters too (I'm thinking turning the screenpad on and off, control the fans etc.), but I haven't looked into it yet.

If you want to take a look at it yourself, decompile AsusLibraService.exe and search for the string `Backlight` or `"\\\\.\\ATKACPI"`, you'll find the function pretty quickly.

## References and useful links

The ScreenPad Pro control scheme is eerily similar to Aura Sync. ASUS has an official [Aura SDK](https://www.ASUS.com/campaign/aura/us/AURA-ready.php) and OpenRGB [already has functionality to control the ATKACPI device driver, but for RGB purposes](https://gitlab.com/CalcProgrammer1/OpenRGB).
