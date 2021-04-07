# screenpadpro_brightness

Brightness Controller for ASUS ScreenPad Pro. This has been tested and works with the ASUS ZenBook Pro Duo UX851

This program allows you to set the ScreenPad Pro brightness in Windows without the massive bloatware that is ScreenXpert.

Run `python .\set_screenpad_brigthness.py <VALUE>` where VALUE is between 0 (backlight off) and 255 (maximum brigthness).

It may be possible to control other ASUS parameters too (I'm thinking turning the screenpad on and off, control the fans etc.), but I haven't looked into it yet. Maybe someone can build a neat GUI on top of it, or maybe I will.

## Technical explanation

ASUS uses the ATKACPI driver to control various devices, including the ScreenPad Pro. These controls, such as the ScreenPad brightness, don't show up in Windows natively.

By opening a handle to `\\.\ATKACPI` using CreateFileW, the device can be controlled.

The `execute_device_command` function is a wrapper around the driver controller functionality. In order to control the device, you need to send it a specially prepared DWORD buffer.

THIS IS x64 ONLY!!

### Magic buffer to control the device

The magic buffer you want is an array of 4 DWORDS (that is, 0x10 bytes) and has the contents: `[0x53564544, 8, Command ID, Command Parameter]`. This needs to be packed into a byte array.

0x53564544 is the string "DEVS" (go figure).

The "8" represents the fact that the command you want to send will be 8 bytes (4 bytes of command ID and 4 bytes of command parameter). See below for a list of values.

For example, to set the brigthness to maximum (0xFF), you want to send: `[0x53564544, 8, 0x50032, 0xFF]`.

### Command IDs and parameters

This is a list of Command IDs I found by reverse engineering ASUSLibraService.exe

Command ID | What the command ID does | What the command parameter does
--- | ---
0x50031 | Touchscreen state | ???
0x50032 | Set brightness | New brightness value, between 0x00 and 0xFF (bigger values wrap around).
0x50035 | Lid close action | ???
0x100052 | ??? | ???

To my knowledge there is not a mechanism to obtain the current brightness value, which I imagine is why the first time you launch the ASUS Libra Service (control software), it resets the brightness.

### Other Development

If you want to take a look at it yourself, decompile AsusLibraService.exe and search for the string `Backlight` or `"\\\\.\\ATKACPI"`, you'll find the function pretty quickly.

## References and useful links

The ScreenPad Pro control scheme is eerily similar to Aura Sync. ASUS has an official [Aura SDK](https://www.ASUS.com/campaign/aura/us/AURA-ready.php) and OpenRGB [already has functionality to control the ATKACPI device driver, but for RGB purposes](https://gitlab.com/CalcProgrammer1/OpenRGB).
