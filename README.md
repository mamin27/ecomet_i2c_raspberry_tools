# ecomet_i2c_raspberry_tools

**Last modification:** 20.05.2021
**Contributor:** Marian Minar
**Twitter:** [News and statuses](https://twitter.com/mminar7) **!NEW!**

**Scope:**
The Code for I2C Chip maintenance from **Raspberry PI 3+** and above. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.

**Current CHIP maintained:**
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)
* [Texas Instruments](https://www.ti.com/)
  HDC1080
* [Measurement Specialties, TE Connectivity](https://www.te.com/) MS5637 **!NEW!**,HTU21D
* [Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/2301.pdf) EMC2301

**List of modules:**

* [EEPROM module](i2c_pkg/eeprom_pkg/documentation/eeprom_IIC.md)
* [PCA9632 module](fpc/pca9632/pca9632_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
* [HDC1080 module](fpc/hdc1080/hdc1080_IIC.md) -> High Accuracy Digital Humidity Sensor with Temperature Sensor
* [HTU21D module](i2c_pkg/htu21_pkg/htu21_python_IIC.md) -> Digital Relative Humidity sensor with Temperature output, calculation of Dew Point
* [MS5637 module](i2c_pkg/ms5637_pkg/ms5637_python.IIC.md) ->  **!NEWNew GUI**. Ultra-compact micro altimeter. Integrated digital pressure sensor (24 bit ΔΣ ADC), Operating range: 300 to 1200 mbar, -40 to +85 °C 
* [EMC2301 module](fpc/emc2301/emc2301_IIC.md) -> Fan controller with a PWM fan driver

**Software for Chips:**

| Chip            | Python 3 driver | FPC GUI  | Contributor Notes            | Planned work                   | Requestor Interests           |
| --------------- |:---------------:|:--------:|:----------------------------:|:------------------------------:|:-----------------------------:|
| EEPROM 24cXXX   |      yes        |    no    | currently tested at 24c01,24c04,24c08,24c16,24c32,24c64                  | prepared next chips for testing                      |                               |
| PCA9632         |      yes        |    yes   |                  | testing board developed soon info in wiki                               |                               |
| HDC1080         |      yes        |    yes   |                  | testing board developed soon info in wiki   |                               |
| HTU21D          |      yes        |    no    |                              | currently no GUI planned       |                               |
| MS5637          |      yes        |    no    | [!NEW!](i2c_pkg/ms5637_pkg/ms5637_python.IIC.md) Python driver documentation |                               |
| EMC2301         |      yes        |    yes   |                  | testing board needs to be redesigned   |                               |
 
**Requestor Interests:**
If you would like to reqest some new feature or add some new Chip at the development list let me know by adding issue or by email.
