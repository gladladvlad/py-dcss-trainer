import ctypes

from pdt_win_calls import *
from pdt_bin_buf import *

################ buffers and addresses for patches ################
HP_ADDR = 0x011FC9A4
HP_WRITE_ADDR = 0x00807A28

HP_SUB_ADDR = 0x00807A24
HP_INSTAKILL = bin_buf("0x29C0")
HP_NORMAL = bin_buf("0x29F0")

PC_HP_ADDR = 0x008655F0
PC_HP_NORMAL = bin_buf("A3 543C1C01")
PC_HP_GOD = bin_buf("90 90 90 90 90")

PC_HP_POISON_NORMAL_ADDR = 0x00865DD1
PC_HP_POISON_NORMAL = bin_buf("89 1D 543C1C01")

#################### functions for applying patches ##########
def switch_dmg(proc_handle):
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

##################### god mode ########################
def switch_god(proc_handle):
    print("reading memory")
    read_buf = ctypes.create_string_buffer(5)
    bytes_read = ctypes.c_size_t()
    RPM(proc_handle, PC_HP_ADDR, read_buf, 5, ctypes.byref(bytes_read))
    print(ctypes.WinError(ctypes.get_last_error()), end="\n\n") 

    for i in range(0, 5):
        print("{:02X} ".format(ord(read_buf[i])), end="")
    print(end="\n\n")


    bytes_written = ctypes.c_size_t()
    if read_buf[:5] == PC_HP_NORMAL:
        print("normal; switching to god")
        WPM(proc_handle, PC_HP_ADDR, PC_HP_GOD, 5, ctypes.byref(bytes_written))

    if read_buf[:5] == PC_HP_GOD:
        print("god; switching to normal")
        WPM(proc_handle, PC_HP_ADDR, PC_HP_NORMAL, 5, ctypes.byref(bytes_written))

    print(ctypes.WinError(ctypes.get_last_error()), end="\n\n")
