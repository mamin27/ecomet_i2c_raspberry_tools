# Address:
I2CBUS             = 1         # /dev/i2c-1
SN_GCJA5_ADDRESS   = 0x33   # 8 bit version

# Register
							# On the mass-density valu, update each 1s
							# PM1.0
PM1_0_LL           = 0x00   # LL Byte
PM1_0_LH           = 0x01   # LH Byte
PM1_0_HL           = 0x02   # HL Byte
PM1_0_HH           = 0x03   # HH Byte

							# PM2.5
PM2_5_LL           = 0x04   # LL Byte
PM2_5_LH           = 0x05   # LH Byte
PM2_5_HL           = 0x06   # HL Byte
PM2_5_HH           = 0x07   # HH Byte

							# PM10
PM10_LL            = 0x08   # LL Byte
PM10_LH            = 0x09   # LH Byte
PM10_HL            = 0x0a   # HL Byte
PM10_HH            = 0x0b   # HH Byte

							# Particle cound, update each 1s
							# (0.3-0.5um)
P0_5_L             = 0x0c   # L Byte
P0_5_H             = 0x0d   # H Byte
							# (0.5-1.0um)
P1_L               = 0x0e   # L Byte
P1_H               = 0x0f   # H Byte
							# (1.0-2.5um)
P2_5_L             = 0x10   # L Byte
P2_5_H             = 0x11   # H Byte
							# (2.5-5.0um)
P5_L               = 0x14   # L Byte
P5_H               = 0x15   # H Byte
							# (5.0-7.5um)
P7_5_L             = 0x16   # L Byte
P7_5_H             = 0x17   # H Byte
							# (7.5-10.0um)
P10_L              = 0x18   # L Byte
P10_H              = 0x19   # H Byte

STATE			   = 0x26   # Sensor status information

# STATE (0x26) 8 Bits:        

SENSOR_STAT        = 0xC0   # Sensor status
PD_STAT            = 0x30   # PD status
LD_STAT            = 0x0C   # LD operational status
FAN_STAT           = 0x03   # FAN operational status


# SENSOR_STAT
NULL			   = 0x00
ANY1			   = 0x01   # Any1, nor 2 & 3
ANY2			   = 0x02	# Any 2
ANY3               = 0x03   # Any 3, nor 2

# PD_STAT
PD_NORMAL   	   = 0x00  # Normal status
PD_NORMAL_COR      = 0x01  # Normal status (within -80% against initial value), with S/W correction
PD_ABNORM          = 0x02  # Abnormal (below -90% against initial value), loss of function
PD_ABNORM_COR      = 0x03  # Abnormal (below -80% against initial value), with S/W correct

# LD_STAT
LD_NORMAL		   = 0x00  # Normal status
LD_NORMAL_COR      = 0x01  # Normal status (within -70% against initial LOP), with S/W correction
LD_ABNORM          = 0x02  # Abnormal (below -90% against initial LOP) or no LOP, loss of function
LD_ABNORM_COR      = 0x03  # Abnormal (below -70% against initial LOP), with S/W correcti

# FAN_STAT
FAN_NORMAL         = 0x00  # Normal status
FAN_NORMAL_COR     = 0x01  # Normal status (1,000rpm or more), with S/W correction
FAN_CALIB          = 0x02  # In initial calibration
FAN_ABNORM         = 0x03  # Abnormal (below 1,000rpm), out of contr
