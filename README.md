# ecomet_i2c_raspberry_tools

**Last modification:** 21.06.2021
**Contributor:** Marian Minar
**Twitter:** [News and statuses](https://twitter.com/mminar7)

**[Wiki:](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki)** Let's see Wiki for these who would like to buy prototypes boards. Each day will be something added. **!NEW!**

**Scope:**
The Code for I2C Chip maintenance from **Raspberry PI 3+** and above. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.

**Current CHIP maintained:**
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)
  PCA9557
* [Texas Instruments](https://www.ti.com/)
  HDC1080,PCA9557
* [Measurement Specialties, TE Connectivity](https://www.te.com/) MS5637,HTU21D
* [Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/2301.pdf) EMC2301
* [Solomon Systech](https://www.solomon-systech.com/) **!NEW!** SSD1309

**List of modules:**

* [EEPROM module](i2c_pkg/eeprom_pkg/documentation/eeprom_IIC.md)
* [PCA9557 module](i2c_pkg/pca9557_pkg/pca9557_python.IIC.md) -> **!NEW!** Remote8-Bit I2C and SMBusLow-PowerI/O ExpanderWith Reset andConfigurationRegisters
* [PCA9632 module](fpc/pca9632/pca9632_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
* [HDC1080 module](fpc/hdc1080/hdc1080_IIC.md) -> High Accuracy Digital Humidity Sensor with Temperature Sensor
* [HTU21D module](i2c_pkg/htu21_pkg/htu21_python_IIC.md) -> Digital Relative Humidity sensor with Temperature output, calculation of Dew Point
* [MS5637 module](i2c_pkg/ms5637_pkg/ms5637_python.IIC.md) ->  Ultra-compact micro altimeter. Integrated digital pressure sensor (24 bit ΔΣ ADC), Operating range: 300 to 1200 mbar, -40 to +85 °C
* [EMC2301 module](fpc/emc2301/emc2301_IIC.md) -> Fan controller with a PWM fan driver
* [SSD1306 module](i2c_pkg/ssd1306_pkg/ssd1306_python.IIC.md) -> **!NEW!**. SSD1306 is a single-chip CMOS OLED/PLED driver with controller for organic / polymer light emitting
diode dot-matrix graphic display system.

**Software for Chips:**

| Chip            | Python 3 driver | FPC GUI  | Hardware Board | Contributor Notes            | Planned work                   | Requestor Interests           |
| --------------- |:---------------:|:--------:|:--------------:|:----------------------------:|:------------------------------:|:-----------------------------:|
| EEPROM 24cXXX   |[yes](i2c_pkg/eeprom_pkg/documentation/eeprom_IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board),[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board),[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)| currently tested at 24c01,24c04,24c08,24c16,24c32,24c64                  | prepared next chips for testing                      |                               |
| PCA9557         |[yes](i2c_pkg/pca9557_pkg/pca9557_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board)|  [!NEW!](i2c_pkg/pca9557_pkg/pca9557_python.IIC.md) Python driver documentation |            |
| PCA9632         |[yes](i2c_pkg/pca9632_pkg/pca_9632_python_IIC.md)|[yes](fpc/pca9632/pca9632_IIC.md)|[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |                               |                               |
| HDC1080         |[yes](i2c_pkg/hdc1080_pkg/hdc1080_python_IIC.md)|[yes](fpc/hdc1080/hdc1080_IIC.md)|[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |    |                               |
| HTU21D          |[yes](i2c_pkg/htu21_pkg/htu21_python_IIC.md)|    no    |[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                              |       |                               |
| MS5637          |[yes](i2c_pkg/ms5637_pkg/ms5637_python.IIC.md)|    no    |[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |      |
| EMC2301         |[yes](i2c_pkg/emc2301_pkg/emc2301_python_IIC.md)|[yes](fpc/emc2301/emc2301_IIC.md)|[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board)|                  |    |  add EMC2302-05 chips in design                             |
| SSD1306         |[yes](i2c_pkg/ssd1306_pkg/ssd1306_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board) |[!NEW!](i2c_pkg/ssd1306_pkg/ssd1306_python.IIC.md) Python driver documentation |     |
 
**! NEW ! Alternative command for I2C chip detection**
Here is alternative command to i2cdetect for detection of active I2C chips at I2C bus:
***i2c_ecomet_detect.py***

``` python
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 i2c_ecomet_detect.py
3.7.3 (default, Jan 22 2021, 20:04:44)
[GCC 8.3.0]
ecomet.Board_Platform: INFO     Start logging ...
ecomet.Board_Platform: INFO     Board platform: RASPBERRY_PI 3.2
ecomet.Board_Platform: INFO     Number of I2C buses at the board: 2
i2c_pkg.platform_pkg.i2c_platform: INFO     >>> Testing at bus: 0
i2c_pkg.platform_pkg.i2c_platform: INFO     No Chip connected
i2c_pkg.platform_pkg.i2c_platform: INFO     >>> Testing at bus: 1
i2c_pkg.platform_pkg.i2c_platform: INFO     Default bus number: 1
i2c_pkg.platform_pkg.i2c_platform: INFO     Identified Slaves Chips: 0x2f:0x40:0x50:0x51:0x52:0x53:0x54:0x55:0x56:0x57:0x62:0x70:0x76
```
 
**Requestor Interests:**
If you would like to reqest some new feature or add some new Chip at the development list let me know by adding issue or by email.
