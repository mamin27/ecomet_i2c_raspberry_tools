#chip_list.py
# Author: Marian Minar
# Copyright 2020

def init():
     global xchip

     xchip = { "24c01":[1,127],         # 1-Kbit (128x8)         A6  - A0 max  007F
               "24c02":[2,255],         # 2-Kbit (256x8)         A7  - A0 max  00FF
               "24c04":[3,511],         # 4-Kbit (512x8)         A8  - A0 max  01FF
               "24c08":[4,1023],        # 8-Kbit (1024x8)        A9  - A0 max  03FF
               "24c16":[5,2047],        # 16-Kbit (2048x8)       A10 - A0 max  07FF
               "24c32":[6,4095],        # 32-Kbit (4096x8)       A11 - A0 max  0FFF
               "24c64":[7,8191],        # 64-Kbit (8192x8)       A12 - A0 max  1FFF
               "24c128":[8,16383],      # 128-Kbit (16384x8)     A13 - A0 max  3FFF
               "24c256":[9,32767],      # 256-Kbit (32768x8)     A14 - A0 max  7FFF
               "24c512":[10,65535],     # 512-Kbit (65536x8)     A15 - A0 max  FFFF
               "24c1024":[11,1048575]}  # 1024-Kbit (1048576x8)  A16 - A0 max FFFFF
