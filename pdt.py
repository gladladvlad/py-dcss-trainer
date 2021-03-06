import sys
import os
import ctypes

from pdt_uac import *
from pdt_bin_buf import *
from pdt_win_calls import *
from pdt_patch import *

############## first, get admin rights #############
if not is_admin():
    get_admin()
    #leave commented for now
    #useful for debugging
    sys.exit()

############### init stuff ###########################
if len(sys.argv) != 2:
    proc_id = int(input("input pid: ").strip())
else:
    proc_id = int(sys.argv[1].strip())

print("opening proc {}...".format(proc_id))

proc_handle = OP(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, False, proc_id)

if proc_handle == 0:
        print("no proc!")
        print(ctypes.WinError(ctypes.get_last_error()))
        #sys.exit()

################# some patches #######################
god = patch(0x008655F0, bin_buf('90 90 90 90 90'), bin_buf('A3 543C1C01'))
instakill = patch(0x00807A24, bin_buf('29C0'), bin_buf('29F0'))
#hunger 011C4C78 
#wall 00A78D77
#xcoord 011C3BAC
#ycoord 011C3BB0
#map 0122B6D8
#wall: 07; floor: 21
######################################################
cmd = ""
while cmd == "" or cmd[0] != "exit":
    cmd = input(">>>>>")
    if cmd == "":
        continue

    cmd = cmd.strip().split()

    if cmd[0] == "damage":
        instakill.toggle(proc_handle)
    if cmd[0] == "god":
        god.toggle(proc_handle)
    if cmd[0] == "pos":
        get_xy(proc_handle)
    if cmd[0] == "modmap":
        if len(cmd) == 4:
            mod_map(proc_handle, int(cmd[1], 10), int(cmd[2], 10), bin_buf(cmd[3]))
        else:
            print("not enough args for modmap")
    if cmd[0] == "dig":
        digger_patch(proc_handle)

CH(proc_handle)
