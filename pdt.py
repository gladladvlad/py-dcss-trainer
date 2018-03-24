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
        sys.exit()

######################################################
cmd = ""
while cmd == "" or cmd[0] != "exit":
    cmd = input(">>>>>")
    if cmd == "":
        continue

    cmd = cmd.strip().split()

    if cmd[0] == "damage":
        switch_dmg(proc_handle)
    if cmd[0] == "god":
        switch_god(proc_handle)


CH(proc_handle)
