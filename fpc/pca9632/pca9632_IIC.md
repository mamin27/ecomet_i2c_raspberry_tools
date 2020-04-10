# pca9632_IIC module

**Last modification:** 10.04.2020

**Schematics of Module:**
*schematics for testing will be added later*

![Schematics](Schematics.PNG)

**Reconnection with Raspberry PI 3+:**

![Interface to PI](pca9632_schema.PNG)
* schematics of PI reconnection*

* Configuration for /dev/i2c-1
* port 2 (SDA), port 3 (SCL)
* pull-up resistor is used from module board (R2,R3)

### How to install? ###

Install Lazarus-ide at raspberry [FPC & Lazarus Installation](../lazarus.md)
Install Python3 and next modules for pca9632 [Python3 & modules](../../i2c_pkg/pca9632_pkg/pca_9632_python_IIC.md)

### Run application: ###
```console
ecomet_i2c_tools/pca_9632
```

**Features:**

*  Read status of pca_9632 chip and show on concole
*  Click at Enumerated Buttons (as ALLCALL), choice from values for register (MODE1, MODE2, LEDOUT)
*  Write to Register - Actually modified value visible by red rectangular 
*  Apply write changes for all actually selected attributes (buttons) - click at **APPLY** button
*  Click at button (with values) changed to color to white. Then able to change value
* PWMx, GRPPWM DutyCycle recalculated to percentage
* GRPFREQ transfered to frequency, time

   **>>Sub Features:**

* Register MODE1, MODE2 enumerate ON, OFF status
* Register MODE2 (DBMLNK) enumerate DIMMING, BLINKING status
* Register LEDOUT, enumerate ON, OFF, PWM, PWM_GRPPWM status
* Register PWMx, GRPPWN, GRPFREQ (in Hz, in Time)

**Limitation**

* TrackBar not used now
* Chip Address currently not able to change

![console](pca9632_console.png  "Console")

**Source Code (FPC):**
* Path: ~/ecomet_i2c_tools/fpc/pca9632
