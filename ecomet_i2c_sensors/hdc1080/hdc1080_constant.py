# Address:

HDC1080_ADDRESS    = 0x40      # 8 bit version

# Register

TEMP               = 0x00
HUMDT              = 0x01
CONF               = 0x02
SER_ID1            = 0xFB
SER_ID2            = 0xFC
SER_ID3            = 0xFD
MANUF              = 0xFE
DEVID              = 0xFF

# CONF 16 Bits allow (MBS):        

HRES               = 8    # rw, humidity measurement resolution - 2 bits
TRES               = 10   # rw, temperature measurement resolution - 1 bit
BTST               = 11   # r, Battery voltage > 2.8V(readonly) -1 bit
MODE               = 12   # rw, temperature or humidity is acquired, serial or once - 1 bit
HEAT               = 13   # rw, heater bit - 1 bit
RST                = 15   # w, software reset 1-bit

#Status of CONF Bit
MODE_BOTH          = 0
MODE_ONLY          = 1
HRES_14            = 0b00   # rw, humidity measurement resolution 14 bit
HRES_11            = 0b01   # rw, humidity measurement resolution 11 bit
HRES_08            = 0b11   # rw, humidity measurement resolution 8 bit
TRES_14            = 0      # rw, humidity measurement resolution 14 bit
TRES_11            = 1      # rw, humidity measurement resolution 11 bit
HEAT_DISABLE       = 0      # rw, heater disabled
HEAT_ENABLE        = 1      # rw, heater enable
RST_ON             = 1      # r, software reset enable

#Status Mask of CONF Bit
MODE_Mask          = 0b1
HRES_Mask          = 0b11   # rw, humidity measurement resolution 2 bits
TRES_Mask          = 0b1    # rw, humidity measurement resolution 1 bit
HEAT_Mask          = 0b1    # rw, heater disabled
BTST_Mask          = 0b1
