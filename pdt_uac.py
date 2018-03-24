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

########################################
