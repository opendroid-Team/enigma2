from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, eTimer
from Components.Element import cached
from Tools.Directories import fileExists
from Components.Sensors import sensors
import re

class OPD_ExtraInfo(Converter, object):
    PROV_CA_ID = 1
    NETCARD_INFO = 2
    CRYPT_INFO = 3
    TEMPERATURE = 4
    PROV_ID = 5
    CAID_ID = 6
    PROV_CA_SOURCE = 7

    def __init__(self, type):
        Converter.__init__(self, type)
        self.DynamicSwitch = False
        self.type = {'ProvCaid': self.PROV_CA_ID,
         'ExtraEcm': self.NETCARD_INFO,
         'CryptInfo': self.CRYPT_INFO,
         'Temperature': self.TEMPERATURE,
         'ProvID': self.PROV_ID,
         'CaidID': self.CAID_ID,
         'ProvID_CaidID_Source': self.PROV_CA_SOURCE}[type]
        self.pat_caid = re.compile('CaID (.*),')
        self.DynamicTimer = eTimer()
        self.DynamicTimer.callback.append(self.doSwitch)

    def hex_str2dec(self, str):
        ret = 0
        try:
            ret = int(re.sub('0x', '', str), 16)
        except:
            pass

        return ret

    def norm_hex(self, str):
        return '%04x' % self.hex_str2dec(str)

    def getExpertInfo(self, theId):
        expertString = '  '
        fileString = ''
        try:
            fp = open('/tmp/share.info', 'r')
            while 1:
                currentLine = fp.readline()
                if currentLine == '':
                    break
                foundIdIndex = currentLine.find('id:' + theId)
                if foundIdIndex is not -1:
                    fileString = currentLine
                    break
                atIndex = fileString.find(' at ')
                cardIndex = fileString.find(' Card ')
                if atIndex is not -1 and cardIndex is not -1:
                    addy = fileString[atIndex + 4:cardIndex]
                    addyLen = len(addy)
                    if addyLen > 15:
                        addy = addy[:9] + '*' + addy[addyLen - 5:]
                        expertString = expertString + addy
                expertString = expertString + '  BoxId:' + theId
                distIndex = fileString.find('dist:')
                if distIndex is not -1:
                    expertString = expertString + ' ' + 'D:' + fileString[distIndex + 5]
                levelIndex = fileString.find('Lev:')
                if levelIndex is not -1:
                    expertString = expertString + ' ' + 'L:' + fileString[levelIndex + 4]

        except:
            print 'Infobar'

        return expertString

    def isGParameter(self, boxId, caId):
        isInGParameter = ''
        try:
            caId = caId[2:]
            fp = open('/usr/keys/cwshare.cfg', 'r')
            while 1:
                currentLine = fp.readline()
                if currentLine == '':
                    break
                line = currentLine.strip()
                if line[:2] == 'G:':
                    rightCurlyIndex = line.find('}')
                    line = line[:rightCurlyIndex]
                    line = line[2:]
                    line = line.strip(' {}\n')
                    c, b = line.split(' ')
                    c = c[:4]
                    if c == caId and b == boxId:
                        isInGParameter = isInGParameter + '(G)'

            fp.close()
            return isInGParameter
        except:
            return isInGParameter

    def getCryptSystemName(self, caID):
        caID = int(caID, 16)
        if caID >= 256 and caID <= 511:
            syID = 'Seca Mediaguard'
        elif caID >= 1280 and caID <= 1535:
            syID = 'Viaccess'
        elif caID >= 1536 and caID <= 1791:
            syID = 'Irdeto'
        elif caID >= 2304 and caID <= 2559:
            syID = 'NDS Videoguard'
        elif caID >= 2816 and caID <= 3071:
            syID = 'Conax'
        elif caID >= 3328 and caID <= 3583:
            syID = 'Cryptoworks'
        elif caID >= 3584 and caID <= 3839:
            syID = 'PowerVu'
        elif caID >= 5888 and caID <= 6143:
            syID = 'Betacrypt'
        elif caID >= 6144 and caID <= 6399:
            syID = 'Nagravision'
        elif caID >= 8704 and caID <= 8959:
            syID = 'Codicrypt'
        elif caID >= 9728 and caID <= 9983:
            syID = 'EBU Biss'
        elif caID >= 18944 and caID <= 19199:
            syID = 'DreamCrypt'
        elif caID >= 21760 and caID <= 22015:
            syID = 'Griffin'
        elif caID >= 41216 and caID <= 41471:
            syID = 'RusCrypt'
        else:
            syID = 'Other'
        return syID

    def getStreamInfo(self, ltype):
        print '============> getText PROV_CA_ID'
        try:
            file = open('/tmp/ecm.info', 'r')
        except:
            return ''

        ee = 0
        caid = '0000'
        provid = '0000'
        while True:
            line = file.readline().strip()
            if line == '':
                break
            x = line.split(':', 1)
            mo = self.pat_caid.search(line)
            if mo:
                caid = mo.group(1)
            if x[0] == 'prov':
                y = x[1].strip().split(',')
                provid = y[0]
            if x[0] == 'provid':
                provid = x[1].strip()
            if x[0] == 'caid':
                caid = x[1].strip()

        file.close()
        if self.hex_str2dec(caid) == 0:
            return ' '
        if ltype == self.PROV_CA_ID:
            return 'CA: ' + self.norm_hex(caid) + '  ID: ' + self.norm_hex(provid)
        if ltype == self.PROV_ID:
            return self.norm_hex(provid)
        if ltype == self.CAID_ID:
            return self.norm_hex(caid)
        return ''

    def getSourceInfo(self, ltype):
        print '============> getText NETCARD_INFO'
        try:
            file = open('/tmp/ecm.info', 'r')
        except:
            return ''

        boxidString = ''
        caIdString = ''
        using = ''
        address = ''
        network = ''
        ecmtime = ''
        hops = ''
        ee = 0
        while True:
            line = file.readline().strip()
            if line == '':
                break
            x = line.split(':', 1)
            if x[0] == 'source':
                address = x[1].strip()
                ee = 2
            if x[0] == 'using':
                using = x[1].strip()
                ee = 1
            if x[0] == 'ecm time':
                ecmtime = x[1].strip()
                ecmtime = ' Time: ' + ecmtime
                ee = 1
            if x[0] == 'hops':
                hops = x[1].strip()
                hops = ' Hops: ' + hops
                ee = 1
            if x[0] == 'decode':
                address = x[1].strip()
                boxidIndex = line.find('prov')
                caidIndex = line.find('CaID')
                caIdString = line[caidIndex + 7:caidIndex + 11]
                if boxidIndex is not -1:
                    boxidString = currentLine[boxidIndex + 6:boxidIndex + 10]
                ee = 3
            if x[0] == 'address':
                address = x[1].strip()
            if x[0] == 'network':
                network = x[1].strip()
            if ecmtime == '':
                x = line.split('--', 1)
                msecIndex = x[0].find('msec')
                if msecIndex is not -1:
                    ecmtime = x[0].strip()
                    ecmtime = ' Time: ' + ecmtime

        file.close()
        if ee == 1:
            emuExpertString = ' ' + using + ' ' + address + ' ' + network + ecmtime + ' s ' + hops
        else:
            emuExpertString = ' ' + using + ' ' + address + ' ' + network + ecmtime + ' ' + self.getExpertInfo(boxidString) + ' ' + self.isGParameter(boxidString, caIdString)
        return emuExpertString

    @cached
    def getText(self):
        service = self.source.service
        if service:
            info = service.info()
            if not info:
                return ''
            self.DynamicTimer.start(3000)
            nazwaemu = 'CI'
            print self.type
            if (self.type == self.PROV_CA_ID or self.type == self.PROV_ID or self.type == self.CAID_ID) and info.getInfo(iServiceInformation.sIsCrypted) == 1 and self.DynamicSwitch:
                return self.getStreamInfo(self.type)
            if self.type == self.NETCARD_INFO and info.getInfo(iServiceInformation.sIsCrypted) == 1 and self.DynamicSwitch:
                return self.getSourceInfo(self.type)
            if self.type == self.PROV_CA_SOURCE and info.getInfo(iServiceInformation.sIsCrypted) == 1 and self.DynamicSwitch:
                first = self.getStreamInfo(self.PROV_CA_ID)
                second = self.getSourceInfo(self.NETCARD_INFO)
                if len(second.strip()) > 0:
                    first = first + '  From:' + second
                return first
            if self.type == self.CRYPT_INFO and self.DynamicSwitch:
                isCrypted = info.getInfo(iServiceInformation.sIsCrypted)
                id_ecm = isCrypted == 1 and ''
                caID = ''
                syID = ''
                try:
                    file = open('/tmp/ecm.info', 'r')
                except:
                    return ''

                while True:
                    line = file.readline().strip()
                    if line == '':
                        break
                    x = line.split(':', 1)
                    if x[0] == 'caid':
                        caID = x[1].strip()
                        sysID = self.getCryptSystemName(caID)
                        return sysID
                    cellmembers = line.split()
                    for x in range(len(cellmembers)):
                        if 'ECM' in cellmembers[x]:
                            if x <= len(cellmembers):
                                caID = cellmembers[x + 3]
                                caID = caID.strip(',;.:-*_<>()[]{}')
                                sysID = self.getCryptSystemName(caID)
                                return sysID

            else:
                return ''
        elif self.type == self.TEMPERATURE and self.DynamicSwitch:
            maxtemp = 0
            try:
                templist = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
                tempcount = len(templist)
                for count in range(tempcount):
                    id = templist[count]
                    tt = sensors.getSensorValue(id)
                    if tt > maxtemp:
                        maxtemp = tt

            except:
                pass

            return str(maxtemp) + '\xc2\xb0C'
        return ''

    @cached
    def getValue(self):
        service = self.source.service
        if service:
            info = service.info()
            return info or -1
        return -1

    text = property(getText)
    value = property(getValue)

    def changed(self, what):
        self.what = what
        Converter.changed(self, what)

    def doSwitch(self):
        self.DynamicSwitch = True
        self.DynamicTimer.stop()
        Converter.changed(self, self.what)

