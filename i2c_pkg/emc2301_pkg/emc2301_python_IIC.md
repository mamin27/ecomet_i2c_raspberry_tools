# emc2301_IIC python3 module

**Last modification:** 27.09.2020

### List of python files: ###

**Chip description**
The EMC2301 is an SMBus compliant fan controller with a  PWM  fan  driver.  The  fan  driver  is  controlled  by  a programmable  frequency  PWM  driver  and  Fan  Speed Control  algorithm  that  operates  in  either  a  closed  loop fashion  or  as  a  directly  PWM-controlled  device.

**emc2301_constant.py**

* list of emc2301 chip registers and their statuses

**emc2301.py**

* EMC2301 - main chip class
* EMC2301.self_test - check chip connection
* EMC2301.read_register - read status of one register
* EMC2301.write_register - write new value to chip register
* EMC2301.speed - check fan speed calculated in RPM
* EMC2301.productid - chip product id
* EMC2301.manufid - chip manufacture id
* EMC2301.revisionid - chip revisionid

**limitation:**

* function write_register - only CON, FAN_CONF1, FAN_CONF2,
                                           FAN_SETTING, TACH_TARGET, TACH_COUNT, 
                                           FAN_FAIL_BAND

### How to call python sub? ###

**fan_type.py**

*library - parameters for RPM calculation (curently Noctua NF-8A Fan
*poles - number od poles
*edge - number od edge
*multiplier,range,edges - see id emc2301 spread sheet
*fan_tach - frequenci for tachometer monitoring (32.768kHz is internal frequency)

![x](2poles_dc.png  "2 Poles DC Moto")

see **emc2301_i2c_test.py** script

### Measure FAN RPM accuracy ###

For Fan managing is important to know accuracy of Chip speed setting and Fan RPM response. 

To measure FAN accuracy use script:
emc2301_i2c_speed_graph.py > fan.log
*produce file usable for excel:

![xy](nf-a8.png  "Graph of RPM accuracy")
