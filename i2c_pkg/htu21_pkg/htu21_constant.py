# Address:
I2CBUS             = 1         # /dev/i2c-1
HTU21_ADDRESS    = 0x40      # 8 bit version

# Register

TEMP               = 0xE3
HUMDT              = 0xE5
WRITE_USER         = 0xE6
READ_USER          = 0xE7
SRESET             = 0xFE

# USER REGISTER 8 Bits:        

MEAS_RES1          = 0x00   # temperature 14 bit, humidity measurement resolution 12 bit
MEAS_RES2          = 0x01   # temperature 12 bit, humidity measurement resolution 8 bit
MEAS_RES3          = 0x80   # temperature 13 bit, humidity measurement resolution 10 bit
MEAS_RES4          = 0x81   # temperature 11 bit, humidity measurement resolution 11 bit
BTST_HI			   = 0x00   # Battery voltage > 2.25V(readonly)
BTST_LO            = 0x40   # Battery voltage < 2.25V(readonly)
HEAT_DISABLE       = 0x00   # heater disabled
HEAT_ENABLE        = 0x04   # heater enable
OTP_RELOAD_DISABLE = 0x01   # OTP reload disable
OTP_RELOAD_ENABLE  = 0x00   # OTP reload enable

# USER REGISTER 8 Bits clear:        

MEAS_RES1_CLR      = 0x7E   # temperature & humidity resolution bits clear
MEAS_RES2_CLR      = 0x7E   # temperature & humidity resolution bits clear
MEAS_RES3_CLR      = 0x7E   # temperature & humidity resolution bits clear
MEAS_RES4_CLR      = 0x7E   # temperature & humidity resolution bits clear
BTST_HI_CLR        = 0xBF   # battery check bit clear
BTST_LO_CLR        = 0xBF   # battery check bit clear
HEAT_DISABLE_CLR   = 0xFB   # heater bit clear
HEAT_ENABLE_CLR    = 0xFB   # heater bit clear
OTP_CLR            = 0xFE   # OTP bit clear

# REGISTER Mask bites
REG_MEAS          = 0x81
REG_BAT           = 0x40
REG_HEAT          = 0x04
REG_OTP           = 0x02
