import ctypes
import pdt_win_calls 
import pdt_bin_buf
import sys
import io

class patch:
    def __init__ (self, new_address, new_buffer_patch, new_buffer_normal=b''):
        self.address = int(new_address)
        self.buffer_patch = bytes(new_buffer_patch)
        self.buffer_normal = bytes(new_buffer_normal)
        if len(self.buffer_patch) != len(self.buffer_normal) and self.buffer_normal != b'':
            raise ValueError('patch and normal are different lengths!')
        self.buffer_size = len(self.buffer_patch)
        self.output = sys.stdout
        self.name = 'misc'

    def __len__ (self):
        return self.buffer_size

    def set_output (self, new_output):
        self.output = io.TextIOWrapper(new_output)

    def set_name (self, new_name):
        self.name = new_name

    def toggle (self, proc_handle):
        print("reading {} bytes at {:X}...".format(self.buffer_size, self.address), file=self.output)
        read_buffer = ctypes.create_string_buffer(self.buffer_size)
        bytes_read = ctypes.c_size_t()
        pdt_win_calls.RPM(proc_handle, self.address, read_buffer, self.buffer_size, ctypes.byref(bytes_read))
        print(ctypes.WinError(ctypes.get_last_error()), file=self.output)


        for i in range(0, self.buffer_size):
            print("{:02X} ".format(ord(read_buffer[i])), end="")
        print("\n\n")


        bytes_written = ctypes.c_size_t()

        if read_buffer[:self.buffer_size] == self.buffer_patch:
            if self.buffer_normal != b'':
                print("patched; reverting to normal...")
                pdt_win_calls.WPM(proc_handle, self.address, self.buffer_normal, self.buffer_size, ctypes.byref(bytes_written))
        else:
            print("normal; applying patch...")
            pdt_win_calls.WPM(proc_handle, self.address, self.buffer_patch, self.buffer_size, ctypes.byref(bytes_written))

        print(ctypes.WinError(ctypes.get_last_error()))
        print("{} bytes written".format(bytes_written))

    def apply (self, proc_handle):
        print("applying patch")
        pdt_win_calls.WPM(proc_handle, self.address, self.buffer_patch, self.buffer_size, ctypes.byref(bytes_written))


def get_xy (proc_handle):
    pos_address = 0x011C3BAC
    print("player is at position: (", end='')
    read_buffer = ctypes.create_string_buffer(8)
    bytes_read = ctypes.c_size_t()
    pdt_win_calls.RPM(proc_handle, pos_address, read_buffer, 8, ctypes.byref(bytes_read))
    print("{}, {})".format(int.from_bytes(read_buffer[:4], byteorder='little'), int.from_bytes(read_buffer[4:8], byteorder='little')))

#map 0122B6D8
#wall: 0x07; floor: 0x21
#tile is at map_address + 4 * (newX * 0x46 + newY)
def mod_map (proc_handle, x, y, tile):
    map_address = 0x0122B6D8
    bytes_written = ctypes.c_size_t()
    tile_address = int(map_address + 4 * (x * 70 + y))
    print("writing a {} at ({}, {}) ({:X})".format(tile, x, y, tile_address))
    pdt_win_calls.WPM(proc_handle, tile_address, bytes(tile), len(tile), ctypes.byref(bytes_written))
    print(ctypes.WinError(ctypes.get_last_error()))
    print("{} bytes written".format(bytes_written))

def digger_patch (proc_handle):
    patch_jump = patch(0x005A6630, pdt_bin_buf.bin_buf("E9 D6 D2 90 00"), pdt_bin_buf.bin_buf("8B 75 08 8B 45"))
    patch_dig = patch(0x00EB390B, pdt_bin_buf.bin_buf("8B 75 08 8B 45 08 8B 16 8B 40 04 52 50 6B D2 46 01 D0 8D 04 85 D8 B6 22 01 8B 10 83 EA 21 72 07 8B 10 83 EA 7A 72 33 8B 10 83 EA 01 72 07 8B 10 83 EA 04 72 25 EB 1D 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 C7 00 21 00 00 00 8B 00 58 5A E9 CD 2C 6F FF"))
    patch_jump.toggle(proc_handle)
    patch_dig.toggle(proc_handle)
