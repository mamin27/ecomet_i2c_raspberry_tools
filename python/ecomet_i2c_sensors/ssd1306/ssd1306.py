from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.ssd1306 import ssd1306_constant

logger = logging.getLogger(__name__) 


class SSD1306(object):
    '''SSD1306() micro altimeter. It is optimized for  altimeter  and  barometer  applications.'''

    def __init__(self, address=ssd1306_constant.SSD1306_ADDRESS_CMD, busnum=ssd1306_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the ssd1306.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._const = ssd1306_constant.register
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self._address = address
        self.mode = '1'
        self.width = 128
        self.height = 64
        self.pages = int(self.height / 8)
        self.cmd_mode = 0x00
        self.data_mode = 0x40
    def sw_reset (self) :
        ret = 0
        try:
            self.set_command (register = self._const.DISPLAY_OFF)
            self.width = 128
            self.height = 64
            self.pages = int(self.height / 8)
            self.set_command (register = self._const.SET_DISPLAY_CLOCK, value = 0x80 )
            self.set_command (register = self._const.SET_MULTIPLEX_RATION, value = 0x3F )
            self.set_command (register = self._const.SET_DISPLAY_OFFSET, value = 0x00 )
            self.set_command (register = self._const.SET_COLUMN_LO, value = 0x00 )
            self.set_command (register = self._const.SET_COLUMN_HI, value = 0x00 )
            self.set_command (register = self._const.SET_PAGE_ADDR, value = 0 )
            self.set_command (register = self._const.SET_COLUMN_ADDRESS, value = 0, value2 = 127 )
            self.set_command (register = self._const.SET_SEGM_REMAP_0 )
            self.set_command (register = self._const.SET_VERTICAL_SCROLL, value = 0x00, value2 = 0x40)
            self.set_command (register = self._const.SET_START_LINE, value = 0x00 )
            self.set_command (register = self._const.CHARGEPUMP, value = 0x14 )
            self.set_command (register = self._const.SET_MEMORY_MODE, value = 0x00 )  #0x02
            self.set_command (register = self._const.SET_REMAP_LEFT )
            self.set_command (register = self._const.SET_OUTPUT_SCAN_UP)
            self.set_command (register = self._const.SET_HW_CONF_MODE, value = 0x12 )
            self.set_command (register = self._const.SET_CONTRAST, value = 0x7F )
            self.set_command (register = self._const.SET_CHARGE_PERIOD, value = 0x22 )
            self.set_command (register = self._const.SET_VCOM, value = 0x20 )
            self.set_command (register = self._const.SET_ENTIRE_DISP )
            self.set_command (register = self._const.SET_NORMAL_DISP ) 
            self.set_command (register = self._const.DISPLAY_ON )
        except :
            ret = ret + 1
            self._logger.debug('write error')
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def setup (self) :
        ret = 0
        try:
            self.set_command (register = self._const.DISPLAY_OFF)
            self.width = 128
            self.height = 64
            self.pages = int(self.height / 8)
            self.set_command (register = self._const.SET_DISPLAY_CLOCK, value = 0x80 )
            self.set_command (register = self._const.SET_MULTIPLEX_RATION, value = 0x3F )
            self.set_command (register = self._const.SET_DISPLAY_OFFSET, value = 0x00 )
            self.set_command (register = self._const.SET_START_LINE, value = 0x00 )
            self.set_command (register = self._const.CHARGEPUMP, value = 0x14 )
            self.set_command (register = self._const.SET_MEMORY_MODE, value = 0x00 )
            self.set_command (register = self._const.SET_REMAP_LEFT )
            self.set_command (register = self._const.SET_OUTPUT_SCAN_UP )
            self.set_command (register = self._const.SET_HW_CONF_MODE, value = 0x12 )
            self.set_command (register = self._const.SET_CONTRAST, value = 0x7F )
            self.set_command (register = self._const.SET_CHARGE_PERIOD, value = 0xF1 )
            self.set_command (register = self._const.SET_VCOM, value = 0x20 )
            self.set_command (register = self._const.SET_ENTIRE_DISP )
            self.set_command (register = self._const.SET_NORMAL_DISP )
            self.set_command (register = self._const.DISPLAY_ON )
        except :
            ret = ret + 1
            self._logger.debug('write error')
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def set_command (self, register, value = None, value2 = None) :
        ret = 0
        if register in [self._const.SET_REMAP_RIGHT,self._const.SET_REMAP_LEFT,
                        self._const.SET_ENTIRE_DISP,self._const.SET_ENTIRE_DISP_IGN,
                        self._const.SET_NORMAL_DISP,self._const.SET_REVERSE_DISP,
                        self._const.SET_REVERSE_DISP,
                        self._const.DATA_DC_DC_OFF,self._const.DATA_DC_DC_ON,
                        self._const.DISPLAY_OFF,self._const.DISPLAY_ON,
                        self._const.SET_SEGM_REMAP_0,self._const.SET_SEGM_REMAP_127,
                        self._const.SET_OUTPUT_SCAN_UP,self._const.SET_OUTPUT_SCAN_DOWN,
                        ] :
           try :
              self._device.writeList(self.cmd_mode,list([register]))
           except :
              ret += 1
        elif register in [self._const.SET_MEMORY_MODE,
                          self._const.CHARGEPUMP,
                          self._const.SET_CONTRAST,
                          self._const.SET_MULTIPLEX_RATION,
                          self._const.SET_DISPLAY_OFFSET,
                          self._const.SET_DISPLAY_CLOCK,
                          self._const.SET_CHARGE_PERIOD,
                          self._const.SET_HW_CONF_MODE,
                          self._const.SET_VCOM
                         ] :
           try :
               self._device.writeList(self.cmd_mode,list([register, value]))
           except :
               ret += 1
        elif register in [self._const.SET_COLUMN_LO,
                          self._const.SET_COLUMN_HI,
                          self._const.SET_START_LINE,
                          self._const.SET_PAGE_ADDR,
                          self._const.SET_MEMORY_MODE] :
           if value > 63 or ( value > 7 and register == self._conf_SET_PAGE_ADDR ) :
               ret += 2
           else :
               register = register + value
               try :
                  self._device.writeList(self.cmd_mode,list([register]))
               except :
                  ret += 1
        elif register in [self._const.SET_COLUMN_ADDRESS,
                          self._const.SET_VERTICAL_SCROLL
                         ] :
           bit_list = [register,value,value2]
           try :
               self._device.writeList(self.cmd_mode,list(bit_list));
           except :
               ret += 1
        if ret > 0 :
           self._logger.debug('write command %s failed (%s)',register,ret)
        else :
           self._logger.debug('write command 0x%s success', '{0:02x}'.format(register))
        return (ret)
    def display(self, image):
        ret = 0
        assert(image.mode == '1')
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        self.set_command(self._const.SET_COLUMN_ADDRESS, 0x00, self.width-1)	# Column start/end address
        self.set_command(self._const.SET_PAGE_ADDR, 0x00, self.pages-1)			# Page start/end address

        pix = list(image.getdata())
        step = self.width * 8
        buf = []
        for y in iter(range(0, self.pages * step, step)):
            i = y + self.width-1
            while i >= y:
                byte = 0
                for n in iter(range(0, step, self.width)):
                    byte |= (pix[i + n] & 0x01) << 8
                    byte >>= 1

                buf.append(byte)
                i -= 1

        self.data(buf)
        return (ret)
    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the
        device - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this it is sent in chunks.
        """
        for i in iter(range(0, len(data), 32)):
            self._device.writeList(self.data_mode,
                                          list(data[i:i+32]))
