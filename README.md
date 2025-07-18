# ecomet_i2c_raspberry_tools

**Last modification:** 09/07/2025
**Contributor:** Marian Minar

**Dont forget to add ![/python_test_script/display/images/star.png](https://github.com/mamin27/ecomet_i2c_raspberry_tools/blob/master/python_test_scripts/display/images/star.png) if you were satisfy with the software!**

<a href="https://www.buymeacoffee.com/scQ8LwgTBt"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=scQ8LwgTBt&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>

**Twitter:** [News and statuses](https://twitter.com/mminar7)

**NEW! SourceForge.net:**
* Oscilloscope-like application **eCScope** for Raspberry PI 3+ (32bit Raspbian) based on INA260 chips and built with the Ecomet-i2c-sensors Python library.

[![Download eCScope](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/ecomet-i2c-raspberry-tools/files/latest/download)

Project eCScope was created to show progress in development. Insert the #eCScope keyword into the issue section.

**PyPi module:** [ecomet-i2c-sensor](https://pypi.org/project/ecomet-i2c-sensors/)

**Current release:** 0.1.9 !NEW!

**New features**

* AS3935 driver added (Sciosens)
* SGP40 driver added (Sensirion)
* MCP3221 driver added (Microchip)
* MCP3221 added feature for convert measured number to range or 360 degree, or cardinal points
* Fixes in PCA9632, prepared for multiple chips at I2C bus
* HDC1080 driver mainly code rewritten, different method calls

```sh
pip install ecomet-i2c-sensors
```
**Test release:** 0.1.9

```sh
pip3 install -i https://test.pypi.org/simple/ecomet-i2c-sensors
```

**Wiki Hardware prototypes boards:** [link](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki)

**Scope:**
The Driver for I2C Chip maintenance from **Raspberry PI 1B+** and above and **AllWinner CPU**. This code tools contains python & free pascal code focused to I2C communication of raspberry pi with IOT modules.
* tested at Raspberry PI 1B+, 3B+, 4B+, 4CM
* tested at AllWinner CPU H616, mangopi MCore-H616, Orange PI Zero2

**Current CHIP maintained:**
* [AMS-ScioSense](https://www.sciosense.com/) AS3935
* [AMS-OSRAM](https://ams.com/en/tsl25911) TSL25911
* EEPROM Chip
  24c01,24c02,24c04,24c08,24c16,24c32,24c64,24c128,24c256,24c512,24c1024
* [Measurement Specialties, TE Connectivity](https://www.te.com/) MS5637,HTU21D
* [Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/2301.pdf) EMC2301, MCP3221
* [NXP Semiconductor](https://www.nxp.com/)
  PCA9632 (could be modified for PCA9624,PCA9635PW,PCA9685,PCA9955B,PCA9956B)
  PCA9557
* [Panasonic](https://na.industrial.panasonic.com/products/sensors/air-quality-gas-flow-sensors/lineup/laser-type-pm-sensor/series/123557/model/123559) SN-GCJA5
* [Renesas](https://www.renesas.com/eu/en) ISL28022
* [Sensirion](https://sensirion.com/) SGP40
* [Solomon Systech](https://www.solomon-systech.com/) SSD1309
* [Texas Instruments](https://www.ti.com/)
  HDC1080,PCA9557,INA226,INA260
* [X-Powers](http://www.x-powers.com/en.php) AXP209


**List of modules:**

* [AS3935](https://www.sciosense.com/as3935-franklin-lightning-sensor-ic/) -> **!NEW!** Franklin Lightning Sensor
* [AXP209](ecomet_i2c_sensors/axp209/AXP209.PDF) -> PMU (Power Management Unit) Sensor
* [EEPROM module](ecomet_i2c_sensors/eeprom/documentation/eeprom_IIC.md) -> EEPROM read/write 24cXXX chips
* [EMC2301 module](fpc/emc2301/emc2301_IIC.md) -> Fan controller with a PWM fan driver
* [HDC1080 module](fpc/hdc1080/hdc1080_IIC.md) -> High Accuracy Digital Humidity Sensor with Temperature Sensor
* [HTU21D module](ecomet_i2c_sensors/htu21/htu21_python_IIC.md) -> Digital Relative Humidity sensor with Temperature output, calculation of Dew Point
* [INA226,INA260 module](ecomet_i2c_sensors/ina260/ina260_python.IIC.md) -> Precision Digital Current and Power Monitor With Low-Drift, Precision Integrated Shunt
* ISL2802x module ->  will be added python module description
* [MCP3221 module](https://ww1.microchip.com/downloads/en/DeviceDoc/20001732E.pdf) ->  **!NEW!** Low-Power 12-Bit A/D Converter
* [MS5637 module](ecomet_i2c_sensors/ms5637/ms5637_python.IIC.md) ->  Ultra-compact micro altimeter. Integrated digital pressure sensor (24 bit ΔΣ ADC), Operating range: 300 to 1200 mbar, -40 to +85 °C
* [PCA9557 module](ecomet_i2c_sensors/pca9557/pca9557_python.IIC.md) -> Remote8-Bit I2C and SMBusLow-PowerI/O ExpanderWith Reset andConfigurationRegisters
* [PCA9632 module](fpc/pca9632/pca9632_IIC.md) -> 4-bit Fm+ I2C-bus low power LED driver (could be used for motor control)
* [SGP40 module](https://sensirion.com/products/catalog/SGP40) -> Indoor Air Quality Sensor for VOC Measurements
* [SN-GCJA5](ecomet_i2c_sensors/sn_gcja5/sn_gcja5_python.IIC.md) -> Laser Type PM Sensor
* [SSD1306 module](ecomet_i2c_sensors/ssd1306/ssd1306_python.IIC.md) -> SSD1306 is a single-chip CMOS OLED/PLED driver with controller for organic / polymer light emitting
diode dot-matrix graphic display system.
* [TSL25911](ecomet_i2c_sensors/tsl2591/tsl2591_python.IIC.md) -> Ambient Light Sensor



**Software for Chips:**

| Chip            | Python 3 driver | FPC GUI  | Hardware Board | Contributor Notes            | Planned work                   | Requestor Interests           |
| --------------- |:---------------:|:--------:|:--------------:|:----------------------------:|:------------------------------:|:-----------------------------:|
|**!NEW!** AS3935|yes [check](wiki/common/support.md)|    no    | | | |
|AXP209|yes [check](wiki/common/support.md)|    no    |[A10 Olimex](https://www.olimex.com/Products/OLinuXino/A10/open-source-hardware) | Only partially implemented [pdf](ecomet_i2c_sensors/axp209/AXP209.PDF), [check](wiki/common/support.md)   | |
| EEPROM 24cXXX   |[yes](ecomet_i2c_sensors/eeprom/documentation/eeprom_IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board),[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board),[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)| currently tested at 24c01,24c04,24c08,24c16,24c32,24c64                  |                        |                               |
| EMC2301         |[yes](ecomet_i2c_sensors/emc2301/emc2301_python_IIC.md)|[yes](fpc/emc2301/emc2301_IIC.md)|[I02](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_fan_board)|                  |    |  add EMC2302-05 chips in design                             |
| HDC1080         |[yes](ecomet_i2c_sensors/hdc1080/hdc1080_python_IIC.md)|[yes](fpc/hdc1080/hdc1080_IIC.md)|[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)| **!NEW!** python lib not compatible with previous version, see test script                 |    |                               |
| HTU21D          |[yes](ecomet_i2c_sensors/htu21/htu21_python_IIC.md)|    no    |[I03](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_board),[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                              |       |                               |
| INA226, INA260  |[yes](ecomet_i2c_sensors/ina260/ina260_python_IIC.md)|    yes    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board) | |     |
| ISL2802x  |in progress |    no    | | |     |
| MCP3221  |yes [check](wiki/common/support.md) |    no    | | |     |
| MS5637          |[yes](ecomet_i2c_sensors/ms5637/ms5637_python.IIC.md)|    no    |[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |      |
| PCA9557         |[yes](ecomet_i2c_sensors/pca9557/pca9557_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board)|  |            |
| PCA9632         |[yes](ecomet_i2c_sensors/pca9632/pca_9632_python_IIC.md)|[yes](fpc/pca9632/pca9632_IIC.md)|[I04](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_temp_hmd_pressure_board)|                  |                               |                               |
|SN-GCJA5|yes [check](wiki/common/support.md)|    no    | | |     |
|SGP40|yes [check](wiki/common/support.md)|    no    | | |     |
| SSD1306         |[yes](ecomet_i2c_sensors/ssd1306/ssd1306_python.IIC.md)|    no    |[I01](https://github.com/mamin27/ecomet_i2c_raspberry_tools/wiki/_display_current_board) | |     |
|TSL25911|yes [check](wiki/common/support.md)|    no    | | |     |



**Setting of config file for ecomet-i2c-sensors python library:**

Library is looking in directory **~/.comet** for file config.yaml that contains i2c parameters for custom linux distribution and I2C EEPROM memory setting.
Here is a example of config file content:

```sh
comet@orangepizero2:~/.comet $ cat config.yaml
--- # The I2C config file

i2c:
    smb: i2c-3 # set bus i2c-1
    smb_detect: 0..3 # list of monitored smb bus by i2cdetect
    eeprom:
      ic: '24c01'
      slaveaddr: 0x50
      writestrobe: 26 # hold pin low to write to eeprom
    sensor:
      ms5637:
        pressure:
          { min: 600, max: 1300 }
      sn_gcja5:
        PM1_0:
          { min: 0, max: 1200 }
        PM2_5:
          { min: 0, max: 1200 }
        PM10:
          { min: 0, max: 1200 }

```

| parameter | sub-parameter | description | example value |
| --------------- |:---------------:|:--------:|:---:|
| smb: | | name of active i2c in /dev | i2c-1 |
| smb_detect: | | list of monitored i2c neworks used by command **i2c_ecomet_detect** | 0..1 |
| eeprom: | | eeprom section | |
| | ic: | 24x00 series of eeprom chip name | '24c01' |
| | slaveaddr: | address of eeprom chip in hex | 0x50 |
| | writestrobe: | GPIO pin number used as CS (chip select) signal for eeprom IC | 26 |
| sensor: ||part for setting particular sensors ||
| | ms5637: | preasure min max | { min: 600, max: 1300 }|
| | sn_gcja5: | air quality min max ||

**Note: Currently only one eeprom chip could be added.**

**Alternative command for I2C chip detection:**

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
