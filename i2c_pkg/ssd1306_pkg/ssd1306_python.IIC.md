# ssd1306_IIC python3 module

**Last modification:** 14.06.2021

### List of python files: ###

**Chip description**
The SSD1306 OLED/PLED dot-matrix display IC's. 128x64 dots.

**ssd1306_constant.py**

* list of SSD1306 chip registers and their statuses

**ssd1306.py**

* SSD1306 - main chip class
* SSD1306.set_command - call commands in command mode.
* SSD1306.display - display prepared image into chip
* SSD1306.data - call data in data mode.
* SSD1306.sw_reset - software Reset CHIP (emulate HW reset)
* SSD1306.setup - initial setup of CHIP, not necessary to use

**render.py**
file under MIT License, Copyright (c) 2019 Vincent Studio
library for rendering image in virtual canvas in defined size
* used PIL library and feature Image, ImageDraw

### How to call python sub? ###

see **ssd1309_i2c_test.py** script located in python_test_scripts directory

set logging:
```python
logging.basicConfig(level=logging.INFO
```
set for INFO level logging. possible used DEBUG, ERROR loogin
script will produce log ssd1309.log

initialize chip:
```python
sens = ssd1309.SSD1309()
```

sw reset:
```python
ret = sens.sw_reset()     # make sw reset of chip, emulate hardware reset of chip
```
default preparation of chip like it is after hardware reset.

**return value:** ```(<ret>)```
   *  ret = 0 -> correct software reset, ret > 0 -> issue during resetting

setup:
```python
ret = sens.setup()
```

my recommended Display setup, similar to sw reset.

**return value:** ```(<ret>)```
   *  ret = 0 -> correct setup, ret > 0 -> issue during setup


**Chip is setting in two modes:***
* command mode - chip is waiting for commands
* data mode - chip is waiting for data that will be displayed

write command:
```python 
ret = sens.set_command( register = <command>, value = <value#1>, value2 = <value#2>)
```
write command into chip.
There are three types of commands:
* direct command ( there is not set value and value2 )
* one value command ( set command name and value as data )
* two byte command ( set command name and value and value2 as data )
* command range ( set command in range, range is set by value parameter )
     * SET_COLUMN_LO could be in range 0x00 - 0x0F when you want to set 0x0F ( sens.set_command( register = 'SET_COLUMN_LO', value = 0x0F )
       0x0F will be added tu SET_COLUMN_LO value -> 0x00 + 0x0F => 0x0F is final command that is prepared to write into the Chip
       
**return value:** ```(<ret>)```
   *  ret = 0 -> correct writing, ret > 0 -> issue during writing process

data:
```python
self.data(data = <data>)
```

used mostly internally by **display def**
* send in sequence raw of data into the RAM of chip.

display:
```python
self.device.display(self.image)
```

mostly used by render.py library
* display image

**return value:** ```(<ret>)```
   *  ret = 0 -> correct display, ret > 0 -> issue during displaying process
  
  
 **How to write Picture or Text into display?**
 
 * writing picture or text into display is done by render.py library functionality
 
 example of writing image which is prepared in file:
 ```python
 with render.canvas(disp) as draw:
   zoom = Image.open('images/zoom.png')
   draw.bitmap((0, 0), zoom, fill=1)
   zoom.close()
   del draw
 ```
 
 example of writing image and text:
  ```python
  with render.canvas(disp) as draw:
   sleep(5)
   logo = Image.open('images/comet_black_white_62x62.png')
   draw.bitmap((0, 0), logo, fill=1)
   draw.text((75, 20), 'eComet', font=font, fill=1)
   draw.text((90, 32 ), 'Slovakia', font=font, fill=1)
   logo.close()
   del draw
  ```
 
 font of the letters could be set by ttf file:
 ```python
 font = ImageFont.truetype('./fonts/C&C Red Alert [INET].ttf', 12)
 ```


output of test script:
```shell
pi@raspberrypi:~/ecomet_i2c_raspberry_tools $ python3 ssd1306_i2c_test.py
3.7.3 (default, Jan 22 2021, 20:04:44)
[GCC 8.3.0]
```

video from running script:
[![ssd1309 test sequence]({./ssd1309_display.png})]({https://github.com/mamin27/ecomet_i2c_raspberry_tools/blob/master/i2c_pkg/ssd1306_pkg/zoom_display.mkv} "ssd1309 display")

**Note:** for more details look into ssd1306_i2c_test.py
