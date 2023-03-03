#!/usr/bin/env python3

import sys
import re
print (sys.version)
from  ecomet_i2c_sensors.platform import i2c_platform
import logging

i2c_count = [ '^RASPBERRY_PI 1\..*$',
              '^RASPBERRY_PI 1B\..*$',
              '^RASPBERRY_PI 2\..*$',
              '^RASPBERRY_PI 3\..*$',
              '^RASPBERRY_PI 3B\..*$',
              '^RASPBERRY_PI 4B\:.*$',
              '^RASPBERRY_PI_\(CM4\).*$',
              '^RASPBERRY_PI ZERO 2 W.*$',
              '^OTHER$' ]

i2c_count_max = [ 2,
                  2,
                  2,
                  2,
                  2,
                  2,
                  11,
                  2,
                  21 ]

plat = i2c_platform.Board_plat(busnum=0)

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='i2c_ecomet_detect.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

plat._logger = logging.getLogger('ecomet.Board_Platform')
plat._logger.info('Start logging ...')
board = plat.board()
plat._logger.info('Board platform: {}'.format(board))

idx = 0
for match_str in i2c_count :
  match = re.search(match_str, board, flags=re.IGNORECASE)
  if match :
    max = i2c_count_max[idx]
  idx += 1

plat._logger.info('Number of I2C buses at the board: {}'.format(max))

for bus_nm in range(0,max) :
  plat = i2c_platform.Board_plat(busnum=bus_nm)
  board = plat.board()
  bus = plat.bus()
  slave = plat.slaves()

  plat._logger.info('>>> Testing at bus: {}'.format(bus_nm))
  if not slave :
    plat._logger.info('No Chip connected')
  else :
    plat._logger.info('Default bus number: {}'.format(bus))
    plat._logger.info('Identified Slaves Chips: {}'.format(slave))
