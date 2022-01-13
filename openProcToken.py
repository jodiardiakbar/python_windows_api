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

# Token Access Rights
STANDARD_RIGHTS_REQUIRED = 0x000F0000
STANDARD_RIGHTS_READ = 0x00020000
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATION = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED |
					TOKEN_ASSIGN_PRIMARY     |
					TOKEN_DUPLICATE          |
					TOKEN_IMPERSONATION      |
					TOKEN_QUERY              |
					TOKEN_QUERY_SOURCE       |
					TOKEN_ADJUST_PRIVILEGES  |
					TOKEN_ADJUST_GROUPS      |
					TOKEN_ADJUST_DEFAULT     |
					TOKEN_ADJUST_SESSIONID)

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

# Open a Handle to Process's Token Directly
ProcessHandle = hProcess
DesiredAccess = TOKEN_ALL_ACCESS
TokenHandle = ctypes.c_void_p()

# Call OpenAccessToken function
response = kernel_Handle.OpenProcessToken(ProcessHandle, DesiredAccess, ctypes.byref(TokenHandle))

# Error Handling
if response <= 0:
	print(f"[ERROR] Could not Grab Token! Error Code: {kernel_Handle.GetLastError()}")
else:
	print(f"[INFO] Handle to Process Token Created!")