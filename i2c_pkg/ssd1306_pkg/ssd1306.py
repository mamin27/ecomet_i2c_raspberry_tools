from __future__ import division
import logging
import time
import math
from i2c_pkg.ssd1306_pkg import ssd1306_constant

logger = logging.getLogger(__name__) 


class SSD1306(object):
    '''SSD1306() micro altimeter. It is optimized for  altimeter  and  barometer  applications.'''

    def __init__(self, address=ssd1306_constant.SSD1306_ADDRESS_CMD, busnum=ssd1306_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the ssd1306.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import i2c_pkg.i2c as I2C
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
            self.write_register('REGISTER1', value = 0)
            self.write_register('REGISTER2', value = 0)
            self.write_register('REGISTER3', value = 255)
        except :
            ret = ret + 1
            self._logger.debug('write error')
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def set_command (self, register, value = None, pointer = None) :
        ret = 0
        if register in [self._const.SET_REMAP_RIGHT,self._const.SET_REMAP_LEFT,
                        self._const.SET_ENTIRE_DISP_ON,self._const.SET_ENTIRE_DISP_OFF,
                        self._const.SET_NORMAL_DISP,self._const.SET_REVERSE_DISP,
                        self._const.SET_REVERSE_DISP,
                        self._const.DATA_DC_DC_OFF,self._const.DATA_DC_DC_ON,
                        self._const.DISPLAY_OFF,self._const.DISPLAY_ON
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
                          self._const.SET_VCOM,
                         ] :
           try :
               self._device.writeList(self.cmd_mode,list([register, value]))
           except :
               ret += 1
        elif register in [self._const.SET_COLUMN_ADDRESS,
                          self._const.SET_PAGE_ADDR,
           
                         ] :
           bit_list = [value,pointer]
           byt_reg = bytearray(bit_list)
           try :
               self._device.writeList(register,byt_reg);
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
