# htu21_IIC python3 module

**Last modification:** 31.07.2020

### List of python files: ###

**Chip description**
The HTU21D is a new digital humidity sensor with temperature output. Every sensor is individually calibrated and tested. 

**htu21_constant.py**

* list of HTU21D chip registers and their statuses

**htu21.py**

* HTU21 - main chip class
* HTU21.read_register - read status of one register
* HTU21.write_register - write new value to chip register
* HTU21.measure_temp - read only value of TEMP register
* HTU21.measure_hmdt - read only value of HUMDT register
* HTU21.sw_reset - software Reset CHIP
* HTU21.battery - check status of battery or power supply (must by > 2.25V)
* HTU21.dew_point - temperature at which the water vapor in the air becomes saturated and condensation begins

### How to call python sub? ###

see **htu21_i2c_test.py** script

set logging:
```python
logging.basicConfig(level=logging.INFO
```
set for INFO level logging. possible used DEBUG, ERROR loogin
script will produce log htu21.log

initialize chip:
```python
sens = htu21.HTU21()
```

sw reset & battery test:
```python
ret = sens.sw_reset()     # make sw reset of chip
ret = sens.battery()      # will check power_supply status, correct when voltage over than 2.25V
```

write to register:
```python 
ret = sens.write_register ( register = *reg_name*, bits = [*bit1*,*bit2* ...])
ret = sens.write_register ( register = *reg_name*, bits = [{*bit_name1* : *bit_value1*}, ... ]
```
example:
``` python
ret = sens.write_register( register = "WRITE_USER", bits = ['MEAS_RES1','HEAT_DISABLE'])

meausre:
```python
(temp, ret) = sens.measure_temp()
(hmdt, ret) = sens.measure_hmdt()
(hmdt, ret) = sens.dew_point()
```
measure temperature, humidity or dew point individually 

ret value:
return value for each procedure (0 - correct, >0 - incorrect)

output of test script:
```shell
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 htu21_i2c_test.py 
3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0]
ecomet.htu21: INFO     Start logging ...
ecomet.htu21: INFO     SW Reset correct
ecomet.htu21: INFO     Battery > 2.4V, correct
ecomet.htu21: INFO     Write WRITE_REG register correct
{'REG': {'HRES': '12BIT', 'TRES': '14BIT', 'BAT': 'GOOD', 'HEAT': 'DISABLE', 'OTP': 'DISABLE'}}
ecomet.htu21: INFO     Measured Temperate IND:      27.99 ℃
ecomet.htu21: INFO     Measured Humidity IND:      36.62 %
ecomet.htu21: INFO     Write WRITE_REG register correct
{'REG': {'HRES': '11BIT', 'TRES': '11BIT', 'BAT': 'GOOD', 'HEAT': 'DISABLE', 'OTP': 'DISABLE'}}
ecomet.htu21: INFO     Measured Temperate IND:      28.00 ℃
ecomet.htu21: INFO     Measured Humidity IND:      36.62 %
{'MEASURE': {'TEMP': 27.968281249999997, 'HMDT': 36.6177978515625, 'DEW_POINT': 11.826074255509837}}
ecomet.htu21: INFO     Calculated Dew Point IND:      11.85 ℃
```

**Note:** for more details look into htu21_i2c_test.py
