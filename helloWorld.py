import ctypes

# interacting with GUI, fonts, windows, keyboard, mouse, etc
user_handle = ctypes.windll("User32.dll")

# interacting with Processes, File Systems, Threads
kernel_handle = ctypes.windll("Kernel32.dll")

# parameters for MessageBoxW function
hWnd = None
lpText = "Python and Windows API"
lpCaption = "PyWinAPI"
uType = 0x00000001 # OK CANCEL Box
# uType = 0x00000002 # ABORT RETRY IGNORE Box

# error handling
error = kernel_handle.GetLastError()
if error != 0:
    print(f"Err Code: {error}")
    exit(1)

# response result
response = user_handle.MessageBoxW(hWnd, lpText, lpCaption, uType)
if response == 1:
    print(f"User Clicked OK")
elif response == 2:
    print(f"User Clicked CANCEL")
