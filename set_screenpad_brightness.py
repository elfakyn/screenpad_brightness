import ctypes
import ctypes.wintypes
import struct
import sys

INPUT_BUFFER_SIZE = 0x10
OUTPUT_BUFFER_SIZE = 0x400
DWORD_SIZE = 4

COMMAND_ASUS_CONTROL = 0x53564544
COMMAND_SET_BRIGHTNESS = 0x50032

DEVICE_DRIVER = ctypes.wintypes.LPCWSTR('\\\\.\\ATKACPI')
DEVICE_DESIRED_ACCESS = ctypes.wintypes.DWORD(0xc0000000)
DEVICE_SHARE_MODE = ctypes.wintypes.DWORD(3)
DEVICE_SECURITY_ATTRIBUTES = None
DEVICE_CREATION_DISPOSITION = ctypes.wintypes.DWORD(3)
DEVICE_FLAGS = ctypes.wintypes.DWORD(0)
DEVICE_HANDLE = None

DEVICE_CONTROL_CODE = ctypes.wintypes.DWORD(0x22240c)
DEVICE_LPOVERLAPPED = None

def change_brightness(brightness_value):
    execute_device_command(COMMAND_SET_BRIGHTNESS, brightness_value)

def execute_device_command(command_id, command_parameter):
    kernel32 = ctypes.WinDLL('kernel32')

    driver_handle = kernel32.CreateFileW(
        DEVICE_DRIVER,
        DEVICE_DESIRED_ACCESS,
        DEVICE_SHARE_MODE,
        DEVICE_SECURITY_ATTRIBUTES,
        DEVICE_CREATION_DISPOSITION,
        DEVICE_FLAGS,
        DEVICE_HANDLE
    )

    if driver_handle != ctypes.wintypes.DWORD(-1):
        if driver_handle != ctypes.wintypes.DWORD(0):
            command = struct.pack(
                '<IIII',
                COMMAND_ASUS_CONTROL,
                8,
                command_id,
                command_parameter
            )

            device_input_buffer = ctypes.create_string_buffer(command)
            device_output_buffer = ctypes.create_string_buffer(b'\x00' * OUTPUT_BUFFER_SIZE)

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

        if driver_handle == ctypes.wintypes.DWORD(0xf):
            kernel32.CloseHandle(driver_handle)
            driver_handle = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a value between 0 and 255.")

    change_brightness(int(sys.argv[1]))
