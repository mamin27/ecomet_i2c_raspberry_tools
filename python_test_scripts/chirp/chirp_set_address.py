#!/usr/bin/env python3

import argparse

from ecomet_i2c_sensors.chirp import Chirp
from ecomet_i2c_sensors.chirp import chirp_constant


def parse_address(value):
    try:
        address = int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "address must be an integer such as 0x21"
        ) from exc

    if not (
        chirp_constant.CHIRP_ADDRESS_MIN
        <= address
        <= chirp_constant.CHIRP_ADDRESS_MAX
    ):
        raise argparse.ArgumentTypeError(
            "address must be from 0x{:02X} to 0x{:02X}".format(
                chirp_constant.CHIRP_ADDRESS_MIN,
                chirp_constant.CHIRP_ADDRESS_MAX
            )
        )
    return address


def main():
    parser = argparse.ArgumentParser(
        description="Set the EEPROM I2C address of one Chirp soil moisture sensor"
    )
    parser.add_argument(
        "new_address",
        type=parse_address,
        help="new 7-bit I2C address (0x20 through 0x29)",
    )
    parser.add_argument(
        "--current-address",
        type=parse_address,
        default=chirp_constant.CHIRP_ADDRESS,
        help="address where this sensor currently responds (default: 0x20)",
    )
    parser.add_argument("--bus", type=int, default=None, help="I2C bus number")
    args = parser.parse_args()

    sensor = Chirp(address=args.current_address, busnum=args.bus)
    try:
        sensor.set_address(args.new_address)
        stored_address = sensor.get_stored_address()
        if stored_address != args.new_address:
            raise RuntimeError(
                "EEPROM address verification failed: wrote 0x{:02X}, "
                "read back 0x{:02X}".format(args.new_address, stored_address)
            )

        print("EEPROM address set and verified: 0x{:02X}".format(stored_address))
        print(
            "Power-cycle this sensor before using its new address. "
            "Only one sensor at the current address should be connected "
            "during programming."
        )
        print(
            "Only the address EEPROM byte was written; the light threshold "
            "and other EEPROM data were left unchanged."
        )
    finally:
        sensor.close()


if __name__ == "__main__":
    main()
