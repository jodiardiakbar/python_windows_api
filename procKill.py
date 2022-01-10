"""
FindWindowA(lpClassName, lpWindowName) -> User32.dll
GetWindowThreadProcessId(hWnd, lpdwProcessId) -> User32.dll
OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId) -> Kernel32.dll
TerminateProcess(hProcess, uExitCode) -> Kernel32.dll

"""

# Import the required module to handle Windows API Calls
import ctypes

# Grab a handle to kernel32.dll & USer32.dll
user_handle = ctypes.windll("User32.dll")
kernel_Handle = ctypes.windll("Kernel32.dll")

# Access Rights
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

lpClassName = None
# Grab The Windows Name from User32
# for example : Task Manager
lpWindowName = ctypes.c_char_p(input("Enter Window Name to Kill: ").encode('utf-8'))

# Grab a Handle to the Process
hWnd = user_handle.FindWindowA(lpClassName, lpWindowName)

# Check to see if we have the Handle
if hWnd == 0:
	print(f"[ERROR] Could Not Grab Handle! Error Code: {kernel_Handle.GetLastError()}")
	exit(1)
else:
	print(f"[INFO] Grabbed Handle...")

# Get the PID of the process at the handle
lpdwProcessId = ctypes.c_ulong()
print(f"lpdwProcessId: {lpdwProcessId}")

# We use byref to pass a pointer to the value as needed by the API Call
response = user_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

# Check to see if the call Completed
if response == 0:
	print(f"[ERROR] Could Not Get PID from Handle! Error Code: {kernel_Handle.GetLastError()}")
	exit(1)
else:
	print(f"[INFO] Found PID...")

# Opening the Process by PID with Specific Access
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
dwProcessId = lpdwProcessId

# Calling the Windows API Call to Open the Process
hProcess = kernel_Handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

# Check to see if we have a valid Handle to the process
if hProcess <= 0:
	print(f"[ERROR] Could Not Grab Privileged Handle! Error Code: {kernel_Handle.GetLastError()}")
	exit(1)
else:
	print(f"[INFO] Privileged Handle Opened...")
	
# Send Kill to the process
uExitCode = 0x1

response = kernel_Handle.TerminateProcess(hProcess, uExitCode)

if response == 0:
	print(f"[ERROR] Could Not Kill Process! Error Code: {kernel_Handle.GetLastError()}")
	exit(1)
else:
	print(f"[INFO] Process Killed...")