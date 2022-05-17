from __future__ import division
import logging
import time
import math
import struct
import binascii
from ecomet_i2c_sensors.isl2802x import isl2802x_constant

logger = logging.getLogger(__name__) 

def conf_register_list(address=isl2802x_constant.ISL28022_ADDRESS) :

   _address = address
   isl = ISL28022(address=_address)
   isl._logger = logging.getLogger('ecomet.isl2802x.reglist') 
   register = {}
   reg_conf = {}
   reg_mask_enable = {}
   reg_manuf = {}
   reg_die = {}

# bus Voltage Range, Usable Full Scale Range
   brng = { 0: '16',
            1: '32',
            2: '60',
            3: '60'
   }

# only Shunt Voltage Only, GAIN
   pg = { 0: '40mV',  # +- 40mV
          1: '80mV',  # +- 80mV
          2: '160mV',  # +- 160mV
          3: '320mV'   # +- 320mV
   }

   adc = { 0: '1/12-bit',  # from 72us ... 64.01 ms
            1: '1/13-bit',
            2: '1/14-bit',
            3: '1/15-bit',
            4: '1/12-bit',
            5: '1/13-bit',
            6: '1/14-bit',
            7: '1/15-bit',
            8: '1/15-bit',
            9: '2/15-bit',
            10: '4/15-bit',
            11: '8/15-bit',
            12: '16/15-bit',
            13: '32/15-bit',
            14: '64/15-bit',
            15: '128/15-bit'
   }

   mode = { 0: 'Power-Down',
            1: 'Shunt voltage, triggered',
            2: 'Bus voltage, triggered',
            3: 'Shunt and bus, triggered',
            4: 'ADC off',
            5: 'Shunt Voltage, continuous',
            6: 'Bus voltage, continuous',
            7: 'Shunt and bus, continuous'
   }

   reg_conf['BRNG'] = brng[isl.bits_get(2, isl._const.REG_CONFIG, 13, 2, False)]
   reg_conf['PG'] = pg[isl.bits_get(2, isl._const.REG_CONFIG, 11, 2, False)]
   reg_conf['BADC'] = adc[isl.bits_get(4, isl._const.REG_CONFIG, 7, 2, False)]
   reg_conf['SADC'] = adc[isl.bits_get(4, isl._const.REG_CONFIG, 3, 2, False)]
   reg_conf['MODE'] = mode[isl.bits_get(3, isl._const.REG_CONFIG, 0, 2, False)]

   register['CONF'] = reg_conf
   return (register);

'''
   reg_conf['RESET'] = 'RESET' if ina.bit_get(ina._const.REG_CONFIG, 15, 2, False) else 'N/A'
   reg_conf['AVGC'] = avgcnt[ina.bits_get(3, ina._const.REG_CONFIG, 9, 2, False)]
   reg_conf['VBUSCT'] = vbusct[ina.bits_get(3, ina._const.REG_CONFIG, 6, 2, False)]
   reg_conf['ISHCT'] = curct[ina.bits_get(3, ina._const.REG_CONFIG, 3, 2, False)]

   reg_mask_enable['OCL'] = 'ALERT OCL' if ina.bit_get(ina._const.REG_MASK_ENABLE, 15, 2, False) else 'N/A'
   reg_mask_enable['UCL'] = 'ALERT UCL' if ina.bit_get(ina._const.REG_MASK_ENABLE, 14, 2, False) else 'N/A'
   reg_mask_enable['BOL'] = 'ALERT BOL' if ina.bit_get(ina._const.REG_MASK_ENABLE, 13, 2, False) else 'N/A'
   reg_mask_enable['BUL'] = 'ALERT BUL' if ina.bit_get(ina._const.REG_MASK_ENABLE, 12, 2, False) else 'N/A'
   reg_mask_enable['POL'] = 'ALERT POL' if ina.bit_get(ina._const.REG_MASK_ENABLE, 11, 2, False) else 'N/A'
   reg_mask_enable['CNVR'] = 'ASSERTING' if ina.bit_get(ina._const.REG_MASK_ENABLE, 10, 2, False) else 'ASSERTED'
   reg_mask_enable['AFF'] = 'ON' if ina.bit_get(ina._const.REG_MASK_ENABLE, 4, 2, False) else 'OFF' 
   reg_mask_enable['CVRF'] = 'SET' if ina.bit_get(ina._const.REG_MASK_ENABLE, 3, 2, False) else 'CLEAR'
   reg_mask_enable['OVF'] = 'OVERFLOW' if ina.bit_get(ina._const.REG_MASK_ENABLE, 2, 2, False) else 'EXCEED'
   reg_mask_enable['APOL'] = 'INVERTED' if ina.bit_get(ina._const.REG_MASK_ENABLE, 1, 2, False) else 'NORMAL'
   reg_mask_enable['LEN'] = 'LATCH' if ina.bit_get(ina._const.REG_MASK_ENABLE, 0, 2, False) else 'TRANSP'

   reg_manuf['ID'] = (ina.unaryStruct_get(ina._const.REG_MANUFACTURER_ID, ">H")).to_bytes(2,'big').decode('utf-8')

   reg_die['DID'] = hex(ina.bits_get(12, ina._const.REG_DIE_UID, 4, 2, False))
   reg_die['RID'] = ina.bits_get(4, ina._const.REG_DIE_UID, 0, 2, False)

   register['MASK_ENBL'] = reg_mask_enable
   register['MANUF'] = reg_manuf
   register['DIE'] = reg_die
'''

class ISL28022(object):
    '''ISL28022()'''

    def __init__(self, address=isl2802x_constant.ISL28022_ADDRESS, busnum=isl2802x_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the isl2802x.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._const = isl2802x_constant.register
        self._logger = logging.getLogger(__name__)
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self._address = address
        self._pg = { 0: '40mV',  # +- 40mV
          1: '80mV',  # +- 80mV
          2: '160mV',  # +- 160mV
          3: '320mV'   # +- 320mV
        }
        self._brng = { 0: '16',
            1: '32',
            2: '60',
            3: '60'
        }

        self._adc = { 1: '1/13-bit',
            2: '1/14-bit',
            3: '1/15-bit',
            4: '1/12-bit',
            5: '1/13-bit',
            6: '1/14-bit',
            7: '1/15-bit',
            8: '1/15-bit',
            9: '2/15-bit',
            10: '4/15-bit',
            11: '8/15-bit',
            12: '16/15-bit',
            13: '32/15-bit',
            14: '64/15-bit',
            15: '128/15-bit'
        }

        self._mode = { 0: 'Power-Down',
            1: 'Shunt voltage, triggered',
            2: 'Bus voltage, triggered',
            3: 'Shunt and bus, triggered',
            4: 'ADC off',
            5: 'Shunt Voltage, continuous',
            6: 'Bus voltage, continuous',
            7: 'Shunt and bus, continuous'
        }

        self.bit_mask = 0
        self.lowest_bit = 0
        self.buffer = {}
        self.buffer[0] = self._const.REG_CONFIG
        self.brng = int(self._brng[self.bits_get(2, self._const.REG_CONFIG, 13, 2, False)])
        self.measure_buffer_voltage = {}
        self.measure_buffer_current = {}
        self.measure_buffer_power = {}
        self.lsb_first = True
        self.sign_bit = False
        self._vol_unit = 0
        self._voltage_scale = 60

        self.format = '>H'

    def current_conversion (self, current, unit) :
        if unit == 'mA' :
           result = current * 1.25
        elif unit == 'A' :
           result = (current * 1.25)/1000
        return result
    def voltage_conversion (self, voltage, vtype, unit) :
        #self._logger.info("voltage: %s unit: %s",voltage, self._vol_unit)
        if vtype == 'SHUNT' : multiplier = self._vol_shunt_unit
        else : multiplier = self._vol_unit
        if unit == 'mV' :
           if vtype == 'SHUNT' : result = (voltage * multiplier)
           else : result = (voltage * multiplier) * 1000
        elif unit == 'V' :
           if vtype == 'SHUNT' : result = (voltage * multiplier)/1000
           else: result = voltage * multiplier
        return result
    def power_conversion (self, power, unit) :
        if unit == 'mW' :
           result = power * 1.25
        elif unit == 'W' :
           result = (power * 1.25)/1000
        return result
    def bit_init (self, register, bit, register_width=1, lsb_first=True):
        self.bit_mask = 1 << (bit % 8)  # the bitmask *within* the byte!
        self.buffer = bytearray(1 + register_width)
        self.buffer[0] = register
        import binascii
        if lsb_first:
            self.byte = bit // 8 + 1  # the byte number within the buffer
        else:
            self.byte = register_width - (bit // 8)  # the byte number within the buffer
    def bit_get (self, register, bit, register_width=1, lsb_first=True) :
        self.bit_init (register, bit, register_width, lsb_first)
        self._device.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        self._logger.debug("Read from register %s: bit: %s value:%s [mask:%s]" ,register, bit, self.buffer[self.byte] & self.bit_mask, bin(self.bit_mask))
        return bool(self.buffer[self.byte] & self.bit_mask)
    def bit_set (self, register, bit, register_width=1, lsb_first=True, value=None) :
        self.bit_init (register, bit, register_width, lsb_first)
        self._device.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        if value:
           self.buffer[self.byte] |= self.bit_mask
        else:
           self.buffer[self.byte] &= ~self.bit_mask
        self._logger.debug("Buffer %s" ,self.buffer)
        self._device.writeList(self.buffer[0],self.buffer[1:])
    def bits_init(  # pylint: disable=too-many-arguments
        self,
        num_bits,
        register_address,
        lowest_bit,
        register_width=1,
        lsb_first=True,
        signed=False,
    ):
        self.bit_mask = ((1 << num_bits) - 1) << lowest_bit
        if self.bit_mask >= 1 << (register_width * 8):
            raise ValueError("Cannot have more bits than register size")
        self.lowest_bit = lowest_bit
        self.buffer = bytearray(1 + register_width)
        self.buffer[0] = register_address
        self.lsb_first = lsb_first
        self.sign_bit = (1 << (num_bits - 1)) if signed else 0
    def bits_get(self,
        num_bits,
        register_address,
        lowest_bit,
        register_width=1,
        lsb_first=True,
        signed=False,
    ):
        self.bits_init(num_bits,register_address,lowest_bit,register_width,lsb_first,signed)
        self._device.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        reg = 0
        order = range(len(self.buffer) - 1, 0, -1)
        if not self.lsb_first:
            order = reversed(order)
        for i in order:
            reg = (reg << 8) | self.buffer[i]
        reg = (reg & self.bit_mask) >> self.lowest_bit
        # If the value is signed and negative, convert it
        if reg & self.sign_bit:
            reg -= 2 * self.sign_bit
        self._logger.debug("Read from register 0x%02X: %s" ,register_address, bin(reg))
        return reg
    def bits_set(self,
                 num_bits,
                 register_address,
                 lowest_bit,
                 register_width=1,
                 lsb_first=True,
                 signed=False,
                 value = None,
        ):
        value <<= lowest_bit  # shift the value over to the right spot
        self.bits_init(num_bits,register_address,lowest_bit,register_width,lsb_first,signed)
        self._device.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        reg = 0
        order = range(len(self.buffer) - 1, 0, -1)
        if not self.lsb_first:
           order = range(1, len(self.buffer))
        for i in order:
           reg = (reg << 8) | self.buffer[i]
        #print("old reg: ", hex(reg))
        reg &= ~self.bit_mask  # mask off the bits we're about to change
        reg |= value  # then or in our new value
        #print("new reg: ", hex(reg))
        for i in reversed(order):
            self.buffer[i] = reg & 0xFF
            reg >>= 8
        self._device.writeList(self.buffer[0],self.buffer[1:])
        self._logger.debug("Write to register 0x%02X: %s" ,register_address, binascii.hexlify(self.buffer[1:]))
        return reg
    def unaryStruct_get (self,register,sformat='>H',sign_bit=None,left_move_bit=None, mask_bit=None):
        buf = bytearray(1 + struct.calcsize(sformat))
        buf[0] = register
        sign_val = 1
        self._device.write_then_readinto(buf, buf, out_end=1, in_start=1)
        self._logger.info("source: %s:%s",buf[1],buf[2])
        byte_val = bytes(buf[1:])
        int_val = int.from_bytes(byte_val, "big")
        self._logger.info("source+: %s",int_val)
        if sign_bit :
           byte_val = bytes(buf[1:])
           int_val = int.from_bytes(byte_val, "big")
           if int_val & sign_bit > 0 :
             sign_val = (-1)
           self._logger.info("source1: %s",sign_val)
        if mask_bit :
           byte_val = bytes(buf[1:])
           int_val = int.from_bytes(byte_val, "big") & mask_bit
           #int_val = int_val * sign_val
           buf[1:] = int_val.to_bytes(2,"big")
           self._logger.info("source2: %s:%s",buf[1],buf[2])
        if left_move_bit :
           byte_val = bytes(buf[1:])
           int_val = int.from_bytes(byte_val, "big") >> left_move_bit
           #self._logger.info("source3+: %s",int_val)
           buf[1:] = int_val.to_bytes(2,"big")
           self._logger.info("source3: %s:%s",buf[1],buf[2])
        return struct.unpack_from(sformat,buf,1)[0]
    def unaryStruct_set (self,register,sformat=">H",value=None):
        buf = bytearray(1 + struct.calcsize(sformat))
        buf[0] = register
        struct.pack_into(sformat, buf, 1, value)
        self._device.writeList(buf[0],buf[1,])
    def write_funct (self, function, value):
        if function == 'SADC' :
          self.bits_set(4, self._const.REG_CONFIG, 3, 2, False, value=value)
        if function == 'BADC' :
          self.bits_set(4, self._const.REG_CONFIG, 7, 2, False, value=value)
        if function == 'BRNG' :
          self.bits_set(2, self._const.REG_CONFIG, 13, 2, False, value=value)
        if function == 'MODE' :
          self.bits_set(3, self._const.REG_CONFIG, 0, 2, False, value=value)
        elif function == 'PG' :
          self.bits_set(2, self._const.REG_CONFIG, 11, 2, False, value=value)
        else :
          return 1
        return 0
    def read_funct (self, function):
        if function == 'BRNG' :
          return self._brng[self.bits_get(2, self._const.REG_CONFIG, 13, 2, False)]
        elif function == 'PG' :
          return self._pg[self.bits_get(2, self._const.REG_CONFIG, 11, 2, False)]
        elif function == 'SADC' :
          return self._adc[self.bits_get(4, self._const.REG_CONFIG, 3, 2, False)]
        elif function == 'BADC' :
          return self._adc[self.bits_get(4, self._const.REG_CONFIG, 7, 2, False)]
        elif function == 'MODE' :
          return self._mode[isl.bits_get(3, self._const.REG_CONFIG, 0, 2, False)]
        elif function == 'VOLTAGE' :
          if self._voltage_scale == 16 :
             self._raw_voltage = self.unaryStruct_get(self._const.REG_BUS_VOLTAGE, ">H", left_move_bit=3, mask_bit=0b0111111111111000)  # big endian unsigned short
             self._vol_unit = 16/4096
          elif self._voltage_scale == 32 :
             self._raw_voltage = self.unaryStruct_get(self._const.REG_BUS_VOLTAGE, ">H", left_move_bit=3, mask_bit=0b1111111111111000)
             self._vol_unit = 32/8192
          else :
             self._raw_voltage = self.unaryStruct_get(self._const.REG_BUS_VOLTAGE, ">H", left_move_bit=2, mask_bit=0b1111111111111100)
             self._vol_unit = 60/16384
          #self._logger.info("volt: %s peas: %s", self._raw_voltage, self._vol_unit)
          return self._raw_voltage
        elif function == 'SHUNT_VOLTAGE' :
          if self._voltage_shunt_scale == '40mV' :
             self._raw_shunt_voltage = self.unaryStruct_get(self._const.REG_SHUNT_VOLTAGE, ">H", sign_bit=0b0001000000000000, mask_bit=0b0000111111111111)  # big endian signed short
             self._vol_shunt_unit = 40/4096
          elif self._voltage_shunt_scale == '80mV' :
             self._raw_shunt_voltage = self.unaryStruct_get(self._const.REG_SHUNT_VOLTAGE, ">H", sign_bit=0b0010000000000000, mask_bit=0b0001111111111111)
             self._vol_shunt_unit = 80/8192
          elif self._voltage_shunt_scale == '160mV' :
             self._raw_shunt_voltage = self.unaryStruct_get(self._const.REG_SHUNT_VOLTAGE, ">H", sign_bit=0b0100000000000000, mask_bit=0b0011111111111111)
             self._vol_shunt_unit = 160/16384
          else :
             self._raw_shunt_voltage = self.unaryStruct_get(self._const.REG_SHUNT_VOLTAGE, ">H", sign_bit=0b1000000000000000, mask_bit=0b0111111111111111)
             self._vol_shunt_unit = 320/32768
          self._logger.info("shut_volt: %s peas: %s", self._raw_shunt_voltage, self._vol_shunt_unit)
          return self._raw_shunt_voltage
        elif function == 'CURRENT' :
          self._raw_current = self.unaryStruct_get (self._const.REG_CURRENT, '>h')
          return self._raw_current
    def measure_voltage (self, stime = 1, unit = 'V', voltage_scale = 60):
        self.measure_buffer_voltage = {}
        size = 0
        if voltage_scale == 16 :
           self.write_funct('BRNG', value = self._const.BRNG_16V)
        elif voltage_scale == 32 :
           self.write_funct('BRNG', value = self._const.BRNG_32V)
        elif voltage_scale == 60 :
           self.write_funct('BRNG', value = self._const.BRNG_60V)
        from time import time,sleep
        t_start = time()
        while (time() - t_start) <= stime :
           while not(self.bit_get(self._const.REG_BUS_VOLTAGE, 1, 2, False)) :  # wait for CVRF
              sleep(0.001)
           self._voltage_scale = voltage_scale
           self.measure_buffer_voltage[size] = self.voltage_conversion(self.read_funct('VOLTAGE'),vtype = 'BASE', unit = unit)
           size += 1
        return (size,unit,self.measure_buffer_voltage)
    def measure_shunt_voltage (self, stime = 1, unit = 'mV', voltage_shunt_scale = '80mV'):
        self.measure_buffer_voltage = {}
        size = 0
        if voltage_shunt_scale == '40mV' :
           self.write_funct('PG', value = self._const.PG_40mV)
        elif voltage_shunt_scale == '80mV' :
           self.write_funct('PG', value = self._const.PG_80mV)
        elif voltage_shunt_scale == '160mV' :
           self.write_funct('PG', value = self._const.PG_160mV)
        elif voltage_shunt_scale == '320mV' :
           self.write_funct('PG', value = self._const.PG_320mV)
        from time import time,sleep
        t_start = time()
        while (time() - t_start) <= stime :
           #while not(self.bit_get(self._const.REG_BUS_VOLTAGE, 1, 2, False)) :  # wait for CVRF
           sleep(0.005)
           self._voltage_shunt_scale = voltage_shunt_scale
           self.measure_buffer_voltage[size] = self.voltage_conversion(self.read_funct('SHUNT_VOLTAGE'),vtype = 'SHUNT', unit = unit)
           size += 1
        return (size,unit,self.measure_buffer_voltage)
'''

    def sw_reset (self) :
        ret = 0
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
           
    def self_test(self) :
        ret = 0
        TEXAS_INSTRUMENT_ID = 'TI'
        INA260_ID = 0x227
        _manufacturer_id = self.unaryStruct_get(self._const.REG_MANUFACTURER_ID, ">H").to_bytes(2,'big').decode('utf-8')
        _device_id = hex(self.bits_get(12, self._const.REG_DIE_UID, 4, 2, False))
        revision_id = self.bits_get(4, self._const.REG_DIE_UID, 0, 2, False)
        if not ( _manufacturer_id == TEXAS_INSTRUMENT_ID and _device_id == hex(0x227)) :
           ret = 1
        return ret

    def current_conversion (self, current, unit) :
        if unit == 'mA' :
           result = current * 1.25
        elif unit == 'A' :
           result = (current * 1.25)/1000
        return result

    def power_conversion (self, power, unit) :
        if unit == 'mW' :
           result = power * 1.25
        elif unit == 'W' :
           result = (power * 1.25)/1000
        return result

    def measure_current (self, stime = 1, unit = 'mA'):
        self.measure_buffer_voltage = {}
        size = 0
        from time import time,sleep
        t_start = time()
        while (time() - t_start) <= stime :
           while not(self.bit_get(self._const.REG_MASK_ENABLE, 3, 2, False)) :  # wait for CVRF
              sleep(0.001)
           self.measure_buffer_voltage[size] = self.current_conversion(self.read_funct('CURRENT'),unit)
           size += 1
        return (size,unit,self.measure_buffer_voltage)
'''
