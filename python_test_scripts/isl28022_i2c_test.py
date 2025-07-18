#!/usr/bin/env python3

import sys
print (sys.version)
from ecomet_i2c_sensors.isl2802x	import isl2802x,isl2802x_constant
from time import sleep
import logging
import os

_mconst = isl2802x_constant
measure = isl2802x.ISL28022(address=_mconst.ISL28022_ADDRESS)

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='isl28022.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

measure.write_funct('BADC', value = _mconst.register.ADC_4_15)
measure.write_funct('SADC', value = _mconst.register.ADC_4_15)
measure.write_funct('PG', value = _mconst.register.PG_80mV)
measure.write_funct('MODE', value = _mconst.register.MODE_BUSV_CONT)
'''
measure2.write_funct('AVGC', value = _mconst.register.COUNT_4)
measure2.write_funct('ISHCT', value = _mconst.register.TIME_1_1_ms)
measure2.write_funct('VBUSCT', value = _mconst.register.TIME_332_us)
measure2.write_funct('MODE', value = _mconst.register.INA260_MODE_CONTINUOUS)

buf = {}
(buf,unit,size) = measure.measure_voltage(stime = 0.1, voltage_scale = 16)
measure._logger.info("Size: %s", size)
measure._logger.info("Unit: %s", unit)
measure._logger.info("Buff: %s", buf)

r1list = isl2802x.conf_register_list(address=_mconst.ISL28022_ADDRESS)

measure._logger.info("Array: %s" ,r1list)
'''
shunt_buf = {}
(buf,unit,size) = measure.measure_shunt_voltage(stime = 0.1, voltage_shunt_scale = '40mV')
measure._logger.info("Size: %s", size)
measure._logger.info("Unit: %s", unit)
measure._logger.info("Buff: %s", buf)

r2list = isl2802x.conf_register_list(address=_mconst.ISL28022_ADDRESS)

measure._logger.info("Array: %s" ,r2list)
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
