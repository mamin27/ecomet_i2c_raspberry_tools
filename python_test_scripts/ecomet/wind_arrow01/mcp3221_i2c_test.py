#!/usr/bin/env python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.mcp3221 import mcp3221
import logging

mcp = mcp3221.MCP3221()

logging.basicConfig(level=logging.DEBUG,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='mcp3221.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
mcp._logger = logging.getLogger('ecomet.mcp3221')
mcp._logger.info('Start logging ...')

(val,ret) = mcp.to_max_const
mcp._logger.info('Degree: %s',format(round(val,1)))
(val,ret) = mcp.degrees_to_cardinal_calibrated
mcp._logger.info('Cardinal: %s',format(val))
