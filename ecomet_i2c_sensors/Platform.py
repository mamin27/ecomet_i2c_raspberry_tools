# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import platform
import re

# Platform identification constants.
UNKNOWN          = 0
RASPBERRY_PI     = 1
BEAGLEBONE_BLACK = 2
MINNOWBOARD      = 3
JETSON_NANO      = 4
H616             = 5
A10              = 6

def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black and return the
    platform type.  Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN."""
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        return RASPBERRY_PI

    # Handle Beaglebone Black
    # TODO: Check the Beaglebone Black /proc/cpuinfo value instead of reading
    # the platform.
    plat = platform.platform()

    if plat.lower().find('sun50iw9-aarch64-with-glibc2') > -1:
        return H616
    elif plat.lower().find('olimex-armv7l-with-glibc2') > -1:
        return A10
    elif plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-ubuntu') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-glibc2') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('tegra-aarch64-with-ubuntu') > -1:
        return JETSON_NANO

    # Handle Minnowboard
    # Assumption is that mraa is installed
    try: 
        import mraa 
        if mraa.getPlatformName()=='MinnowBoard MAX':
            return MINNOWBOARD
    except ImportError:
        pass
    
    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN


def pi_revision():
    """Detect the revision number of a Raspberry Pi, useful for changing
    functionality like default I2C bus based on revision."""
    # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            # Match a line of the form "Revision : 0002" while ignoring extra
            # info in front of the revsion (like 1000 when the Pi was over-volted).
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                # Return revision 1 if revision ends with 0000, 0002 or 0003.
                return 1
            elif match:
                # Assume revision 2 if revision ends with any other 4 chars.
                return 2
        # Couldn't find the revision, throw an exception.
        raise RuntimeError('Could not determine Raspberry Pi revision.')


def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # 2835 is pi 3 on 4.9.x kernel
    # 2711 is pi 4
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return ' 1'
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return ' 2'
    elif match.group(1) == 'BCM2835':
        match = re.search('^Model\s+:\s+(.+)$', cpuinfo,
                       flags=re.MULTILINE | re.IGNORECASE)
        match2 = re.search('^Raspberry\s+Pi\s+(.+)(Rev.+)$', match.group(1),
                       flags=re.MULTILINE | re.IGNORECASE)
        match3 = re.sub(r'\s*$','',match2.group(1))
        revision = re.search('^.\.|\s+(\d+)$',match2.group(2), re.IGNORECASE)
        if match3.upper() == 'MODEL B' : # Raspberry Pi Model B Rev 2
          if revision :
            return ' 1B' + '.' + str(revision.group(1))
        if match3.upper() == '3 MODULE B PLUS' :
          if revision :
            return ' 3B' + '.' + str(revision.group(1))
          return ' 3'
        elif match3.upper() == 'COMPUTE MODULE 4' :
          if revision :
            return '_(CM4) ' + str(4) + '.' + str(revision.group(1))
          return '_(CM4) ' + 4
        elif match3.upper() == 'ZERO 2 W' :
          revision = re.search('(\d+\.\d+)$',match2.group(2), re.IGNORECASE)
          if revision.group(1):
            return ' ZERO 2 W ' + str(revision.group(1))
          return ' ZERO 2 W'
        # Pi 3 / Pi on 4.9.x kernel
        return ' 3'
    elif match.group(1) == 'BCM2711':
        match = re.search('^Model\s+:\s+(.+)$', cpuinfo,
                        flags=re.MULTILINE | re.IGNORECASE)
        match2 = re.search('^Raspberry\s+Pi\s+(.+)(Rev.+)$', match.group(1),
                        flags=re.MULTILINE | re.IGNORECASE)
        match3 = re.sub(r'\s*$','',match2.group(1))
        revision = re.search('^.\.|\s+(\d+\.\d+)$',match2.group(2), re.IGNORECASE)
        if match3.upper() == '4 MODEL B' :
          if revision :
            return ' 4B' + ':' + str(revision.group(1))
          return ' 4B'
        return ' 4'
    else:
        # Something else, not a pi.
        return None
	
