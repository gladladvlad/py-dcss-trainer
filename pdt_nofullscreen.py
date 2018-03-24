from pdt_bin_buf import *

'''
use this function to create a patched game executable that runs in windowed mode
it's convenient when testing stuff :^)
'''
def create_windowed_exe (file_path):
    patch_addr = 0x006654FB
    patch = bin_buf("B8 22 20 00 00 90")
    file = open(file_path, "r+b")

    file.seek(patch_addr)
    file.write(patch)
    file.close()


'''
this one just reverts that change
'''
def create_full_exe (file_path):
    patch_addr = 0x006654FB
    patch = bin_buf("8B 85 54 FF FF FF")
    file = open(file_path, "r+b")

    file.seek(patch_addr)
    file.write(patch)
    file.close()
