#!/usr/bin/env python3

import sys
print (sys.version)
from  zmod4510 import zmod4510, ZMODStatus
import logging

logger = logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='zmod4510.log',
                    filemode='w')
#console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)

sensor = zmod4510.ZMOD4510(logger=logger)

sensor.logger = logging.getLogger('zmod4510.zmod4510')
sensor.logger.info('Start logging ...')

    
try:
    if not sensor.start():
        raise RuntimeError("Failed to start sensor.")
    sensor.logger.info("Sensor started. Press Ctrl+C to stop.")
    print (f"Sensor started. Press Ctrl+C to stop.")
        
    while True:
        # Example: You could get real T/RH from another Python library here
        data = sensor.get_data()
            
        match data.status:
            case ZMODStatus.STABILIZATION:
                sensor.logger.info("Warming up...")

            case ZMODStatus.OK:
                sensor.logger.info(f"O3: {data.o3_ppb:.2f} ppb | NO2: {data.no2_ppb:.2f} ppb | "
                    f"Fast AQI: {data.fast_aqi} | EPA AQI: {data.epa_aqi}")

            case ZMODStatus.DAMAGE:
                sensor.logger.error("Damaged.")
            case _:
                sensor.logger.error(f"Unknown status: {data.status}")

except KeyboardInterrupt:
    sensor.logger.info("\nStopping sensor...")
    print (f"\nStopping sensor...")
finally:
    sensor.stop()
