# ecomet_i2c_tools

**Last modification:** 9.04.2020
**Contributor:** Marian Minar

**Scope:**
The Code for I2C Chip maintenance from **Raspberry PI 3+** and above. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.

**Current CHIP maintained:**
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)


**List of modules:**

* [EEPROM module](i2c_pkg/eeprom_pkg/documentation/eeprom_IIC.md)
* [PCA9632 module](fpc/pca6532/pca6532_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
