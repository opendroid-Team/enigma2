<<<<<<< HEAD
#
#  ODExtraInfo - Converter
#  ver 1.2.2 28.12.2014
#
#  Coded by bigroma & 2boom

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Tools.Directories import fileExists
from Components.Element import cached
from Poll import Poll
import os

info = {}
old_ecm_mtime = None

class ODExtraInfo(Poll, Converter, object):
	CAID = 0
	PID = 1
	PROV = 2
	ALL = 3
	IS_NET = 4
	IS_EMU = 5
	CRYPT = 6
	BETA = 7
	CONAX = 8
	CRW = 9
	DRE = 10
	IRD = 11
	NAGRA = 12
	NDS = 13
	SECA = 14
	VIA = 15
	BETA_C = 16
	CONAX_C = 17
	CRW_C = 18
	DRE_C = 19
	IRD_C = 20
	NAGRA_C = 21
	NDS_C = 22
	SECA_C = 23
	VIA_C = 24
	BISS = 25
	BISS_C = 26
	EXS = 27
	EXS_C = 28
	HOST = 29
	DELAY = 30
	FORMAT = 31
	CRYPT2 = 32
	CRD = 33
	CRDTXT = 34
	SHORT = 35
	IS_FTA = 36
	IS_CRYPTED = 37
	my_interval = 1000


	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		if type == "CAID":
			self.type = self.CAID
		elif type == "PID":
			self.type = self.PID
		elif type == "ProvID":
			self.type = self.PROV
		elif type == "Delay":
			self.type = self.DELAY
		elif type == "Host":
			self.type = self.HOST
		elif type == "Net":
			self.type = self.IS_NET
		elif type == "Emu":
			self.type = self.IS_EMU
		elif type == "CryptInfo":
			self.type = self.CRYPT
		elif type == "CryptInfo2":
			self.type = self.CRYPT2
		elif type == "BetaCrypt":
			self.type = self.BETA
		elif type == "ConaxCrypt":
			self.type = self.CONAX
		elif type == "CrwCrypt":
			self.type = self.CRW
		elif type == "DreamCrypt":
			self.type = self.DRE
		elif type == "ExsCrypt":
			self.type = self.EXS
		elif type == "IrdCrypt":
			self.type = self.IRD
		elif type == "NagraCrypt":
			self.type = self.NAGRA
		elif type == "NdsCrypt":
			self.type = self.NDS
		elif type == "SecaCrypt":
			self.type = self.SECA
		elif type == "ViaCrypt":
			self.type = self.VIA
		elif type == "BetaEcm":
			self.type = self.BETA_C
		elif type == "ConaxEcm":
			self.type = self.CONAX_C
		elif type == "CrwEcm":
			self.type = self.CRW_C
		elif type == "DreamEcm":
			self.type = self.DRE_C
		elif type == "ExsEcm":
			self.type = self.EXS_C
		elif type == "IrdEcm":
			self.type = self.IRD_C
		elif type == "NagraEcm":
			self.type = self.NAGRA_C
		elif type == "NdsEcm":
			self.type = self.NDS_C
		elif type == "SecaEcm":
			self.type = self.SECA_C
		elif type == "ViaEcm":
			self.type = self.VIA_C
		elif type == "BisCrypt":
			self.type = self.BISS
		elif type == "BisEcm":
			self.type = self.BISS_C
		elif type == "Crd":
			self.type = self.CRD
		elif type == "CrdTxt":
			self.type = self.CRDTXT
		elif  type == "IsFta":
			self.type = self.IS_FTA
		elif  type == "IsCrypted":
			self.type = self.IS_CRYPTED
		elif type == "Short":
			self.type = self.SHORT
		elif type == "Default" or type == "" or type == None or type == "%":
			self.type = self.ALL
		else:
			self.type = self.FORMAT
			self.sfmt = type[:]

		self.systemTxtCaids = {
			"26" : "BiSS",
			"01" : "Seca Mediaguard",
			"06" : "Irdeto",
			"17" : "BetaCrypt",
			"05" : "Viacces",
			"18" : "Nagravision",
			"09" : "NDS-Videoguard",
			"0B" : "Conax",
			"0D" : "Cryptoworks",
			"4A" : "DRE-Crypt",
			"27" : "ExSet",
			"0E" : "PowerVu",
			"22" : "Codicrypt",
			"07" : "DigiCipher",
			"56" : "Verimatrix",
			"7B" : "DRE-Crypt",
			"A1" : "Rosscrypt"}

		self.systemCaids = {
			"26" : "BiSS",
			"01" : "SEC",
			"06" : "IRD",
			"17" : "BET",
			"05" : "VIA",
			"18" : "NAG",
			"09" : "NDS",
			"0B" : "CON",
			"0D" : "CRW",
			"27" : "EXS",
			"7B" : "DRE",
			"4A" : "DRE" }

	@cached
	def getBoolean(self):

		service = self.source.service
		info = service and service.info()
		if not info:
			return False

		caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if self.type is self.IS_FTA:
			if caids:
				return False
			return True
		if self.type is self.IS_CRYPTED:
			if caids:
				return True
			return False
		if caids:
			if self.type == self.SECA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "01":
						return True
				return False
			if self.type == self.BETA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "17":
						return True
				return False
			if self.type == self.CONAX:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "0B":
						return True
				return False
			if self.type == self.CRW:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "0D":
						return True
				return False
			if self.type == self.DRE:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "7B" or ("%0.4X" % int(caid))[:2] == "4A" :
						return True
				return False
			if self.type == self.EXS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "27":
						return True
			if self.type == self.NAGRA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "18":
						return True
				return False
			if self.type == self.NDS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "09":
						return True
				return False
			if self.type == self.IRD:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "06":
						return True
				return False
			if self.type == self.VIA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "05":
						return True
				return False
			if self.type == self.BISS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == "26":
						return True
				return False
			self.poll_interval = self.my_interval
			self.poll_enabled = True
			ecm_info = self.ecmfile()
			if ecm_info:
				caid = ("%0.4X" % int(ecm_info.get("caid", ""),16))[:2]
				if self.type == self.SECA_C:
					if caid == "01":
						return True
					return False
				if self.type == self.BETA_C:
					if caid == "17":
						return True
					return False
				if self.type == self.CONAX_C:
					if caid == "0B":
						return True
					return False
				if self.type == self.CRW_C:
					if caid == "0D":
						return True
					return False
				if self.type == self.DRE_C:
					if caid == "4A" or caid == "7B":
						return True
					return False
				if self.type == self.EXS_C:
					if caid == "27":
						return True
					return False
				if self.type == self.NAGRA_C:
					if caid == "18":
						return True
					return False
				if self.type == self.NDS_C:
					if caid == "09":
						return True
					return False
				if self.type == self.IRD_C:
					if caid == "06":
						return True
					return False
				if self.type == self.VIA_C:
					if caid == "05":
						return True
					return False
				if self.type == self.BISS_C:
					if caid == "26":
						return True
					return False
				#oscam
				reader = ecm_info.get("reader", None)
				#cccam	
				using = ecm_info.get("using", "")
				#mgcamd
				source = ecm_info.get("source", "")
				if self.type == self.CRD:
					#oscam
					if source == "sci":
						return True
					#wicardd
					if source != "cache" and source != "net" and source.find("emu") == -1:
						return True
					return False
				source = ecm_info.get("source", "")
				if self.type == self.IS_EMU:
					return using == "emu" or source == "emu" or source == "card" or reader == "emu" or source.find("card") > -1 or source.find("emu") > -1 or source.find("biss") > -1 or source.find("cache") > -1
				source = ecm_info.get("source", "")
				if self.type == self.IS_NET:
					if using == "CCcam-s2s":
						return 1
					else:
						if source != "cache" and source == "net" and source.find("emu") == -1:
							return True
						#return  (source != None and source == "net") or (source != None and source != "sci") or (source != None and source != "emu") or (reader != None and reader != "emu") or (source != None and source != "card") 
						
				else:
					return False

		return False

	boolean = property(getBoolean)

	@cached
	def getText(self):
		textvalue = ""
		server = ""
		service = self.source.service
		if service:
			if self.type == self.CRYPT2:
				self.poll_interval = self.my_interval
				self.poll_enabled = True
				ecm_info = self.ecmfile()
				if fileExists("/tmp/ecm.info"):
					try:
						caid = "%0.4X" % int(ecm_info.get("caid", ""),16)
						return "%s" % self.systemTxtCaids.get(caid[:2])
					except:
						return 'nondecode'
				else:
					return 'nondecode'
		if service:
			info = service and service.info()
			if info:
				if info.getInfoObject(iServiceInformation.sCAIDs):
					self.poll_interval = self.my_interval
					self.poll_enabled = True
					ecm_info = self.ecmfile()
					# crypt2
					if ecm_info:
						# caid
						caid = "%0.4X" % int(ecm_info.get("caid", ""),16)
						if self.type == self.CAID:
							return caid
						# crypt
						if self.type == self.CRYPT:
							return "%s" % self.systemTxtCaids.get(caid[:2].upper())
						#pid
						try:
							pid = "%0.4X" % int(ecm_info.get("pid", ""),16)
						except:
							pid = ""
						if self.type == self.PID:
							return pid
						# oscam
						try:
							prov = "%0.6X" % int(ecm_info.get("prov", ""),16)
						except:
							prov = ecm_info.get("prov", "")
						if self.type == self.PROV:
							return prov
						if ecm_info.get("ecm time", "").find("msec") > -1:
							ecm_time = ecm_info.get("ecm time", "")
						else:
							ecm_time = ecm_info.get("ecm time", "").replace(".","").lstrip("0") + " msec"
						if self.type == self.DELAY:
							return ecm_time
						#protocol
						protocol = ecm_info.get("protocol", "")
						#port
						port = ecm_info.get("port", "")
						# source	
						source = ecm_info.get("source", "")
						# server
						server = ecm_info.get("server", "")
						# hops
						hops = ecm_info.get("hops", "")
						#system
						system = ecm_info.get("system", "")
						#provider
						provider = ecm_info.get("provider", "")
						# reader
						reader = ecm_info.get("reader", "")
						if self.type == self.CRDTXT:
							info_card = "False"
							#oscam
							if source == "sci":
								info_card = "True"
							#wicardd
							if source != "cache" and source != "net" and source.find("emu") == -1:
								info_card = "True"
							return info_card
						if self.type == self.HOST:
							return server
						if self.type == self.FORMAT:
							textvalue = ""
							params = self.sfmt.split(" ")
							for param in params:
								if param != '':
									if param[0] != '%':
										textvalue+=param
									#server
									elif param == "%S":
										textvalue+=server
									#hops
									elif param == "%H":
										textvalue+=hops
									#system
									elif param == "%SY":
										textvalue+=system
									#provider
									elif param == "%PV":
										textvalue+=provider
									#port
									elif param == "%SP":
										textvalue+=port
									#protocol
									elif param == "%PR":
										textvalue+=protocol
									#caid
									elif param == "%C":
										textvalue+=caid
									#Pid
									elif param == "%P":
										textvalue+=pid
									#prov
									elif param == "%p":
										textvalue+=prov
									#sOurce
									elif param == "%O":
										textvalue+=source
									#Reader
									elif param == "%R":
										textvalue+=reader
									#ECM Time
									elif param == "%T":
										textvalue+=ecm_time
									elif param == "%t":
										textvalue+="\t"
									elif param == "%n":
										textvalue+="\n"
									elif param[1:].isdigit():
										textvalue=textvalue.ljust(len(textvalue)+int(param[1:]))
									if len(textvalue) > 0:
										if textvalue[-1] != "\t" and textvalue[-1] != "\n":
											textvalue+=" "
							return textvalue[:-1]
						if self.type == self.ALL:
							if source == "emu":
								textvalue = "%s - %s (Prov: %s, Caid: %s)" % (source, self.systemTxtCaids.get(caid[:2]), prov, caid)
							#new oscam ecm.info with port parametr
							elif reader != "" and source == "net" and port != "": 
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (%s:%s) - %s" % (source, prov, caid, reader, protocol, server, port, ecm_time.replace('msec','ms'))
							elif reader != "" and source == "net": 
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (%s) - %s" % (source, prov, caid, reader, protocol, server, ecm_time.replace('msec','ms'))
							elif reader != "" and source != "net": 
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (local) - %s" % (source, prov, caid, reader, protocol, ecm_time.replace('msec','ms'))
							elif server == "" and port == "" and protocol != "": 
								textvalue = "%s - Prov: %s, Caid: %s, %s - %s" % (source, prov, caid, protocol, ecm_time.replace('msec','ms'))
							elif server == "" and port == "" and protocol == "": 
								textvalue = "%s - Prov: %s, Caid: %s - %s" % (source, prov, caid, ecm_time.replace('msec','ms'))
							else:
								try:
									textvalue = "%s - Prov: %s, Caid: %s, %s (%s:%s) - %s" % (source, prov, caid, protocol, server, port, ecm_time.replace('msec','ms'))
								except:
									pass
						if self.type == self.SHORT:
							if source == "emu":
								textvalue = "%s - %s (Prov: %s, Caid: %s)" % (source, self.systemTxtCaids.get(caid[:2]), prov, caid)
							elif server == "" and port == "": 
								textvalue = "%s - Prov: %s, Caid: %s - %s" % (source, prov, caid, ecm_time.replace('msec','ms'))
							else:
								try:
									textvalue = "%s - Prov: %s, Caid: %s, %s:%s - %s" % (source, prov, caid, server, port, ecm_time.replace('msec','ms'))
								except:
									pass
					else:
						if self.type == self.ALL or self.type == self.SHORT or (self.type == self.FORMAT and (self.sfmt.count("%") > 3 )):
							textvalue = "No parse cannot emu"
				else:
					if self.type == self.ALL or self.type == self.SHORT or (self.type == self.FORMAT and (self.sfmt.count("%") > 3 )):
						textvalue = "Free-to-air"
		return textvalue

	text = property(getText)

	def ecmfile(self):
		global info
		global old_ecm_mtime
		ecm = None
		service = self.source.service
		if service:
			try:
				ecm_mtime = os.stat("/tmp/ecm.info").st_mtime
				if not os.stat("/tmp/ecm.info").st_size > 0:
					info = {}
				if ecm_mtime == old_ecm_mtime:
					return info
				old_ecm_mtime = ecm_mtime
				ecmf = open("/tmp/ecm.info", "rb")
				ecm = ecmf.readlines()
			except:
				old_ecm_mtime = None
				info = {}
				return info

			if ecm:
				for line in ecm:
					x = line.lower().find("msec")
					#ecm time for mgcamd and oscam
					if x != -1:
						info["ecm time"] = line[0:x+4]
					else:
						item = line.split(":", 1)
						if len(item) > 1:
							#wicard block
							if item[0] == "Provider":
								item[0] = "prov"
								item[1] = item[1].strip()[2:]
							elif item[0] == "ECM PID":
								item[0] = "pid"
							elif item[0] == "response time":
								info["source"] = "net"
								it_tmp = item[1].strip().split(" ")
								info["ecm time"] = "%s msec" % it_tmp[0]
								y = it_tmp[-1].find('[')
								if y !=-1:
									info["server"] = it_tmp[-1][:y]
									info["protocol"] = it_tmp[-1][y+1:-1]
								#item[0]="port"
								#item[1] = ""
								y = it_tmp[-1].find('(')
								if y !=-1:
									info["server"] = it_tmp[-1].split("(")[-1].split(":")[0]
									info["port"] = it_tmp[-1].split("(")[-1].split(":")[-1].rstrip(")")
								elif y == -1:
									item[0] = "source"
									item[1] = "sci"
								#y = it_tmp[-1].find('emu')
								if it_tmp[-1].find('emu') >-1 or it_tmp[-1].find('cache') > -1 or it_tmp[-1].find('card') > -1 or it_tmp[-1].find('biss') > -1:
									item[0] = "source"
									item[1] = "emu"
							elif item[0] == "hops":
								item[1] = item[1].strip("\n")
							elif item[0] == "system":
								item[1] = item[1].strip("\n")
							elif item[0] == "provider":
								item[1] = item[1].strip("\n")
							elif item[0][:2] == 'cw'or item[0] =='ChID' or item[0] == "Service": 
								pass
							#mgcamd new_oscam block
							elif item[0] == "source":
								if item[1].strip()[:3] == "net":
									it_tmp = item[1].strip().split(" ")
									info["protocol"] = it_tmp[1][1:]
									info["server"] = it_tmp[-1].split(":",1)[0]
									info["port"] = it_tmp[-1].split(':',1)[1][:-1]
									item[1] = "net"
							elif item[0] == "prov":
								y = item[1].find(",")
								if y != -1:
									item[1] = item[1][:y]
							#old oscam block
							elif item[0] == "reader":
								if item[1].strip() == "emu":
									item[0] = "source"
							elif item[0] == "from":
								if item[1].strip() == "local":
									item[1] = "sci"
									item[0] = "source"
								else:
									info["source"] = "net"
									item[0] = "server"
							#cccam block
							elif item[0] == "provid":
								item[0] = "prov"
							elif item[0] == "using":
								if item[1].strip() == "emu" or item[1].strip() == "sci":
									item[0] = "source"
								else:
									info["source"] = "net"
									item[0] = "protocol"
							elif item[0] == "address":
								tt = item[1].find(":")
								if tt != -1:
									info["server"] = item[1][:tt].strip()
									item[0] = "port"
									item[1] = item[1][tt+1:]
							info[item[0].strip().lower()] = item[1].strip()
						else:
							if not info.has_key("caid"):
								x = line.lower().find("caid")
								if x != -1:
									y = line.find(",")
									if y != -1:
										info["caid"] = line[x+5:y]
							if not info.has_key("pid"):
								x = line.lower().find("pid")
								if x != -1:
									y = line.find(" =")
									z = line.find(" *")
									if y != -1:
										info["pid"] = line[x+4:y]
									elif z != -1:
										info["pid"] = line[x+4:z]
				ecmf.close()
		return info

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))

=======
# cryptoinfo modified to suit my needs, by j,puig 13-1-2015
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, eTimer, eServiceReference, eEPGCache
from Components.Element import cached
from Tools.Directories import fileExists
from os import path, popen
import re

class ODExtraInfo(Converter, object):
    TEMPERATURE = 1
    EMU = 2
    HOPS = 3 
    SYSTEM = 4
    CAID = 5
    PROVID = 6
    ECMPID  = 7
    ECMTIME = 8
    ADDRESS = 9

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Temp': self.TEMPERATURE,
         'Emu': self.EMU,
         'Hops': self.HOPS,
         'System': self.SYSTEM,
         'Caid': self.CAID,
         'Provid': self.PROVID,
         'Ecmpid': self.ECMPID,
         'Ecmtime': self.ECMTIME,
         'Address': self.ADDRESS}[type]
        self.pat_caid = re.compile('CaID (.*),')
        self.DynamicTimer = eTimer()
        self.DynamicTimer.callback.append(self.doSwitch)

    def getCryptName(self, caID):
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
            syID = 'CryptoWorks'
        elif caID >= 3584 and caID <= 3839:
            syID = 'PowerVu'
        elif caID >= 5888 and caID <= 6143:
            syID = 'BetaCrypt'
        elif caID >= 6144 and caID <= 6399:
            syID = 'NagraVision'
        elif caID >= 8704 and caID <= 8959:
            syID = 'CodiCrypt'
        elif caID >= 9728 and caID <= 9983:
            syID = 'EBU Biss'
        elif caID >= 18944 and caID <= 19169:
            syID = 'DreamCrypt'
        elif caID >= 19182 and caID <= 19182:
            syID = 'BulCrypt 1'
        elif caID >= 21760 and caID < 21889:
            syID = 'Griffin'
        elif caID == 21889:
            syID = 'BulCrypt 2'
        elif caID > 21889 and caID <= 22015:
            syID = 'Griffin'
        elif caID >= 41216 and caID <= 41471:
            syID = 'RusCrypt'
        else:
            syID = 'Other'
        return syID

    def hex_str2dec(self, str):
        ret = 0
        try:
            ret = int(re.sub('0x', '', str), 16)
        except:
            pass

        return ret

    def getTemperature(self):
        while True:
		systemp = ""
		cputemp = ""
		try:
			if path.exists('/proc/stb/sensors/temp0/value'):
				out_line = popen("cat /proc/stb/sensors/temp0/value").readline()
				systemp = 'Sys Temp : ' + out_line.replace('\n', '') + str('\xc2\xb0') + "C"
			elif path.exists('/proc/stb/fp/temp_sensor'):
				out_line = popen("cat /proc/stb/fp/temp_sensor").readline()
				systemp = 'Board : ' + out_line.replace('\n', '') + str('\xc2\xb0') + "C"
			if path.exists('/proc/stb/fp/temp_sensor_avs'):
				out_line2 = popen("cat /proc/stb/fp/temp_sensor_avs").readline()
				cputemp = 'CPU : ' + out_line2.replace('\n', '') + str('\xc2\xb0') + "C"
		except:
			pass
		if (systemp ==  "") and (cputemp == ""):
			return "No Temp. Sensors Detected"
		elif systemp == "":
			return cputemp
		elif cputemp == "":
			return systemp
		else:
			return systemp + '  -  ' + cputemp

    def getCryptInfo(self):
        service = self.source.service
        info = service and service.info()
        isCrypted = info.getInfo(iServiceInformation.sIsCrypted)
        if isCrypted == 1:
            id_ecm = ''
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
                    sysID = self.getCryptName(caID)
                    return sysID
                cellmembers = line.split()
                for x in range(len(cellmembers)):
                    if 'ECM' in cellmembers[x]:
                        if x <= len(cellmembers):
                            caID = cellmembers[x + 3]
                            caID = caID.strip(',;.:-*_<>()[]{}')
                            sysID = self.getCryptName(caID)
                            return sysID
            file.close()
        else:
            return ''

    def getInfos(self, ltype):
        try:
            file = open('/tmp/ecm.info', 'r')
        except:
            return ''

        caid = '0000'
        provid = '000000'
        pid = '0'
        using = ''
        address = ''
        network = ''
        ecmtime = '1'
        ecmtime2 = 'Waiting...'
        source = ''
        hops = '---'
        emun = ''
        protocol = ''
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
            if x[0] == 'pid':
                pid = x[1].strip()
            if x[0] == 'source':
                source = x[1].strip() 
                address = x[1].strip()
                if 'net (cccamd' in address:
                    address = address.lstrip('net (camd').rstrip(')')
                if 'net (newcamd' in address:
                    address = address.lstrip('net (wcamd').rstrip(')')
            if x[0] == 'address':
                address = x[1].strip()
            if x[0] == 'from':
                address = x[1].strip()
            if x[0] == 'using':
                using = x[1].strip()
                using2 = using
                if using == 'CCcam-s2s':
                    using2 = 'CCcam'
            if x[0] == 'ecm time':
                ecmtime = x[1].strip()
                ecmtime2 = ''
            if x[0] == 'hops':
                hops = x[1].strip()
            if x[0] == 'protocol':
                protocol = x[1].strip()
            if x[0] == 'reader':
                reader = x[1].strip()
            if x[0] == 'network':
                network = x[1].strip()
            if ecmtime2 != '':
                x = line.split('--', 1)
                msecIndex = x[0].find('msec')
                if msecIndex is not -1:
                    ecmtime = x[0].strip()
            ecmtime2 = ecmtime
            emun = "Unknown EMU"
            if (protocol != "" and reader != ""):
            	emun = "EMU : OsCam"
		if (float(ecmtime) >= 1):
		    ecmtime2 = str(ecmtime) + " s"
		else:
                    ecmtime2 = str(int(float(ecmtime) * 1000)) + " ms"

            if (source != ""):
               	emun = "EMU : MgCamd"
		ecmtime = ecmtime.rstrip('ce')
		if (int(ecmtime.split()[0]) >= 1000):
		    ecmtime2 = str(float(ecmtime.split()[0])/1000) + " s"
		else:
                    ecmtime2 = str(ecmtime)

	    if (len(provid) == 8 and using != "") or (using == "SBox"):
		emun = "EMU : SBox"
		if (int(ecmtime.split()[0]) >= 1000):
		    ecmtime2 = str(float(ecmtime.split()[0])/1000) + " s"
		else:
                    ecmtime2 = str(ecmtime)

	    if ((len(provid)<= 7) and (using != "")):
		emun = "EMU : CCcam"
		if (float(ecmtime) >= 1):
		    ecmtime2 = str(ecmtime) + " s"
		else:
                    ecmtime2 = str(int(float(ecmtime) * 1000)) + " ms"

        file.close()
        if self.hex_str2dec(caid) == 0:
            return ' '
        if ltype == self.CAID:
            datadec = int(caid[2:],16)
            datahex = "0x%0.4X" % datadec
            data = str(datadec) + " (" + datahex + ")"
            return "CA ID : " + data
        elif ltype == self.PROVID:
            datadec = int(provid[2:],16)
            datahex = "0x%0.6X" % datadec
            data = str(datadec) + " (" + datahex + ")"
            return "Prov ID : " + data
        elif ltype == self.ECMPID:
            datadec = int(pid[2:],16)
            datahex = "0x%0.4X" % datadec
            data = str(datadec) + " (" + datahex + ")"
            return "ECM PID : " + data
        elif ltype == self.EMU:
            return emun
        elif ltype == self.HOPS:
            return 'Hops : ' + str(hops)
        elif ltype == self.ECMTIME:
            return 'ECM Time : ' + str(ecmtime2)
        elif ltype == self.ADDRESS:
            return 'From : ' + str(address)
        else:
            return ' '

    @cached
    def getText(self):
        self.DynamicTimer.start(500)
        service = self.source.service
        info = service and service.info()
        if not info:
            return ''
        if self.type == self.TEMPERATURE:
            return self.getTemperature()
        if (self.type == self.EMU) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.HOPS) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.SYSTEM) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return 'CA System : ' + str(self.getCryptInfo())
        if (self.type == self.CAID) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.PROVID) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.ECMPID) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.ECMTIME) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
        if (self.type == self.ADDRESS) and info.getInfo(iServiceInformation.sIsCrypted) == 1:
            return self.getInfos(self.type)
       
        return ''

    text = property(getText)

    def changed(self, what):
        self.what = what
        Converter.changed(self, what)

    def doSwitch(self):
        self.DynamicTimer.stop()
        Converter.changed(self, self.what)
>>>>>>> master

