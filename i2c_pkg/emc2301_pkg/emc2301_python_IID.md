# emc2301_IID python3 module Details

**Last modification:** 07.03.2021

**emc2301.py**

* EMC2301 - main chip class
* EMC2301.self_test - check chip connection

* EMC2301.read_register - read status of one register
* EMC2301.write_register - write new value to chip register
* EMC2301.speed - check fan speed calculated in RPM
* EMC2301.fan_kick_up - measure RPM samples after kick new speed value
  * call: fan_kick_up(offset,interval,sum_sample,new_value)
  * offset - time offset in sec before kick
  * interval - measure time between two samples in sec
  * sum_sample - number of samples
  * new_value - new RPM value
* EMC2301.productid - chip product id
* EMC2301.manufid - chip manufacture id
* EMC2301.revisionid - chip revisionid

**function: EMC2301**


* **method: self_test**
test if chip communicate by I2C lines
```python3
def EMC2301.self_test->int
  return
  0 - chip connected
  1 - chip not connected

from  i2c_pkg.emc2301_pkg import emc2301
sens = emc2301.EMC2301() 
ret = sens.self_test()
if ret == 0 :
    print(":TEST_PASSED:")
else :
    print(":MISSING_CHIP:")
``` 

* **method: read_register**
read from chip register
```python3
def EMC2301.read_register(
   param register: string) ->
type1:     (param:byte int, param ret: int) or
type2:     (param:byte_lo int,param:byte_hi int, param ret: int)

for ['CONF','FAN_STAT','PWM_DIVIDE','FAN_SETTING','FAN_CONF1','FAN_CONF2',
     'FAN_SPIN','DRIVE_FALL','FAN_INTERRUPT',
     'GAIN', 'FAN_SPIN_UP', 'FAN_MAX_STEP','FAN_MIN_DRIVE',
     'PWM_POLARITY','PWM_OUTPUT','PWM_BASE',
     'TACH_COUNT','FAN_FAIL_BAND_LB','FAN_FAIL_BAND_HB','TACH_TARGET_LB','TACH_TARGET_HB','TACH_READ_LB','TACH_READ_HB',
     'PRODUCT_ID','MANUF_ID','REVISION_ID','SOFTWARE_LOCK']
 is type1
 
 for ['TACH_READ']
 is type2

if ret == 0 :
  read command OK
else :
  read command FALSE

call method:

from  i2c_pkg.emc2301_pkg import emc2301
emc = EMC2301()
emc.read_register( register = 'CONF' )[0]

```

* **method: write_register**
write to chip register
```python3
def EMC2301.write_register(
  param registe: string, 
  param bits = list of strings default(None), 
  param bit = list of strings default(None), 
  param value = real default(None)) ->
  param ret int
  
if ret == 0 :
  read command OK
else :
  read command FALSE
  

1)
for register ['CONF','FAN_CONF1','FAN_CONF2','FAN_SPIN_UP','GAIN',
              'FAN_INTERRUPT','PWM_POLARITY','PWM_OUTPUT','PWM_BASE','SOFTWARE_LOCK','SOFTWARE_LOCK','FAN_CONF1','FAN_CONF2','GAIN','FAN_SPIN_UP',
              'FAN_INTERRUPT','PWM_POLARITY','PWM_OUTPUT','PWM_BASE']
              
set bits and bit (each register use different bits and bit)
see ems2301_constant.py and fan_type.py
if bits use only two status use <BIT_NAM> for SET and <BIT_NAME>_CLR for UNSET 

example:
from  i2c_pkg.emc2301_pkg import emc2301
from i2c_pkg.emc2301_pkg import fan_type
fan_list = { 'RANGE' : fan_type.RANGE , 'EDGES' : fan_type.EDGES }
sens = emc2301.EMC2301()
sens.write_register(register = 'FAN_CONF1', bits = ['EN_ALGO_CLR'])
sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )


for registr ['FAN_SETTING','FAN_MAX_STEP','FAN_MIN_DRIVE','PWM_DIVIDE',
              'TACH_TARGET','FAN_FAIL_BAND','TACH_COUNT']

set value

example:
from  i2c_pkg.emc2301_pkg import emc2301
sens.write_register(register = 'FAN_SETTING', value = 160)

```

* **method: speed**
calculate speed under mathematic algorithm
```python3
def EMC2301.speed() ->
  param out int
  param ret int
  
out - Integer calculated from settings or next register under mathematic algorithm:
out = int(1/fan_list['POLES'] * ((fan_list['EDGE'] - 1)/(res * 1/fan_list['MULTIPLIER'])) * fan_list['FAN_TACH'] * 60)
  
if ret == 0 :
  read command OK
else :
  read command FALSE
  
example:

speed = 16
while speed <= 255 :
   measure = []
   for i in range (10) :
     measure.append(sens.speed()[0])   
     sleep(0.5)
   print ('{}:{}'.format(speed,int(statistics.mean(measure))))
   sens.write_register(register = 'FAN_SETTING', bits = [speed])
   speed = speed + 1
```

* **method: fan_kick_up**
read more speed values in one measure cycle only in DIRECT MODE
```python3
 def fan_kick_up (
 param: offset float,     # time interval waiting before start measure
 param: interval float,   # wait time between two samples 
 param: sum_sample int,   # summary of measure samples after start
 param: new_value float,  # new speed value (in percentage) how the speed value will change
 param: time_offset float Default(None)) :  #second offset setting when first offset ends
 ->
 param: sample list       # list of measured speed data
 param: time list         # list of time when sample data was measured


example:
from time import sleep
sleep(5)
sens.write_register(register = 'FAN_MAX_STEP', value = 63)

(v_interva, v_sum_sample) = (0.001,3000)
sample1 = []
time1 = []
(sample1,time1) = sens.fan_kick_up(offset = 10, time_offset = 10, interval = v_interva, sum_sample = v_sum_sample, new_value = 170)

sample2 = []
time2 = []
(sample2,time2) = sens.fan_kick_up(offset = 5, time_offset = v_interva * v_sum_sample + 15, interval = v_interva, sum_sample = v_sum_sample, new_value = 100)

(v_interva, v_sum_sample) = (0.001,4000)
sample3 = []
time3 = []
(sample3,time3) = sens.fan_kick_up(offset = 5, time_offset = v_interva * v_sum_sample + 20, interval = v_interva, sum_sample = v_sum_sample, new_value = 255)

sample = sample1 + sample2 + sample3
time = time1 + time2 + time3

for index in range (0,10000) :
	print ('{}:{}:{}'.format(index,sample[index],time[index]))
```

* **method: productid**
read chip product id from PRODUC_ID register
```python3
()
-> param: product_id int,
   param: ret int
   
if ret == 0 :
  read command OK
else :
  read command FALSE

example:
(val,ret) = sens.productid()
sens._logger.info('PRODUCT Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('PRODUCT ID: %s',format(val))
```

* **method: manufid**
read chip product id from MANUF_ID register
```python3
()
-> param: manuf_id int,
   param: ret int
   
if ret == 0 :
  read command OK
else :
  read command FALSE
  

example:
(val,ret) = sens.manufid()
sens._logger.info('MANUFID Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MANUF ID: %s',format(val))
```

* **method: revisionid**
read chip product id from REVISION_ID register
```python3
()
-> param: revision_id int,
   param: ret int
   
if ret == 0 :
  read command OK
else :
  read command FALSE

example:
(val,ret) = sens.revisionid()
sens._logger.info('REVISIONID Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('REVISION ID: %s',format(val))
```

**function: conf_register_list** - list of all chip register (used in update register status)
```python3
def conf_register_list() 
  -> dictionary{
    dictionary,  #reg_conf
    dictionary,  #reg_spin_up
    dictionary,  #reg_fan_stat
    dictionary,  #reg_pwm
    dictionary,  #reg_tach
    dictionary   #reg_id
    }:
 ```
 
 ```python3
 from  i2c_pkg.emc2301_pkg import emc2301
 sens = emc2301.EMC2301()
 register = sens.speed()[0]
 print ('{}'.format(register))
```
