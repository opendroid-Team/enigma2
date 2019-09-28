from Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import config
from Components.Sources.StaticText import StaticText
from Components.Harddisk import Harddisk, harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Console import Console
from enigma import eTimer, getEnigmaVersionString, getDesktop
from boxbranding import getBoxType, getMachineBuild, getMachineBrand, getMachineName, getImageVersion, getImageBuild, getDriverDate, getOEVersion, getImageType, getBrandOEM
from Components.SystemInfo import SystemInfo
from skin import isOPDSkin

from Components.Pixmap import MultiPixmap
from Components.Network import iNetwork
from Components.Button import Button
from Components.Label import Label
from Components.ProgressBar import ProgressBar
import re
from Tools.StbHardware import getFPVersion
from enigma import ePicLoad, getDesktop, eSize, eTimer, eLabel, eConsoleAppContainer
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from Components.AVSwitch import AVSwitch
from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
import skin, os
import time
from os import path, popen, system
from re import search
def parse_ipv4(ip):
	ret = ""
	idx = 0
	if ip is not None:
		for x in ip:
			if idx == 0:
				ret += str(x)
			else:
				ret += "." + str(x)
			idx += 1
	return ret

def parseFile(filename):
	ret = "N/A"
	try:
		f = open(filename, "rb")
		ret = f.read().strip()
		f.close()
	except IOError:
		print "[ERROR] failed to open file %s" % filename
	return ret

def parseLines(filename):
	ret = ["N/A"]
	try:
		f = open(filename, "rb")
		ret = f.readlines()
		f.close()
	except IOError:
		print "[ERROR] failed to open file %s" % filename
	return ret

def MyDateConverter(StringDate):
	## StringDate must be a string "YYYY-MM-DD"
	try:
		StringDate = StringDate.replace("-"," ")
		StringDate = time.strftime(_("%Y-%m-%d"), time.strptime(StringDate, "%Y %m %d"))
		return StringDate
	except:
		return _("unknown")

def find_rootfssubdir(file):
	startup_content = read_startup("/boot/" + file)
	rootsubdir = startup_content[startup_content.find("rootsubdir=")+11:].split()[0]
	if rootsubdir.startswith("linuxrootfs"):
		return rootsubdir
	return

def read_startup(FILE):
	file = FILE
	try:
		with open(file, 'r') as myfile:
			data=myfile.read().replace('\n', '')
		myfile.close()
	except IOError:
		print "[ERROR] failed to open file %s" % file
		data = " "
	return data

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Image Information"))
		self.skinName = ["AboutOE","About"]
		self.populate()

		self["key_green"] = Button(_("Translations"))
                self["key_info"] = StaticText(_("Contact Info"))
		self["actions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"log": self.showAboutReleaseNotes,
				"blue": self.showModelPic,
                                "info": self.showContactInfo,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
				"green": self.showTranslationInfo,
				"yellow": self.showMemoryInfo,
			})

	def populate(self):
		def netspeed():
			netspeed=""
			for line in popen('ethtool eth0 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)
		def netspeed_eth1():
			netspeed=""
			for line in popen('ethtool eth1 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)
		def netspeed_ra0():
			netspeed=""
			for line in popen('iwconfig ra0 | grep Bit | cut -c 75-85','r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def netspeed_wlan0():
			netspeed=""
			for line in popen('iwconfig wlan0 | grep Bit | cut -c 75-85','r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def netspeed_wlan1():
			netspeed=""
			for line in popen('iwconfig wlan1 | grep Bit | cut -c 75-85','r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def freeflash():
			freeflash=""
			for line in popen("df -mh / | grep -v '^Filesystem' | awk '{print $4}'",'r'):
				line = line.strip()
				freeflash += line
				return str(freeflash)
		self["lab1"] = StaticText(_("OpenDroid by OPD Image Team"))
		self["lab2"] = StaticText(_("Support at") + " www.droidsat.org")
		model = None
		AboutText = ""
		self["lab2"] = StaticText(_("Support:") + " www.droidsat.org")
		AboutText += _("Model:\t%s %s\n") % (getMachineBrand(), getMachineName())

		if path.exists('/proc/stb/info/chipset'):
			if SystemInfo["HasHiSi"]:
				AboutText += _("Chipset:\tHiSilicon %s\n") % about.getChipSetString().upper()
			elif about.getIsBroadcom():
				AboutText += _("Chipset:\tBroadcom %s\n") % about.getChipSetString().upper()
			else:
				AboutText += _("Chipset:\t%s\n") % about.getChipSetString().upper()

				AboutText += _("CPU:\t%s %s %s\n") % (about.getCPUArch(), about.getCPUSpeedString(), about.getCpuCoresString())

		cmd = 'cat /proc/cpuinfo | grep "cpu MHz" -m 1 | awk -F ": " ' + "'{print $2}'"
		cmd2 = 'cat /proc/cpuinfo | grep "BogoMIPS" -m 1 | awk -F ": " ' + "'{print $2}'"
		try:
			res = popen(cmd).read()
			res2 = popen(cmd2).read()
		except:
			res = ""
			res2 = ""
		cpuMHz = ""

		bootloader = ""
		if path.exists('/sys/firmware/devicetree/base/bolt/tag'):
			f = open('/sys/firmware/devicetree/base/bolt/tag', 'r')
			bootloader = f.readline().replace('\x00', '').replace('\n', '')
			f.close()
		BootLoaderVersion = 0
		try:
			if bootloader:
				AboutText += _("Bootloader:\t%s\n") % (bootloader)
				BootLoaderVersion = int(bootloader[1:])
		except:
			BootLoaderVersion = 0

		if getMachineBuild() in ('u41','u42','u43'):
			cpuMHz = _("   (1.0 GHz)")
		elif getMachineBuild() in ('vusolo4k','vuultimo4k','vuzero4k'):
			cpuMHz = _("   (1.5 GHz)")
		elif getMachineBuild() in ('formuler1tc','formuler1', 'triplex', 'tiviaraplus'):
			cpuMHz = _("   (1.3 GHz)")
		elif getMachineBuild() in ('gbmv200','u51','u5','u53','u532','u533','u52','u54','u55','u56','u5pvr','h9','h9combo','h10','cc1','sf8008','hd60','hd61','i55plus','ustym4kpro','beyonwizv2','viper4k','v8plus','multibox'):
			cpuMHz = _("   (1.6 GHz)")
		elif getMachineBuild() in ('vuuno4kse','vuuno4k','dm900','dm920', 'gb7252', 'dags7252','xc7439','8100s'):
			cpuMHz = _("   (1.7 GHz)")
		elif getMachineBuild() in ('alien5',):
			cpuMHz = _("   (2.0 GHz)")
		elif getMachineBuild() in ('vuduo4k',):
			cpuMHz = _("   (2.1 GHz)")
		elif getMachineBuild() in ('sf5008','et13000','et1x000','hd52','hd51','sf4008','vs1500','h7','osmio4k','osmio4kplus'):
			try:
				import binascii
				f = open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb')
				clockfrequency = f.read()
				f.close()
				cpuMHz = _("   (%s MHz)") % str(round(int(binascii.hexlify(clockfrequency), 16)/1000000,1))
			except:
				cpuMHz = _("   (1.7 GHz)")
		else:
			if path.exists('/proc/cpuinfo'):
				f = open('/proc/cpuinfo', 'r')
				temp = f.readlines()
				f.close()
				try:
					for lines in temp:
						lisp = lines.split(': ')
						if lisp[0].startswith('cpu MHz'):
							#cpuMHz = "   (" +  lisp[1].replace('\n', '') + " MHz)"
							cpuMHz = "   (" +  str(int(float(lisp[1].replace('\n', '')))) + " MHz)"
							break
				except:
					pass

		bogoMIPS = ""
		if res:
			cpuMHz = "" + res.replace("\n", "") + " MHz"
		if res2:
			bogoMIPS = "" + res2.replace("\n", "")

		if getMachineBuild() in ('vusolo4k','hd51','hd52','sf4008','dm900','h7','gb7252'):
			AboutText += _("CPU:\t%s") % about.getCPUString() + cpuMHz + "\n"
		else:
			AboutText += _("CPU:\t%s") % about.getCPUString() + " " + cpuMHz + "\n"
		dMIPS = 0
		if getMachineBuild() in ('vusolo4k','vuultimo4k'):
			dMIPS = "10.500"
		elif getMachineBuild() in ('hd52','hd51','sf4008','dm900','h7','gb7252'):
			dMIPS = "12.000"
		if getMachineBuild() in ('vusolo4k','hd51','hd52','sf4008','dm900','h7','gb7252'):
			AboutText += _("DMIPS:\t") + dMIPS + "\n"
		else:
			AboutText += _("BogoMIPS:\t%s") % bogoMIPS + "\n"
		AboutText += _("Cores:\t%s") % about.getCpuCoresString() + "\n"
		AboutText += _("OPD Version:\tV%s") % getImageVersion() + " Build " + getImageBuild() + " based on " + getOEVersion() + "\n"
		AboutText += _("Kernel (Box):\t%s") % about.getKernelVersionString() + " (" + getBoxType() + ")" + "\n"
		imagestarted = ""
		bootname = ''
		if path.exists('/boot/bootname'):
			f = open('/boot/bootname', 'r')
			bootname = f.readline().split('=')[1]
			f.close()
		if SystemInfo["HasRootSubdir"]:
			image = find_rootfssubdir("STARTUP")
			AboutText += _("Selected Image:\t%s") % "STARTUP_" + image[-1:] + bootname + "\n"
		elif getMachineBuild() in ('gbmv200','cc1','sf8008','ustym4kpro','beyonwizv2',"viper4k"):
			if path.exists('/boot/STARTUP'):
				f = open('/boot/STARTUP', 'r')
				f.seek(5)
				image = f.read(4)
				if image == "emmc":
					image = "1"
				elif image == "usb0":
					f.seek(13)
					image = f.read(1)
					if image == "1":
						image = "2"
					elif image == "3":
						image = "3"
					elif image == "5":
						image = "4"
					elif image == "7":
						image = "5"
				f.close()
				if bootname: bootname = "   (%s)" %bootname 
				AboutText += _("Selected Image:\t\t%s") % _("STARTUP_") + image + bootname + "\n"
	        elif getMachineBuild() in ('osmio4k'):
		        if path.exists('/boot/STARTUP'):
			        f = open('/boot/STARTUP', 'r')
			        f.seek(38)
			        image = f.read(1)
			        f.close()
			        if bootname: bootname = "   (%s)" %bootname 
			        AboutText += _("Selected Image:\t%s") % "STARTUP_" + image + bootname + "\n"
		elif path.exists('/boot/STARTUP'):
			f = open('/boot/STARTUP', 'r')
			f.seek(22)
			image = f.read(1) 
			f.close()
			if bootname: bootname = "   (%s)" %bootname
			AboutText += _("Selected Image:\t%s") % "STARTUP_" + image + bootname + "\n"
		elif path.exists('/boot/cmdline.txt'):
			f = open('/boot/cmdline.txt', 'r')
			f.seek(38)
			image = f.read(1) 
			f.close()
			if bootname: bootname = "   (%s)" %bootname 
			AboutText += _("Selected Image:\t%s") % "STARTUP_" + image + bootname + "\n"

		if path.isfile("/etc/issue"):
			version = open("/etc/issue").readlines()[-2].upper().strip()[:-6]
			if path.isfile("/etc/image-version"):
				build = self.searchString("/etc/image-version", "^build=")
				version = "%s #%s" % (version,build)
			AboutText += _("Image:\t%s") % version + "\n"
		AboutText += _("Build:\t%s") % getImageBuild() + "\n"
		AboutText += _("Kernel:\t%s") % about.getKernelVersionString() + "\n"

		string = getDriverDate()
		year = string[0:4]
		month = string[4:6]
		day = string[6:8]
		driversdate = '-'.join((year, month, day))
		gstcmd = 'opkg list-installed | grep "gstreamer1.0 -" | cut -c 16-32'
		gstcmd2 = os.system(gstcmd)
		AboutText += _("Drivers:\t%s") % driversdate + "\n"
		AboutText += _("GStreamer:\t%s") % about.getGStreamerVersionString() + "\n"
		AboutText += _("Python:\t%s\n") % about.getPythonVersionString()
		if path.exists('/boot/STARTUP'):
			AboutText += _("Flashed:\tMultiboot active\n")
		else:
			AboutText += _("Flashed:\t%s\n") % about.getFlashDateString()
		AboutText += _("Free Flash:\t%s\n") % freeflash()
		AboutText += _("Skin:\t%s (%s x %s)\n") % (config.skin.primary_skin.value.split('/')[0], getDesktop(0).size().width(), getDesktop(0).size().height())
		AboutText += _("Last update:\t%s") % getEnigmaVersionString() + " to Build #" + getImageBuild() + "\n"
		AboutText += _("E2 (re)starts:\t%s\n") % config.misc.startCounter.value
		if getMachineBuild() not in ('vuduo4k','osmio4k','h9','h9combo','h10','vuzero4k','sf5008','et13000','et1x000','hd51','hd52','vusolo4k','vuuno4k','vuuno4kse','vuultimo4k','sf4008','dm820','dm7080','dm900','dm920', 'gb7252', 'dags7252', 'vs1500','h7','xc7439','8100s','u5','u5pvr','u52','u53','u54','u55','u56','u51','sf8008','i55plus'):
			AboutText += _("Installed:\t\t%s") % about.getFlashDateString() + "\n"
		AboutText += _("Network:")
		eth0 = about.getIfConfig('eth0')
		eth1 = about.getIfConfig('eth1')
		ra0 = about.getIfConfig('ra0')
		wlan0 = about.getIfConfig('wlan0')
		wlan1 = about.getIfConfig('wlan1')
		if eth0.has_key('addr'):
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + " (" + netspeed() + ")\n"
		elif eth1.has_key('addr'):
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + " (" + netspeed_eth1() + ")\n"
		elif ra0.has_key('addr'):
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + " (~" + netspeed_ra0() + ")\n"
		elif wlan0.has_key('addr'):
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + " (~" + netspeed_wlan0() + ")\n"
		elif wlan1.has_key('addr'):
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + " (~" + netspeed_wlan1() + ")\n"
		else:
			for x in about.GetIPsFromNetworkInterfaces():
				AboutText += "\t" + x[0] + ": " + x[1] + "\n"

		fp_version = getFPVersion()
		if fp_version is None:
			fp_version = ""
		elif fp_version != 0:
			fp_version = _("Frontprocessor:\tVersion %s") % fp_version
			AboutText += fp_version + "\n"

		tempinfo = ""
		if path.exists('/proc/stb/sensors/temp0/value'):
			f = open('/proc/stb/sensors/temp0/value', 'r')
			tempinfo = f.read()
			f.close()
		elif path.exists('/proc/stb/fp/temp_sensor'):
			f = open('/proc/stb/fp/temp_sensor', 'r')
			tempinfo = f.read()
			f.close()
		elif path.exists('/proc/stb/sensors/temp/value'):
			f = open('/proc/stb/sensors/temp/value', 'r')
			tempinfo = f.read()
			f.close()
		elif path.exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
			if getBoxType() in ('mutant51', 'ax51', 'zgemmah7'):
				tempinfo = ""
			else:
				f = open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r')
				tempinfo = f.read()
				tempinfo = tempinfo[:-4]
				f.close()
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			mark = str('\xc2\xb0')
			AboutText += _("System Temperature:\t%s") % tempinfo.replace('\n', '').replace(' ','') + mark + "C\n"

		tempinfo = ""
		if path.exists('/proc/stb/fp/temp_sensor_avs'):
			f = open('/proc/stb/fp/temp_sensor_avs', 'r')
			tempinfo = f.read()
			f.close()
		elif path.exists('/proc/stb/power/avs'):
			f = open('/proc/stb/power/avs', 'r')
			tempinfo = f.read()
			f.close()
		elif path.exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
			try:
				f = open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r')
				tempinfo = f.read()
				tempinfo = tempinfo[:-4]
				f.close()
			except:
				tempinfo = ""
		elif path.exists('/proc/hisi/msp/pm_cpu'):
			try:
				for line in open('/proc/hisi/msp/pm_cpu').readlines():
					line = [x.strip() for x in line.strip().split(":")]
					if line[0] in ("Tsensor"):
						temp = line[1].split("=")
						temp = line[1].split(" ")
						tempinfo = temp[2]
						if getMachineBuild() in ('u41','u42','u43'):
							tempinfo = str(int(tempinfo) - 15)
			except:
				tempinfo = ""
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			mark = str('\xc2\xb0')
			AboutText += _("Processor Temperature:\t%s") % tempinfo.replace('\n', '').replace(' ','') + mark + "C\n"
		AboutLcdText = AboutText.replace('\t', ' ')

		self["AboutScrollLabel"] = ScrollLabel(AboutText)
#		self["key_red"] = Button(_("Devices"))
		self["key_yellow"] = Button(_("Memory Info"))
		self["key_blue"] = Button(_("%s ") % getMachineName() + _("picture"))

		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions", "ChannelSelectEPGActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"info": self.showContactInfo,
				"yellow": self.showMemoryInfo,
				"blue": self.showModelPic,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})
	def populate_opd(self):
		pass

	def showID(self):
		if SystemInfo["HaveID"]:
			try:
				f = open("/etc/.id")
				id = f.read()[:-1].split('=')
				f.close()
				from Screens.MessageBox import MessageBox
				self.session.open(MessageBox,id[1], type = MessageBox.TYPE_INFO)
			except:
				pass
	def searchString(self, file, search):
		f = open(file)
		for line in f:
			if re.match(search, line):
				return line.split("=")[1].replace('\n', '')
		f.close()

	def showTranslationInfo(self):
		self.session.open(TranslationInfo)

	def showDevices(self):
		self.session.open(Devices)
	def showContactInfo(self):
		self.session.open(ContactInfo)
	def showMemoryInfo(self):
		self.session.open(MemoryInfo)

	def showAboutReleaseNotes(self):
		self.session.open(ViewGitLog)

	def createSummary(self):
		return AboutSummary

	def showModelPic(self):
		self.session.open(ModelPic)

	def pageUp(self):
		if isOPDSkin:
			self["FullAbout"].pageUp()
		else:
			self["AboutScrollLabel"].pageUp()

	def pageDown(self):
		if isOPDSkin:
			self["FullAbout"].pageDown()

class ModelPic(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["ModelPic", "About"]

		self["key_green"] = Button(_(" "))
		self["key_red"] = Button(_(" "))
		self["key_yellow"] = Button(_(" "))
		self["key_blue"] = Button(_("%s ") % (getMachineName()) + _("Info"))

		self["model"] = Label(_("%s %s") % (getMachineBrand(), getMachineName()))
		self["boxpic"] = Pixmap()
		self.onFirstExecBegin.append(self.poster_resize)

		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"blue": self.close
			}, -2)

	def poster_resize(self):
		if getBoxType() in ('sf108'):
			model = "sf108.png"
		elif getBoxType() in ('sf4008'):
			model = "sf4008.png"
		elif getBoxType() in ('sf5008'):
			model = "sf5008.png"
		elif getBoxType() in ('sf8008'):
			model = "sf8008.png"
		elif getBoxType() in ('sf8008s'):
		        model = "sf8008s.png"
		elif getBoxType() in ('sf3038'):
			model = "sf3038.png"
		elif getBoxType() in ('sf128'):
			model = "sf128.png"
		elif getBoxType() in ('sf138'):
			model = "sf138.png"
		elif getBoxType() in ('sf208'):
			model = "sf208.png"
		elif getBoxType() in ('sf228'):
			model = "sf228.png"
		elif getBoxType() in ('sf98'):
			model = "sf98.png"
		elif getBoxType() in ('zgemmah7'):
			model = "zgemmah7.png"
		elif getBoxType() in ('zgemmah7c'):
			model = "zgemmah7c.png"
		elif getBoxType() in ('zgemmah7s'):
			model = "zgemmah7s.png"
		elif getBoxType() in ('zgemmah2h'):
			model = "zgemmah2h.png"
		elif getBoxType() in ('zgemmah2s'):
			model = "zgemmah2s.png"
		elif getBoxType() in ('zgemmah2splus'):
			model = "zgemmah2splus.png"
		elif getBoxType() in ('zgemmah32tc'):
			model = "zgemmah32tc.png"
		elif getBoxType() in ('zgemmah3ac'):
			model = "zgemmah3ac.png"
		elif getBoxType() in ('zgemmah4'):
			model = "zgemmah4.png"
		elif getBoxType() in ('zgemmah5'):
			model = "zgemmah5.png"
		elif getBoxType() in ('zgemmah52s'):
			model = "zgemmah52s.png"
		elif getBoxType() in ('zgemmah7'):
			model = "zgemmah7.png"
		elif getBoxType() in ('zgemmah7c'):
			model = "zgemmah7c.png"
		elif getBoxType() in ('zgemmah7s'):
			model = "zgemmah7s.png"
		elif getBoxType() in ('zgemmah52splus'):
			model = "zgemmah52splus.png"
		elif getBoxType() in ('zgemmah52tc'):
			model = "zgemmah52tc.png"
		elif getBoxType() in ('zgemmah5ac'):
			model = "zgemmah5ac.png"
		elif getBoxType() in ('zgemmah6'):
			model = "zgemmah6.png"
		elif getBoxType() in ('zgemmah9s'):
			model = "zgemmah9s.png"
		elif getBoxType() in ('zgemmah9splus'):
			model = "zgemmah9splus.png"
		elif getBoxType() in ('zgemmah9t'):
			model = "zgemmah9t.png"
		elif getBoxType() in ('zgemmah92h'):
			model = "zgemmah92h.png"
		elif getBoxType() in ('zgemmah92s'):
			model = "zgemmah92s.png"
		elif getBoxType() in ('zgemmah9twin'):
			model = "zgemmah9twin.png"
		elif getBoxType() in ('zgemmah9combo'):
			model = "zgemmah9combo.png"
		elif getBoxType() in ('zgemmah10'):
			model = "zgemmah10.png"
		elif getBoxType() in ('zgemmahs'):
			model = "zgemmahs.png"
		elif getBoxType() in ('zgemmai55'):
			model = "zgemmai55.png"
		elif getBoxType() in ('zgemmai55plus'):
			model = "zgemmai55plus.png"
		elif getBoxType() in ('vuduo'):
			model = "vuduo.png "
		elif getBoxType() in ('vuduo2'):
			model = "vuduo2.png"
		elif getBoxType() in ('vusolo'):
			model = "vusolo.png"
		elif getBoxType() in ('vusolo2'):
			model = "vusolo2.png"
		elif getBoxType() in ('vusolo4k'):
			model = "vusolo4k.png"
		elif getBoxType() in ('vusolose'):
			model = "vusolose.png"
		elif getBoxType() in ('vuultimo'):
			model = "vuultimo.png"
		elif getBoxType() in ('vuultimo4k'):
			model = "vuultimo4k.png"
		elif getBoxType() in ('vuuno'):
			model = "vuuno.png"
		elif getBoxType() in ('vuuno4k'):
			model = "vuuno4k.png"
		elif getBoxType() in ('vuuno4kse'):
			model = "vuuno4kse.png"
		elif getBoxType() in ('vuduo4k'):
		        model = "vuduo4k.png"
		elif getBoxType() in ('vuzero'):
			model = "vuzero.png"
		elif getBoxType() in ('vuzero4k'):
		        model = "vuzero4k.png"
		elif getBoxType() in ('gb800se'):
			model = "gb800se.png "
		elif getBoxType() in ('gb800seplus'):
			model = "gb800seplus.png"
		elif getBoxType() in ('gb800solo'):
			model = "gb800solo.png"
		elif getBoxType() in ('gb800ue'):
			model = "gb800ue.png "
		elif getBoxType() in ('gb800ueplus'):
			model = "gb800ueplus.png"
		elif getBoxType() in ('gbipbox'):
			model = "gbipbox.png"
		elif getBoxType() in ('gbquad'):
			model = "gbquad.png"
		elif getBoxType() in ('gbquad4k'):
			model = "gbquad4k.png"
		elif getBoxType() in ('gbquadplus'):
			model = "gbquadplus.png"
		elif getBoxType() in ('gbue4k'):
			model = "gbue4k.png"
		elif getBoxType() in ('gbultrase'):
			model = "gbultrase.png"
		elif getBoxType() in ('gbultraue'):
			model = "gbultraue.png"
		elif getBoxType() in ('gbx1'):
			model = "gbx1.png"
		elif getBoxType() in ('gbx2'):
			model = "gbx2.png"
		elif getBoxType() in ('gbx3'):
			model = "gbx3.png"
		elif getBoxType() in ('gbx3h'):
			model = "gbx3h.png "
		elif getBoxType() in ('dinobot4k'):
			model = "dinobot4k.png"
		elif getBoxType() in ('dinobot4kplus'):
			model = "dinobot4kplus.png"
		elif getBoxType() in ('dinobot4kmini'):
			model = "dinobot4kmini.png"
		elif getBoxType() in ('dinobot4kse'):
			model = "dinobot4kse.png"
		elif getBoxType() in ('dinobot4kpro'):
			model = "dinobot4kpro.png"
		elif getBoxType() in ('hitube4k'):
			model = "hitube4k.png"
		elif getBoxType() in ('atemio5x00'):
			model = "atemio5x00.png"
		elif getBoxType() in ('atemio6000'):
			model = "atemio6000.png"
		elif getBoxType() in ('atemio6100'):
			model = "atemio6100.png"
		elif getBoxType() in ('atemio6200'):
			model = "atemio6200.png"
		elif getBoxType() in ('atemionemesis'):
			model = "atemionemesis.png"
		elif getBoxType() in ('mutant51'):
			model = "mutant51.png"
		elif getBoxType() in ('mutant60'):
			model = "mutant60.png"
		elif getBoxType() in ('mutant61'):
			model = "mutant61.png"
		elif getBoxType() in ('osmio4k'):
			model = "osmio4k.png"
		elif getBoxType() in ('osmega'):
			model = "osmega.png"
		elif getBoxType() in ('osmini'):
			model = "osmini.png"
		elif getBoxType() in ('osminiplus'):
			model = "osminiplus.png"
		elif getBoxType() in ('osnino'):
			model = "osnino.png"
		elif getBoxType() in ('osninoplus'):
			model = "osninoplus.png"
		elif getBoxType() in ('osninopro'):
			model = "osninopro.png"	
		elif getBoxType() in ('gbtrio4k'):
			model = "gbtrio4k.png"	
		else:
			model = None
		poster_path = "/usr/share/enigma2/%s" % model
		self["boxpic"].hide()
		sc = AVSwitch().getFramebufferScale()
		self.picload = ePicLoad()
		size = self["boxpic"].instance.size()
		self.picload.setPara((size.width(), size.height(), sc[0], sc[1], False, 1, "#00000000"))
		if self.picload.startDecode(poster_path, 0, 0, False) == 0:
			ptr = self.picload.getData()
			if ptr != None:
				self["boxpic"].instance.setPixmap(ptr)
				self["boxpic"].show()

class Devices(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["Devices", "About"]
		Screen.setTitle(self, _("Device Information"))
		self["TunerHeader"] = StaticText(_("Detected NIMs:"))
		self["HDDHeader"] = StaticText(_("Detected Devices:"))
		self["MountsHeader"] = StaticText(_("Network Servers:"))
		self["nims"] = StaticText()
		self["hdd"] = StaticText()
		self["mounts"] = StaticText()
		self["devices"] = ScrollLabel()
		self.list = []
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.populate2)
		self["actions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
			{
				"up": self["devices"].pageUp,
				"down": self["devices"].pageDown,
				"cancel": self.close,
				"ok": self.close,
			})
		self.onLayoutFinish.append(self.populate)

	def populate(self):
		self.mountinfo = ''
		self["actions"].setEnabled(False)
		scanning = _("Wait please while scanning for devices...")
		self["nims"].setText(scanning)
		self["hdd"].setText(scanning)
		self['mounts'].setText(scanning)
		self['devices'].setText(scanning)
		self.activityTimer.start(1)

	def populate2(self):
		self.activityTimer.stop()
		self.Console = Console()
		niminfo = ""
		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if niminfo:
				niminfo += "\n"
			niminfo += nims[count]
		self["nims"].setText(niminfo)

		self.list = []
		list2 = []
		f = open('/proc/partitions', 'r')
		for line in f.readlines():
			parts = line.strip().split()
			if not parts:
				continue
			device = parts[3]
			if not search('sd[a-z][1-9]', device):
				continue
			if device in list2:
				continue

			mount = '/dev/' + device
			f = open('/proc/mounts', 'r')
			for line in f.readlines():
				if device in line:
					parts = line.strip().split()
					mount = str(parts[1])
					break
			f.close()

			if not mount.startswith('/dev/'):
				size = Harddisk(device).diskSize()
				free = Harddisk(device).free()

				if ((float(size) / 1024) / 1024) >= 1:
					sizeline = _("Size: ") + str(round(((float(size) / 1024) / 1024), 2)) + _("TB")
				elif (size / 1024) >= 1:
					sizeline = _("Size: ") + str(round((float(size) / 1024), 2)) + _("GB")
				elif size >= 1:
					sizeline = _("Size: ") + str(size) + _("MB")
				else:
					sizeline = _("Size: ") + _("unavailable")

				if ((float(free) / 1024) / 1024) >= 1:
					freeline = _("Free: ") + str(round(((float(free) / 1024) / 1024), 2)) + _("TB")
				elif (free / 1024) >= 1:
					freeline = _("Free: ") + str(round((float(free) / 1024), 2)) + _("GB")
				elif free >= 1:
					freeline = _("Free: ") + str(free) + _("MB")
				else:
					freeline = _("Free: ") + _("full")
				self.list.append(mount + '\t' + sizeline + ' \t' + freeline)
			else:
				self.list.append(mount + '\t' + _('Not mounted'))

			list2.append(device)
		self.list = '\n'.join(self.list)
		self["hdd"].setText(self.list)
		self["devices"].setText(
			self["TunerHeader"].getText() + "\n\n" +
			self["nims"].getText() + "\n\n" +
			self["HDDHeader"].getText() + "\n\n" +
			self["hdd"].getText() + "\n\n"
			)

		self.Console.ePopen("df -mh | grep -v '^Filesystem'", self.Stage1Complete)

	def Stage1Complete(self, result, retval, extra_args=None):
		result = result.replace('\n                        ', ' ').split('\n')
		self.mountinfo = ""
		for line in result:
			self.parts = line.split()
			if line and self.parts[0] and (self.parts[0].startswith('192') or self.parts[0].startswith('//192')):
				line = line.split()
				try:
					ipaddress = line[0]
				except:
					ipaddress = ""
				try:
					mounttotal = line[1]
				except:
					mounttotal = ""
				try:
					mountfree = line[3]
				except:
					mountfree = ""
				if self.mountinfo:
					self.mountinfo += "\n"
				self.mountinfo += "%s (%sB, %sB %s)" % (ipaddress, mounttotal, mountfree, _("free"))

		if self.mountinfo:
			self["mounts"].setText(self.mountinfo)
		else:
			self["mounts"].setText(_('none'))

		self["devices"].setText(
			self["devices"].getText() +
			self["MountsHeader"].getText() + "\n\n" +
			self["mounts"].getText()
			)
		self["actions"].setEnabled(True)

	def createSummary(self):
		return AboutSummary

class SystemMemoryInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Memory Information"))
		self.skinName = ["SystemMemoryInfo", "About"]
		self["lab1"] = StaticText(_("OpenDroid"))
		self["lab2"] = StaticText(_("By OPD Image Team"))
		self["AboutScrollLabel"] = ScrollLabel()

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
			})

		out_lines = file("/proc/meminfo").readlines()
		self.AboutText = _("RAM") + '\n\n'
		RamTotal = "-"
		RamFree = "-"
		for lidx in range(len(out_lines) - 1):
			tstLine = out_lines[lidx].split()
			if "MemTotal:" in tstLine:
				MemTotal = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Total Memory:")) + "\t" + MemTotal[1] + "\n"
			if "MemFree:" in tstLine:
				MemFree = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Free Memory:")) + "\t" + MemFree[1] + "\n"
			if "Buffers:" in tstLine:
				Buffers = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Buffers:")) + "\t" + Buffers[1] + "\n"
			if "Cached:" in tstLine:
				Cached = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Cached:")) + "\t" + Cached[1] + "\n"
			if "SwapTotal:" in tstLine:
				SwapTotal = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Total Swap:")) + "\t" + SwapTotal[1] + "\n"
			if "SwapFree:" in tstLine:
				SwapFree = out_lines[lidx].split()
				self.AboutText += '{:<35}'.format(_("Free Swap:")) + "\t" + SwapFree[1] + "\n\n"

		self["actions"].setEnabled(False)
		self.Console = Console()
		self.Console.ePopen("df -mh / | grep -v '^Filesystem'", self.Stage1Complete)

	def MySize(self, RamText):
		RamText_End = RamText[len(RamText)-1]
		RamText_End2 = RamText_End
		if RamText_End == "G":
			RamText_End = _("GB")
		elif RamText_End == "M":
			RamText_End = _("MB")
		elif RamText_End == "K":
			RamText_End = _("KB")
		if RamText_End != RamText_End2:
			RamText = RamText[0:len(RamText)-1] + " " + RamText_End
		return RamText
	def Stage1Complete(self, result, retval, extra_args=None):
		flash = str(result).replace('\n', '')
		flash = flash.split()
		RamTotal = self.MySize(flash[1])
		RamFree = self.MySize(flash[3])

		self.AboutText += _("FLASH") + '\n\n'
		self.AboutText += _("Total:") + "\t" + RamTotal + "\n"
		self.AboutText += _("Free:") + "\t" + RamFree + "\n\n"

		self["AboutScrollLabel"].setText(self.AboutText)
		self["actions"].setEnabled(True)

	def createSummary(self):
		return AboutSummary

class SystemNetworkInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Network Information"))
		self.skinName = ["SystemNetworkInfo", "WlanStatus"]
		self["LabelBSSID"] = StaticText()
		self["LabelESSID"] = StaticText()
		self["LabelQuality"] = StaticText()
		self["LabelSignal"] = StaticText()
		self["LabelBitrate"] = StaticText()
		self["LabelEnc"] = StaticText()
		self["BSSID"] = StaticText()
		self["ESSID"] = StaticText()
		self["quality"] = StaticText()
		self["signal"] = StaticText()
		self["bitrate"] = StaticText()
		self["enc"] = StaticText()

		self["IFtext"] = StaticText()
		self["IF"] = StaticText()
		self["Statustext"] = StaticText()
		self["statuspic"] = MultiPixmap()
		self["statuspic"].setPixmapNum(1)
		self["statuspic"].show()

		self.iface = None
		self.createscreen()
		self.iStatus = None

		if iNetwork.isWirelessInterface(self.iface):
			try:
				from Plugins.SystemPlugins.WirelessLan.Wlan import iStatus
				self.iStatus = iStatus
			except:
				pass
			self.resetList()
			self.onClose.append(self.cleanup)
		self.updateStatusbar()

		self["key_red"] = StaticText(_("Close"))

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

	def createscreen(self):
		def netspeed():
			netspeed=""
			for line in popen('ethtool eth0 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)
		def netspeed_eth1():
			netspeed=""
			for line in popen('ethtool eth1 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)
		self.AboutText = ""
		self.iface = "eth0"
		eth0 = about.getIfConfig('eth0')
		if eth0.has_key('addr'):
			if eth0.has_key('ifname'):
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + eth0['ifname'] + "\n"
			self.AboutText += '{:<35}'.format(_("IP:")) + "\t" + eth0['addr'] + "\n"
			if eth0.has_key('netmask'):
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + eth0['netmask'] + "\n"
			if eth0.has_key('hwaddr'):
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + eth0['hwaddr'] + "\n"
			self.AboutText += '{:<35}'.format(_("Network Speed:")) + "\t" + netspeed() + "\n"
			self.iface = 'eth0'

		eth1 = about.getIfConfig('eth1')
		if eth1.has_key('addr'):
			if eth1.has_key('ifname'):
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + eth1['ifname'] + "\n"
			self.AboutText += '{:<35}'.format(_("IP:")) + "\t" + eth1['addr'] + "\n"
			if eth1.has_key('netmask'):
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + eth1['netmask'] + "\n"
			if eth1.has_key('hwaddr'):
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + eth1['hwaddr'] + "\n"
			self.AboutText += '{:<35}'.format(_("Network Speed:")) + "\t" + netspeed_eth1() + "\n"
			self.iface = 'eth1'

		ra0 = about.getIfConfig('ra0')
		if ra0.has_key('addr'):
			if ra0.has_key('ifname'):
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + ra0['ifname'] + "\n"
			self.AboutText += '{:<35}'.format(_("IP:")) + "\t" + ra0['addr'] + "\n"
			if ra0.has_key('netmask'):
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + ra0['netmask'] + "\n"
			if ra0.has_key('hwaddr'):
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + ra0['hwaddr'] + "\n"
			self.iface = 'ra0'

		wlan0 = about.getIfConfig('wlan0')
		if wlan0.has_key('addr'):
			if wlan0.has_key('ifname'):
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + wlan0['ifname'] + "\n"
			self.AboutText += '{:<35}'.format(_("IP:")) + "\t" + wlan0['addr'] + "\n"
			if wlan0.has_key('netmask'):
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + wlan0['netmask'] + "\n"
			if wlan0.has_key('hwaddr'):
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + wlan0['hwaddr'] + "\n"
			self.iface = 'wlan0'

		wlan1 = about.getIfConfig('wlan1')
		if wlan1.has_key('addr'):
			if wlan1.has_key('ifname'):
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + wlan1['ifname'] + "\n"
			self.AboutText += '{:<35}'.format(_("IP:")) + "\t" + wlan1['addr'] + "\n"
			if wlan1.has_key('netmask'):
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + wlan1['netmask'] + "\n"
			if wlan1.has_key('hwaddr'):
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + wlan1['hwaddr'] + "\n"
			self.iface = 'wlan1'

		rx_bytes, tx_bytes = about.getIfTransferredData(self.iface)
		self.AboutText += "\n" + '{:<35}'.format(_("Bytes received:")) + "\t" + rx_bytes + "\n"
		self.AboutText += '{:<35}'.format(_("Bytes sent:")) + "\t" + tx_bytes + "\n"

		hostname = file('/proc/sys/kernel/hostname').read()
		self.AboutText += "\n" + '{:<35}'.format(_("Hostname:")) + "\t" + hostname + "\n"
		self["AboutScrollLabel"] = ScrollLabel(self.AboutText)

	def cleanup(self):
		if self.iStatus:
			self.iStatus.stopWlanConsole()

	def resetList(self):
		if self.iStatus:
			self.iStatus.getDataForInterface(self.iface, self.getInfoCB)

	def getInfoCB(self, data, status):
		self.LinkState = None
		if data is not None:
			if data is True:
				if status is not None:
					if self.iface == 'wlan0' or self.iface == 'wlan1' or self.iface == 'ra0':
						if status[self.iface]["essid"] == "off":
							essid = _("No Connection")
						else:
							essid = str(status[self.iface]["essid"])
						if status[self.iface]["accesspoint"] == "Not-Associated":
							accesspoint = _("Not-Associated")
							essid = _("No Connection")
						else:
							accesspoint = str(status[self.iface]["accesspoint"])
						if self.has_key("BSSID"):
							self.AboutText += _('Accesspoint:') + '\t' + accesspoint + '\n'
						if self.has_key("ESSID"):
							self.AboutText += _('SSID:') + '\t' + essid + '\n'

						quality = str(status[self.iface]["quality"])
						if self.has_key("quality"):
							self.AboutText += _('Link Quality:') + '\t' + quality + '\n'

						if status[self.iface]["bitrate"] == '0':
							bitrate = _("Unsupported")
						else:
							bitrate = str(status[self.iface]["bitrate"]) + " Mb/s"
						if self.has_key("bitrate"):
							self.AboutText += _('Bitrate:') + '\t' + bitrate + '\n'

						signal = str(status[self.iface]["signal"])
						if self.has_key("signal"):
							self.AboutText += _('Signal Strength:') + '\t' + signal + '\n'

						if status[self.iface]["encryption"] == "off":
							if accesspoint == "Not-Associated":
								encryption = _("Disabled")
							else:
								encryption = _("Unsupported")
						else:
							encryption = _("Enabled")
						if self.has_key("enc"):
							self.AboutText += _('Encryption:') + '\t' + encryption + '\n'

						if status[self.iface]["essid"] == "off" or status[self.iface]["accesspoint"] == "Not-Associated" or status[self.iface]["accesspoint"] is False:
							self.LinkState = False
							self["statuspic"].setPixmapNum(1)
							self["statuspic"].show()
						else:
							self.LinkState = True
							iNetwork.checkNetworkState(self.checkNetworkCB)
						self["AboutScrollLabel"].setText(self.AboutText)

	def exit(self):
		self.close(True)

	def updateStatusbar(self):
		self["IFtext"].setText(_("Network:"))
		self["IF"].setText(iNetwork.getFriendlyAdapterName(self.iface))
		self["Statustext"].setText(_("Link:"))
		if iNetwork.isWirelessInterface(self.iface):
			try:
				self.iStatus.getDataForInterface(self.iface, self.getInfoCB)
			except:
				self["statuspic"].setPixmapNum(1)
				self["statuspic"].show()
		else:
			iNetwork.getLinkState(self.iface, self.dataAvail)

	def dataAvail(self, data):
		self.LinkState = None
		for line in data.splitlines():
			line = line.strip()
			if 'Link detected:' in line:
				if "yes" in line:
					self.LinkState = True
				else:
					self.LinkState = False
		if self.LinkState:
			iNetwork.checkNetworkState(self.checkNetworkCB)
		else:
			self["statuspic"].setPixmapNum(1)
			self["statuspic"].show()

	def checkNetworkCB(self, data):
		try:
			if iNetwork.getAdapterAttribute(self.iface, "up") is True:
				if self.LinkState is True:
					if data <= 2:
						self["statuspic"].setPixmapNum(0)
					else:
						self["statuspic"].setPixmapNum(1)
					self["statuspic"].show()
				else:
					self["statuspic"].setPixmapNum(1)
					self["statuspic"].show()
			else:
				self["statuspic"].setPixmapNum(1)
				self["statuspic"].show()
		except:
			pass

	def createSummary(self):
		return AboutSummary

class AboutSummary(Screen):
	def __init__(self, session, parent):
		Screen.__init__(self, session, parent = parent)
		self["selected"] = StaticText("OPD:" + getImageVersion())

		AboutText = _("Model: %s %s\n") % (getMachineBrand(), getMachineName())

		if path.exists('/proc/stb/info/chipset'):
			chipset = open('/proc/stb/info/chipset', 'r').read()
			AboutText += _("Chipset: BCM%s") % chipset.replace('\n','') + "\n"

		AboutText += _("Version: %s") % getImageVersion() + "\n"
		AboutText += _("Build: %s") % getImageVersion() + "\n"
		AboutText += _("Kernel: %s") % about.getKernelVersionString() + "\n"

		string = getDriverDate()
		year = string[0:4]
		month = string[4:6]
		day = string[6:8]
		driversdate = '-'.join((year, month, day))
		AboutText += _("Drivers: %s") % driversdate + "\n"
		AboutText += _("Last update: %s") % getEnigmaVersionString()

		tempinfo = ""
		if path.exists('/proc/stb/sensors/temp0/value'):
			tempinfo = open('/proc/stb/sensors/temp0/value', 'r').read()
		elif path.exists('/proc/stb/fp/temp_sensor'):
			tempinfo = open('/proc/stb/fp/temp_sensor', 'r').read()
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			mark = str('\xc2\xb0')
			AboutText += _("Temperature: %s") % tempinfo.replace('\n', '') + mark + "C"

		self["AboutText"] = StaticText(AboutText)

class ViewGitLog(Screen):
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.skinName = "SoftwareUpdateChanges"
		self.setTitle(_("OE Changes"))
		self.logtype = 'oe'
		self["text"] = ScrollLabel()
		self['title_summary'] = StaticText()
		self['text_summary'] = StaticText()
		self["key_red"] = Button(_("Close"))
		self["key_green"] = Button(_("OK"))
		self["key_yellow"] = Button(_("Show E2 Log"))
		self["myactions"] = ActionMap(['ColorActions', 'OkCancelActions', 'DirectionActions'],
		{
			'cancel': self.closeRecursive,
			'green': self.closeRecursive,
			"red": self.closeRecursive,
			"yellow": self.changelogtype,
			"left": self.pageUp,
			"right": self.pageDown,
			"down": self.pageDown,
			"up": self.pageUp
		},-1)
		self.onLayoutFinish.append(self.getlog)

	def changelogtype(self):
		if self.logtype == 'e2':
			self["key_yellow"].setText(_("Show E2 Log"))
			self.setTitle(_("OE Changes"))
			self.logtype = 'oe'
		else:
			self["key_yellow"].setText(_("Show OE Log"))
			self.setTitle(_("Enigma2 Changes"))
			self.logtype = 'e2'
		self.getlog()

	def pageUp(self):
		self["text"].pageUp()

	def pageDown(self):
		self["text"].pageDown()

	def getlog(self):
		try:
			fd = open('/etc/' + self.logtype + '-git.log', 'r')
			releasenotes = fd.read()
			fd.close()
			releasenotes = releasenotes.replace('\nOpendroid: build', "\n\nOpendroid: build")
			self["text"].setText(releasenotes)
			summarytext = releasenotes
		except:
			print "there is a problem with reading log file"
		try:
			if self.logtype == 'e2':
				self['title_summary'].setText(_("E2 Log"))
				self['text_summary'].setText(_("Enigma2 Changes"))
			else:
				self['title_summary'].setText(_("OE Log"))
				self['text_summary'].setText(_("OE Changes"))
		except:
			self['title_summary'].setText("")
			self['text_summary'].setText("")

	def unattendedupdate(self):
		self.close((_("Unattended upgrade without GUI and reboot system"), "cold"))

	def closeRecursive(self):
		self.close((_("Cancel"), ""))

class TranslationInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Translation Information"))
		info = _("TRANSLATOR_INFO")
		if info == "TRANSLATOR_INFO":
			info = "(N/A)"

		infolines = _("").split("\n")
		infomap = {}
		for x in infolines:
			l = x.split(': ')
			if len(l) != 2:
				continue
			(type, value) = l
			infomap[type] = value
		self["actions"] = ActionMap(["SetupActions"],{"cancel": self.close,"ok": self.close})

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")
		self["TranslatorName"] = StaticText(translator_name)
		linfo= ""
		linfo += _("Translations Info")		+ ":" + "\n\n"
		linfo += _("Project")				+ ":" + infomap.get("Project-Id-Version", "") + "\n"
		linfo += _("Language")				+ ":" + infomap.get("Language", "") + "\n"
		print infomap.get("Language-Team", "")
		if infomap.get("Language-Team", "") == "" or infomap.get("Language-Team", "") == "none":
			linfo += _("Language Team") 	+ ":" + "n/a"  + "\n"
		else:
			linfo += _("Language Team") 	+ ":" + infomap.get("Language-Team", "")  + "\n"
		linfo += _("Last Translator") 		+ ":" + translator_name + "\n"
		linfo += "\n"
		linfo += _("Source Charset")		+ ":" + infomap.get("X-Poedit-SourceCharset", "") + "\n"
		linfo += _("Content Type")			+ ":" + infomap.get("Content-Type", "") + "\n"
		linfo += _("Content Encoding")		+ ":" + infomap.get("Content-Transfer-Encoding", "") + "\n"
		linfo += _("MIME Version")			+ ":" + infomap.get("MIME-Version", "") + "\n"
		linfo += "\n"
		linfo += _("POT-Creation Date")		+ ":" + infomap.get("POT-Creation-Date", "") + "\n"
		linfo += _("Revision Date")			+ ":" + infomap.get("PO-Revision-Date", "") + "\n"
		linfo += "\n"
		linfo += _("Generator")				+ ":" + infomap.get("X-Generator", "") + "\n"

		if infomap.get("Report-Msgid-Bugs-To", "") != "":
			linfo += _("Report Msgid Bugs To")	+ ":" + infomap.get("Report-Msgid-Bugs-To", "") + "\n"
		else:
			linfo += _("Report Msgid Bugs To")	+ ":" + "opendroid2013@gmail.com" + "\n"
		self["AboutScrollLabel"] = ScrollLabel(linfo)


class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Latest Commits"))
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))
		self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
				"left": self.left,
				"right": self.right,
				"deleteBackward": self.left,
				"deleteForward": self.right
			})

		self["key_red"] = Button(_("Cancel"))

		self.project = 0
		self.projects = [
			("opendroid-Team",      "enigma2",               "opendroid-Team Enigma2",             "6.8", "github"),
                        ("formiano",      "E2",               "formiano E2",             "6.8", "github"),
			("opendroid-Team",      "OPD-Blue-Line",             "opendroid-Team Skin OPD-Blue-Line",   "master", "github"),
			("oe-alliance",   "oe-alliance-core",     "OE Alliance Core",             "4.3", "github"),
			("oe-alliance",   "oe-alliance-plugins",  "OE Alliance Plugins",          "master", "github"),
			("oe-alliance",   "enigma2-plugins",      "OE Alliance Enigma2 Plugins",  "master", "github")
		]
		self.cachedProjects = {}
		self.Timer = eTimer()
		self.Timer.callback.append(self.readGithubCommitLogs)
		self.Timer.start(50, True)

	def readGithubCommitLogs(self):
		if self.projects[self.project][4] == "github":
			url = 'https://api.github.com/repos/%s/%s/commits?sha=%s' % (self.projects[self.project][0], self.projects[self.project][1], self.projects[self.project][3])
		if self.projects[self.project][4] == "gitlab":
			url1 = 'https://gitlab.com/api/v4/projects/%s' % (self.projects[self.project][0])
			url2 = '%2F'
			url3 = '%s/repository/commits?ref_name=%s' % (self.projects[self.project][1], self.projects[self.project][3])
			url = url1 + url2 + url3
		commitlog = ""
		from datetime import datetime
		from json import loads
		from urllib2 import urlopen
		if self.projects[self.project][4] == "github":
			try:
				commitlog += 80 * '-' + '\n'
				commitlog += self.projects[self.project][2] + ' - ' + self.projects[self.project][1] + ' - branch ' + self.projects[self.project][3] + '\n'
				commitlog += 'URL: https://github.com/' + self.projects[self.project][0] + '/' + self.projects[self.project][1] + '/tree/' + self.projects[self.project][3] + '\n'
				commitlog += 80 * '-' + '\n'
				for c in loads(urlopen(url, timeout=5).read()):
					creator = c['commit']['author']['name']
					title = c['commit']['message']
					date = datetime.strptime(c['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%x %X')
					if title.startswith ("Merge "):
						pass
					else:
						commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
				commitlog = commitlog.encode('utf-8')
				self.cachedProjects[self.projects[self.project][2]] = commitlog
			except:
				commitlog += _("Currently the commit log cannot be retrieved - please try later again")
		if self.projects[self.project][4] == "gitlab":
			try:
				commitlog += 80 * '-' + '\n'
				commitlog += self.projects[self.project][2] + ' - ' + self.projects[self.project][1] + ' - branch ' + self.projects[self.project][3] + '\n'
				commitlog += 'URL: https://gitlab.com/' + self.projects[self.project][0] + '/' + self.projects[self.project][1] + '/tree/' + self.projects[self.project][3] + '\n'
				commitlog += 80 * '-' + '\n'
				for c in loads(urlopen(url, timeout=5).read()):
					creator = c['author_name']
					title = c['message']
					date = datetime.strptime(c['committed_date'], '%Y-%m-%dT%H:%M:%S.000+02:00').strftime('%x %X')
					if title.startswith ("Merge "):
						pass
					else:
						commitlog += date + ' ' + creator + '\n' + title + '\n'
				commitlog = commitlog.encode('utf-8')
				self.cachedProjects[self.projects[self.project][2]] = commitlog
			except:
				commitlog += _("Currently the commit log cannot be retrieved - please try later again")
		self["AboutScrollLabel"].setText(commitlog)

	def updateCommitLogs(self):
		if self.projects[self.project][2] in self.cachedProjects:
			self["AboutScrollLabel"].setText(self.cachedProjects[self.projects[self.project][2]])
		else:
			self["AboutScrollLabel"].setText(_("Please wait"))
			self.Timer.start(50, True)

	def left(self):
		self.project = self.project == 0 and len(self.projects) - 1 or self.project - 1
		self.updateCommitLogs()

	def right(self):
		self.project = self.project != len(self.projects) - 1 and self.project + 1 or 0
		self.updateCommitLogs()

class ContactInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self["actions"] = ActionMap(["SetupActions"],{"cancel": self.close,"ok": self.close})
		self.setTitle(_("Contact info"))
		self["manufacturerinfo"] = StaticText(self.getManufacturerinfo())

	def getManufacturerinfo(self):
		minfo = "Opendroid Team\n"
		minfo += "https://droidsat.org/forum\n"
		return minfo
class MemoryInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"ok": self.getMemoryInfo,
				"green": self.getMemoryInfo,
				"blue": self.clearMemory,
			})
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Refresh"))
		self["key_blue"] = Label(_("Clear"))
		self['lmemtext'] = Label()
		self['lmemvalue'] = Label()
		self['rmemtext'] = Label()
		self['rmemvalue'] = Label()
		self['pfree'] = Label()
		self['pused'] = Label()
		self["slide"] = ProgressBar()
		self["slide"].setValue(100)
		self["params"] = MemoryInfoSkinParams()

		self['info'] = Label(_("This info is for developers only.\nFor a normal users it is not relevant.\nDon't panic please when you see values being displayed that you think look suspicious!"))

		Typ = _("%s  ") % (getMachineName())
		self.setTitle(Typ + "[" + (_("Memory Info"))+ "]")
		self.onLayoutFinish.append(self.getMemoryInfo)

	def getMemoryInfo(self):
		try:
			ltext = rtext = ""
			lvalue = rvalue = ""
			mem = 1
			free = 0
			rows_in_column = self["params"].rows_in_column
			for i, line in enumerate(open('/proc/meminfo','r')):
				s = line.strip().split(None, 2)
				if len(s) == 3:
					name, size, units = s
				elif len(s) == 2:
					name, size = s
					units = ""
				else:
					continue
				if name.startswith("MemTotal"):
					mem = int(size)
				if name.startswith("MemFree") or name.startswith("Buffers") or name.startswith("Cached"):
					free += int(size)
				if i < rows_in_column:
					ltext += "".join((name,"\n"))
					lvalue += "".join((size," ",units,"\n"))
				else:
					rtext += "".join((name,"\n"))
					rvalue += "".join((size," ",units,"\n"))
			self['lmemtext'].setText(ltext)
			self['lmemvalue'].setText(lvalue)
			self['rmemtext'].setText(rtext)
			self['rmemvalue'].setText(rvalue)
			self["slide"].setValue(int(100.0*(mem-free)/mem+0.25))
			self['pfree'].setText("%.1f %s" % (100.*free/mem,'%'))
			self['pused'].setText("%.1f %s" % (100.*(mem-free)/mem,'%'))
		except Exception, e:
			print "[About] getMemoryInfo FAIL:", e

	def clearMemory(self):
		eConsoleAppContainer().execute("sync")
		open("/proc/sys/vm/drop_caches", "w").write("3")
		self.getMemoryInfo()

class MemoryInfoSkinParams(HTMLComponent, GUIComponent):
	def __init__(self):
		GUIComponent.__init__(self)
		self.rows_in_column = 25

	def applySkin(self, desktop, screen):
		if self.skinAttributes is not None:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "rowsincolumn":
					self.rows_in_column = int(value)
			self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, screen)

	GUI_WIDGET = eLabel
