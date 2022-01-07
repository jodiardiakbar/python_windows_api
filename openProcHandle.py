import ctypes

# interacting with Processes, File Systems, Threads
kernel_handle = ctypes.windll("Kernel32.dll")

# process security and access rights
PROCESS_ALL_ACCESS = (0x000F0000L | 0x00100000L | 0xFFFF)

# parameters for OpenProcess function
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False

# grep from window task manager, in hexadecimal
PID = input("Insert PID number you want to handle: ")
dwProcessId = int(hex(int(PID)))
print(f"dwProcessId = {dwProcessId}")

# error handling
error = kernel_handle.GetLastError()
if error != 0:
    print(f"Err Code: {error}")
    exit(1)

# response result
response = kernel_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)
if response <= 0:
    print(f"Handle was not created, response = {response}")
else:
    print(f"Handle created !, response = {response}")