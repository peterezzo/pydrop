# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: PyZMQ Developers, Pete Ezzo

import struct
import zlib
from typing import Optional


class EncodeZ85:
    """
    Encode a raw blob to compressed encoded blob

    Usage:

        encoded_blob = EncodeZ85(raw_blob).bytestring

    """
    Symbols = r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'
    Offsets = [52200625, 614125, 7225, 85, 1]  # [85**i for i in range(5)][::-1]

    def __init__(self, elf: bytes, args: Optional[list] = None):
        self.bytestring = self.encode(elf)
        self.args = args or []
        self.line_length = 120

    def encode(self, elf: bytes):
        elf = zlib.compress(elf)
        bytes_over_multiple = len(elf) % 4
        if bytes_over_multiple > 0:
            elf += (4 - bytes_over_multiple) * b'\x00'

        nvalues = len(elf) / 4
        values = struct.unpack('>%dI' % nvalues, elf)
        encodedelf = ''.join([self.Symbols[(v // offset) % 85] for v in values for offset in self.Offsets])
        return encodedelf

    def text(self):
        lines = [self.encodedelf[i:i+self.line_length] for i in range(0, len(self.encodedelf), self.line_length)]
        linelist = [f"    b'{line}'\n" for line in lines]
        python_string = ''.join(['encoded_data = (\n'] + linelist + [')\n', f'arguments = {str(self.args)}\n'])
        return python_string
