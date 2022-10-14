from __future__ import division
import logging
import time
import math
import struct
import binascii
from ecomet_i2c_sensors.ina260 import ina260_constant

logger = logging.getLogger(__name__) 

def conf_register_list(address=ina260_constant.INA260_ADDRESS) :

   _address = address
   ina = INA260(address=_address)
   ina._logger = logging.getLogger('ecomet.ina260.reglist') 
   register = {}
   reg_conf = {}
   reg_mask_enable = {}
   reg_manuf = {}
   reg_die = {}

   avgcnt = { 0: 1,
              1: 4,
              2: 16,
              3: 64,
              4: 128,
              5: 256,
              6: 512,
              7: 1024,
   }

   vbusct = { 0: '140us',
              1: '204us',
              2: '332us',
              3: '588us',
              4: '1.1ms',
              5: '2.116ms',
              6: '4.156ms',
              7: '8.244ms'
   }

   curct = { 0: '140us',
             1: '204us',
             2: '332us',
             3: '588us',
             4: '1.1ms',
             5: '2.116ms',
             6: '4.156ms',
             7: '8.244ms'
   }

   mode = { 0: 'PowerDown',
            1: 'Current-Triggered',
            2: 'Voltage-Triggered',
            3: 'Cur-Volt-Triggered',
            4: 'PowerDown',
            5: 'Current-Continued',
            6: 'Voltage-Continued',
            7: 'Cur-Volt-Continued'
   }

   reg_conf['RESET'] = 'RESET' if ina.bit_get(ina._const.REG_CONFIG, 15, 2, False) else 'N/A'
   reg_conf['AVGC'] = avgcnt[ina.bits_get(3, ina._const.REG_CONFIG, 9, 2, False)]
   reg_conf['VBUSCT'] = vbusct[ina.bits_get(3, ina._const.REG_CONFIG, 6, 2, False)]
   reg_conf['ISHCT'] = curct[ina.bits_get(3, ina._const.REG_CONFIG, 3, 2, False)]
   reg_conf['MODE'] = mode[ina.bits_get(3, ina._const.REG_CONFIG, 0, 2, False)]

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

   register['CONF'] = reg_conf
   register['MASK_ENBL'] = reg_mask_enable
   register['MANUF'] = reg_manuf
   register['DIE'] = reg_die

   return (register);

class INA260(object):
    '''INA260()'''

    def __init__(self, address=ina260_constant.INA260_ADDRESS, busnum=ina260_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the ina260.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._const = ina260_constant.register
        self._logger = logging.getLogger(__name__)
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self._address = address

        self._device_id_allowed = [hex(0x227),hex(0x226)]

        self.bit_mask = 0
        self.lowest_bit = 0
        self.buffer = {}
        self.buffer[0] = self._const.REG_CONFIG
        self.measure_buffer_voltage = {}
        self.measure_buffer_current = {}
        self.measure_buffer_power = {}
        self.lsb_first = True
        self.sign_bit = False
        self._ioffset = 0
        self._uoffset = 0

        self.format = '>H'

        _raw_current = self.unaryStruct_get (self._const.REG_CURRENT, '>h')
        self._logger.debug("Current %s mA",self.current_conversion(_raw_current, unit = 'mA'))
        _raw_voltage = self.unaryStruct_get (self._const.REG_BUSVOLTAGE, ">H")
        self._logger.debug("Voltage %s V",self.voltage_conversion(_raw_voltage, unit = 'V'))
        _raw_power = self.unaryStruct_get (self._const.REG_POWER, ">H")
        self._logger.debug("Power %s W",self.power_conversion(_raw_power, unit = 'W'))
        self.setup()

    def sw_reset (self) :
        ret = 0
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret

    def setup (self) :
        overcurrent_limit = self.bit_get(self._const.REG_MASK_ENABLE, 15, 2, False)
        under_current_limit = self.bit_get(self._const.REG_MASK_ENABLE, 14, 2, False)
        bus_voltage_over_voltage = self.bit_get(self._const.REG_MASK_ENABLE, 13, 2, False)
        bus_voltage_under_voltage = self.bit_get(self._const.REG_MASK_ENABLE, 12, 2, False)
        power_over_limit = self.bit_get(self._const.REG_MASK_ENABLE, 11, 2, False)
        conversion_ready = self.bit_get(self._const.REG_MASK_ENABLE, 10, 2, False)
        alert_function_flag = self.bit_get(self._const.REG_MASK_ENABLE, 4, 2, False)
        _conversion_ready_flag = self.bit_get(self._const.REG_MASK_ENABLE, 3, 2, False)
        math_overflow_flag = self.bit_get(self._const.REG_MASK_ENABLE, 2, 2, False)
        alert_polarity_bit = self.bit_get(self._const.REG_MASK_ENABLE, 1, 2, False)
        alert_latch_enable = self.bit_get(self._const.REG_MASK_ENABLE, 0, 2, False)
        reset_bit = self.bit_get(self._const.REG_CONFIG, 15, 2, False)

        self.averaging_count = self.bits_get(3, self._const.REG_CONFIG, 9, 2, False)
        self.voltage_conversion_time = self.bits_get(3, self._const.REG_CONFIG, 6, 2, False)
        self.current_conversion_time = self.bits_get(3, self._const.REG_CONFIG, 3, 2, False)
        self.mode = self.bits_get(3, self._const.REG_CONFIG, 0, 2, False)
        mask_enable = self.bits_get(16, self._const.REG_MASK_ENABLE, 0, 2, False)
        alert_limit = self.bits_get(16, self._const.REG_ALERT_LIMIT, 0, 2, False)

        TEXAS_INSTRUMENT_ID = 'TI'
        INA260_ID = 0x227
        _manufacturer_id = self.unaryStruct_get(self._const.REG_MANUFACTURER_ID, ">H").to_bytes(2,'big').decode('utf-8')
        _device_id = hex(self.bits_get(12, self._const.REG_DIE_UID, 4, 2, False))
        revision_id = self.bits_get(4, self._const.REG_DIE_UID, 0, 2, False)
        if not ( _manufacturer_id == TEXAS_INSTRUMENT_ID and _device_id in self._device_id_allowed) :
           self._logger.error("Chip is not INA260")
           
    def self_test(self) :
        ret = 0
        TEXAS_INSTRUMENT_ID = 'TI'
        INA260_ID = 0x227
        _manufacturer_id = self.unaryStruct_get(self._const.REG_MANUFACTURER_ID, ">H").to_bytes(2,'big').decode('utf-8')
        _device_id = hex(self.bits_get(12, self._const.REG_DIE_UID, 4, 2, False))
        revision_id = self.bits_get(4, self._const.REG_DIE_UID, 0, 2, False)
        self._logger.debug("Manufacturer: %s Device: %s Revision_id:%s" ,_manufacturer_id, _device_id, revision_id)
        if not ( _manufacturer_id == TEXAS_INSTRUMENT_ID and _device_id in self._device_id_allowed) :
           ret = 1
        return ret

    def current_conversion (self, current, unit) :
        if unit == 'mA' :
           result = current * 1.25
        elif unit == 'A' :
           result = (current * 1.25)/1000
        return result

    def voltage_conversion (self, voltage, unit) :
        if unit == 'mV' :
           result = voltage * 1.25
        elif unit == 'V' :
           result = (voltage * 1.25)/1000
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

    def unaryStruct_get (self,register,sformat='>H'):
        buf = bytearray(1 + struct.calcsize(sformat))
        buf[0] = register
        self._device.write_then_readinto(buf, buf, out_end=1, in_start=1)
        return struct.unpack_from(sformat,buf,1)[0]

    def unaryStruct_set (self,register,sformat=">H",value=None):
        buf = bytearray(1 + struct.calcsize(sformat))
        buf[0] = register
        struct.pack_into(sformat, buf, 1, value)
        self._device.writeList(buf[0],buf[1,])

    def write_funct (self, function, value):
        if function == 'VBUSCT' :
          self.voltage_conversion_time = self.bits_set(3, self._const.REG_CONFIG, 6, 2, False, value=value)
          return self.voltage_conversion_time
        elif function == 'ISHCT' :
          self.current_conversion_time = self.bits_set(3, self._const.REG_CONFIG, 3, 2, False, value=value)
          return self.current_conversion_time
        elif function == 'AVGC' :
          self.averaging_count = self.bits_set(3, self._const.REG_CONFIG, 9, 2, False, value=value)
          return self.averaging_count
        elif function == 'MODE' :
          self.mode = self.bits_set(3, self._const.REG_CONFIG, 0, 2, False, value=value)
          return self.mode

    def read_funct (self, function, offset):
        if function == 'VBUSCT' :
          self.voltage_conversion_time = self.bits_get(3, self._const.REG_CONFIG, 6, 2, False)
          return self.voltage_conversion_time
        elif function == 'ISHCT' :
          self.current_conversion_time = self.bits_get(3, self._const.REG_CONFIG, 3, 2, False)
          return self.current_conversion_time
        elif function == 'AVGC' :
          self.averaging_count = self.bits_get(3, self._const.REG_CONFIG, 9, 2, False)
          return self.averaging_count
        elif function == 'MODE' :
          self.mode = self.bits_get(3, self._const.REG_CONFIG, 0, 2, False)
          return self.mode
        elif function == 'VOLTAGE' :
          self._raw_voltage = self.unaryStruct_get(self._const.REG_BUSVOLTAGE, ">H") + offset
          return self._raw_voltage
        elif function == 'CURRENT' :
          self._raw_current = self.unaryStruct_get (self._const.REG_CURRENT, '>h') + offset
          return self._raw_current

    def measure_voltage (self, stime = 1, unit = 'mV', uoffset = None):
        self.measure_buffer_voltage = {}
        size = 0
        if not uoffset:
           uoffset = self._uoffset
        from time import time
        t_start = time()
        while (time() - t_start) <= stime :
           while not(self.bit_get(self._const.REG_MASK_ENABLE, 3, 2, False)) :  # wait for CVRF
              pass
           self.measure_buffer_voltage[size] = self.voltage_conversion(self.read_funct(function = 'VOLTAGE',offset = uoffset),unit = unit)
           size += 1
        return (size,unit,self.measure_buffer_voltage)

    def measure_current (self, stime = 1, unit = 'mA', ioffset = None):
        self.measure_buffer_current = {}
        size = 0
        if not ioffset:
           ioffset = self._ioffset
        from time import time
        t_start = time()
        while (time() - t_start) <= stime :
           while not(self.bit_get(self._const.REG_MASK_ENABLE, 3, 2, False)) :  # wait for CVRF
              pass
           self.measure_buffer_current[size] = self.current_conversion(self.read_funct(function = 'CURRENT',offset = ioffset),unit = unit)
           self._logger.info("Current: %s",self.measure_buffer_current[size])
           size += 1
        return (size,unit,self.measure_buffer_current)
