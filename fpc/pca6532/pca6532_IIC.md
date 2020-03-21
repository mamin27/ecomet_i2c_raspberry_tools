# pca9632_IIC module

**Last modification:** 21.03.2020

**Schematics of Module:**
*schematics in working process*

![Schematics](Schematics.PNG)

**Reconnection with Raspberry PI 3+:**

![Schematics_2](Schematics_2.PNG)
* schematics in working process*

* Configuration for /dev/i2c-1
* port 2 (SDA), port 3 (SCL)
* pull-up resistor is used from module board (R2,R3)

### How to install? ###

Install Lazarus-ide at raspberry [FPC & Lazarus Installation](../lazarus.md)
Install Python3 and next modules for pca9632 [Python3 & modules](../../i2c_pkg/pca9632_pkg/pca_9632_python_IIC.md)

### Run application: ###
```console
ecomet_i2c_tools/pca_6532
```

**Features:**

*  Read status of pca_6532 chip and show on concole
*  Click at button (with values) changed to color to white. Then able to change value

**Limitations**
 
* All Registers are correctly read after application run
* Buttons are switchable but without effect

![console](pca6532_console.png  "Console")

**Source Code (FPC):**
* Path: ~/ecomet_i2c_tools/fpc/pca9632