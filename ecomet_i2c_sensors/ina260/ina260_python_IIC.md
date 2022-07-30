# ina260_IIC python3 module

**Last modification:** 1.08.2022

### List of python files: ###

**Chip description**
The INA260 Precision Digital Current and Power Monitor With Low-Drift, Precision Integrated Shunt

**ina260_constant.py**

* list of INA260 chip registers and their statuses

**ina260_ui_constant.py**

* default values of important registers for more INA260 chips (chip0, chip1..)
- class set_measure_0   ... for chip0
- class set_measure_1   ... for chip1

**ina260.py**
- constant are locateded in **ina260_constant.py**

* INA260 - main chip class
* INA260.self_test - check chip connection (allowed chip_id hex(0x227),hex(0x226) )
* INA260.setup - setup chip after class initialization (used automaticaly)

* INA260.measure_voltage - run voltage measuring
* INA260.measure_current - run current measuring

internal function:
* INA260.read_register - read status of registers ['VBUSCT','ISHCT','AVGC','MODE','VOLTAGE','CURRENT' ]
* INA260.write_register - write new value to chip registers ['VBUSCT','ISHCT','AVGC','MODE']
* INA260.current_conversion - conversoin current units between [mA,A]
* INA260.voltage_conversion - conversion voltage units between [mV,V]

**ina260_ui.py**
- ina260_ui.py uses ina260.py library
- constant are locateded in **ina260_ui_constant.py**

* INA260_UI - main measure class
* INA260_UI.measure_ui - run measurement of voltage and current at once
* INA260_UI.measure_u - run measurement of voltage
* INA260_UI.measure_i - run measurement of current

**initialize chip**
-- set chip address 
   *  '0#0x40'  ...`Chip number`#`chip address`
   *  0   address of chip read from **ina260_constant.INA260_ADDRESS1**
   *  1   address of chip read from **ina260_constant.INA260_ADDRESS2**
-- set attributes 
  * time (set default time of measure in seconds)
  * i_unit (set default current units [mA,A]
  * u_unit (set default voltage units [mV,V]
  * avgc ()
  * ishct ()
  * vbusct ()
  * mode

if you not set the attributes it will be read from **ina260_ui_constant.py**, values are from ina260_constat.py
```sh
class set_measure_0(object):
# set parameters of measure for INA260 chip 0
	_mconst = ina260_constant.register
	AVGC	= _mconst.COUNT_1					# average count
	ISHCT	= _mconst.TIME_1_1_ms				# measure current time
	VBUSCT	= _mconst.TIME_1_1_ms				# measure voltage time
	MODE	= _mconst.MODE_SHUNT_CURRENT_CONT	# measure mode
```

example1:
   
```python
from ecomet_i2c_sensors.ina260 import ina260, ina260_ui

chip0 = ina260_ui.INA260_UI(chip = '0#0x40', time = 0.01, i_unit = 'mA', v_unit = 'V')
chip1 = ina260_ui.INA260_UI(chip = '1#0x45', time = 0.01, i_unit = 'mA', v_unit = 'V')
```

example2:

```python
from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

chip0 = ina260_ui.INA260_UI(chip = '0#0x44', time = 1, v_unit = 'mV', i_unit = 'mA', mode = ina260_constant.register.MODE_CUR_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, vbusct = ina260_constant.register.TIME_1_1_ms, ishct = ina260_constant.register.TIME_1_1_ms
```

**list content of INA260 registers:**
- used for current status of registers

```python
from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

sens0 = ina260.conf_register_list(address = 0x40)
sens1 = ina260.conf_register_list(address = 0x45)
print ('Reg:{}',format(sens0))
print ('Reg:{}',format(sens1))
```

output:
```sh
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 ./test.py
Reg:{} {'CONF': {'RESET': 'N/A', 'AVGC': 1, 'VBUSCT': '1.1ms', 'ISHCT': '1.1ms', 'MODE': 'Cur-Volt-Continued'}, 'MASK_ENBL': {'OCL': 'N/A', 'UCL': 'N/A', 'BOL': 'N/A', 'BUL': 'N/A', 'POL': 'N/A', 'CNVR': 'ASSERTED', 'AFF': 'OFF', 'CVRF': 'CLEAR', 'OVF': 'EXCEED', 'APOL': 'NORMAL', 'LEN': 'TRANSP'}, 'MANUF': {'ID': 'TI'}, 'DIE': {'DID': '0x227', 'RID': 0}}
Reg:{} {'CONF': {'RESET': 'N/A', 'AVGC': 1, 'VBUSCT': '1.1ms', 'ISHCT': '1.1ms', 'MODE': 'Cur-Volt-Continued'}, 'MASK_ENBL': {'OCL': 'N/A', 'UCL': 'N/A', 'BOL': 'N/A', 'BUL': 'N/A', 'POL': 'N/A', 'CNVR': 'ASSERTED', 'AFF': 'OFF', 'CVRF': 'CLEAR', 'OVF': 'EXCEED', 'APOL': 'NORMAL', 'LEN': 'TRANSP'}, 'MANUF': {'ID': 'TI'}, 'DIE': {'DID': '0x227', 'RID': 0}}
```


**functions: INA260**

* **method: self_test**
test if chip communicate by I2C lines

```sh
def INA260.self_test ()
return value (integer)
  0 - INA260 chip connected
  1 - INA260 chip not connected
```

```python
from ecomet_i2c_sensors.ina260	import ina260

try:
  inaA = ina260.INA260(address=0x40,busnum=1)
  chip0 = inaA.self_test()
  
  if not chip0 == 0 :
    statA = 'NOK'
  else :
    statA = 'OK'
  
except:
  statA = 'NCON'
try:  
  inaB = ina260.INA260(address=0x46,busnum=1)
  chip1 = inaB.self_test()
  
  if not chip1 == 0 :
    statB = 'NOK'
  else :
    statB = 'OK'
  
except:
  statB = 'NCON'

print (':TEST::Address::#A:{}::#B:{}'.format(statA,statB))
``` 

* **method: measure_voltage**
run measure of voltage at dedicated chip

```sh
def INA260.measure_voltage(stime=0.1,unit='mV')
attributes (stime = integer [seconds];
                 units = enum ['mV','V']
return values (size = integer;
                      units = enum['mV,'V'];
					  buf = dictionary {number: measured_value})
```

Example:
```python3
from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

buf = {}
sens0 = ina260.INA260(address = 0x40)
(size,unit,buf) = sens0.measure_voltage(stime=0.1,unit='mV')
print ('Size: ',format(size))
print ('Units: ', format(unit))
print ('Values: ', format(buf))
```

Output:
```sh
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 ./test.py
Size:  46
Units:  mV
Values:  {0: 0.0, 1: 0.0, 2: 5.0, 3: 2.5, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 6.25, 12: 1.25, 13: 0.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.0, 18: 0.0, 19: 0.0, 20: 6.25, 21: 1.25, 22: 0.0, 23: 0.0, 24: 0.0, 25: 0.0, 26: 0.0, 27: 0.0, 28: 2.5, 29: 6.25, 30: 1.25, 31: 0.0, 32: 0.0, 33: 0.0, 34: 0.0, 35: 0.0, 36: 0.0, 37: 2.5, 38: 5.0, 39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0, 43: 0.0, 44: 0.0, 45: 0.0}
```

* **method: measure_current**
run measure of current at dedicated chip

```sh
def INA260.measure_current(stime=0.1,unit='mA')
attributes (stime = integer [seconds];
                 units = enum ['mA','A']
return values (size = integer;
                      units = enum['mA,'A'];
					  buf = dictionary {number: measured_value})
```

Example:
```python3
from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

buf = {}
sens0 = ina260.INA260(address = 0x40)
(size,unit,buf) = sens0.measure_current(stime=0.1,unit='mA')
print ('Size: ',format(size))
print ('Units: ', format(unit))
print ('Values: ', format(buf))
```

Output:
```sh
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 ./test.py
Size:  45
Units:  mA
Values:  {0: 1.25, 1: 0.0, 2: -1.25, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: -1.25, 10: 0.0, 11: -1.25, 12: 0.0, 13: 0.0, 14: 1.25, 15: 0.0, 16: 0.0, 17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 22: 0.0, 23: 0.0, 24: 1.25, 25: 1.25, 26: 0.0, 27: 0.0, 28: -1.25, 29: 0.0, 30: 0.0, 31: 0.0, 32: 0.0, 33: 0.0, 34: -1.25, 35: 0.0, 36: 0.0, 37: 0.0, 38: -1.25, 39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0, 43: 0.0, 44: 0.0}
```

* **method: measure_ui**
run measure of current and voltage at once at dedicated chip

see [ina260_i2c_ui.py](../../../python_test_scripts/ina260/ina260_i2c_ui.py)

data are temporary stored in __ina_chip__ file because data will be read parallely
final result will be stored in __file = 'ina260.data'__ in json format

* **method: measure_i**
run measure of current and voltage at once at dedicated chip

see [ina260_i2c_i_1.py](../../../python_test_scripts/ina260/ina260_i2c_i_1.py)

final result will be stored in __file = 'ina260.data'__ in json format

* **method: measure_u**
run measure of current and voltage at once at dedicated chip

see [ina260_i2c_u_1.py](../../../python_test_scripts/ina260/ina260_i2c_i_1.py)

final result will be stored in __file = 'ina260.data'__ in json format

**All test script: INA260:**

see directory  [INA260 test scripts](../../../python_test_scripts/ina260)



| file name | Description |
| -------- | -------- |
|i2c_address_search.py     | Search INA chip at I2C bus     | 
|i2c_address_test.py   | Test if INA chip A & B are connected      | 
|ina260_i2c_graph.py   | Text      | 
|ina260_i2c_i_1.py    | Collecting measurements from INA chip A I      | 
|ina260_i2c_i_1_u_2.py     | Text      | 
|ina260_i2c_i_2.py   |  Collecting measurements from INA chip B I       | 
|ina260_i2c_test.py     | Text      | 
|ina260_i2c_u_1.py     | Collecting measurements from INA chip A U     | 
|ina260_i2c_u_2.py   | Collecting measurements from INA chip B U       | 
|ina260_i2c_ui.py    | Collecting measurements from INA chip A&B and U&I      | 
|ina260_i2c_ui_1.py   | Collecting measurements from INA chip A U&I       | 
|ina260_i2c_ui_1_i_2.py    | Collecting measurements from INA chip A U&I  and chip B I        | 
|ina260_i2c_ui_1_u_2.py  |  Collecting measurements from INA chip A U&I  and chip B U      | 
|ina260_i2c_ui_2.py     | Collecting measurements from INA chip B U&I        | 
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A

