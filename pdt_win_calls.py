import ctypes

############### DECLARING THE WINAPI CALLS ###############
RPM = ctypes.WinDLL('kernel32', use_last_error=True).ReadProcessMemory
RPM.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
RPM.restype = ctypes.c_bool

WPM = ctypes.WinDLL('kernel32', use_last_error=True).WriteProcessMemory
WPM.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
WPM.restype = ctypes.c_bool


PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008

OP = ctypes.WinDLL('kernel32', use_last_error=True).OpenProcess
OP.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_int]
OP.restype = ctypes.c_int

CH = ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle
CH.argtypes = [ctypes.c_int]
CH.restype = ctypes.c_bool
##########################################################
