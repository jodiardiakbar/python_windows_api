import ctypes
from ctypes.wintypes import HANDLE, DWORD, WORD, LPSTR, LPBYTE
# from ctypes.wintypes import HANDLE, DWORD, WORD, LPWSTR, LPBYTE

kernel_handle = ctypes.windll("Kernel32.dll")

"""
typedef struct _STARTUPINFOA {
  DWORD  cb;
  LPSTR  lpReserved;
  LPSTR  lpDesktop;
  LPSTR  lpTitle;
  DWORD  dwX;
  DWORD  dwY;
  DWORD  dwXSize;
  DWORD  dwYSize;
  DWORD  dwXCountChars;
  DWORD  dwYCountChars;
  DWORD  dwFillAttribute;
  DWORD  dwFlags;
  WORD   wShowWindow;
  WORD   cbReserved2;
  LPBYTE lpReserved2;
  HANDLE hStdInput;
  HANDLE hStdOutput;
  HANDLE hStdError;
} STARTUPINFOA, *LPSTARTUPINFOA;
"""
# structure for STARTUPINFOA
class STARTUPINFOA(ctypes.Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPSTR),
        ("lpDesktop", LPSTR),
        ("lpTitle", LPSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE)
    ]
startupinfoa_handle = STARTUPINFOA()

"""
typedef struct _PROCESS_INFORMATION {
  HANDLE hProcess;
  HANDLE hThread;
  DWORD  dwProcessId;
  DWORD  dwThreadId;
} PROCESS_INFORMATION, *PPROCESS_INFORMATION, *LPPROCESS_INFORMATION;
"""
# structure for _PROCESS_INFORMATION
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]
process_information_handle = PROCESS_INFORMATION()

"""
BOOL CreateProcessW(
  [in, optional]      LPCWSTR               lpApplicationName,
  [in, out, optional] LPWSTR                lpCommandLine,
  [in, optional]      LPSECURITY_ATTRIBUTES lpProcessAttributes,
  [in, optional]      LPSECURITY_ATTRIBUTES lpThreadAttributes,
  [in]                BOOL                  bInheritHandles,
  [in]                DWORD                 dwCreationFlags,
  [in, optional]      LPVOID                lpEnvironment,
  [in, optional]      LPCWSTR               lpCurrentDirectory,
  [in]                LPSTARTUPINFOW        lpStartupInfo,
  [out]               LPPROCESS_INFORMATION lpProcessInformation
);
"""
# setup parameters for CreateProcessW
lpApplicationName = "C:\\Windows\\System32\\cmd.exe"
lpCommandLine = None
lpProcessAttributes = None
lpThreadAttributes = None
bInheritHandles = False
dwCreationFlags = 0x00000010    # creating new console
lpEnvironment = None
lpCurrentDirectory = None
lpStartupInfo = STARTUPINFOA()
lpStartupInfo.wShowWindow = 0x1
lpStartupInfo.dwFlags = 0x1
lpProcessInformation = PROCESS_INFORMATION()

# lpStartupInfo and lpProcessInformation type is a pointer
# to pass the pointer always use ctypes.byref()

response = kernel_handle.CreateProcessW(
    lpApplicationName,
    lpCommandLine,
    lpProcessAttributes,
    lpThreadAttributes,
    bInheritHandles,
    dwCreationFlags,
    lpEnvironment,
    lpCurrentDirectory,
    ctypes.byref(lpStartupInfo),
    ctypes.byref(lpProcessInformation)
)

if response > 0:
    print(f"[INFO] Spawning Process...")
else:
    print(f"[ERROR] Failed to Spawn Process, Error Code: {kernel_handle.GetLastError()}")