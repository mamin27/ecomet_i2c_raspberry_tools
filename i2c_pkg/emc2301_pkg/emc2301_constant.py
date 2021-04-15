# Address:
I2CBUS             = 1         # /dev/i2c-1
EMC2301_ADDRESS    = 0x2F   # 8 bit version

# Register

CONF               = 0x20   # Configuration
FAN_STAT           = 0x24   # Fan Status
FAN_STALL          = 0x25   # Fan Stall Status *
FAN_SPIN           = 0x26   # Fan Spin Status *
DRIVE_FALL         = 0x27   # Drive Fall Status
FAN_INTERRUPT      = 0x29   # Controls the masking of interrupts on all fan related channels
PWM_POLARITY       = 0x2A   # Configures Polarity of the PWM driver
PWM_OUTPUT         = 0x2B   # Configures Output type of the PWM driver
PWM_BASE           = 0x2D   # Selects the base frequency for the PWM output
FAN_SETTING        = 0x30   # Displays Driver inputs or Direct control of fan
PWM_DIVIDE         = 0x31   # Store the divide ratio to set the frequency
FAN_CONF1          = 0x32   # FAN configuration #1
FAN_CONF2          = 0x33   # FAN configuration #2
GAIN               = 0x35   # Holds the gain terms
FAN_SPIN_UP        = 0x36   # Sets the config for Spin Up Routine
FAN_MAX_STEP       = 0x37   # Sets the maximum change per update
FAN_MIN_DRIVE      = 0x38   # Sets the minimum drive value
TACH_COUNT         = 0x39   # Holds the tachometer reading
FAN_FAIL_BAND      = 0x3A
FAN_FAIL_BAND_LB   = 0x3A   # Stores the number of Tach counts used to determine how the actual fan speed must match the target fan speed low byte
FAN_FAIL_BAND_HB   = 0x3B   # -- High byte
TACH_TARGET        = 0x3C
TACH_TARGET_LB     = 0x3C   # Holds the target tachometer low byte
TACH_TARGET_HB     = 0x3D   # -- High byte
TACH_READ          = 0x3E
TACH_READ_HB       = 0x3E   # Holds the tachometer reading high byte
TACH_READ_LB       = 0x3F   # -- Low byte
SOFTWARE_LOCK      = 0xEF   # Lock all SWL register *
PRODUCT_ID         = 0xFD   # Stores the unique Product ID
MANUF_ID           = 0xFE   # Manufacturer ID
REVISION_ID        = 0xFF   # Revision ID

# CONF (0x20) 8 Bits:        

MASK               = 0x80   # Blocks the ALERT# pin
DIS_TO             = 0x40   # Disables the SMBus timeout function
WD_EN              = 0x20   # Enables the WatchDog timer
DR_EXT_CLK         = 0x02   # Enables the internal tachometer clock or external clock
USE_EXT_CLK        = 0x01   # Enables to use a clock present on the CLK pin

# FAN STATUS (0x24) 8 Bits:

WATCH              = 0x80   # Indicates that the Watchdog Timer has expired
DRIVE_FAIL         = 0x04   # Indicates that the Fan driver cannot meet the programmed fan speed at maximum PWM duty cycle
FAN_SPIN           = 0x02   # Indicates that the Fan driver cannot spin up.
FAN_STALL          = 0x01   # Indicates that the Fan driver have stalled.

# FAN STALL STATUS (0x25) 8 Bits:

FAN_STALL_I        = 0x01

# FAN SPIN STATUS (0x26) 8 Bits:

FAN_SPIN_I         = 0x01

# FAN DRIVE STATUS (0x27) 8 Bits:

DRIVE_FAIL_I       = 0x01

# FAN INTERRUPT ENABLE (0x29) 8 Bits:

FAN_INT_EN         = 0x01  # Allows the Fan to assert the ALERT# pin

# PWM_POLARITY (0x2A) 8 Bits:

POLARITY           = 0x01  # Determine the polarity of PWM

# PWM_OUTPUT (0x2B) 8 Bits:

PWM_OT             = 0x01 #  Determine of output type of PWM driver

# PWM_BASE (0x2D) 8 Bits:

BASE               = 0x03 # 00 - 26 kHz (def)
                          # 01 - 19.531 kHz
                          # 10 - 4.882 Hz
                          # 11 - 2.441 Hz
                          
# FAN_CONF1 (0x32) 8 Bits:

UPDATE             = 0x07 # Ramp rate to the driver response
                          # 000 - 100ms
                          # 001 - 200ms
                          # 010 - 300ms
                          # 011 - 400ms (def)
                          # 100 - 500ms
                          # 101 - 800ms
                          # 110 - 1200ms
                          # 111 - 1600ms
EDGES			   = 0x18 # Number of Poles of the Fan
                          # 00 - 1 pole, effective tach multiplier 0.5
                          # 01 - 2 poles (def), -- 1
                          # 10 - 3 poles, -- 1.5
                          # 11 - 4 poles, -- 2
RANGE              = 0x60 # Range of TACH
                          # 00 - min 500 RPM, tach multiplier 1
                          # 01 - min 1000 RPM (def), tach multiplier 2
                          # 10 - min 2000 RPM, tach multiplier 4
                          # 11 - min 4000 RPM, tach multiplier 8
EN_ALGO            = 0x80 # Enables Fan Speed Control Algorithm

# FAN_CONF2 (0x33) 8 Bits:

ERR_RNG            = 0x06 # Control Advanced Control (Error window)
                          # 00 - 0 RPM (def)
                          # 01 - 50 RPM
                          # 10 - 100 RPM
                          # 11 - 200 RPM
DER_OPT            = 0x18 # Control Advanced Control
                          # 00 - No derivate option used
                          # 01 - Basic derivate
                          # 10 - Step derivate
                          # 11 - Basic and Step derivate
GLITCH_EN          = 0x20 # Disable low pass Glitch filter (remove high frequency noise)
EN_RRC             = 0x40 # Enable Ramp Rate Control

# GAIN (0x35) 8 Bits:

GAINP              = 0x03 # Control proportional Gain
                          # 00 - gain factor 1x
                          # 01 - gain factor 2x
                          # 10 - gain factor 4x (def)
                          # 11 - gain factor 8x
GAINI             = 0x0C  # Control integral Gain 
GAIND             = 0x30  # Control derivate Gain

# FAN_SPIN_UP (0x36) 8 Bits:

FAN_SPIN_UP_TIME       = 0x03  # Determines max spin up time
                          # 00 - 250ms
                          # 01 - 500ms (def)
                          # 10 - 1s
                          # 11 - 2s
FAN_SPIN_UP_LVL          = 0x1C  # Determines final drive level used by Spin Up Routines
                          # 000 - 30%
                          # 001 - 35%
                          # 010 - 40%
                          # 011 - 45%
                          # 100 - 50%
                          # 101 - 55%
                          # 110 - 60% (def)
                          # 111 - 65%
FAN_SPIN_UP_NOKICK            = 0x20  # Determines if the Spin UP Routines will drive fan  to 100% duty cycle for 1/4 of the programed spin
FAN_SPIN_UP_DRIVE_FAIL_CNT    = 0xC0  # Determines how many updates cycles are used for Drive fail detection function
                          # 00 - Disabled
                          # 01 - 16 updates period
                          # 10 - 32 --
                          # 11 - 64 --

# FAN_MAX_STEP (0x37) 8 Bits:

FAN_MAX_STEP_MASK  = 0x3F

# FAN_MIN_DRIVE (0x38) 8 Bits:

FAN_MIN_DRIVE_MASK = 0xFF     # Def 40% (0x66)

# FAN_TACH (0x39) 8 Bits:

FAN_TACH_MASK      = 0xFF     # Def (0xF5)

# TACH Reg (0x3A,3B,3C,3D,3E,3F) 8 Bits:

FAN_FAIL_BAND_LB_M = 0xF8   # def (0xF8)
FAN_FAIL_BAND_HB_M = 0xFF   # def (0xFF)
TACH_TARGET_LB_M   = 0xF8   # def (0xF8)
TACH_TARGET_HB_M   = 0xFF   # def (0xFF)
TACH_READ_HB_MASK  = 0xFF   # def (0xFF)
TACH_READ_LB_MASK  = 0xF8   # def (0xF8)

# SOFTWARE_LOCK (0xEF) 8 Bits:

LOCK               = 0x01   # locked register

# CONF Mask (0x20) 8 Bits clear :        

MASK_M           = 0x7F   # Blocks the ALERT# pin
DIS_TO_M         = 0xBF   # Disables the SMBus timeout function
WD_EN_M          = 0xDF   # Enables the WatchDog timer
DR_EXT_CLK_M     = 0xFD   # Enables the internal tachometer clock or external clock
USE_EXT_CLK_M    = 0xFE

# FAN_STAT Mask (0x24) 8 Bits clear :        

WATCH_M           = 0x7F  # Watchdog Timer expire?
DRIVE_FAIL_M      = 0xFB  # Speed can't meet the max of PWM duty cycle
FAN_SPIN_M        = 0xFD  # Can't spin up FAN driver
FAN_STALL_M       = 0xFE  # Fan driver stalled?

# FAN DRIVE Mask (0x27) 8 Bits:

DRIVE_FAIL_I_M    = 0xFE

# FAN INTERRUPT ENABLE Mask (0x29) 8 Bits:

FAN_INT_EN_M      = 0xFE  # Allows the Fan to assert the ALERT# pin

# PWM_POLARITY Mask (0x2A) 8 Bits:

POLARITY_M        = 0xFE  # Determine the polarity of PWM

# PWM_OUTPUT Mask (0x2B) 8 Bits:

PWM_OT_M          = 0xFE #  Determine of output type of PWM driver

# PWM_BASE Mask (0x2D) 8 Bits:

BASE_M            = 0xFC #  Base frequency

# FAN_CONF1 Mask (0x32) 8 Bits clear :

EN_ALGO_M         = 0x7F  # Enables Fan Speed Control Algorithm
RANGE_M           = 0x9F  # Range of TACH
EDGES_M           = 0xE7  # Number of Poles of the Fan
UPDATE_M          = 0xF8  # Ramp rate to the driver response

# FAN_CONF2 Mask (0x33) 8 Bits clear :

ERR_RNG_M         = 0xF9  # Control Advanced Control (Error window)
DER_OPT_M         = 0xE7  # Control Advanced Control
GLITCH_EN_M       = 0xDF  # Disable low pass Glitch filtelter (remove high frequency noise)
EN_RRC_M          = 0xBF  # Enable Ramp Rate Control

# GAIN Mask (0x35) 8 Bits clear:

GAINP_M          = 0xFC # Control proportional Gain
GAINI_M          = 0xF3 # Control integral Gain 
GAIND_M          = 0xCF # Control derivate Gain

# FAN_SPIN_UP Mask (0x36) 8 Bits clear:

FAN_SPIN_UP_TIME_M       = 0xFC  # Determines max spin up time
FAN_SPIN_UP_LVL_M        = 0xE3  # Determines final drive level used by Spin Up Routines
FAN_SPIN_UP_NOKICK_M     = 0xDF  # Determines if the Spin UP Routines will drive fan  to 100% duty cycle for 1/4 of the programed spin
FAN_SPIN_UP_DRIVE_FAIL_CNT_M  = 0x3F  # Determines how many updates cycles are used for Drive fail detection function

# SOFTWARE_LOCK Mask (0xEF) 8 Bits clear:

LOCK_M               = 0xFE   # locked register

# CONF Clear (0x20) 8 Bits:        

MASK_CLR             = 0x80   # Blocks the ALERT# pin
DIS_TO_CLR           = 0x40   # Disables the SMBus timeout function
WD_EN_CLR            = 0x20   # Enables the WatchDog timer
DR_EXT_CLK_CLR       = 0x02   # Enables the internal tachometer clock or external clock
USE_EXT_CLK_CLR      = 0x01   # Enables to use a clock present on the CLK pin

# FAN_STAT Clear (0x24) 8 Bits:        

WATCH_CLR            = 0x80   # Watchdog Timer expire?
DRIVE_FAIL_CLR       = 0x04   # Speed can't meet the max of PWM duty cycle
FAN_SPIN_CLR         = 0x02   # Can't spin up FAN driver
FAN_STALL_CLR        = 0x01   # Fan driver stalled?

# FAN DRIVE STATUS Clear (0x27) 8 Bits:

DRIVE_FAIL_I_CLR     = 0x01

# FAN INTERRUPT ENABLE Clear (0x29) 8 Bits:

FAN_INT_EN_CLR       = 0x01  # Allows the Fan to assert the ALERT# pin

# PWM_POLARITY Clear (0x2A) 8 Bits:

POLARITY_CLR         = 0x01  # Determine the polarity of PWM

# PWM_OUTPUT Clear (0x2B) 8 Bits:

PWM_OT_CLR           = 0x01 #  Determine of output type of PWM driver

# PWM_BASE Clear (0x2D) 8 Bits:

BASE_CLR             = 0x03 #  Base frequency

# FAN_CONF1 Clear (0x32) 8 Bits:

EN_ALGO_CLR         = 0x80  # Enables Fan Speed Control Algorithm
RANGE_CLR           = 0x60  # Range of TACH
EDGES_CLR           = 0x18  # Number of Poles of the Fan
UPDATE_CLR          = 0x07  # Ramp rate to the driver response

# FAN_CONF2 Clear (0x33) 8 Bits:

ERR_RNG_CLR         = 0x06  # Control Advanced Control (Error window)
DER_OPT_CLR         = 0x18  # Control Advanced Control
GLITCH_EN_CLR       = 0x20  # Disable low pass Glitch filtelter (remove high frequency noise)
EN_RRC_M_CLR        = 0x40  # Enable Ramp Rate Control

# GAIN Clear (0x35) 8 Bits:

GAINP_CLR            = 0x03 # Control proportional Gain
GAINI_CLR            = 0x0C # Control integral Gain 
GAIND_CLR            = 0x30 # Control derivate Gain

# FAN_SPIN_UP Clear (0x36) 8 Bits:

SPIN_UP_TIME_CLR     = 0x03  # Determines max spin up time
SPIN_UP_LVL_CLR        = 0x1C  # Determines final drive level used by Spin Up Routines
SPIN_UP_NOKICK_CLR          = 0x20  # Determines if the Spin UP Routines will drive fan  to 100% duty cycle for 1/4 of the programed spin
SPIN_UP_DRIVE_FAIL_CNT_CLR  = 0xC0  # Determines how many updates cycles are used for Drive fail detection function

# SOFTWARE_LOCK CLER (0xEF) 8 Bits:

LOCK_CLR              = 0x00   # locked register
