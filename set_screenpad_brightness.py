import ctypes
import ctypes.wintypes

COMMAND_SET_BRIGHTNESS = 0x50032

DEVICE_DRIVER = ctypes.wintypes.LPCWSTR('\\\\.\\ATKACPI')
DEVICE_DESIRED_ACCESS = ctypes.wintypes.DWORD(0xc0000000)
DEVICE_SHARE_MODE = ctypes.wintypes.DWORD(3)
DEVICE_SECURITY_ATTRIBUTES = None
DEVICE_CREATION_DISPOSITION = ctypes.wintypes.DWORD(3)
DEVICE_FLAGS = ctypes.wintypes.DWORD(0)
DEVICE_HANDLE = None


def execute_device_command(command, arg1, arg2):
    kernel32 = ctypes.WinDLL('kernel32')

    # Open driver handle
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


        #
        if driver_handle == ctypes.wintypes.DWORD(0xf):
            kernel32.CloseHandle(driver_handle)
            driver_handle = None
