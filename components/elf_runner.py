# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Pete Ezzo

import os
import pathlib
import random
from typing import Optional


class ELFRunner:
    """
    Execute an ELF file without writing to disk

    Usage:

        bin = ELFRunner(bytestring).execute([arg1, arg2, ..., argn])

        daemon = ELFRunner(bytestring).daemonize([arg1, arg2, ..., argn])

    """
    CHILD_PID = 0

    def __init__(self, elf: bytes, fd_name: Optional[str] = None):
        """
        Create an anonymous in-memory file and write child binary
        """
        fd_name = fd_name or random.randomint(10, 20)
        self.fd = os.memfd_create(self.fd_name, 0)
        self.memfd_path = f'/proc/self/fd/{self.fd}'
        pathlib.Path(self.memfd_path).write_bytes(elf)

    def execute(self, args: Optional[list] = None):
        """
        Run the binary as a child process of python
        """
        args = ['memfd'] + (args or [])
        pid = os.fork()
        if pid == self.CHILD_PID:
            os.execve(self.memfd_path, args, dict(os.environ))

    def daemonize(self, args: Optional[list] = None):
        """
        Run the binary as an independent process (child of pid 1 init)
        """
        args = ['memfd'] + (args or [])
        pid = os.fork()
        if pid == self.CHILD_PID:
            os.setsid()
            pid = os.fork()
            if pid == self.CHILD_PID:
                os.execve(self.memfd_path, args, dict(os.environ))
