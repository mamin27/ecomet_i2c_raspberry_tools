#!/usr/bin/env python3

from  i2c_pkg.hdc1080_pkg import hdc1080
sens = hdc1080.HDC1080()
ret = sens.write_register( register = 'CONF', bits = ['TRES_RES2'])
print (":WRITE_REG_CONF:") if ret == 0 else print (":WRITE_REG_CONF_ERR:")
