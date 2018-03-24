import ctypes
import pdt_win_calls 
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


