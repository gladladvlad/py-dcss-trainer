import sys
import os
import ctypes

############### UAC RELATED ############
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([script] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if not is_admin():
    get_admin()
    #sys.exit()
########################################

from bin_buf import *

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
##########################################################
HP_ADDR = 0x011FC9A4
HP_WRITE_ADDR = 0x00807A28

HP_SUB_ADDR = 0x00807A24
HP_INSTAKILL = bin_buf("0x29C0")
HP_NORMAL = bin_buf("0x29F0")

PC_HP_NORMAL_ADDR = 0x008655F0
PC_HP_NORMAL = bin_buf("A3 543C1C01")

PC_HP_POISON_NORMAL_ADDR = 0x00865DD1
PC_HP_POISON_NORMAL = bin_buf("89 1D 543C1C01")
############### init stuff ###########################
if len(sys.argv) != 2:
    proc_id = int(input().strip())
else:
    proc_id = int(sys.argv[1].strip())

print("opening proc {}...".format(proc_id))

proc_handle = OP(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, False, proc_id)


if proc_handle == 0:
        print("no proc!")
        print(ctypes.WinError(ctypes.get_last_error()))
        sys.exit()

#################### functions for patches ##########
def switch_dmg():
    print("reading memory")
    read_buf = ctypes.create_string_buffer(4)
    bytes_read = ctypes.c_size_t()
    RPM(proc_handle, HP_SUB_ADDR, read_buf, 4, ctypes.byref(bytes_read))
    print(ctypes.WinError(ctypes.get_last_error()), end="\n\n") 

    for i in range(0, 4):
        print("{:02X} ".format(ord(read_buf[i])), end="")
    print(end="\n\n")


    bytes_written = ctypes.c_size_t()
    if read_buf[:2] == HP_NORMAL:
        print("normal; switching to insta")
        WPM(proc_handle, HP_SUB_ADDR, HP_INSTAKILL, 2, ctypes.byref(bytes_written))

    if read_buf[:2] == HP_INSTAKILL:
        print("insta; switching to normal")
        WPM(proc_handle, HP_SUB_ADDR, HP_NORMAL, 2, ctypes.byref(bytes_written))

    print(ctypes.WinError(ctypes.get_last_error()), end="\n\n")
#########################################################


######################################################
cmd = ""
while cmd == "" or cmd[0] != "exit":
    cmd = input(">>>>>")
    if cmd == "":
        continue

    cmd = cmd.strip().split()

    if cmd[0] == "damage":
        switch_dmg()

