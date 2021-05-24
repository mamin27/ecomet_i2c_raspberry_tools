# ms5637_IIC python3 module

**Last modification:** 20.05.2021

### List of python files: ###

**Chip description**
The MS5637 is an ultra-compact micro altimeter. It is optimized for  altimeter  and  barometer  applications. Thesensor  module  includes  a  high-linearity  pressure  sensor with  internal  factory-calibrated coefficients. 
Integrated digital pressure sensor (24 bit ΔΣ ADC). Operating range: 300 to 1200 mbar, -40 to +85 °C 

**ms5637_constant.py**

* list of MS5673 chip registers and their statuses

**ms5637.py**

* MS5637 - main chip class
* MS5637.read_register - read status of one register
* MS5637.write_register - write new value to chip register
* MS5637.sw_reset - software Reset CHIP
* MS5637.measure - read in one shot temperature & pressure with deffined accuracy

### How to call python sub? ###

see **ms5637_i2c_test.py** script located in python_test_scripts directory

set logging:
```python
logging.basicConfig(level=logging.INFO
```
set for INFO level logging. possible used DEBUG, ERROR loogin
script will produce log hdc1080.log

initialize chip:
```python
sens = ms5637.MS5637()
```

sw reset & battery test:
```python
ret = sens.sw_reset()     # make sw reset of chip !!necessary command before start CHIP connecting!!
```

write to register:
```python 
sens.write_register(register = <command>, stime = <variable>)
```
register parameter is name of command,
stime is accuracy adviced for measurement calculation, see in table accuracy parameters

| variable | measurement accuracy | accurcy OSR  | Min measure time in [ms]   | Resolution Pressure [mbar]  | Resolution Temp [C]   |
| -------- |:--------------------:|:------------:|:--------------------------:|:---------------------------:|:---------------------:|
| d1_time  | 1                    | 256          | 0.54                       | 0.11                        | 0.012                 |
| d2_time  | 2                    | 512          | 1.06                       | 0.062                       | 0.009                 |
| d3_time  | 3                    | 1024         | 2.08                       | 0.039                       | 0.006                 |
| d4_time  | 4                    | 2048         | 4.13                       | 0.028                       | 0.004                 |
| d5_time  | 5                    | 4096         | 8.22                       | 0.021                       | 0.003                 |
| d6_time  | 6                    | 8192         | 16.44                      | 0.016                       | 0.002                 |

variable dX_time is defined in MS5637 class.
also PROM calibration variable are defined in MS5637 class as (c1 - c6)

example:
``` python
sens.write_register(register = 'D2_CONV_256', stime = sens.d1_time)
```

read from register:

```python
(val,ret) = sens.read_register(<register>)
```
read content of register from MS5637 chip, it is only 'ADC_READ' register used for reading measured Temperature and Pressure

example:
``` python
D2 = sens.read_register('ADC_READ')
```

meausre:
```python
(temp_celsius,temp_fahrenheit,pressure, ret) = sens.measure (accuracy = <acc_number 1-6>)
```
measure temperature in celsius, fahrenheits and pressure in mbar

ret value:
return value for each procedure (0 - correct, >0 - incorrect)

output of test script:
```shell
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 ms5637_i2c_test.py
3.7.3 (default, Jan 22 2021, 20:04:44)
[GCC 8.3.0]
ecomet.ms5637: INFO     Start logging ...
ecomet.ms5637: INFO     SW Reset correct
ecomet.ms5637: INFO     Pressure =    1002.22 mbar
ecomet.ms5637: INFO     Temperature in Celsius =      24.00 ℃
ecomet.ms5637: INFO     Temperature in Fahrenheit =      75.19 F
```

**Note:** for more details look into ms5637_i2c_test.py
