import ctypes
import ctypes.wintypes
import struct
import sys

KERNEL_32 = 'kernel32'

INPUT_BUFFER_SIZE = 0x10
OUTPUT_BUFFER_SIZE = 0x400
DWORD_SIZE = 4

COMMAND_STRUCTURE = '<IIII'
COMMAND_ASUS_CONTROL = 0x53564544
COMMAND_LENGTH = 8

COMMAND_SET_BRIGHTNESS = 0x50032
COMMAND_TURN_OFF = 0x50031
COMMAND_TURN_OFF_PARAMETER = 0

BRIGHTNESS_OFF = -1
BRIGHTNESS_MIN = 0
BRIGHTNESS_MAX = 255

HANDLE_INVALID = ctypes.wintypes.DWORD(-1)
HANDLE_NONE = ctypes.wintypes.DWORD(0)

DEVICE_DRIVER = ctypes.wintypes.LPCWSTR('\\\\.\\ATKACPI')
DEVICE_DESIRED_ACCESS = ctypes.wintypes.DWORD(0xc0000000)
DEVICE_SHARE_MODE = ctypes.wintypes.DWORD(3)
DEVICE_SECURITY_ATTRIBUTES = None
DEVICE_CREATION_DISPOSITION = ctypes.wintypes.DWORD(3)
DEVICE_FLAGS = ctypes.wintypes.DWORD(0)
DEVICE_HANDLE = None

DEVICE_CONTROL_CODE = ctypes.wintypes.DWORD(0x22240c)
DEVICE_LPOVERLAPPED = None

ARGUMENT_POSITION_BRIGHTNESS = 1

EXCEPTION_BRIGHTNESS_OOB = 'Brightness out of bounds'
ERROR_INVALID_BRIGHTNESS_VALUE = 'The brightness must be a number between 0 (backlight off) and 255 (maximum brightness). Or choose -1 to turn off the ScreenPad.'
ERROR_MISSING_BRIGHTNESS_PARAMETER = 'Please provide a brightness between 0 and 255, or choose -1 to turn off the ScreenPad. For example: python set_screenpad_brightness.py 200'
MESSAGE_TURN_OFF = 'Turning ScreenPad off. To turn it back on, provide a non-zero brightness value.'
ERROR_BAD_HANDLE = 'Error! Cannot connect to the ASUS ScreenPad Driver.'

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_BAD_HANDLE = 2


def execute_device_command(command_id, command_parameter):
    kernel32 = ctypes.WinDLL(KERNEL_32)

    driver_handle = kernel32.CreateFileW(
        DEVICE_DRIVER,
        DEVICE_DESIRED_ACCESS,
        DEVICE_SHARE_MODE,
        DEVICE_SECURITY_ATTRIBUTES,
        DEVICE_CREATION_DISPOSITION,
        DEVICE_FLAGS,
        DEVICE_HANDLE
    )

    if driver_handle == HANDLE_INVALID or driver_handle == HANDLE_NONE:
        print(ERROR_BAD_HANDLE)
        exit(EXIT_BAD_HANDLE)

    command = struct.pack(
        COMMAND_STRUCTURE,
        COMMAND_ASUS_CONTROL,
        COMMAND_LENGTH,
        command_id,
        command_parameter
    )

    device_input_buffer = ctypes.create_string_buffer(command, INPUT_BUFFER_SIZE)
    device_output_buffer = ctypes.create_string_buffer(OUTPUT_BUFFER_SIZE)
    num_returned_bytes = ctypes.wintypes.LPDWORD()

    kernel32.DeviceIoControl(
        driver_handle,
        DEVICE_CONTROL_CODE,
        device_input_buffer,
        ctypes.wintypes.DWORD(INPUT_BUFFER_SIZE),
        device_output_buffer,
        ctypes.wintypes.DWORD(OUTPUT_BUFFER_SIZE),
        num_returned_bytes,
        DEVICE_LPOVERLAPPED
    )

    kernel32.CloseHandle(driver_handle)
    driver_handle = None

if __name__ == "__main__":
    try:
        new_brightness = int(sys.argv[ARGUMENT_POSITION_BRIGHTNESS])

        if new_brightness == BRIGHTNESS_OFF:
            execute_device_command(COMMAND_TURN_OFF, COMMAND_TURN_OFF_PARAMETER)
            print(MESSAGE_TURN_OFF)
            exit(EXIT_OK)
        if new_brightness >= BRIGHTNESS_MIN and new_brightness <= BRIGHTNESS_MAX:
            execute_device_command(COMMAND_SET_BRIGHTNESS, new_brightness)
            exit(EXIT_OK)

        raise ValueError(EXCEPTION_BRIGHTNESS_OOB)

    except ValueError:
        print(ERROR_INVALID_BRIGHTNESS_VALUE)
        exit(EXIT_USAGE)
    except IndexError:
        print(ERROR_MISSING_BRIGHTNESS_PARAMETER)
        exit(EXIT_USAGE)

    exit(EXIT_OK)
