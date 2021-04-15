# Address:

I2CBUS             = 1         # /dev/i2c-1
HDC1080_ADDRESS    = 0x40      # 8 bit version

# Register

TEMP               = 0x00
HUMDT              = 0x01
CONF               = 0x02
SER_ID1            = 0xFB
SER_ID2            = 0xFC
SER_ID3            = 0xFD
MANUF              = 0xFE
DEVID			   = 0xFF

# CONF 16 Bits allow (MBS):        

HRES_RES1          = 0x0000   # rw, humidity measurement resolution 14 bit
HRES_RES2          = 0x0100   # rw, humidity measurement resolution 11 bit
HRES_RES3          = 0x0200   # rw, humidity measurement resolution 8 bit
TRES_RES1          = 0x0000   # rw, temperature measurement resolution 14 bit
TRES_RES2          = 0x0400   # rw, temperature measurement resolution 11 bit
BTST_HI			   = 0x0000   # r, Battery voltage > 2.8V(readonly)
BTST_LO            = 0x0800   # r, Battery voltage < 2.8V(readonly)
MODE_BOTH          = 0x1000   # rw, temperature or humidity is acquired
MODE_ONLY          = 0x0000   # rw, temperature and humidity are acquiredin sequence,temperature first
HEAT_DISABLE       = 0x0000   # rw, heater disabled
HEAT_ENABLE        = 0x3000   # rw, heater enable
RST_ON             = 0x8000   # w, software reset

# CONF 16 Bits clear (MBS):        

HRES_RES1_CLR      = 0xFCFF   # rw, humidity measurement clear (set to 14 bit)
HRES_RES2_CLR      = 0xFCFF   # rw, humidity measurement clear (set to 14 bit)
HRES_RES3_CLR      = 0xFCFF   # rw, humidity measurement clear (set to 14 bit)
TRES_RES1_CLR      = 0xFBFF   # rw, temperature measurement resolution clear (set to 14 bit)
TRES_RES2_CLR      = 0xFBFF   # rw, temperature measurement resolution clear (set to 14 bit)
BTST_HI_CLR        = 0xF7FF
BTST_LO_CLR        = 0xF7FF
MODE_ONLY_CLR      = 0xEFFF   # rw, temperature or humidity clear ( set MODE_ONLY)
MODE_BOTH_CLR      = 0xEFFF   # rw, temperature and humidity clear ( set MODE_ONLY)
HEAT_DISABLE_CLR   = 0xDFFF   # rw, heater disabled
HEAT_ENABLE_CLR    = 0xDFFF   # rw, heater enable
RST_ON_CLR         = 0x7FFF   # w, software reset

# CONF Mask bites
CONF_HRES          = 0x0300
CONF_TRES          = 0x0400
CONF_BAT           = 0x0800
CONF_MODE          = 0x1000
CONF_HEAT          = 0x2000
