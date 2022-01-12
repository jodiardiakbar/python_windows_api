import ctypes
from ctypes.wintypes import HANDLE, DWORD, LPWSTR

kernel_handle = ctypes.windll("Kernel32.dll")
dns_handle = ctypes.windll("DNSAPI.dll")

class DNS_CACHE_ENTRY(ctypes.Structure):
    _fields_ = [
        ("pNext", HANDLE),
        ("recName", LPWSTR),
        ("wType", DWORD),
        ("wDataLength", DWORD),
        ("dwFlags", DWORD)
    ]

dce_handle = DNS_CACHE_ENTRY()
dce_handle.wDataLength = 1024
response = dns_handle.DnsGetCacheDataTable(ctypes.byref(dce_handle))

if response <= 0:
    print(f"[ERROR] Error Code: {kernel_handle.GetLastError()}")

dce_handle = ctypes.cast(dce_handle.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))

while True:
    try:
        print(f"DNS Entry: {dce_handle.contents.recName} - DNS Type: {dce_handle.contents.wType}")
        dce_handle = ctypes.cast(dce_handle.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))
    except:
        break
