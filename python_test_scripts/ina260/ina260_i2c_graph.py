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
import os
import pickle

def child_lvl3():
   fd = open('ina260_lvl4.pkl','wb')
   print("child3: %d" % os.getpid())
   shared = measure2.measure_voltage(stime = 1)
   pickle.dump(shared, fd,-1)
   fd.close()
   os._exit(0)

def child_lvl2():
   while True:
     newpid_lvl3 = os.fork()
     if newpid_lvl3 == 0:
        child_lvl3()
     else:
        print("child2: %d" % os.getpid())
        fd = open('ina260_lvl3.pkl','wb')
        shared = measure2.measure_current(stime = 1)
        pickle.dump(shared, fd,-1)
        fd.close()
        os.waitid(os.P_PID,newpid_lvl3,os.WEXITED)
        break
   os._exit(0)

def child():
   while True:
     newpid_lvl2 = os.fork()
     if newpid_lvl2 == 0:
        child_lvl2()
     else:
        print("child: %d" % os.getpid())
        fd = open('ina260_lvl2.pkl','wb')
        shared = measure1.measure_voltage(stime = 1)
        pickle.dump(shared, fd,-1)
        fd.close()
        os.waitid(os.P_PID,newpid_lvl2,os.WEXITED)
        break
   os._exit(0)

def parent():
   while True:
      newpid = os.fork()
      if newpid == 0:
         child()
      else:
         print("parent: %d" % os.getpid())
         C0_current = measure1.measure_current(stime = 1)
         os.waitid(os.P_PID,newpid,os.WEXITED)
         break
   fd = open('ina260_lvl2.pkl','rb')
   C0_voltage = pickle.load(fd)
   fd.close()
   fd_lvl2 = open('ina260_lvl3.pkl','rb')
   C1_current = pickle.load(fd_lvl2)
   fd_lvl2.close()
   fd_lvl3 = open('ina260_lvl4.pkl','rb')
   C1_voltage = pickle.load(fd_lvl3)
   fd_lvl3.close()
   os.remove('ina260_lvl2.pkl')
   os.remove('ina260_lvl3.pkl')
   os.remove('ina260_lvl4.pkl')

   multi_measure = [C0_current,C0_voltage,C1_current,C1_voltage]
   return (multi_measure)

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
measure1.write_funct('ISHCT', value = _mconst.register.TIME_332_us)
measure1.write_funct('VBUSCT', value = _mconst.register.TIME_332_us)
measure1.write_funct('MODE', value = _mconst.register.INA260_MODE_CONTINUOUS)

measure2.write_funct('AVGC', value = _mconst.register.COUNT_1)
measure2.write_funct('ISHCT', value = _mconst.register.TIME_332_us)
measure2.write_funct('VBUSCT', value = _mconst.register.TIME_332_us)
measure2.write_funct('MODE', value = _mconst.register.INA260_MODE_CONTINUOUS)

rlist1 = ina260.conf_register_list(address=_mconst.INA260_ADDRESS1)
rlist2 = ina260.conf_register_list(address=_mconst.INA260_ADDRESS2)

buf_voltage_1 = {}
buf_current_1 = {}
buf_voltage_2 = {}
buf_current_2 = {}

((size_current_1,buf_current_1),(size_voltage_1,buf_voltage_1),(size_current_2,buf_current_2),(size_voltage_2,buf_voltage_2)) = parent()

measure1._logger.info("Measure Current 0")
measure1._logger.info("Size: %s", size_current_1)
measure1._logger.info("Buff: %s", buf_current_1)

measure1._logger.info("Measure Voltage 0")
measure1._logger.info("Size: %s", size_voltage_1)
measure1._logger.info("Buff: %s", buf_voltage_1)

measure1._logger.info("Measure Current 1")
measure1._logger.info("Size: %s", size_current_2)
measure1._logger.info("Buff: %s", buf_current_2)

measure1._logger.info("Measure Voltage 1")
measure2._logger.info("Size: %s", size_voltage_2)
measure2._logger.info("Buff: %s", buf_voltage_2)


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
