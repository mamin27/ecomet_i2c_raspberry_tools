# ecomet_i2c_raspberry_tools

**Last modification:** 10.10.2022
**Contributor:** Marian Minar

<a href="https://www.buymeacoffee.com/scQ8LwgTBt"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=scQ8LwgTBt&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>

**Twitter:** [News and statuses](https://twitter.com/mminar7)

**NEW! SourceForge.net:**
* Oscilloscope-like application **eCScope** for Raspberry PI 3+ (32bit Raspbian) based on INA260 chips and built with the Ecomet-i2c-sensors Python library.

[![Download eCScope](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/ecomet-i2c-raspberry-tools/files/latest/download)

Project eCScope was created to show progress in development. Insert the #eCScope keyword into the issue section.

**PyPi module:** [ecomet-i2c-sensor](https://test.pypi.org/project/ecomet-i2c-sensors/)

Python3 library - currently **Beta status**
```sh
pip install ecomet-i2c-sensors
```

**Wiki Hardware prototypes boards:** [link](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki)

**Scope:**
The Driver for I2C Chip maintenance from **Raspberry PI 1B+** and above. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.
* tested at Raspberry PI 1B+, 3B+, 4B+, 4CM

**Current CHIP maintained:**
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)
  PCA9557
* [Texas Instruments](https://www.ti.com/)
  HDC1080,PCA9557,INA226,INA260
* [Measurement Specialties, TE Connectivity](https://www.te.com/) MS5637,HTU21D
* [Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/2301.pdf) EMC2301
* [Solomon Systech](https://www.solomon-systech.com/) SSD1309
* [Renesas](https://www.renesas.com/eu/en) ISL28022

**List of modules:**

* [EEPROM module](ecomet_i2c_sensors/eeprom/documentation/eeprom_IIC.md) -> EEPROM read/write 24cXXX chips
* [PCA9557 module](ecomet_i2c_sensors/pca9557/pca9557_python.IIC.md) -> Remote8-Bit I2C and SMBusLow-PowerI/O ExpanderWith Reset andConfigurationRegisters
* [PCA9632 module](fpc/pca9632/pca9632_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
* [HDC1080 module](fpc/hdc1080/hdc1080_IIC.md) -> High Accuracy Digital Humidity Sensor with Temperature Sensor
* [HTU21D module](ecomet_i2c_sensors/htu21/htu21_python_IIC.md) -> Digital Relative Humidity sensor with Temperature output, calculation of Dew Point
* [MS5637 module](ecomet_i2c_sensors/ms5637/ms5637_python.IIC.md) ->  Ultra-compact micro altimeter. Integrated digital pressure sensor (24 bit ΔΣ ADC), Operating range: 300 to 1200 mbar, -40 to +85 °C
* [EMC2301 module](fpc/emc2301/emc2301_IIC.md) -> Fan controller with a PWM fan driver
* [SSD1306 module](ecomet_i2c_sensors/ssd1306/ssd1306_python.IIC.md) -> SSD1306 is a single-chip CMOS OLED/PLED driver with controller for organic / polymer light emitting
diode dot-matrix graphic display system.
* [INA226,INA260 module](ecomet_i2c_sensors/ina260/ina260_python.IIC.md) -> **!NEW!** will be added python module description
* ISL2802x module -> **!NEW!** will be added python module description

**Software for Chips:**

| Chip            | Python 3 driver | FPC GUI  | Hardware Board | Contributor Notes            | Planned work                   | Requestor Interests           |
| --------------- |:---------------:|:--------:|:--------------:|:----------------------------:|:------------------------------:|:-----------------------------:|
| EEPROM 24cXXX   |[yes](ecomet_i2c_sensors/eeprom/documentation/eeprom_IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board),[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board),[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)| currently tested at 24c01,24c04,24c08,24c16,24c32,24c64                  |                        |                               |
| PCA9557         |[yes](ecomet_i2c_sensors/pca9557/pca9557_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board)|  |            |
| PCA9632         |[yes](ecomet_i2c_sensors/pca9632/pca_9632_python_IIC.md)|[yes](fpc/pca9632/pca9632_IIC.md)|[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |                               |                               |
| HDC1080         |[yes](ecomet_i2c_sensors/hdc1080/hdc1080_python_IIC.md)|[yes](fpc/hdc1080/hdc1080_IIC.md)|[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |    |                               |
| HTU21D          |[yes](ecomet_i2c_sensors/htu21/htu21_python_IIC.md)|    no    |[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                              |       |                               |
| MS5637          |[yes](ecomet_i2c_sensors/ms5637/ms5637_python.IIC.md)|    no    |[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |      |
| EMC2301         |[yes](ecomet_i2c_sensors/emc2301/emc2301_python_IIC.md)|[yes](fpc/emc2301/emc2301_IIC.md)|[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board)|                  |    |  add EMC2302-05 chips in design                             |
| SSD1306         |[yes](ecomet_i2c_sensors/ssd1306/ssd1306_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board) | |     |
| INA226, INA260  |[yes](ecomet_i2c_sensors/ina260/ina260_python_IIC.md)|    yes    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board) |[!NEW!](ecomet_i2c_sensors/ina260/ina260_python_IIC.md) |     |
| ISL2802x  |in progress |    no    | | |     |

```sh
hdc1080 -disableaccurateframe
```


**Alternative command for I2C chip detection**
Here is alternative command to i2cdetect for detection of active I2C chips at I2C bus:
***i2c_ecomet_detect.py***

``` python
pi@raspberrypi:~/ecomet_i2c_raspberry_tools/bin $ python3 i2c_ecomet_detect.py
3.9.9 (main, Jan 16 2022, 22:51:22)
[GCC 11.2.0]
ecomet.Board_Platform: INFO     Start logging ...
ecomet.Board_Platform: INFO     Board platform: RASPBERRY_PI 4B:1.4
ecomet.Board_Platform: INFO     Number of I2C buses at the board: 2
ecomet_i2c_sensors.platform.i2c_platform: INFO     >>> Testing at bus: 0
ecomet_i2c_sensors.platform.i2c_platform: INFO     No Chip connected
ecomet_i2c_sensors.platform.i2c_platform: INFO     >>> Testing at bus: 1
ecomet_i2c_sensors.platform.i2c_platform: INFO     Default bus number: 1
ecomet_i2c_sensors.platform.i2c_platform: INFO     Identified Slaves Chips: 0xc:0x1a:0x2f:0x40:0x50:0x51:0x52:0x53:0x54:0x55:0x56:0x57:0x62:0x70:0x76
```
 
**Requestor Interests:**
If you would like to reqest some new feature or add some new Chip at the development list let me know by adding issue or by email.
