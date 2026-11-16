#!/usr/bin/env python3

import logging
import sys

from ecomet_i2c_sensors.rainfall import RainfallSensor


RAINFALL_PERIOD_HOURS = 1


def main():
    print(sys.version)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
    )
    logger = logging.getLogger("ecomet.rainfall")
    sensor = None

    try:
        sensor = RainfallSensor()
        if not sensor.begin():
            logger.error(
                "Rainfall sensor not recognized (PID=0x%X, VID=0x%X)",
                sensor.pid, sensor.vid
            )
            return 1

        logger.info(
            "Sensor initialized (PID=0x%X, VID=0x%X)",
            sensor.pid, sensor.vid
        )
        logger.info("Firmware version: %s", sensor.get_firmware_version())
        logger.info(
            "Working time: %.2f hours",
            sensor.get_sensor_working_time()
        )
        logger.info("Cumulative rainfall: %.4f mm", sensor.get_rainfall())
        logger.info(
            "Rainfall in the preceding %d hour(s): %.4f mm",
            RAINFALL_PERIOD_HOURS,
            sensor.get_rainfall_time(RAINFALL_PERIOD_HOURS)
        )
        logger.info("Raw tipping-bucket count: %d", sensor.get_raw_data())
        return 0
    except Exception:
        logger.exception("Rainfall sensor test failed")
        return 1
    finally:
        if sensor is not None:
            sensor.close()


if __name__ == "__main__":
    sys.exit(main())
