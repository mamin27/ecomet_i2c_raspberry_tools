# Address:

I2CBUS					= 1         # /dev/i2c-1
SSD1306_ADDRESS_CMD		= 0x3C      # 8 bit version Command Mode


# LED Registers

class register(object):
    SET_COLUMN_LO		= 0x00		# 0x00 - 0x0F  (0 - 131) 132 columns
    SET_COLUMN_HI		= 0x10		# 0x10 - 0x1F
    SET_MEMORY_MODE		= 0x20		# Set Memory address mode
    SET_COLUMN_ADDRESS	= 0x21		# Set Column Address
    SET_PAGE_ADDR		= 0x22
    SET_START_LINE		= 0x40		# 0x40 - 0x7F (0 - 63) 64 lines
    SET_CONTRAST		= 0x81		# Data byte (0x00 - 0xFF)
    CHARGEPUMP			= 0x8D		# Charge Pump Setting
    SET_REMAP_RIGHT		= 0xA0		# Segment ReMap Right
    SET_REMAP_LEFT		= 0xA1		# Segment ReMap Left
    SET_VERTICAL_SCROLL	= 0xA3		# Set Vertical Scroll Area
    SET_ENTIRE_DISP		= 0xA4		# Set Entire Display RAM Displayed
    SET_ENTIRE_DISP_IGN	= 0xA5		# Set Entire Display RAM Ignored
    SET_NORMAL_DISP		= 0xA6		# Set Normal Display
    SET_REVERSE_DISP	= 0xA7		# Set Reverse Display
    SET_MULTIPLEX_RATION= 0xA8		# Set Multiplex Ration Data (0x00 - 0x3F) 64 Multiplex ration modes
    DC_DC_CONTROL_MODE	= 0xAD		# Control DC-DC converter + (Data are next)
    DATA_DC_DC_OFF		= 0x8A		# DC-DC OFF (sleep mode)
    DATA_DC_DC_ON		= 0x8B		# DC-DC ON (External Vpp or Internal DC-DC)
    SET_SEGM_REMAP_0	= 0xA0		# Set Segment Remap, column address 0 to SEG0
    SET_SEGM_REMAP_127	= 0xA1		# Set Segment Remap, column address 127 to SEG0
    DISPLAY_OFF			= 0xAE		# Display ON
    DISPLAY_ON			= 0xAF		# Display OFF
    SET_PAGE_ADDR		= 0xB0		# Set Page Address (0xB0 - 0xB7) 8 Pages
    SET_OUTPUT_SCAN_UP	= 0xC0		# Scan common output allowing layout flexible, (from COM0 -> COM[n-1])
    SET_OUTPUT_SCAN_DOWN= 0xC8		# Scan common output allowing layout flexible, (from COM[n-1] -> COM0) 
    SET_DISPLAY_OFFSET	= 0xD3		# Mapping of display start line to one of COM0-63 (Data 0x00 - 0x3F) 64 offsets
    SET_DISPLAY_CLOCK	= 0xD5		# Set frequency of internal display clock (Data 0x00 - 0xFF) Divider bit[4-0] Freq bit[7-4]
    SET_CHARGE_PERIOD	= 0xD9		# Duration of pre-charged period (Data 0x00 - 0xFF) Pre-Charget_Period_adjust bit[4-0] Dis-Charget_Period_adjustFreq bit[7-4]
    SET_HW_CONF_MODE	= 0xDA		# Common Pads Hardware Configuration Mode Set
    SET_VCOM			= 0xDB		# Set the common pad output voltage level (data 0x00 - 0xFF)
    READ_MODIFY_WRITE	= 0xE0		# Automatic write
    END_RMW				= 0xEE		# End Read_Modify_Write automatic write
    NOP					= 0xE3		# NOP command

