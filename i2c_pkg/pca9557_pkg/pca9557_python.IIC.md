# pca9557_IIC python3 module

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
script will produce log pca9557.log

initialize chip:
```python
sens = pca9557.PCA9557()
```

sw reset:
```python
ret = sens.sw_reset()     # make sw reset of chip !!necessary command before start CHIP connecting!!
```
default setting of REGISTERs

**return value:** ```(<ret>)```
   *  ret = 0 -> correct setting REGISTERS, ret > 0 -> issue during setting

read from register:
```python 
value = sens.read_register(register = <command>)[0]
```
register parameter is name of chip register ('REGISTER0-3')

**return value:** ```(<8bit value>, <ret>)```
   *  first return parameter is content of register
   *  ret = 0 -> correct writing into register, ret > 0 -> issue during reading process

write to register:
```python 
ret = sens.write_register(register = <command>, value = <variable>)
```
register parameter is name of chip register ('REGISTER0-3'),
value is 8bit value written into register
   
**return value:** ```(<ret>)```
   *  ret = 0 -> correct writing into register, ret > 0 -> issue during writing process

port_init:
```python
self.port_init()
```

initialize pseudo registers _iport (all input ports) and _oport (all output ports)
both registers are object registe that you can directly manage which are set to default values during object init.
it's array of 8 items (for each PIN one array) 

```[10,Sleep,'X-------',NI]   #[<pin number>,<pin status>,<pin name>,<pin inversion>```
* ```<pin number>```
    * from 0 - 7 coresponded to chip pin number P0-P7, default value 10 means no existing pin
* ```<pin status>```
    * Sleep - INPUT-OUTPUT (pin is not initialized) -> could not read or write to it
    * Init - INPUT-OUTPUT (pin is initialized) -> prepared for reading or writing to it
    * Measure - INPUT (prepared for measure input pin)
    * Threshold - INPUT (pin reached threshold value)
    * High - OUTPUT (pin set to logical value 1)
    * Low - OUTPUT (pin set to logical value 0)
* ```<pin name>```
    * INPUT-OUTPUT use word without space and other special characters, only _ character is accepted
* ```<pin inversion>```
    * Invert - INPUT pin is inverted
    * Normal - INPUT pin si not inverted
    * NoAppl - OUTPUT inversion is not applicable

Values of pin statuses are constant of pca9557.py library
sub port_init is called internally by port_io sub, but could be used also externally

**return value:** ```(0)```
   *  0 -> correctly initialized

set_io: 
```python
set_io(<pattern>)
# example
set_io('OOIIIIOO')
```
setting of port configuration (I as input pin) and (O as output pin)
at end of def is called port_init()

**return value:** ```(<mask_byte>,<ret>)```
   *  mask_byte - byte O->0, I->1 used for REGISTER3 (is already set in def)
   *  ret = 0 -> correct writing into register, ret > 0 -> issue during reading process

set_invert:  
```python
set_invert('<pattern>')
#example
set_invert('NNNNNNNI')
```
setting of inversion **only for input pins** (I as inverted) and (N as normal use or not inverted)

**return value:** ```(<mask_byte>,<ret>)```
   *  mask_byte - byte N->0, I->1 used for REGISTER3 (is already set in def)
   *  ret = 0 -> correct writing into register, ret > 0 -> issue during reading process

set_io_name: 
```python
set_io_name(port_arr=<array>)
#example
sens.set_io_name(port_arr = [[0,'LED1'],[1,'LED2'],[2,'BUT_RIG_DWN'],[3,'BUT_RIG_UP'],
                             [4,'BUT_LFT_DWN'],[5,'BUT_LFT_UP'],[6,'DIS_RST'],[7,'D/C']])
```
add to pseudo registers _iport and _oport PIN name for ease managing for developer
* array:  8 items
   *  <port_number> (0-7)
   *  <port_name> 'string'

**return value:** ```(0)```
   *  0 -> correctly initialized

reset_inputs: 
```python
reset_inputs()
```
set _iport pseudo register to Init status
* set _iport register set all named inputs to default status status ['Init']

reset_outputs: 
```python
reset_outputs()
```
set _oport pseudo register to Init status
* set _oport register set all named outputs to default status status ['Init']

read_input_port:
```python
interrupt = sens.read_input_port(thr = 'Unset', mtime = 6, offset = 0.5)
```
in loop reading of input PINS and set _iport register which maintains changed values ( Set for reached threshold ) and ( Unset for losing threshold)

*  mtime = max time of loop length in [seconds]
*  offset = waiting time after catching first input threshold (waiting for multiple touching inputs) in [seconds]

example:

| PIN   | Name         | Status     | Note           |
| ----- |:------------:|:----------:|:--------------:|
|    2  | BUT_RIG_DWN  | Measure    |                |
|    3  | BUT_RIG_UP   | Measure    |                |
|    4  | BUT_LFT_DWN  | Threshold  | <- catched pin |
|    5  | BUT_LFT_UP   | Measure    |                |

```python
ecomet.pca9557: INFO     PIN0: 2 : 3 : BUT_RIG_DWN
ecomet.pca9557: INFO     PIN1: 3 : 3 : BUT_RIG_UP
ecomet.pca9557: INFO     Loop:0 -> PIN4: BUT_LFT_DWN ... pushed
ecomet.pca9557: INFO     PIN2: 4 : 4 : BUT_LFT_DWN
ecomet.pca9557: INFO     PIN3: 5 : 3 : BUT_LFT_UP
ecomet.pca9557: INFO     PIN4: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN5: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN6: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN7: 10 : 20 : X-------
```


**return value:** ```(<_iport>)```
   *  array of values [<pin_number>,<pin_status>,<pin_name>]

write_output_port:
```python
write_output_port (status = <pin_output_status>, pin = <pin_name>)
#example
sens.write_output_port (status = pca9557.Low, pin = 'LED1')
```
write output value into output PIN and update _oport register ( Low for 0V ) and (High for 3.3 - 5V )
*  status = pin output status 
   *  Low = 0V
   *  High = 3.3 - 5V

**return value:** ```(<_oport>,<ret>)```
*  array of values [<pin_number>,<pin_status>,<pin_name>]
*  ret = 0 -> correct writing into register, ret > 0 -> issue during reading process

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
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 pca9557_i2c_test.py
3.7.3 (default, Jan 22 2021, 20:04:44)
[GCC 8.3.0]
ecomet.pca9557: INFO     Start logging ...
ecomet.pca9557: INFO     Show Ports:
ecomet.pca9557: INFO     PIN0: LED1 : OUTPUT : 3
ecomet.pca9557: INFO     PIN1: LED2 : OUTPUT : 3
ecomet.pca9557: INFO     PIN2: BUT_RIG_DWN : INPUT : 2
ecomet.pca9557: INFO     PIN3: BUT_RIG_UP : INPUT : 2
ecomet.pca9557: INFO     PIN4: BUT_LFT_DWN : INPUT : 2
ecomet.pca9557: INFO     PIN5: BUT_LFT_UP : INPUT : 2
ecomet.pca9557: INFO     PIN6: DIS_RST : OUTPUT : 3
ecomet.pca9557: INFO     PIN7: D/C : OUTPUT : 3
ecomet.pca9557: INFO     Push 10 times any Button ....
ecomet.pca9557: INFO     PIN0: 2 : 3 : BUT_RIG_DWN
ecomet.pca9557: INFO     PIN1: 3 : 3 : BUT_RIG_UP
ecomet.pca9557: INFO     Loop:0 -> PIN4: BUT_LFT_DWN ... pushed
ecomet.pca9557: INFO     PIN2: 4 : 4 : BUT_LFT_DWN
ecomet.pca9557: INFO     PIN3: 5 : 3 : BUT_LFT_UP
ecomet.pca9557: INFO     PIN4: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN5: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN6: 10 : 20 : X-------
ecomet.pca9557: INFO     PIN7: 10 : 20 : X-------
ecomet.pca9557: INFO     Show Ports:
ecomet.pca9557: INFO     PIN    Name            Status          Invert          Direction
ecomet.pca9557: INFO     -----------------------------------------------------------------------------------------
ecomet.pca9557: INFO     PIN0:  LED1 :          Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN1:  LED2 :          Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN2:  BUT_RIG_DWN :   Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN3:  BUT_RIG_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN4:  BUT_LFT_DWN :   Thresh. :       Normal :        INPUT
ecomet.pca9557: INFO     PIN5:  BUT_LFT_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN6:  DIS_RST :       Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN7:  D/C :           Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     Show Ports:
ecomet.pca9557: INFO     PIN    Name            Status          Invert          Direction
ecomet.pca9557: INFO     -----------------------------------------------------------------------------------------
ecomet.pca9557: INFO     PIN0:  LED1 :          Low     :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN1:  LED2 :          High    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN2:  BUT_RIG_DWN :   Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN3:  BUT_RIG_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN4:  BUT_LFT_DWN :   Thresh. :       Normal :        INPUT
ecomet.pca9557: INFO     PIN5:  BUT_LFT_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN6:  DIS_RST :       Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN7:  D/C :           Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     Show Ports:
ecomet.pca9557: INFO     PIN    Name            Status          Invert          Direction
ecomet.pca9557: INFO     -----------------------------------------------------------------------------------------
ecomet.pca9557: INFO     PIN0:  LED1 :          High    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN1:  LED2 :          Low     :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN2:  BUT_RIG_DWN :   Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN3:  BUT_RIG_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN4:  BUT_LFT_DWN :   Thresh. :       Normal :        INPUT
ecomet.pca9557: INFO     PIN5:  BUT_LFT_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN6:  DIS_RST :       Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN7:  D/C :           Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     Show Ports:
ecomet.pca9557: INFO     PIN    Name            Status          Invert          Direction
ecomet.pca9557: INFO     -----------------------------------------------------------------------------------------
ecomet.pca9557: INFO     PIN0:  LED1 :          High    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN1:  LED2 :          High    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN2:  BUT_RIG_DWN :   Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN3:  BUT_RIG_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN4:  BUT_LFT_DWN :   Thresh. :       Normal :        INPUT
ecomet.pca9557: INFO     PIN5:  BUT_LFT_UP :    Init    :       Normal :        INPUT
ecomet.pca9557: INFO     PIN6:  DIS_RST :       Init    :       NotApl :        OUTPUT
ecomet.pca9557: INFO     PIN7:  D/C :           Init    :       NotApl :        OUTPUT
R0 = 63
R1 = 3
R2 = 0
R3 = 60

```

**Note:** for more details look into pca9557_i2c_test.py
