#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Pete Ezzo

import base64
import pathlib
import subprocess
import jinja2

subprocess.run(['gcc', 'payload.c', '-o', 'payload'])
raw_data = pathlib.Path('payload').read_bytes()
encoded_data = base64.b64encode(raw_data)
encoded_data_lines = [encoded_data[i:i+120] for i in range(0, len(encoded_data), 120)]
template = jinja2.Template(pathlib.Path('innocent_name_here.py.j2').read_text())
rendered_script = template.render(blob=encoded_data_lines)
pathlib.Path('innocent_name_here.py').write_text(rendered_script)
