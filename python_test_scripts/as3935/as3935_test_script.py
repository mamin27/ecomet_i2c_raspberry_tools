#!/usr/bin/python3

import sys
#print (sys.version)
from time import sleep
from  ecomet_i2c_sensors.as3935 import as3935,as3935_constant
import OPi.GPIO as GPIO
import logging
from datetime import datetime

#I2C address
AS3935_I2C_ADDR1 = 0X01
AS3935_I2C_ADDR2 = 0X02
AS3935_I2C_ADDR3 = 0X03

#Antenna tuning capcitance (must be integer multiple of 8, 8 - 120 pf)
AS3935_CAPACITANCE = 96
IRQ_PIN = 7

GPIO.setmode(GPIO.BOARD)

sens = as3935.AS3935(AS3935_I2C_ADDR3)

logging.basicConfig(level=logging.DEBUG,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='as3935.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.as3935')
sens._logger.info('Start logging ...')

if (sens.reset == 0):
  print("init sensor sucess.")
else:
  print("init sensor fail")
  while True:
    pass

#Configure sensor
sens.power_up()
#Clear statistics
sens.clear_statistics()
sens._logger.info('Clear statistics')

#set indoors or outdoors models
#sens.set_indoors()
sens.set_outdoors()

#disturber detection
sens.disturber_en()
#sens.disturber_dis()

sens.set_irq_output_source(0)
sleep(0.5)
#set capacitance
sens.set_tuning_caps(AS3935_CAPACITANCE)

# Connect the IRQ and GND pin to the oscilloscope.
# uncomment the following sentences to fine tune the antenna for better performance.
# This will dispaly the antenna's resonance frequency/16 on IRQ pin (The resonance frequency will be divided by 16 on this pin)
# Tuning AS3935_CAPACITANCE to make the frequency within 500/16 kHz plus 3.5% to 500/16 kHz minus 3.5%
#
# sens.set_lco_fdiv(0)
# sens.set_irq_output_source(as3935_constant.SET_IRQ_SIGNAL_FLAGS.irq_lco)

#Set the noise level,use a default value greater than 7
sens.set_noise_floor_lv1(as3935_constant.STAT_REG_1_FLAGS.nfl_in_2)
#noiseLv = sens.get_noise_floor_lv1()
#sens._logger.info('Noise Floor Level: %02x'%noiseLv)

#used to modify WDTH,alues should only be between 0x00 and 0x0F (0 and 7)
sens.set_watchdog_threshold(as3935_constant.STAT_REG_1_FLAGS.wdth_2)
#wtdgThreshold = sens.get_watchdog_threshold()
#sens._logger.info('Threshold Level: %02x'%wtdgThreshold)

#used to modify SREJ (spike rejection),values should only be between 0x00 and 0x0F (0 and 7)
sens.set_spike_rejection(as3935_constant.STAT_REG_2_FLAGS.srej_2)
#spikeRejection = sens.get_spike_rejection()
#sens._logger.info('Spike Rejection: %02x'%spikeRejection)

#view all register data
sens.print_all_regs()

#def callback_handle(channel):
def callback_handle():
  global sens
  sleep(0.005)
  intSrc = sens.get_interrupt_src()
  print (intSrc)
  if intSrc == 1:
    lightning_distKm = sens.get_lightning_distKm()
    print('Lightning occurs!')
    print('Distance: %dkm'%lightning_distKm)

    lightning_energy_val = sens.get_strike_energy_raw()
    print('Intensity: %d '%lightning_energy_val)
  elif intSrc == 2:
    print('Disturber discovered!')
  elif intSrc == 3:
    print('Noise level too high!')
  else:
    pass
#Set to input mode
#GPIO.setup(IRQ_PIN, GPIO.IN)
#Set the interrupt pin, the interrupt function, rising along the trigger
#GPIO.add_event_detect(IRQ_PIN, GPIO.RISING, callback = callback_handle)

callback_handle()
print("start lightning detect.")

while True:
  sleep(1.0)


