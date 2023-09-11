# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Pete Ezzo

import ctypes
import mmap


class ShellcodeRunner:
    """
    Execute arbitrary shellcode

    Usage:

        ShellcodeRunner(bytestring).run()

        result = ShellcodeRunner(bytestring).run(arg1, arg2, ..., argn)

    """
    def __init__(self, shellcode):
        """
        Write shellcode to an executable address space and prepare to use
        """
        buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
        buf.write(shellcode)

        fpointer = ctypes.c_void_p.from_buffer(buf)
        ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
        self.function_ref = ftype(ctypes.addressof(fpointer))

    def run(self, *args):
        """
        Execute the shellcode
        """
        return self.function_ref(*args)
