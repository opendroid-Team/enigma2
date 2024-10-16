from Screens.Screen import Screen
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
from boxbranding import getBoxType, getMachineBuild, getMachineBrand, getMachineName, getImageVersion, getImageBuild, getDriverDate, getOEVersion, getImageType, getBrandOEM
from Components.SystemInfo import BoxInfo, getBoxDisplayName, getDemodVersion
from skin import isOPDSkin
from Components.Pixmap import MultiPixmap
from Components.Network import iNetwork
from Components.Button import Button
from Components.Label import Label
from Components.ProgressBar import ProgressBar
import re
from Tools.StbHardware import getFPVersion
from Tools.MultiBoot import MultiBoot
from enigma import eConsoleAppContainer, eDVBResourceManager, eGetEnigmaDebugLvl, eStreamServer, eTimer, getDesktop, getE2Rev, ePicLoad, getDesktop, eSize, eLabel
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from Components.AVSwitch import AVSwitch
from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
import skin, os
import time
from os import path, popen, system
from re import search
from datetime import datetime
from locale import format_string
import six

MODULE_NAME = __name__.split(".")[-1]

DISPLAY_BRAND = BoxInfo.getItem("displaybrand")
DISPLAY_MODEL = BoxInfo.getItem("displaymodel")
MACHINE_BUILD = BoxInfo.getItem("machinebuild")
MODEL = BoxInfo.getItem("model")

API_GITHUB = 0
API_GITLAB = 1

SIGN = u"\u00B0"


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
		print("[ERROR] failed to open file %s" % filename)
	return ret


def parseLines(filename):
	ret = ["N/A"]
	try:
		f = open(filename, "rb")
		ret = f.readlines()
		f.close()
	except IOError:
		print("[ERROR] failed to open file %s" % filename)
	return ret


def convertDate(StringDate):
	## StringDate must be a string "YYYY-MM-DD" or "YYYYMMDD" / or integer YYYYMMDD
	try:
		if type(StringDate) == int:
			StringDate = str(StringDate)
		if len(StringDate) == 8:
			year = StringDate[0:4]
			month = StringDate[4:6]
			day = StringDate[6:8]
			StringDate = ' '.join((year, month, day))
		else:
			StringDate = StringDate.replace("-", " ")
		StringDate = strftime(config.usage.date.full.value, strptime(StringDate, "%Y %m %d"))
		return StringDate
	except:
		return _("Unknown")
def read_startup(FILE):
	file = FILE
	try:
		with open(file, 'r') as myfile:
			data=myfile.read().replace('\n', '')
		myfile.close()
	except IOError:
		print("[ERROR] failed to open file %s" % file)
		data = " "
	return data

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Image Information"))
		self.skinName = ["AboutOE", "About"]
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
			for line in popen('ethtool eth0 |grep Speed', 'r'):
				line = line.strip().split(":")
				line =line[1].replace(' ', '')
				netspeed += line
				return str(netspeed)
		def netspeed_eth1():
			netspeed=""
			for line in popen('ethtool eth1 |grep Speed', 'r'):
				line = line.strip().split(":")
				line =line[1].replace(' ', '')
				netspeed += line
				return str(netspeed)
		def netspeed_ra0():
			netspeed=""
			for line in popen('iwconfig ra0 | grep Bit | cut -c 75-85', 'r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def netspeed_wlan0():
			netspeed=""
			for line in popen('iwconfig wlan0 | grep Bit | cut -c 75-85', 'r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def netspeed_wlan1():
			netspeed=""
			for line in popen('iwconfig wlan1 | grep Bit | cut -c 75-85', 'r'):
				line = line.strip()
				netspeed += line
				return str(netspeed)
		def freeflash():
			freeflash=""
			for line in popen("df -mh / | grep -v '^Filesystem' | awk '{print $4}'", 'r'):
				line = line.strip()
				freeflash += line
				return str(freeflash)
		self["lab1"] = StaticText(_("OpenDroid by OPD Image Team"))
		self["lab2"] = StaticText(_("Support at") + " https://droidsat.org")
		model = None
		AboutText = ""
		self["lab2"] = StaticText(_("Support:") + " https://droidsat.org")
		AboutText += _("Model:\t%s %s\n") % (getMachineBrand(), getMachineName())

		if path.exists('/proc/stb/info/chipset'):
			if BoxInfo.getItem("HasHiSi"):
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

		if getMachineBuild() in ('u41', 'u42', 'u43'):
			cpuMHz = _("   (1.0 GHz)")
		elif getMachineBuild() in ('vusolo4k', 'vuultimo4k', 'vuzero4k', 'gb72604'):
			cpuMHz = _("   (1.5 GHz)")
		elif getMachineBuild() in ('formuler1tc', 'formuler1', 'triplex', 'tiviaraplus'):
			cpuMHz = _("   (1.3 GHz)")
		elif getMachineBuild() in ('gbmv200', 'u51', 'u5', 'u53', 'u532', 'u533', 'u52', 'u54', 'u55', 'u56', 'u5pvr', 'cc1', 'sf8008', 'sf8008m', 'hd60', 'hd61', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'v8plus', 'multibox'):
			cpuMHz = _("   (1.6 GHz)")
		elif getMachineBuild() in ('vuuno4kse', 'vuuno4k', 'dm900', 'dm920', 'gb7252', 'dags7252','xc7439', '8100s'):
			cpuMHz = _("   (1.7 GHz)")
		elif getMachineBuild() in ('alien5', ):
			cpuMHz = _("   (2.0 GHz)")
		elif getMachineBuild() in ('vuduo4k', ):
			cpuMHz = _("   (2.1 GHz)")
		elif getMachineBuild() in ('sf5008', 'et13000', 'et1x000', 'hd52', 'hd51', 'sf4008', 'vs1500', 'osmio4k', 'osmio4kplus', 'osmini4k'):
			try:
				import binascii
				f = open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb')
				clockfrequency = f.read()
				f.close()
				cpuMHz = _("   (%s MHz)") % str(round(int(binascii.hexlify(clockfrequency), 16)/1000000, 1))
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
							cpuMHz = "   (" +  str(int(float(lisp[1].replace('\n', '')))) + " MHz)"
							break
				except:
					pass

		bogoMIPS = ""
		if res:
			cpuMHz = "" + res.replace("\n", "") + " MHz"
		if res2:
			bogoMIPS = "" + res2.replace("\n", "")

		if getMachineBuild() in ('vusolo4k', 'hd51', 'hd52', 'sf4008', 'dm900', 'gb7252'):
			AboutText += _("CPU:\t%s") % about.getCPUString() + cpuMHz + "\n"
		else:
			AboutText += _("CPU:\t%s") % about.getCPUString() + " " + cpuMHz + "\n"
		dMIPS = 0
		if getMachineBuild() in ('vusolo4k', 'vuultimo4k'):
			dMIPS = "10.500"
		elif getMachineBuild() in ('hd52', 'hd51', 'sf4008', 'dm900', 'gb7252'):
			dMIPS = "12.000"
		if getMachineBuild() in ('vusolo4k', 'hd51', 'hd52', 'sf4008', 'dm900', 'gb7252'):
			AboutText += _("DMIPS:\t") + dMIPS + "\n"
		else:
			AboutText += _("BogoMIPS:\t%s") % bogoMIPS + "\n"
		AboutText += _("Cores:\t%s") % about.getCpuCoresString() + "\n"
		AboutText += _("OPD Version:\tV%s") % getImageVersion() + " Build " + getImageBuild() + " based on " + getOEVersion() + "\n"
		AboutText += _("Kernel (Box):\t%s") % about.getKernelVersionString() + " (" + getBoxType() + ")" + "\n"
		imagestarted = ""
		bootname = ""
		if path.exists('/boot/bootname'):
			f = open('/boot/bootname', 'r')
			bootname = f.readline().split('=')[1]
			f.close()
		if BoxInfo.getItem("canMultiBoot"):
			slotCode, bootCode = MultiBoot.getCurrentSlotAndBootCodes()
			device = MultiBoot.getBootDevice()
			if BoxInfo.getItem("HasHiSi") and "sda" in device:
				slotCode = int(slotCode)
				image = slotCode - 4 if slotCode > 4 else slotCode - 1
				device = _("SDcard slot %s%s") % (image, "  -  %s" % device if device else "")
			else:
				if BoxInfo.getItem("HasKexecMultiboot"):
					device = MultiBoot.bootSlots[slotCode]["device"]
				if "mmcblk" in device:
					device = _("eMMC slot %s%s") % (slotCode, f"  -  {device}" if device else "")
				else:
					device = _("USB slot %s%s") % (slotCode, f"  -  {device}" if device else "")
			AboutText += _("Hardware MultiBoot device:\t%s") % _("STARTUP_") + str(slotCode) + "  " + device + "\n"

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
		AboutText += _("Python:\t%s") % about.getPythonVersionString() + "\n"
		AboutText += _("Glibc version:\t%s") % about.getGlibcVersion() + "\n"
		AboutText += _("GCC version:\t%s") % about.getGccVersion() + "\n"
		AboutText += _("OpenSSL:\t%s") % about.getopensslVersionString() + "\n"
		if path.exists('/boot/STARTUP'):
			AboutText += _("Flashed:\tMultiboot active\n")
		else:
			AboutText += _("Flashed:\t%s") % about.getFlashDateString() + "\n"
		AboutText += _("Free Flash:\t%s\n") % freeflash()
		AboutText += _("Flash type:\t%s") % about.getFlashType() + "\n"
		AboutText += _("Skin:\t%s (%s x %s)\n") % (config.skin.primary_skin.value.split('/')[0], getDesktop(0).size().width(), getDesktop(0).size().height())
		AboutText += _("Last update:\t%s") % about.getEnigmaVersionString() + " to Build #" + getImageBuild() + "\n"
		AboutText += _("E2 (re)starts:\t%s\n") % config.misc.startCounter.value
		AboutText += _("Enigma2 debug level:\t%s") % eGetEnigmaDebugLvl() + "\n"
		if getMachineBuild() not in ('vuduo4k','osmio4k','vuzero4k','sf5008','et13000','et1x000','hd51','hd52','vusolo4k','vuuno4k','vuuno4kse','vuultimo4k','sf4008','dm820','dm7080','dm900','dm920', 'gb7252', 'dags7252', 'vs1500','xc7439','8100s','u5','u5pvr','u52','u53','u54','u55','u56','u51','sf8008'):
			AboutText += _("Installed:\t%s") % about.getFlashDateString() + "\n"

		fp_version = getFPVersion()
		if fp_version is None:
			fp_version = ""
		elif fp_version != 0:
			fp_version = _("Frontprocessor version:\t%s") % fp_version
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
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			AboutText += _("System temperature:\t%s") % tempinfo.replace('\n', '').replace(' ', '') + SIGN + "C\n"

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
						if getMachineBuild() in ('u41', 'u42', 'u43'):
							tempinfo = str(int(tempinfo) - 15)
			except:
				tempinfo = ""
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			AboutText += ("Processor temperature:\t%s") % tempinfo.replace('\n', '').replace(' ', '') + SIGN + "C\n"
		AboutLcdText = AboutText.replace('\t', ' ')

		self["AboutScrollLabel"] = ScrollLabel(AboutText)
		self["key_yellow"] = Button(_("Memory Info"))
		self["key_info"] = StaticText(_("Contact Info"))
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
		if BoxInfo.getItem("HaveID"):
			try:
				f = open("/etc/.id")
				id = f.read()[:-1].split('=')
				f.close()
				from Screens.MessageBox import MessageBox
				self.session.open(MessageBox, id[1], type=MessageBox.TYPE_INFO)
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
		elif getBoxType() in ('sf8008m'):
			model = "sf8008m.png"
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
		elif getBoxType() in ('gbip4k'):
			model = "gbip4k.png"
		elif getBoxType() in ('gbx34k'):
			model = "gbx34k.png"
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
		elif getBoxType() in ('hitube4k'):
			model = "hitube4k.png"
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
		elif getBoxType() in ('osmio4kplus'):
			model = "osmio4kplus.png"
		elif getBoxType() in ('osmega'):
			model = "osmega.png"
		elif getBoxType() in ('osmini'):
			model = "osmini.png"
		elif getBoxType() in ('osminiplus'):
			model = "osminiplus.png"
		elif getBoxType() in ('osmini4k'):
			model = "osmini4k.png"
		elif getBoxType() in ('osnino'):
			model = "osnino.png"
		elif getBoxType() in ('osninoplus'):
			model = "osninoplus.png"
		elif getBoxType() in ('osninopro'):
			model = "osninopro.png"	
		elif getBoxType() in ('gbtrio4k'):
			model = "gbtrio4k.png"	
		elif getBoxType() in ('ustym4kpro'):
			model = "ustym4kpro.png"
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
		for count in list(range(len(nims))):
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
					sizeline = _("Size: ") + str(round(((float(size) / 1024) / 1024), 2)) + " " + _("TB")
				elif (size / 1024) >= 1:
					sizeline = _("Size: ") + str(round((float(size) / 1024), 2)) + " " + _("GB")
				elif size >= 1:
					sizeline = _("Size: ") + str(size) + " " + _("MB")
				else:
					sizeline = _("Size: ") + _("unavailable")

				if ((float(free) / 1024) / 1024) >= 1:
					freeline = _("Free: ") + str(round(((float(free) / 1024) / 1024), 2)) + " " + _("TB")
				elif (free / 1024) >= 1:
					freeline = _("Free: ") + str(round((float(free) / 1024), 2)) + " " + _("GB")
				elif free >= 1:
					freeline = _("Free: ") + str(free) + " " + _("MB")
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
		result = six.ensure_str(result)
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

		out_lines = open("/proc/meminfo").readlines()
		self.AboutText = _("RAM") + "\n\n"
		RamTotal = "-"
		RamFree = "-"
		for lidx in list(range(len(out_lines) - 1)):
			tstLine = out_lines[lidx].split()
			if "MemTotal:" in tstLine:
				MemTotal = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Total Memory:")) + "\t" + MemTotal[1] + "\n"
			if "MemFree:" in tstLine:
				MemFree = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Free Memory:")) + "\t" + MemFree[1] + "\n"
			if "Buffers:" in tstLine:
				Buffers = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Buffers:")) + "\t" + Buffers[1] + "\n"
			if "Cached:" in tstLine:
				Cached = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Cached:")) + "\t" + Cached[1] + "\n"
			if "SwapTotal:" in tstLine:
				SwapTotal = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Total Swap:")) + "\t" + SwapTotal[1] + "\n"
			if "SwapFree:" in tstLine:
				SwapFree = out_lines[lidx].split()
				self.AboutText += "{:<35}".format(_("Free Swap:")) + "\t" + SwapFree[1] + "\n\n"

		self["actions"].setEnabled(False)
		self.Console = Console()
		self.Console.ePopen("df -mh / | grep -v '^Filesystem'", self.Stage1Complete)

	def MySize(self, RamText):
		RamText_End = RamText[len(RamText) - 1]
		RamText_End2 = RamText_End
		if RamText_End == "G":
			RamText_End = _("GB")
		elif RamText_End == "M":
			RamText_End = _("MB")
		elif RamText_End == "K":
			RamText_End = _("KB")
		if RamText_End != RamText_End2:
			RamText = RamText[0:len(RamText) - 1] + " " + RamText_End
		return RamText

	def Stage1Complete(self, result, retval, extra_args=None):
		result = six.ensure_str(result)
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
		self["key_red"] = Label(_("Cancel"))
		self["actions"] = ActionMap(["SetupActions", "OkCancelActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.cancel,
				"red": self.cancel,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

	def createscreen(self):
		def netspeed():
			netspeed = ""
			for line in popen('ethtool eth0 |grep Speed', 'r'):
				line = line.strip().split(":")
				line = line[1].replace(' ', '')
				netspeed += line
			return str(netspeed)

		def netspeed_eth1():
			netspeed = ""
			for line in popen('ethtool eth1 |grep Speed', 'r'):
				line = line.strip().split(":")
				line = line[1].replace(' ', '')
				netspeed += line
			return str(netspeed)

		def nameserver():
			nameserver = ""
			v4 = 0
			v6 = 0
			ns4 = ""
			ns6 = ""
			datei = open("/etc/resolv.conf", "r")
			for line in datei.readlines():
				line = line.strip()
				if "nameserver" in line:
					if line.count(".") == 3:
						v4 = v4 + 1
						ns4 += str(v4) + ".IPv4 Nameserver" + ":" + line.strip().replace("nameserver ", "")
					if line.count(":") > 1 and line.count(":") < 8:
						v6 = v6 + 1
						ns6 += str(v6) + ".IPv6 Nameserver" + ":" + line.strip().replace("nameserver ", "")
			nameserver = ns4 + ns6
			datei.close()
			return nameserver.strip()

		def domain():
			domain = ""
			for line in open('/etc/resolv.conf', 'r'):
				line = line.strip()
				if "domain" in line:
					domain += line.strip().replace("domain ", "")
					return domain
				else:
					domain = _("no domain name found")
					return domain

		def gateway():
			gateway = ""
			for line in popen('ip route show'):
				line = line.strip()
				if "default via " in line:
					line = line.split(' ')
					line = line[2]
					return line
				else:
					line = _("no gateway found")
					return line
		self.AboutText = ""
		self.iface = "eth0"
		eth0 = about.getIfConfig('eth0')
		if 'addr' in eth0:
			if 'ifname' in eth0:
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + eth0['ifname'] + "\n"
			self.AboutText += '{:<45}'.format(_("IP:")) + "\t" + eth0['addr'] + "\n"
			self.AboutText += '{:<45}'.format(_("Gateway:")) + "\t" + gateway() + "\n"
			self.AboutText += '{:<45}'.format(_("Nameserver:")) + "\t" + nameserver() + "\n"
			if 'netmask' in eth0:
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + eth0['netmask'] + "\n"
			if 'hwaddr' in eth0:
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + eth0['hwaddr'] + "\n"
			self.AboutText += '{:<35}'.format(_("Network Speed:")) + "\t" + netspeed() + "\n"
			self.AboutText += '{:<35}'.format(_("Domain:")) + "\t" + domain() + "\n"
			self.iface = 'eth0'

		eth1 = about.getIfConfig('eth1')
		if 'addr' in eth1:
			if 'ifname' in eth1:
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + eth1['ifname'] + "\n"
			self.AboutText += '{:<45}'.format(_("IP:")) + "\t" + eth1['addr'] + "\n"
			self.AboutText += '{:<45}'.format(_("Gateway:")) + "\t" + gateway() + "\n"
			self.AboutText += '{:<45}'.format(_("Nameserver:")) + "\t" + nameserver() + "\n"
			if 'netmask' in eth1:
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + eth1['netmask'] + "\n"
			if 'hwaddr' in eth1:
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + eth1['hwaddr'] + "\n"
			self.AboutText += '{:<35}'.format(_("Network Speed:")) + "\t" + netspeed_eth1() + "\n"
			self.AboutText += '{:<35}'.format(_("Domain:")) + "\t" + domain() + "\n"
			self.iface = 'eth1'

		ra0 = about.getIfConfig('ra0')
		if 'addr' in ra0:
			if 'ifname' in ra0:
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + ra0['ifname'] + "\n"
			self.AboutText += '{:<45}'.format(_("IP:")) + "\t" + ra0['addr'] + "\n"
			self.AboutText += '{:<45}'.format(_("Gateway:")) + "\t" + gateway() + "\n"
			self.AboutText += '{:<45}'.format(_("Nameserver:")) + "\t" + nameserver() + "\n"
			if 'netmask' in ra0:
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + ra0['netmask'] + "\n"
			if 'hwaddr' in ra0:
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + ra0['hwaddr'] + "\n"
				self.AboutText += '{:<35}'.format(_("Domain:")) + "\t" + domain() + "\n"
			self.iface = 'ra0'

		wlan0 = about.getIfConfig('wlan0')
		if 'addr' in wlan0:
			if 'ifname' in wlan0:
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + wlan0['ifname'] + "\n"
			self.AboutText += '{:<45}'.format(_("IP:")) + "\t" + wlan0['addr'] + "\n"
			self.AboutText += '{:<45}'.format(_("Gateway:")) + "\t" + gateway() + "\n"
			self.AboutText += '{:<45}'.format(_("Nameserver:")) + "\t" + nameserver() + "\n"
			if 'netmask' in wlan0:
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + wlan0['netmask'] + "\n"
			if 'hwaddr' in wlan0:
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + wlan0['hwaddr'] + "\n"
				self.AboutText += '{:<35}'.format(_("Domain:")) + "\t" + domain() + "\n"
			self.iface = 'wlan0'

		wlan1 = about.getIfConfig('wlan1')
		if 'addr' in wlan1:
			if 'ifname' in wlan1:
				self.AboutText += '{:<35}'.format(_('Interface:')) + "\t" + " /dev/" + wlan1['ifname'] + "\n"
			self.AboutText += '{:<45}'.format(_("IP:")) + "\t" + wlan1['addr'] + "\n"
			self.AboutText += '{:<45}'.format(_("Gateway:")) + "\t" + gateway() + "\n"
			self.AboutText += '{:<45}'.format(_("Nameserver:")) + "\t" + nameserver() + "\n"
			if 'netmask' in wlan1:
				self.AboutText += '{:<35}'.format(_("Netmask:")) + "\t" + wlan1['netmask'] + "\n"
			if 'hwaddr' in wlan1:
				self.AboutText += '{:<35}'.format(_("MAC:")) + "\t" + wlan1['hwaddr'] + "\n"
				self.AboutText += '{:<35}'.format(_("Domain:")) + "\t" + domain() + "\n"
			self.iface = 'wlan1'
		rx_bytes, tx_bytes = about.getIfTransferredData(self.iface)
		self.AboutText += "\n" + '{:<35}'.format(_("Bytes received:")) + "\t" + rx_bytes + "\n"
		self.AboutText += '{:<35}'.format(_("Bytes sent:")) + "\t" + tx_bytes + "\n"
		hostname = open('/proc/sys/kernel/hostname').read()
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
						if "BSSID" in self:
							self.AboutText += '{:<35}'.format(_('Accesspoint:')) + '\t' + accesspoint + '\n'
						if "ESSID" in self:
							self.AboutText += '{:<35}'.format(_('SSID:')) + '\t' + essid + '\n'

						quality = str(status[self.iface]["quality"])
						if "quality" in self:
							self.AboutText += '{:<35}'.format(_('Link Quality:')) + '\t' + quality + '\n'
						channel = str(status[self.iface]["channel"])
						if "channel" in self:
							self.AboutText += '{:<35}'.format(_('Channel:')) + '\t' + channel + '\n'
						frequency = status[self.iface]["frequency"]
						if "frequency" in self:
							self.AboutText += '{:<35}'.format(_('Frequency:')) + '\t' + frequency + '\n'
						frequency_norm = status[self.iface]["frequency_norm"]
						if frequency_norm is not None:
							self.AboutText += '{:<35}'.format(_('Frequency Norm:')) + '\t' + frequency_norm + '\n'

						if status[self.iface]["bitrate"] == '0':
							bitrate = _("Unsupported")
						else:
							bitrate = str(status[self.iface]["bitrate"])
						if "bitrate" in self:
							self.AboutText += '{:<35}'.format(_('Bitrate:')) + '\t' + bitrate + '\n'

						signal = str(status[self.iface]["signal"]) + " dBm"
						if "signal" in self:
							self.AboutText += '{:<35}'.format(_('Signal Strength:')) + '\t' + signal + '\n'
						if status[self.iface]["encryption"] == "off":
							if accesspoint == "Not-Associated":
								encryption = _("Disabled")
							else:
								encryption = _("Unsupported")
						else:
							encryption = _("Enabled")
						if "enc" in self:
							self.AboutText += '{:<35}'.format(_('Encryption:')) + '\t' + encryption + '\n'
						encryption_type = status[self.iface]["encryption_type"]
						if "encryption_type" in self:
							self.AboutText += '{:<35}'.format(_('Encryption Type:')) + '\t' + encryption_type.upper() + '\n'
						if status[self.iface]["essid"] == "off" or status[self.iface]["accesspoint"] == "Not-Associated" or status[self.iface]["accesspoint"] is False:
							self.LinkState = False
							self["statuspic"].setPixmapNum(1)
							self["statuspic"].show()
						else:
							self.LinkState = True
							iNetwork.checkNetworkState(self.checkNetworkCB)
						self["AboutScrollLabel"].setText(self.AboutText)

	def cancel(self):
		self.close()

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
		data = six.ensure_str(data)
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
		AboutText += _("Last update: %s") % about.getEnigmaVersionString()

		tempinfo = ""
		if path.exists('/proc/stb/sensors/temp0/value'):
			tempinfo = open('/proc/stb/sensors/temp0/value', 'r').read()
		elif path.exists('/proc/stb/fp/temp_sensor'):
			tempinfo = open('/proc/stb/fp/temp_sensor', 'r').read()
		if tempinfo and int(tempinfo.replace('\n', '')) > 0:
			AboutText += _("System temperature:\t%s") % tempinfo.replace('\n', '').replace(' ', '') + SIGN + "C\n"

		self["AboutText"] = StaticText(AboutText)



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
		self["actions"] = ActionMap(["SetupActions"], {"cancel": self.close, "ok": self.close})

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")
		self["TranslatorName"] = StaticText(translator_name)
		linfo = ""
		linfo += _("Translations Info") + ":" + "\n\n"
		linfo += _("Project") + ":" + infomap.get("Project-Id-Version", "") + "\n"
		linfo += _("Language") + ":" + infomap.get("Language", "") + "\n"
		print(infomap.get("Language-Team", ""))
		if infomap.get("Language-Team", "") == "" or infomap.get("Language-Team", "") == "none":
			linfo += _("Language Team") + ":" + "n/a" + "\n"
		else:
			linfo += _("Language Team") + ":" + infomap.get("Language-Team", "") + "\n"
		linfo += _("Last Translator") + ":" + translator_name + "\n"
		linfo += "\n"
		linfo += _("Source Charset") + ":" + infomap.get("X-Poedit-SourceCharset", "") + "\n"
		linfo += _("Content Type") + ":" + infomap.get("Content-Type", "") + "\n"
		linfo += _("Content Encoding") + ":" + infomap.get("Content-Transfer-Encoding", "") + "\n"
		linfo += _("MIME Version") + ":" + infomap.get("MIME-Version", "") + "\n"
		linfo += "\n"
		linfo += _("POT-Creation Date") + ":" + infomap.get("POT-Creation-Date", "") + "\n"
		linfo += _("PO-Revision Date") + ":" + infomap.get("PO-Revision-Date", "") + "\n"
		linfo += "\n"
		linfo += _("X-Generator") + ":" + infomap.get("X-Generator", "") + "\n"

		if infomap.get("Report-Msgid-Bugs-To", "") != "":
			linfo += _("Report Msgid Bugs To") + ":" + infomap.get("Report-Msgid-Bugs-To", "") + "\n"
		else:
			linfo += _("Report Msgid Bugs To") + ":" + "opendroid2013@gmail.com" + "\n"
		self["AboutScrollLabel"] = ScrollLabel(linfo)


class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Latest Commits"))
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))
		self["HintText"] = Label(_("Press up/down to scroll through the selected log\n\nPress left/right to see different log types"))
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

		try:
			branch = "?sha=" + "-".join(about.getEnigmaVersionString().split("-")[3:])
		except:
			branch = ""
		branch_e2plugins = "?sha=python3"

		self.project = 0
		self.projects = [
			("https://api.github.com/repos/opendroid-Team/enigma2/commits" + branch, "7.3", API_GITHUB),
			("https://api.github.com/repos/oe-alliance/oe-alliance-core/commits" + branch, "5.5", API_GITHUB),
			("https://api.github.com/repos/oe-alliance/oe-alliance-plugins/commits" + branch, "master", API_GITHUB),
			("https://api.github.com/repos/oe-alliance/aio-grab/commits", "Aio Grab", API_GITHUB),
			("https://api.github.com/repos/openpli/enigma2-plugin-extensions-epgimport/commits", "Plugin EPGImport", API_GITHUB),
			("https://api.github.com/repos/formiano/GlamourAuraSky-skin/commits" + branch, "main", API_GITHUB),
			("https://api.github.com/repos/oe-alliance/OpenWebif/commits", "OpenWebif", API_GITHUB),
		]
		self.cachedProjects = {}
		self.Timer = eTimer()
		self.Timer.callback.append(self.readGithubCommitLogs)
		self.Timer.start(50, True)

	def readGithubCommitLogs(self):
		url = self.projects[self.project][0]
		commitlog = ""
		from datetime import datetime
		from json import loads
		from urllib.request import urlopen
		try:
			commitlog += 80 * '-' + '\n'
			commitlog += url.split('/')[-2] + '\n'
			commitlog += 80 * '-' + '\n'
			try:
				# OpenPli 5.0 uses python 2.7.11 and here we need to bypass the certificate check
				from ssl import _create_unverified_context
				log = loads(urlopen(url, timeout=5, context=_create_unverified_context()).read())
			except:
				log = loads(urlopen(url, timeout=5).read())

			if self.projects[self.project][2] == API_GITHUB:
				for c in log:
					creator = c['commit']['author']['name']
					title = c['commit']['message']
					date = datetime.strptime(c['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%x %X')
					commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
			elif self.projects[self.project][2] == API_GITLAB:
				for c in log:
					creator = c['author_name']
					title = c['title']
					date = datetime.strptime(c['committed_date'], '%Y-%m-%dT%H:%M:%S.000%z').strftime('%x %X')
					commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'

			self.cachedProjects[self.projects[self.project][1]] = commitlog
		except Exception as e:
			commitlog += _("Currently the commit log cannot be retrieved - please try later again.")
		self["AboutScrollLabel"].setText(commitlog)

	def updateCommitLogs(self):
		if self.projects[self.project][1] in self.cachedProjects:
			self["AboutScrollLabel"].setText(self.cachedProjects[self.projects[self.project][1]])
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
		self["actions"] = ActionMap(["SetupActions"], {"cancel": self.close,"ok": self.close})
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
			for i, line in enumerate(open('/proc/meminfo', 'r')):
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
					ltext += "".join((name, "\n"))
					lvalue += "".join((size, " ", units, "\n"))
				else:
					rtext += "".join((name, "\n"))
					rvalue += "".join((size, " ", units, "\n"))
			self['lmemtext'].setText(ltext)
			self['lmemvalue'].setText(lvalue)
			self['rmemtext'].setText(rtext)
			self['rmemvalue'].setText(rvalue)
			self["slide"].setValue(int(100.0 * (mem - free) / mem + 0.25))
			self['pfree'].setText("%.1f %s" % (100. * free / mem, '%'))
			self['pused'].setText("%.1f %s" % (100. * (mem - free) / mem, '%'))
		except Exception as e:
			print("[About] getMemoryInfo FAIL:", e)

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
