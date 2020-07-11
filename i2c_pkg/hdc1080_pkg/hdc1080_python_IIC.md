# hdc1080_IIC python3 module

**Last modification:** 11.07.2020

### List of python files: ###

**Chip description**
The HDC1080 is a digital humidity sensor with integrated temperature sensor that provides excellent measurement accuracy at very low power.
The HDC1080 operates over a wide supply range,and is a low cost,low power alternative to competitive olutions in a wide range of common applications. Thehumidity and temperature sensors are factory calibrated.

**hdc1080_constant.py**

* list of hdc1080 chip registers and their statuses

**hdc1080.py**

* HDC1080 - main chip class
* HDC1080.read_register - read status of one register
* HDC1080.write_register - write new value to chip register
* HDC1080.write_mert_invoke - touch (TEMP or HUMDT) register (used before reading TEMP or HUMDT value
* HDC1080.both_measurement - read in one sequence TEMP and HUMDT register, CONF file will be pre-set for sequence reading, values are calculated to celsius degrees and humidity percentage
* HDC1080.measure_temp - read only value of TEMP register
* HDC1080.measure_hmdt - read only value of HUMDT register
* HDC1080.sw_reset - software Reset CHIP
* HDC1080.battery - check status of battery or power supply (must by > 2.4V)
* HDC1080.serial - read SERIAL ID of CHIP
* HDC1080.manufacturer - read MANUFACTURER ID
* HDC1080.deviceid - read DEVICE ID

### How to call python sub? ###

see **hdc1080_i2c_test.py** script

set logging:
```python
logging.basicConfig(level=logging.INFO
```
set for INFO level logging. possible used DEBUG, ERROR loogin
script will produce log hdc1080.log

initialize chip:
```python
sens = hdc1080.HDC1080()
```

sw reset & battery test:
```python
ret = sens.sw_reset()     # make sw reset of chip
ret = sens.battery()      # will check power_supply status, correct when voltage over than 2.4V
```

write to register:
```python 
ret = sens.write_register ( register = *reg_name*, bits = [*bit1*,*bit2* ...])
ret = sens.write_register ( register = *reg_name*, bits = [{*bit_name1* : *bit_value1*}, ... ]
```
example:
``` python
ret = sens.write_register( register = "CONF", bits = ['MODE_BOTH','HRES_RES3','TRES_RES1'])
```

read ID:
```python
(val,ret) = sens.serial()
(val,ret) = sens.manufacturer()
(val,ret) = sens.deviceid()
```
read ID values (unique for each Texas Instruments HDC1080 chip

meausre:
```python
(temp,hmdt, ret) = sens.both_measurement()
(temp, ret) = sens.measure_temp()
(hmdt, ret) = sens.measure_hmdt()
```
measure temperature or humidity sequentially or individually 

ret value:
return value for each procedure (0 - correct, >0 - incorrect)

output of test script:
```shell
pi@raspberrypi:~/ecomet_i2c_tools $ python3 hdc1080_i2c_test.py 
3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0]
ecomet.hdc1080: INFO     Start logging ...
ecomet.hdc1080: INFO     SW Reset correct
ecomet.hdc1080: INFO     Battery > 2.4V, correct
ecomet.hdc1080: INFO     Write CONF register correct
ecomet.hdc1080: INFO     SERIAL Read correct
ecomet.hdc1080: INFO     SER ID: 0127:1A13:DC00
ecomet.hdc1080: INFO     MANUFACTURER Read correct
ecomet.hdc1080: INFO     MAN ID: 5449
ecomet.hdc1080: INFO     DEVICE Read correct
ecomet.hdc1080: INFO     DEV ID: 1050
ecomet.hdc1080: INFO     Measured Temperate BOTH:      26.44 ℃
ecomet.hdc1080: INFO     Measured Humidity BOTH:      57.86 %
ecomet.hdc1080: INFO     Write CONF register correct
ecomet.hdc1080: INFO     Measured Temperate IND:      26.54 ℃
ecomet.hdc1080: INFO     Measured Humidity IND:      57.76 %
```

**Note:** for more details look into hdc1080_i2c_test.py
