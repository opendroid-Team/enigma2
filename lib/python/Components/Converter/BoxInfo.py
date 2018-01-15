from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Sensors import sensors
import os
from Poll import Poll
from Tools.HardwareInfo import HardwareInfo

class BoxInfo(Poll, Converter, object):
    BOXTYPE = 0
    LOAD = 1
    MEMINFO = 2
    FREEFLASH = 3
    UPTIME = 4
    TEMPSENSOR = 5

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 10000
        self.poll_enabled = True
        if type == 'BoxType':
            self.type = self.BOXTYPE
            self.poll_enabled = False
        elif type == 'LoadAverage':
            self.type = self.LOAD
        elif type == 'MemInfo':
            self.type = self.MEMINFO
        elif type == 'FreeFlash':
            self.type = self.FREEFLASH
        elif type == 'TempSensor':
            self.type = self.TEMPSENSOR
        elif type == 'Uptime':
            self.type = self.UPTIME
        else:
            self.type = self.BOXTYPE

    def getModel(self):
        try:
            box_info = HardwareInfo().get_device_name().upper()
        except:
            return 'Model: N/A'
            box_info = None

        if box_info is not None:
            return 'Dreambox %s' % box_info

    def getLoadAverage(self):
        try:
            with open('/proc/loadavg', 'r') as file:
                load_info = file.read().split()[0:3]
        except:
            return 'Load average: N/A'
            load_info = None

        if load_info is not None:
            return 'Load average: %s' % ', '.join(load_info)

    def getMemInfo(self):
        try:
            with open('/proc/meminfo', 'r') as file:
                mem_info = int(file.read().split()[4])
        except:
            return 'MemFree: N/A'
            mem_info = None

        if mem_info is not None:
            return 'MemFree: %s MB' % (mem_info / 1024)

    def getFreeFlash(self):
        try:
            flash_info = os.statvfs('/')
        except:
            return 'FlashFree: N/A'
            flash_info = None

        if flash_info is not None:
            free_flash = int(flash_info.f_frsize * flash_info.f_bavail / 1024 / 1024)
            return 'FlashFree: %s MB' % free_flash

    def getUptime(self):
        try:
            with open('/proc/uptime', 'r') as file:
                uptime_info = file.read().split()
        except:
            return 'Uptime: N/A'
            uptime_info = None

        if uptime_info is not None:
            total_seconds = float(uptime_info[0])
            MINUTE = 60
            HOUR = MINUTE * 60
            DAY = HOUR * 24
            days = int(total_seconds / DAY)
            hours = int(total_seconds % DAY / HOUR)
            minutes = int(total_seconds % HOUR / MINUTE)
            seconds = int(total_seconds % MINUTE)
            uptime = ''
            if days > 0:
                uptime += str(days) + ' ' + (days == 1 and 'day' or 'days') + ', '
            if len(uptime) > 0 or hours > 0:
                uptime += str(hours) + ' ' + (hours == 1 and 'hour' or 'hours') + ', '
            if len(uptime) > 0 or minutes > 0:
                uptime += str(minutes) + ' ' + (minutes == 1 and 'minute' or 'minutes')
            return 'Uptime: %s' % uptime

    def getTempSensor(self):
        if 'dm7020hd' not in HardwareInfo().get_device_name():
            try:
                sensor_info = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
            except:
                return 'Temp: N/A'
                sensor_info = None

            if sensor_info is not None:
                if len(sensor_info) > 0:
                    return 'Temp: %s\xc2\xb0C' % sensors.getSensorValue(sensor_info[0])
        return 'Temp: No Sensor'

    @cached
    def getText(self):
        if self.type == self.BOXTYPE:
            return self.getModel()
        elif self.type == self.TEMPSENSOR:
            return self.getTempSensor()
        elif self.type == self.LOAD:
            return self.getLoadAverage()
        elif self.type == self.MEMINFO:
            return self.getMemInfo()
        elif self.type == self.FREEFLASH:
            return self.getFreeFlash()
        elif self.type == self.UPTIME:
            return self.getUptime()
        else:
            return '???'

    text = property(getText)

