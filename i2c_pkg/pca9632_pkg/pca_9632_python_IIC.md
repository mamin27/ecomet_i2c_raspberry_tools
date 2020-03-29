# pca9632_IIC python3 module

**Last modification:** 29.03.2020

###List of python files:###

**pca9632_constant.py**

* list of pca9632 chip registers and their statuses

**pca9632.py**

* read_pca9632 - read all registers from chip
* software_reset - make software reset of chip
* ledout_clean - set all LEDRx to OFF status
* PCA9362 - main chip class
* PCA9632.read_register - read status of one register
* PCA9632.write_register - write new value to chip register

### How to call python sub? ###

see **pca_6532_i2c_test.py **script

initialization:
```python
pwm = pca9632.PCA9632()

read all registers:
```python
reg_view = pca9632.read_pca9632();
```

write to register:
```python
ret = pwm.write_register ( register = *reg_name*, bits = [*bit1*,*bit2* ...])
ret = pwm.write_register ( register = *reg_name*, bits = [{*bit_name1* : *bit_value1*}, ... ]
```
example:
```
ret = pwm.write_register( register = "MODE2", bits = ['INVRT_N'])

ret = pwm.write_register( register = 'LEDOUT', bits = [{'LDR0' : 'ON' }, {'LDR1' : 'PWM_GRPPWM'}, {'LDR2' : 'OFF'}, {'LDR3' : 'PWM'}])
```

Register status value:

INVERT - ON INVERT status
INVERT_N - OFF INVERT status
see pca9632_constat.py