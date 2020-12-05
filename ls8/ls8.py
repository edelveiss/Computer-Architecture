#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


cpu = CPU()
# cpu.load()
if len(sys.argv) != 2:
    print("Input is incorrect. Usage: python3 ls8.py examples/mult.ls8")
    sys.exit(1)

cpu.load(sys.argv[1])

cpu.run()


