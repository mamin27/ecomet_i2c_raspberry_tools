#!/usr/bin/env python3

import sys
print (sys.version)
from PIL import ImageFont, Image
from i2c_pkg.ssd1306_pkg import ssd1306,render
from i2c_pkg.pca9557_pkg import pca9557  # could be skipped
from i2c_pkg.ina260_pkg	import ina260,ina260_constant
from time import sleep
import qrcode
import logging

_mconst = ina260_constant
disp = ssd1306.SSD1306()
io = pca9557.PCA9557() # could be skipped
measure1 = ina260.INA260(address=_mconst.INA260_ADDRESS1)
measure2 = ina260.INA260(address=_mconst.INA260_ADDRESS2)

dconst = disp._const

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='ina260.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

measure1.write_funct('AVGC', value = _mconst.register.COUNT_1)
measure1.write_funct('ISHCT', value = _mconst.register.TIME_1_1_ms)
measure1.write_funct('VBUSCT', value = _mconst.register.TIME_1_1_ms)
measure1.write_funct('MODE', value = _mconst.register.INA260_MODE_CONTINUOUS)
measure2.write_funct('AVGC', value = _mconst.register.COUNT_1)
measure2.write_funct('ISHCT', value = _mconst.register.TIME_1_1_ms)
measure2.write_funct('VBUSCT', value = _mconst.register.TIME_1_1_ms)
measure2.write_funct('MODE', value = _mconst.register.INA260_MODE_CONTINUOUS)

rlist1 = ina260.conf_register_list(address=_mconst.INA260_ADDRESS1)
rlist2 = ina260.conf_register_list(address=_mconst.INA260_ADDRESS2)

measure1._logger.info("Array: %s" ,rlist1)
measure2._logger.info("Array: %s" ,rlist2)

'''


# this code could be skipped if you control Reset PIN at ssd1306 different way
io.sw_reset()
io.set_io('OOIIIIOO')
io.set_invert('NNNNNNNN')
io.set_io_name(port_arr = [[0,'LED1'],[1,'LED2'],[2,'BUT_RIG_DWN'],[3,'BUT_RIG_UP'],
                           [4,'BUT_LFT_DWN'],[5,'BUT_LFT_UP'],[6,'D/C'],[7,'DIS_RET']])
io.write_output_port (status = pca9557.High, pin = 'LED1')
io.write_output_port (status = pca9557.High, pin = 'LED2')
io.write_output_port (status = pca9557.Low, pin = 'DIS_RST')
io.write_output_port (status = pca9557.High, pin = 'D/C')
# end of skip
disp.sw_reset()
disp.setup()

qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2,
    )
qr.add_data('https://github.com/mamin27/ecomet_i2c_raspberry_tools')
qr.make(fit=True)
img = qr.make_image()
img.save('./images/code.png')
font = ImageFont.truetype('./fonts/C&C Red Alert [INET].ttf', 12)

# draw Logo
#disp.sw_reset()
with render.canvas(disp) as draw:
   zoom = Image.open('images/zoom.png')
   draw.bitmap((0, 0), zoom, fill=1)
   zoom.close()
   del draw

with render.canvas(disp) as draw:
   sleep(5)
   logo = Image.open('images/comet_black_white_62x62.png')
   draw.bitmap((0, 0), logo, fill=1)
   draw.text((75, 20), 'eComet', font=font, fill=1)
   draw.text((90, 32 ), 'Slovakia', font=font, fill=1)
   logo.close()
   del draw

# draw QR Code
with render.canvas(disp) as draw:
   sleep(5)
   code = Image.open('images/code.png')
   draw.bitmap((0, 0), code, fill=1)
   draw.text((80, 20), 'QR Code', font=font, fill=1)
   code.close()
   del draw

# Clean Display
with render.canvas(disp) as draw:
   sleep(5)
   draw.rectangle((0, 0, disp.width, disp.height), fill=0)     #clear display

'''
