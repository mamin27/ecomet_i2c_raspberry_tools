from __future__ import division
import logging
import time
import math
import numpy as np
from ecomet_i2c_sensors.axp209 import axp209_constant
from ctypes import c_uint8, BigEndianStructure, Union

reg_list = { 'POWER_OPERATING_MODE_REG' : axp209_constant.POWER_OPERATING_MODE_REG, 'POWER_INPUT_STATUS_REG' : axp209_constant.POWER_INPUT_STATUS_REG,
             'BATTERY_GAUGE_REG' : axp209_constant.BATTERY_GAUGE_REG,
             'INTERNAL_TEMPERATURE_REG' : axp209_constant.INTERNAL_TEMPERATURE_REG, 'BATTERY_VOLTAGE_REG' : axp209_constant.BATTERY_VOLTAGE_REG,
             'BATTERY_CHARGE_CURRENT_REG' : axp209_constant.BATTERY_CHARGE_CURRENT_REG,
             'BATTERY_DISCHARGE_CURRENT_REG' : axp209_constant.BATTERY_DISCHARGE_CURRENT_REG, 'BATTERY_VOLTAGE_REG' : axp209_constant.BATTERY_VOLTAGE_REG,
             'VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG' : axp209_constant.VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG,
             'ADC_ENABLE1_REG' : axp209_constant.ADC_ENABLE1_REG, 'ADC_ENABLE2_REG' : axp209_constant.ADC_ENABLE2_REG
        }

logger = logging.getLogger(__name__)

class AXP209(object):
    '''axp209() Power Management  Controller'''

    def __init__(self, address=axp209_constant.AXP209_ADDRESS, busnum=None, i2c=None, **kwargs) :
        '''Initialize the axp209.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface='smbus2', **kwargs)
        #i2c_interface parameter choise smbus2 lib insted of Adafruit PureIO
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.autocleanup:
            self.close()

    def close(self):
        self._device.close()

    @property
    def gpio2_output(self):
        pass

    @gpio2_output.setter
    def gpio2_output(self, val):
        flags = GPIO012_FEATURE_SET_FLAGS()
        if bool(val):
            flags.gpio_function = 0b111
        else:
            flags.gpio_function = 0b000
        #self.bus.write_byte_data(AXP209_ADDRESS, GPIO2_FEATURE_SET_REG, flags.asbyte)

    @property
    def adc_enable1(self):
        flags = axp209_constant.ADC_ENABLE1_FLAGS()
        (flags.asbyte,ret) = self.read_register('ADC_ENABLE1_REG')
        return flags

    @adc_enable1.setter
    def adc_enable1(self, flags):
        if hasattr(flags, "asbyte"):
            flags = flags.asbyte
        self.write_register('ADC_ENABLE1_REG', flags)

    @property
    def adc_enable2(self):
        flags = axp209_constant.ADC_ENABLE2_FLAGS()
        (flags.asbyte,ret) = self.read_register('ADC_ENABLE2_REG')
        return flags

    @adc_enable2.setter
    def adc_enable2(self, flags):
        if hasattr(flags, "asbyte"):
            flags = flags.asbyte
        self.write_register('ADC_ENABLE2_REG', flags)

    @property
    def vbus_current_limit(self):
        """ Returns the current vbus current limit setting """
        limits = { #00:900 mA; 01:500 mA; 10:100 mA; 11: not limit
            0: "900 mA",
            1: "500 mA",
            2: "100 mA",
            3: "not limited",
        }
        (current_data,ret) = self.read_register('VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG')
        current_limit = current_data & 0x03
        return limits.get(current_limit, "invalid setting")

    @vbus_current_limit.setter
    def vbus_current_limit(self, val):
        flags = axp209_constant.VBUS_CURRENT_LIMIT_CONTROL()
        limits = { #00:900 mA; 01:500 mA; 10:100 mA; 11: not limit
            0: "900 mA",
            1: "500 mA",
            2: "100 mA",
            3: "no limit",
        }
        for setting, limit in limits.items():
            if limit == val :
                (flags.asbyte,ret) = self.read_register('VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG')
                flags.vbus_current_limit = setting
        self.write_register('VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG', flags.asbyte)

    @property
    def power_input_status(self):
        flags = axp209_constant.POWER_INPUT_STATUS_FLAGS()
        (flags.asbyte,ret) = self.read_register('POWER_INPUT_STATUS_REG')
        return flags

    @property
    def battery_current_direction(self):
        return bool(self.power_input_status.battery_current_direction)

    @property
    def power_operating_mode(self):
        flags = axp209_constant.POWER_OPERATING_STATUS_FLAGS()
        (flags.asbyte,ret) = self.read_register('POWER_OPERATING_MODE_REG')
        return flags

    # ADC_ENABLE1 REGISTER status
    @property
    def battery_current_adc_enable(self):
        return bool(self.adc_enable1.battery_current_adc_enable)

    @property
    def acin_voltage_adc_enable(self):
        return bool(self.adc_enable1.acin_voltage_adc_enable)

    @property
    def acin_current_adc_enable(self):
        return bool(self.adc_enable1.acin_current_adc_enable)

    @property
    def vbus_voltage_adc_enable(self):
        return bool(self.adc_enable1.vbus_voltage_adc_enable)

    @property
    def vbus_current_adc_enable(self):
        return bool(self.adc_enable1.vbus_current_adc_enable)

    @property
    def aps_voltage_adc_enable(self):
        return bool(self.adc_enable1.aps_voltage_adc_enable)

    @property
    def ts_pin_adc_function_enable(self):
        return bool(self.adc_enable1.ts_pin_adc_function_enable)

    # TBD_ENABLE2_REGISTER status
    @property
    def apx209_internal_temperature_monitoring_adc_enable(self):
        return bool(self.adc_enable2.apx209_internal_temperature_monitoring_adc_enable)

    @property
    def gpio0_adc_function_enable(self):
        return bool(self.adc_enable2.gpio0_adc_function_enable)

    @property
    def gpio1_adc_function_enable(self):
        return bool(self.adc_enable2.gpio1_adc_function_enable)
    #    
    @property
    def battery_exists(self):
        return bool(self.power_operating_mode.battery_exists)

    @property
    def battery_charging(self):
        return bool(self.power_operating_mode.battery_charging)

    @property
    def battery_voltage(self):
        """ Returns voltage in mV """
        (voltage_bin,ret) = self.read_register('BATTERY_VOLTAGE_REG')
        return voltage_bin * 1.1

    @property
    def battery_charge_current(self):
        """ Returns current in mA """
        (charge_bin,ret) = self.read_register('BATTERY_CHARGE_CURRENT_REG')
        # (12 bits)
        # 0 mV -> 000h,	0.5 mA/bit	FFFh -> 1800 mA
        return charge_bin * 0.5

    @property
    def battery_discharge_current(self):
        """ Returns current in mA """
        (discharge_bin,ret) = self.read_register('BATTERY_DISCHARGE_CURRENT_REG')
        # 13bits
        # 0 mV -> 000h,	0.5 mA/bit	1FFFh -> 1800 mA
        return discharge_bin * 0.5

    @property
    def internal_temperature(self):
        """ Returns temperature in celsius C """
        (temp,ret) = self.read_register('INTERNAL_TEMPERATURE_REG')
        # MSB is 8 bits, LSB is lower 4 bits
        # -144.7c -> 000h,	0.1c/bit	FFFh -> 264.8c
        return temp*0.1-144.7

    @property
    def battery_gauge(self):
        (gauge_bin,ret) = self.read_register('BATTERY_GAUGE_REG')
        gauge = gauge_bin & 0x7f
        if gauge > 100:
            return -1
        return gauge
 
    def read_register(self, register) :
        reg_status = -9999
        ret = 0
        if register in ['INTERNAL_TEMPERATURE_REG','BATTERY_VOLTAGE_REG','BATTERY_CHARGE_CURRENT_REG'] :
           try :
			  # 12 bit
              reg_status_bita = self._device.readList(reg_list[register],2)
              reg_status_hex_high = reg_status_bita[0]
              reg_status_hex_low = reg_status_bita[1]
              reg_status = reg_status_hex_high << 4 | reg_status_hex_low & 0x0f
           except :
              ret = ret + 1
        elif register in ['BATTERY_DISCHARGE_CURRENT_REG'] :
           try :
			  # 13 bit
              reg_status_bita = self._device.readList(reg_list[register],2)
              reg_status_hex_high = reg_status_bita[0]
              reg_status_hex_low = reg_status_bita[1]
              reg_status = reg_status_hex_high << 5 | reg_status_hex_low & 0x1f
           except :
              ret = ret + 1
        elif register in ['POWER_OPERATING_MODE_REG','POWER_INPUT_STATUS_REG','BATTERY_GAUGE_REG','BATTERY_GAUGE_REG','VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG',
                          'ADC_ENABLE1_REG','ADC_ENABLE2_REG'] :
           try :
              reg_status = self._device.readU8(reg_list[register])
           except :
              ret = ret + 1
        return(reg_status,ret)

    def write_register(self, register,data) :
        ret = 0
        #print ( register )
        if register in ['VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG'] :
           self._device.write8(reg_list[register],data)
           try :
              self._device.write8(reg_list[register],data)
           except :
              ret = ret + 1
        return (ret)

