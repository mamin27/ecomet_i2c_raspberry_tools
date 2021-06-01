# ms9557_IIC python3 module

**Last modification:** 1.06.2021

### List of python files: ###

**Chip description**
The PCA9557 is 8-bit I/O expander. It consists of one 8-bit configuration (inputor output selection),input port,output port,and polarity inversion (active-high) registers.

**pca9557_constant.py**

* list of PCA9557 chip registers and their statuses

**pca9557.py**

* PCA9557 - main chip class
* PCA9557.read_register - read status of one register
* PCA9557.write_register - write new value to chip register
* PCA9557.sw_reset - software Reset CHIP
* PCA9557.port_init - initialize pseudo registers _iport (all input ports) and _oport (all output ports)
* PCA9557.set_io - setting of port configuration (I as input pin) and (O as output pin)
* PCA9557.set_invert - setting of inversion **only for input pins** (I as inverted) and (N as normal use or not inverted)
* PCA9557.set_io_name - add to pseudo registers _iport and _oport PIN name for ease managing for developer
* PCA9557.reset_inputs - set _iport pseudo register to Init status
* PCA9557.reset_outputs - set _oport pseudo register to Init status
* PCA9557.read_input_port - in loop reading of input PINS and set _iport register which maintains changed values ( Set for reached threshold ) and ( Unset for losing threshold)
* PCA9557.write_output_port - write output value into output PIN and update _oport register ( Low for 0V ) and (High for 3.3 - 5V )
* PCA9557.port_display - show in log current status of _iport and _oport pseudo registers (PIN Name, Status, Inversion, Direction)
* PCA9557.port_show_name - actualise _oport and _iport registers under current status of INPUT and OUTPUT registers. ( 'i' update only _iport, 'o' update only _oport, 'io' update both)

for internal use:
* PCA9557.set_bit - change bit in byte to 1
* PCA9557.get_bit - read bit in byte
* PCA9557.unset_bit  - change bit in byte to 0

### How to call python sub? ###

see **pca9557_i2c_test.py** script located in python_test_scripts directory

set logging:
```python
logging.basicConfig(level=logging.INFO
```
set for INFO level logging. possible used DEBUG, ERROR loogin
script will produce log hdc1080.log

initialize chip:
```python
sens = pca9557.PCA9557()
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


port_display:

```python
sens.port_display()
```
Show current status of _iport and _oport pseudo registers that collect more information about PINs (no actual status, but last actualised or measured or set).
* For pins:
    * Name:
       *  User defined name, no space char allowed 
    * Status:
       *  Sleep - not initialized
       *  Init - initialized and waiting for Input action
       *  Thresh. - threshold measure means reached Set or Unset at INPUT pins - ( Inversion will replace reaching Set as 0 at INPUT pin, or as 1 at INPUT pin when normal inversion )
    * Invert:
       *  NoAppl - when PIN is set as OUTPUT inversion mode is not used (Not Applicable)
       *  Invert - INPUT pin is inverted, threshold is 1->0
       *  Normal - INPUT pin is in normal, threshold is 0->1

example:

| PIN   | Name         | Status  | Invert  | Direction |
| ----- |:------------:|:-------:|:-------:|:---------:|
| PIN0  | LED1         | High    | NoApl   | OUTPUT    |
| PIN1  | LED2         | Low     | NoApl   | OUTPUT    |
| PIN2  | BUT_RIG_DWN  | Thresh. | Normal  | INPUT     |
| PIN3  | BUT_RIG_UP   | Init    | Normal  | INPUT     |
| PIN4  | BUT_LFT_DWN  | Init    | Normal  | INPUT     |
| PIN5  | BUT_LFT_UP   | Init    | Invert  | INPUT     |
| PIN6  | DIS_RST      | Init    | NoApl   | OUTPUT    |
| PIN7  | D/C          | Init    | NoApl   | OUTPUT    |

*  PIN0-1 and PIN6-7 are OUTPUTs, 
*  PIN2-5 are INPUTs, buttons
*  PIN0-1 are LED pins used for LED lighting, LED1 is ligh is dimmed, LED2 light is off
*  PIN2 detect pushed button
*  PIN3-5 buttons are not pushed, PIN5 check status 1->0
*  PIN6 and PIN7 was not currently set and are off (Low value is difault value), status will change after writing new status in _oport

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

**Note:** for more details look into pca9557_i2c_test.py
