# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: PyZMQ Developers, Pete Ezzo

import struct
import zlib


class DecodeZ85:
    """
    Decode a compressed encoded blob to raw blob

    Usage:

        raw_blob = DecodeZ85(encoded_blob).bytestring

    """
    Symbols = r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'
    Offsets = [52200625, 614125, 7225, 85, 1]  # [85**i for i in range(5)][::-1]
    Translation = {ord(character): index for index, character in enumerate(Symbols)}

    def __init__(self, encodedelf: bytes):
        self.bytestring = self.decode(encodedelf)

    def decode(self, bytestring: bytes):
        nvalues = len(bytestring) // 5
        values = []
        for i in range(0, len(bytestring), 5):
            value = sum([self.Translation[bytestring[i + j]] * offset for j, offset in enumerate(self.Offsets)])
            values.append(value)
        compressed = struct.pack('>%dI' % nvalues, *values)
        return zlib.decompress(compressed)
