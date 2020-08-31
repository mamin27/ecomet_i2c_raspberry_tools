# ecomet_i2c_raspberry_tools

**Last modification:** 17.08.2020
**Contributor:** Marian Minar

**Scope:**
The Code for I2C Chip maintenance from **Raspberry PI 3+** and above. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.

**Current CHIP maintained:**
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)
* [Texas Instruments](https://www.ti.com/)
  HDC1080
* [Measurement Specialties](https://www.te.com/) HTU21D
* [Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/2301.pdf) EMC2301 **(new, development started)**

**List of modules:**

* [EEPROM module](i2c_pkg/eeprom_pkg/documentation/eeprom_IIC.md)
* [PCA9632 module](fpc/pca9632/pca9632_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
* [HDC1080 module](fpc/hdc1080/hdc1080_IIC.md) -> High Accuracy Digital Humidity Sensor with Temperature Sensor
* [HTU21D module](i2c_pkg/htu21_pkg/htu21_python_IIC.md) -> Digital Relative Humidity sensor with Temperature output, calculation of Dew Point
* [EMC2301 module] -> Fan controller with a PWM fan driver

**Software for Chips:**

| Chip            | Python 3 driver | FPC GUI  | Contributor Notes          | Planned work                   | Requestor Interests           |
| --------------- |:---------------:|:--------:|:--------------------------:|:------------------------------:|:-----------------------------:|
| EEPROM 24cXXX   |      yes        |    no    | currently tested at        | currently testing at 24c01,    |                               |
|                 |                 |          | 24c04,24c32,24c64          | 24c08, 24c16                   |                               |
| PCA9632         |      yes        |    yes   | GUI finished               |                                |                               |
| HDC1080         |      yes        |    yes   | GUI finished               |                                |                               |
| HTU21D          |      yes        |    no    |                            | currently no GUI planned       |                               |
| EMC2301         |      draft      |    no    | New, in development        | planned python driver and GUI  |                               |

**Requestor Interests:**
If you would like to reqest some new feature or add some new Chip at the development list let me know by adding issue or by email.
