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


**method: self_test**
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



