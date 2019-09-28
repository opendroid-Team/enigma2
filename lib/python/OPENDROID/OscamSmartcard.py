from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.Language import language
from Components.Pixmap import Pixmap
#from skin import parseColor
from enigma import ePicLoad
import gettext, base64, os, time, glob, urllib2
from os import environ, listdir, remove, rename, system, popen, mkdir
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from boxbranding import getBoxType, getImageDistro, getMachineName, getMachineBrand, getImageVersion, getMachineBuild, getImageArch
from datetime import datetime
plugin='[OscamSmartcard] '
dev_null = ' > /dev/null 2>&1'
null =' >/dev/null 2>&1'
def architectures():
	hardwaretype = popen('uname -m').read().strip()
	hostname = popen('uname -n').read().strip()
	kernelversion = popen('uname -r').read().strip()
	ossystem = popen('uname -s').read().strip()
	return ossystem,kernelversion,hardwaretype,hostname

arch = architectures()[2]
extrainfo=(architectures()[3])


config.OscamSmartcard = ConfigSubsection()
config.OscamSmartcard.systemclean = ConfigSelection(default = True, choices = [
				(True, ' ')
				])
config.OscamSmartcard.ConfigPath = ConfigSelection(default="/etc/tuxbox/config/oscam-smartcard/", choices = [
				("/etc/tuxbox/config/oscam-smartcard/", "/etc/tuxbox/config/oscam-smartcard/ (opendroid)"),
				("/etc/tuxbox/config/", "/etc/tuxbox/config/ (openMips)")
				])
config.OscamSmartcard.WebifPort = ConfigSelection(default="83", choices = [
				("81", _("81")),
				("82", _("82")),
				("83", _("83")),
				("8888", _("8888"))
				])
config.OscamSmartcard.oscambinary = ConfigSelection(default="no_binary_install", choices = [
				("no_binary_install", _("No")),
				("yes_binary_install", _("Yes"))
				])
config.OscamSmartcard.cccam  = ConfigSelection(default="no_cccam_import", choices = [
				("no_cccam_import", _("No")),
				("yes_cccam_import", _("Yes"))
				])
config.OscamSmartcard.emu  = ConfigSelection(default= False, choices = [
				(False, _("No")),
				(True, _("Yes"))
				])
config.OscamSmartcard.hasciplus  = ConfigSelection(default="no", choices = [
				("no", _("No")),
				("ciplusV13", _("CI+ V13")),
				("ciplusV14", _("CI+ V14"))
				])

cardlist = [
	("V13", "Sky V13"),
	("V13_fast", "Sky V13 Fastmode"),
	("V14", "Sky V14"),
	("V14_fast", "Sky V14 Fastmode"),
	("HD01", "HD+ HD01 white"),
	("HD02", "HD+ HD02 black"),
	("HD03", "HD+ HD03"),
	("HD04", "HD+ HD04"),
	("I02-Beta", "I02 Beta"),
	("I12-Beta", "I12 Beta"),
	("I12-Nagra", "I12 Nagra"),
	("V23", "KabelBW V23"),
	("ORF_ICE_crypto", "ORF ICE Cryptoworks 0D95"),
	("ORF_ICE_p410", "ORF p410 Cryptoworks 0D98"),
	("ORF_ICE_irdeto", "ORF ICE Irdeto 0648"),
	("ORF_ICE_irdeto650", "ORF ICE Irdeto 0650"),
	("SRG-V2", "SRG V2"),
	("SRG-V4", "SRG V4"),
	("SRG-V5", "SRG V5"),
	("SRG-V6", "SRG V6"),
	("UM01", "UnityMedia UM01"),
	("UM02", "UnityMedia UM02"),
	("UM03", "UnityMedia UM03"),
	("D01", "Kabel Deutschl. D01"),
	("D02", "Kabel Deutschl. D02"),
	("D09", "Kabel Deutschl. D09"),
	("KDG0x", "Kabel Deutschl. G02/G09"),
	("smartHD", "NC+ SmartHD+"),
	("MTV", "MTV"),
	("tivu", "Tivusat"),
	("JSC", "JSC-sports - Viaccess"),
	("RedlightHD", "Redlight Elite HD - Viaccess"),
	("default", "Standard 357/357 MHz"),
	("none", _("None"))
	]

config.OscamSmartcard.internalReader0 = ConfigSelection(default="none", choices = cardlist)
config.OscamSmartcard.internalReader1 = ConfigSelection(default="none", choices = cardlist)
config.OscamSmartcard.externalReader0 = ConfigSelection(default="none", choices = cardlist)
config.OscamSmartcard.externalReader1 = ConfigSelection(default="none", choices = cardlist)
class OscamSmartcard(ConfigListScreen, Screen):
	skin ="""
<screen name="OscamSmartcard" position="center,center" size="1280,720" flags="wfNoBorder" backgroundColor="#90000000">
  <eLabel name="bg" position="40,40" zPosition="-2" size="1200,640" backgroundColor="black" transparent="0" />
  <widget name="config" position="55,299" size="595,210" scrollbarMode="showOnDemand" transparent="1" backgroundColor="black" zPosition="1" />
  <widget name="Title" position="60,50" size="590,50" zPosition="1" font="Regular; 40" halign="left" backgroundColor="black" transparent="1" />
  <eLabel font="Regular; 20" zPosition="1" foregroundColor="black" halign="center" position="375,648" size="200,33" text="Cancel" transparent="1" backgroundColor="red" />
  <eLabel font="Regular; 20" zPosition="1" foregroundColor="white" halign="center" position="60,648" size="200,33" text="Start" transparent="1" backgroundColor="green" />
  <eLabel font="Regular; 20" zPosition="1" foregroundColor="black" halign="center" position="670,648" size="200,33" text="Info" transparent="1" backgroundColor="yellow" />
  <eLabel font="Regular; 20" zPosition="1" foregroundColor="white" halign="center" position="965,648" size="200,33" text="clean up" transparent="1" backgroundColor="blue" />
  <eLabel position="670,645" zPosition="0" size="200,33" backgroundColor="yellow" />
  <eLabel position="60,645" zPosition="0" size="200,33" backgroundColor="green" />
  <eLabel position="375,645" zPosition="0" size="200,33" backgroundColor="red" />
  <eLabel position="965,645" zPosition="0" size="200,33" backgroundColor="blue" />
  <widget name="oscamsmartcardhelperimage" position="671,209" size="330,300" zPosition="3" backgroundColor="black" transparent="1" />
  <widget name="HELPTEXT" position="670,518" size="544,110" zPosition="1" font="Regular; 20" halign="left" backgroundColor="black" transparent="1" />
  <widget name="HEADER" position="60,114" size="590,180" zPosition="1" font="Regular; 20" halign="left" backgroundColor="black" transparent="1" />
  <widget name="INFOTXT" position="60,518" size="590,110" zPosition="1" font="Regular; 20" halign="left" backgroundColor="black" transparent="1" />
  <eLabel text="OscamSmartcard 2.4 by arn354 and Undertaker Mod team OPD" position="874,45" size="360,20" zPosition="1" font="Regular; 15" halign="right" backgroundColor="black" transparent="1" />
<ePixmap pixmap="/usr/lib/enigma2/python/OPENDROID/OscamSmartcard/icons/oscamsmartcard.png" position="958,75" size="275,250" alphatest="blend" zPosition="2" />
</screen>"""
	def __init__(self, session, args = None, picPath = None):
		self.config_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.oscamconfigpath = config.OscamSmartcard.ConfigPath.value
		self.oscamuser = (self.oscamconfigpath + "oscam.user")
		self.oscamuserTMP = (self.oscamuser + ".tmp")
		self.oscamconf = (self.oscamconfigpath + "oscam.conf")
		self.oscamconfTMP = (self.oscamconf + ".tmp")
		self.oscamserver = (self.oscamconfigpath + "oscam.server")
		self.oscamserverTMP = (self.oscamserver + ".tmp")
		self.oscamdvbapi = (self.oscamconfigpath + "oscam.dvbapi")
		self.oscamdvbapiTMP = (self.oscamdvbapi + ".tmp")
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["oscamsmartcardhelperimage"] = Pixmap()
		self["HELPTEXT"] = Label()
		self["HEADER"] = Label()
		self["Title"] = Label()
		self["Title"].setText("OscamSmartcard " + _("Setup"))
		self["INFOTXT"] = Label()
		self["INFOTXT"].setText(_("INFORMATION: make your selection and press GREEN\nAll config files are backed up automatically"))
		self.headers = (getMachineBrand() + ' - '+  getMachineName()+ ' - ' + getImageDistro().title() + ' ' + getImageVersion()) + " - " + extrainfo + "\n"
		self.online = self.onlinecheck()
		self.createoscamsmartcarddata()
		self.oscamsmartcarddata = "/tmp/data/"
		self.downloadurl()

		if self.online == False:
			list = []
			self.headers = _("Error") + "\n"
			self.headers += _("Your STB is not connected to the Internet") + "\n" + _("press color button or lame for exit")
			ConfigListScreen.__init__(self, list)
			self["HEADER"].setText(self.headers)
			self["INFOTXT"].setText("")
			self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions", "SetupActions"], {"red": self.exit,"yellow": self.exit,"blue": self.exit,"green": self.exit,"ok": self.exit,"cancel": self.exit}, -1)
			self.exit
		else:
			if arch != 'armv7l' and arch != 'mips' and arch != 'sh4' and arch != 'ppc' and arch != 'armv7ahf-vfp-neon' and arch != 'aarch64' :
				list = []
				self.headers = _("Error") + "\n"
				self.headers += _("Unsupportet CPU") + ' -> ' + arch + ' <- ' + _("found") + "\n"
				self.headers += _("OScam can not be installed") + "\n"
				self.headers += _("press color button or lame for exit") + "\n"
				self["HEADER"].setText(self.headers)
				self["INFOTXT"].setText("")
				ConfigListScreen.__init__(self, list)
				self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions", "SetupActions"], {"red": self.exit,"yellow": self.exit,"blue": self.exit,"green":self.exit,"ok": self.exit,"cancel": self.exit}, -1)
				self.exit
			else:
				self.installedversion = self.getcurrent()
				a=self.checkallcams()
				anzahl = len(a)
				if len(a)>0:
					list = []
					self.headers = _("Error") + "\n"
					self.headers += str(anzahl) + ' ' + _("valueless Softam found.")  + "\n"
					self.headers += _("Remove all first.\notherwise Oscamsmartcard will not start") + "\n"
					i=0
					zz = ""
					while i < len(a):
						title = a[i].replace("softcams",'')
						desc = a[i]
						xx = str(i)
						xx = ConfigSelection(default="x", choices = [("x"),("x")])
						list.append(getConfigListEntry(str(i+1) + ".)  " + title, xx, ""))
						zz += title + "-" +desc
						i = i + 1
					ConfigListScreen.__init__(self, list)
					self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions", "SetupActions"], 
                                        {
                                                "left": self.keyLeft,
                                                "down": self.keyDown,
                                                "up": self.keyUp,
                                                "right": self.keyRight,
                                                "red": self.exit,
                                                "yellow": self.showNews,
                                                "blue": self.exit,
                                                "green": self.systemcleaning,
                                                "cancel": self.exit,
                                        }, -1)
					self.onLayoutFinish.append(self.UpdatePicture)
					if not self.selectionChanged in self["config"].onSelectionChanged:
						self["config"].onSelectionChanged.append(self.selectionChanged)
					self.selectionChanged()
					self["HEADER"].setText(self.headers)
					self["INFOTXT"].setText( _("Press GREEN to remove all")   )
					self["HELPTEXT"].setText("")
				else:
					try:
						onlineavaible = self.newversion(arch)
					except:
						onlineavaible = _("Error")
					list = []
					if getImageDistro() =='opendroid':
						config.OscamSmartcard.ConfigPath.value = "/etc/tuxbox/config/oscam-smartcard/"
					elif getImageDistro() =='openmips':
						config.OscamSmartcard.ConfigPath.value = "/etc/tuxbox/config/"
					elif getImageDistro() =='teamblue':
						config.OscamSmartcard.ConfigPath.value = "/etc/tuxbox/config/"
					else:
						self.close()
					self.headers += _("Config path set automatically to") 	+ '\t: ' + config.OscamSmartcard.ConfigPath.value + "\n"
					self.headers += _("Oscam type set automatically to") 	+ '\t: ' + arch + "\n"
					self.headers += _("Cardreader found automatically")  	+ '\t: ' + str(self.readercheck()[4]) + "\n"
					self.headers += "\n" + _("Settings:") + "\n"
					list.append(getConfigListEntry(_("Select OScam WebifPort:"), config.OscamSmartcard.WebifPort, _("INFORMATION: Select OScam WebifPort\nOscam Webif will be accessible on the selected port.") + '\nhttp://' + architectures()[3] + ':' +   str(config.OscamSmartcard.WebifPort.value)   + " " + _("or")  + " http://"  + self.getIP()  + ":"  + str(config.OscamSmartcard.WebifPort.value)            ))
					if self.readercheck()[0] == 'installed':
						list.append(getConfigListEntry(_("Internal Reader /dev/sci0:"), config.OscamSmartcard.internalReader0, _("INFORMATION: Internal Reader /dev/sci0\n\nAll STB's having only one cardslot.\nOn STB's having two cardslots it is mostly the lower cardslot.")))
					if self.readercheck()[1] == 'installed':
						list.append(getConfigListEntry(_("Internal Reader /dev/sci1:"), config.OscamSmartcard.internalReader1, _("INFORMATION: Internal Reader /dev/sci1\n\nOn STB's having two cardslots it is mostly the upper cardslot.")))
					if self.readercheck()[2] == 'installed':
						list.append(getConfigListEntry(_("External Reader /dev/ttyUSB0:"), config.OscamSmartcard.externalReader0, _("INFORMATION: External Reader /dev/ttyUSB0\n\nThis Reader can be used to configure for example a connected easymouse.")))
					if self.readercheck()[3] == 'installed':
						list.append(getConfigListEntry(_("External Reader /dev/ttyUSB1:"), config.OscamSmartcard.externalReader1, _("INFORMATION: External Reader /dev/ttyUSB1\n\nThis Reader can be used to configure for example a second connected easymouse.")))
					anzcc= self.cccamcheck()[1]
					anzus= self.cccamcheck()[5]
					anz35= self.cccamcheck()[3]
					cccport= self.cccamcheck()[6]
					if anzcc > 0 or anzus >0 or anz35 >0:
						list.append(getConfigListEntry(( _("CCcam.cfg found. Import your settings") ), config.OscamSmartcard.cccam, ( _("Oscamsmartcard found ") + str(anzcc+anz35) + _(" Server and ") + str(anzus) + " User in CCcam.cfg\n" + str(anzcc) + " x CCcam-Server\t" + str(anz35) +' x Camd35 Server\n' + str(anzus) + ' x Userlines (Friends)\tShareport: ' +cccport  )))
					list.append(getConfigListEntry(_("Oscam binary install"),config.OscamSmartcard.oscambinary,('INFORMATION:    ' + _("Versions Info") + '\n' +  _("installed")  + ' \t: ' + self.installedversion + '\n' + _("online") + '\t: ' + onlineavaible )))
					list.append(getConfigListEntry(_("Is a Ci+ Module installed:"), config.OscamSmartcard.hasciplus, _("INFORMATION: please select your CI+ Modul\n\n")))
					ConfigListScreen.__init__(self, list)
					self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "InputActions", "ColorActions"], 
                                        {       "left": self.keyLeft,
                                                "down": self.keyDown,
                                                "up": self.keyUp,
                                                "right": self.keyRight,
                                                "red": self.exit,
                                                "yellow": self.showNews, 
                                                "blue": self.rmconfig, 
                                                "green": self.save,
                                                "cancel": self.exit,
                                        }, -1)
					self.onLayoutFinish.append(self.UpdatePicture)
                            		self["key_red"] = StaticText(_("Close"))
		                        self["key_green"] = StaticText(_("save"))
		                        self["key_blue"] = StaticText(_("remove current config"))
                                        self["key_yellow"] = StaticText(_("Note Release"))
					if not self.selectionChanged in self["config"].onSelectionChanged:
						self["config"].onSelectionChanged.append(self.selectionChanged)
					self.selectionChanged()

	def selectionChanged(self):
		self["HELPTEXT"].setText(self["config"].getCurrent()[2])
		self["HEADER"].setText(self.headers)

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			path = "/usr/lib/enigma2/python/OPENDROID/icons/" + returnValue + ".png"
			return path
		except:
			return "/usr/lib/enigma2/python/OPENDROID/icons/no.png"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["oscamsmartcardhelperimage"].instance.size().width(),self["oscamsmartcardhelperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#20000000"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["oscamsmartcardhelperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.ShowPicture()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.ShowPicture()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.ShowPicture()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.ShowPicture()

	def systemcleaning(self):
		systemclean = self.session.openWithCallback(self.systemclean,MessageBox,_(_("All Softcams will be deinstalled\nAre you sure ?")), MessageBox.TYPE_YESNO)
		systemclean.setTitle(_("System cleaning"))
		self.close()

	def save(self):
		if self.configcheck() == False:
			return
		msginfo = _("Oscam will be installed with the following settings") + "\n\n"
		msginfo += "Webif Port\t"		+ str(config.OscamSmartcard.WebifPort.value)		+ "\n"
		if self.readercheck()[0] == 'installed':
			if config.OscamSmartcard.internalReader0.value != "none":
				msginfo += "Slot 0\t" + config.OscamSmartcard.internalReader0.value			+ "\n"
			else:
				msginfo += "Slot 0\t" + _("no PayTV Card")											+ "\n"
		if self.readercheck()[1] == 'installed':
			if config.OscamSmartcard.internalReader1.value != "none":
				msginfo += "Slot 1\t" + config.OscamSmartcard.internalReader1.value			+ "\n"
			else:
				msginfo += "Slot 1\t" + _("no PayTV Card")											+ "\n"
		if self.readercheck()[2] == 'installed':
			if config.OscamSmartcard.externalReader0.value != "none":
				msginfo += "USB0\t"  + config.OscamSmartcard.externalReader0.value			+ "\n"
			else:
				msginfo += "USB0\t" + _("no PayTV Card")											+ "\n"
		if self.readercheck()[3] == 'installed':
			if config.OscamSmartcard.externalReader1.value != "none":
				msginfo += "USB1\t"   + config.OscamSmartcard.externalReader1.value			+ "\n"
			else:
				msginfo += "USB1\t" + _("no PayTV Card")											+ "\n"
		msginfo += "CI+ Modul\t"		+ _(config.OscamSmartcard.hasciplus.value)			+ "\n"
		if os.path.exists('/etc/CCcam.cfg'):
			if config.OscamSmartcard.cccam.value == "yes_cccam_import":
				msginfo += "CCcam Import\t" + _("yes") + "\n"
			else:
				msginfo += "CCcam Import\t" + _("no") + "\n"
		mm = ""
		if self.hd34check() == True:
			msginfo += "Binary\t" + "oscam r11400 special HD03/04" + "\n"
		else:
			if self.installedversion[0:5] == "oscam":
				mm = "Binary\t" + _("file already exists and use it")
				if config.OscamSmartcard.oscambinary.value == "yes_binary_install":
					if self.newversion(arch) > self.installedversion:
						mm = "Binary\t" + _("file exists, becomes upgrade")
			else:
				mm = "Binary\t" + str( self.newversion(arch)).replace('-1.20-unstable_svn','') + " " + _("will be installed")	+ "\n"
		if mm != "":
			msginfo += mm + "\n"
		msginfo += "\n"
		msginfo += _("Are the settings correct ?")
		self.session.openWithCallback(self.resume,MessageBox,msginfo, MessageBox.TYPE_YESNO).setTitle(_("check your settings"))

	def resume(self, answer):
		if answer is True:
			self.savego()
		else:
			return

	def savego(self):
		self.oscamconfigpath = config.OscamSmartcard.ConfigPath.value
		self.oscamuser = (self.oscamconfigpath + "oscam.user")
		self.oscamuserTMP = (self.oscamuser + ".tmp")
		self.oscamconf = (self.oscamconfigpath + "oscam.conf")
		self.oscamconfTMP = (self.oscamconf + ".tmp")
		self.oscamserver = (self.oscamconfigpath + "oscam.server")
		self.oscamserverTMP = (self.oscamserver + ".tmp")
		self.oscamdvbapi = (self.oscamconfigpath + "oscam.dvbapi")
		self.oscamdvbapiTMP = (self.oscamdvbapi + ".tmp")
		self.oscamservices = (self.oscamconfigpath + "oscam.services")
		self.oscamservicesTMP = (self.oscamservices + ".tmp")
		self.oscamcamstart = '/etc/oscamsmartcard.emu'
		self.oscamcamstartTMP = (self.oscamcamstart + ".tmp")
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
				pass
		try:
			os.system('mkdir -p ' + config.OscamSmartcard.ConfigPath.value + ' > /dev/null 2>&1')
		except:
			pass
		self.makebackup()
		self.saveoscamserver()
		self.saveoscamdvbapi()
		self.saveoscamuser()
		self.saveoscamconf()
		self.saveoscamservices()
		self.saveoscamfiles()
		if config.OscamSmartcard.oscambinary.value == 'yes_binary_install':
			self.oscambinaryupdate()
		self.savecamstart()
		system ('/etc/init.d/softcam start')
		config.OscamSmartcard.save()
		configfile.save()
		self.rmoscamsmartcarddata()
		self.session.open(MessageBox, _("oscam install finished\nhave fun"), MessageBox.TYPE_INFO, 10).setTitle(_("done"))
		self.close()

	def configcheck(self):
		if not os.path.exists('/usr/bin/oscam_oscamsmartcard') and config.OscamSmartcard.oscambinary.value == "no_binary_install":
			self.session.open(MessageBox,(_("Oscam Binary is not installed\nYou must this install") + "\n\n\tOK"  ), MessageBox.TYPE_ERROR,).setTitle(_("wrong Settings detected"))
			return False

	def getcurrent(self):
		current = _("no")
		if os.path.exists("/usr/bin/oscam_oscamsmartcard"):
			current = popen("chmod 775 /usr/bin/oscam_oscamsmartcard && /usr/bin/oscam_oscamsmartcard -V | grep Version |awk '{print $2}'").read().strip()
		if current ==_("no"):
			return current
		if "oscam" in current:
			return str(current)
		else:
			self.getcurrent()
	def createoscamsmartcarddata(self):
		data = 'wget -T5 --no-check-certificate -O /tmp/data.zip '+ base64.b64decode(self.getdl()[1]) + 'data.zip ' + null
		popen(data)
		popen('unzip -o -q -d /tmp /tmp/data.zip')
		popen('rm /tmp/data.zip')

	def rmoscamsmartcarddata(self):
		popen('rm -rf /tmp/data')

	def saveoscamserver(self):
		try:
			self.appendconfFile(self.oscamsmartcarddata + "header.txt")
			if config.OscamSmartcard.emu.value:
				self.appendconfFile(self.oscamsmartcarddata + "oscam.server_emu.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.server_" + config.OscamSmartcard.internalReader0.value + "_internalReader0.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.server_" + config.OscamSmartcard.internalReader1.value + "_internalReader1.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.server_" + config.OscamSmartcard.externalReader0.value + "_externalReader0.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.server_" + config.OscamSmartcard.externalReader1.value + "_externalReader1.txt")
			if config.OscamSmartcard.cccam.value == "yes_cccam_import":
				self.appendconfFile(self.oscamsmartcarddata + "cccamserver.txt")
			self.appendconfFile(self.oscamsmartcarddata + "footer.txt")
			xFile = open(self.oscamserverTMP, "w")
			for xx in self.config_lines:
				xFile.writelines(xx)
			xFile.close()
			o = open(self.oscamserver,"w")
			for line in open(self.oscamserverTMP):
				o.write(line)
			o.close()
			system('rm -rf ' + self.oscamserverTMP)
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam.server!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def saveoscamdvbapi(self):
		try:
			self.appendconfFile(self.oscamsmartcarddata + "header.txt")
			if config.OscamSmartcard.hasciplus.value =='ciplusV14':
				self.appendconfFile(self.oscamsmartcarddata + "ciplusV14.txt")
			if config.OscamSmartcard.hasciplus.value =='ciplusV13':
				self.appendconfFile(self.oscamsmartcarddata + "ciplusV13.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.dvbapi_" + config.OscamSmartcard.internalReader0.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.dvbapi_" + config.OscamSmartcard.internalReader1.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.dvbapi_" + config.OscamSmartcard.externalReader0.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.dvbapi_" + config.OscamSmartcard.externalReader1.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "footer.txt")
			xFile = open(self.oscamdvbapiTMP, "w")
			for xx in self.config_lines:
				xFile.writelines(xx)
			xFile.close()
			o = open(self.oscamdvbapi,"w")
			for line in open(self.oscamdvbapiTMP):
				o.write(line)
			o.close()
			system('rm -rf ' + self.oscamdvbapiTMP)
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam.dvbapi!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def saveoscamuser(self):
		try:
			self.appendconfFile(self.oscamsmartcarddata + "header.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.user.txt")
			if config.OscamSmartcard.cccam.value == "yes_cccam_import":
				self.appendconfFile(self.oscamsmartcarddata + "cccamuser.txt")
			self.appendconfFile(self.oscamsmartcarddata + "footer.txt")
			xFile = open(self.oscamuserTMP, "w")
			for xx in self.config_lines:
				xFile.writelines(xx)
			xFile.close()
			o = open(self.oscamuser,"w")
			for line in open(self.oscamuserTMP):
				o.write(line)
			o.close()
			system('rm -rf ' + self.oscamuserTMP)
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam.user!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def saveoscamconf(self):
		try:
			self.appendconfFile(self.oscamsmartcarddata + "header.txt")
			if config.OscamSmartcard.emu.value:
				self.appendconfFile(self.oscamsmartcarddata + "oscam.conf.emu.txt")
			else:
				self.appendconfFile(self.oscamsmartcarddata + "oscam.conf.txt")
			if config.OscamSmartcard.cccam.value == "yes_cccam_import":
				self.appendconfFile(self.oscamsmartcarddata + "cccamconfig.txt")
			self.appendconfFile(self.oscamsmartcarddata + "footer.txt")
			xFile = open(self.oscamconfTMP, "w")
			for xx in self.config_lines:
				xFile.writelines(xx)
			xFile.close()
			o = open(self.oscamconf,"w")
			for line in open(self.oscamconfTMP):
				line = line.replace("83", config.OscamSmartcard.WebifPort.value )
				o.write(line)
			o.close()
			system('rm -rf ' + self.oscamconfTMP)
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam.conf!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def saveoscamservices(self):
		try:
			self.appendconfFile(self.oscamsmartcarddata + "header.txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.services_" + config.OscamSmartcard.internalReader0.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.services_" + config.OscamSmartcard.internalReader1.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.services_" + config.OscamSmartcard.externalReader0.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.services_" + config.OscamSmartcard.externalReader1.value + ".txt")
			self.appendconfFile(self.oscamsmartcarddata + "oscam.services.txt")
			self.appendconfFile(self.oscamsmartcarddata + "footer.txt")
			xFile = open(self.oscamservicesTMP, "w")
			for xx in self.config_lines:
				xFile.writelines(xx)
			xFile.close()
			o = open(self.oscamservices,"w")
			for line in open(self.oscamservicesTMP):
				o.write(line)
			o.close()
			system('rm -rf ' + self.oscamservicesTMP)
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam.services!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def saveoscamfiles(self):
		if config.OscamSmartcard.emu.value:
			system('cp -f ' + self.oscamsmartcarddata + 'SoftCam.Key'  + ' ' + config.OscamSmartcard.ConfigPath.value)
		system('cp -f ' + self.oscamsmartcarddata + 'oscam.srvid'  + ' ' + config.OscamSmartcard.ConfigPath.value)
		system('cp -f ' + self.oscamsmartcarddata + 'oscam.srvid2'  + ' ' + config.OscamSmartcard.ConfigPath.value)
		system('cp -f ' + self.oscamsmartcarddata + 'oscam.provid' + ' ' + config.OscamSmartcard.ConfigPath.value)
		system('cp -f ' + self.oscamsmartcarddata + 'oscam.tiers'  + ' ' + config.OscamSmartcard.ConfigPath.value)

	def oscambinaryupdate(self):
		if self.newversion(arch) != _("Download not avaible"):
			system('killall -9 oscam_oscamsmartcard' + null)
			system('wget -T5 --no-check-certificate -q -O /tmp/oscam.tar.gz ' + self.downloadurl() + ' ' + null)
			system('tar -xzf /tmp/oscam.tar.gz -C /tmp' + null)
			system('rm -f /usr/bin/oscam_oscamsmartcard' + null)
			system('mv /tmp/oscam /usr/bin/oscam_oscamsmartcard' + null)
			system('chmod 755 /usr/bin/oscam_oscamsmartcard')
			system('rm -f /tmp/oscam.tar.gz')

	def downloadurl(self):
		binary = 'oscam_oscamsmartcard'
		suffix = '.tar.gz'
		emu=''
		if getImageDistro() =='opendroid':
			if config.OscamSmartcard.emu.value:
				emu='_emu'
		if getImageDistro() =='openmips':
			if config.OscamSmartcard.emu.value:
				emu='_emu'
		if getImageDistro() =='teamblue':
			if config.OscamSmartcard.emu.value:
				emu='_emu'
		archs = ['armv7l','mips','sh4','ppc','armv7ahf-vfp-neon','aarch64']
		if arch =='aarch64':
			emu=''
		if arch in archs:
			downloadurl = base64.b64decode(self.getdl()[1]) + binary + '_' + arch + emu + suffix
			#overwrite if Box is a WeTeKPLAY
			if getMachineBrand() =='WeTeK':
				downloadurl = base64.b64decode(self.getdl()[1]) + binary + '_' + 'wetekplay' + suffix
			if self.hd34check():
				downloadurl = base64.b64decode(self.getdl()[1]) + binary + '_' + arch + '_hd34' + suffix
		else:
			downloadurl = 'unknown_' + arch
		return downloadurl

	def hd34check(self):
		hd34 = ['HD03','HD04']
		if config.OscamSmartcard.internalReader0.value in hd34:
			return True
		if config.OscamSmartcard.internalReader1.value in hd34:
			return True
		if config.OscamSmartcard.externalReader0.value in hd34:
			return True
		if config.OscamSmartcard.externalReader1.value in hd34:
			return True
		return False
	def newversion(self,arch):
		upgradeinfo = _("Download not avaible")
		if self.online == True:
			upgfile = '/tmp/version.zip'
			system('wget -T5 --no-check-certificate -O ' + upgfile + ' ' + base64.b64decode(self.getdl()[2]) + ' ' + null )
			popen('unzip -o -q -d /tmp ' + upgfile)
			file = open("/tmp/version.info", "r")
			for line in file.readlines():
				line = line.strip().split(',')
				if line[0] == arch:
					upgradeinfo = line[1].replace("-unstable","")
			file.close()
			os.remove("/tmp/version.info")
			os.remove(upgfile)
			return upgradeinfo
		return upgradeinfo

	def checkallcams(self):
		if getImageDistro() =='opendroid':
			return []
		ignore =[
		'enigma2-plugin-softcams-oscamsmartcard',
		'enigma2-plugin-pli-softcamsetup',
		'enigma2-plugin-softcams-oscamstatus',
		'enigma2-plugin-softcams-cccam.config',
		'enigma2-plugin-softcams-mgcamd.config',
		'enigma2-plugin-systemplugins-softcamstartup',
		'enigma2-plugin-systemplugins-softcamstartup-src',
		'softcam-feed-mipsel',
		'om-softcam-support',
		'softcam-feed-universal'
		]
		liste=[]
		f = popen('opkg list-installed |grep -i softcam')
		for line in f:
			line=line.strip().split()
			if line[0] not in ignore:
				liste.append(line[0])
		f.close()
		return liste

	def readercheck(self):
		sci0 = 'not installed';
		sci1 = sci0
		usb0 = sci0
		usb1 = sci0
		anz = 0
		if os.path.exists('/dev/sci0'):
			sci0='installed'
			anz=anz+1
		if os.path.exists('/dev/sci1'):
			sci1='installed'
			anz=anz+1
		if os.path.exists('/dev/ttyUSB0'):
			usb0='installed'
			anz=anz+1
		if os.path.exists('/dev/ttyUSB1'):
			usb1='installed'
			anz=anz+1
		return sci0,sci1,usb0,usb1,anz

	def makebackup(self):
		dd = (time.strftime("%Y-%m-%d-%H-%M-%S"))
		if getImageDistro() =='opendroid':
			x = glob.glob("/etc/tuxbox/config/oscam-smartcard/oscam.*")
			if len(x) >0:
				system('tar -czf /etc/tuxbox/config/backup-oscamsmartcard-'+ dd +'.tar.gz /etc/tuxbox/config/oscam-smartcard/oscam.*')
				system('rm -f /etc/tuxbox/config/oscam-smartcard/oscam.*')
		if getImageDistro() =='openmips':
			y = glob.glob("/etc/tuxbox/config/oscam.*")
			if len(y) >0:
				system('tar -czf /etc/tuxbox/config/backup-oscamsmartcard-'+ dd +'.tar.gz /etc/tuxbox/config/oscam.*')
				system('rm -f /etc/tuxbox/config/oscam.*')
		if getImageDistro() =='teamblue':
			y = glob.glob("/etc/tuxbox/config/oscam.*")
			if len(y) >0:
				system('tar -czf /etc/tuxbox/config/backup-oscamsmartcard-'+ dd +'.tar.gz /etc/tuxbox/config/oscam.*')
				system('rm -f /etc/tuxbox/config/oscam.*')

	def makeclean(self):
		a = self.checkallcams()
		if len(a) >0:
			i = 0
			while i < len(a):
				system('opkg remove --force-remove ' + a[i] + null)
				i = i + 1

	def savecamstart(self):
		try:
			system('/etc/init.d/softcam stop && /etc/init.d/cardserver stop')
			self.initd()
			system('rm -f /etc/init.d/cardserver.OscamSmartcard')
			system('rm -f /etc/init.d/softcam.OscamSmartcard')
			system('cp -f /tmp/data/softcam.OscamSmartcard /etc/init.d/softcam.OscamSmartcard')
			system('sed -i /etc/init.d/softcam.OscamSmartcard -e \'s#/etc/tuxbox/config"#' + self.oscamconfigpath + '"#\'')
			system('cp -f /tmp/data/cardserver.OscamSmartcard /etc/init.d/cardserver.OscamSmartcard')
			system('chmod 755 /etc/init.d/softcam.OscamSmartcard')
			system('chmod 755 /etc/init.d/cardserver.OscamSmartcard')
			system('rm -f /etc/init.d/softcam && rm -f /etc/init.d/cardserver')
			system('ln -sf softcam.OscamSmartcard /etc/init.d/softcam')
			system('ln -sf cardserver.None /etc/init.d/cardserver')
			self.config_lines = []
		except:
			self.session.open(MessageBox, _("Error creating oscam camstart files!"), MessageBox.TYPE_ERROR)
			self.config_lines = []

	def appendconfFile(self,appendFileName):
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()
		for x in file_lines:
			self.config_lines.append(x)

	def systemclean(self, answer):
		if answer is True:
			self.makeclean()
			self.close()
		else:
			return

	def onlinecheck(self):
		try:
			response=urllib2.urlopen(base64.b64decode('aHR0cDovLzY5LjE5NS4xMjQuNTA='),timeout=10)
			return True
		except urllib2.URLError as err: pass
		return False

	def exit(self):
		system('rm -rf /tmp/data')
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()

	def rmconfig(self):
		rmconfigset = self.session.openWithCallback(self.rmconfigset,MessageBox,_("Do you really want to remove all\noscam_smartcard configs, binary's and camstartfiles.\nA backup will be created\nPlease restart this plugin again!!" ), MessageBox.TYPE_YESNO)
		rmconfigset.setTitle(_("remove current config"))

	def rmconfigset(self, answer):
		if answer is True:
			self.makebackup()
			system('killall -9 oscam_oscamsmartcard ' + null)
			system('rm /usr/bin/oscam_oscamsmartcard' + null)
			if getImageDistro() =='opendroid':
				system('rm -rf /etc/tuxbox/config/oscam-smartcard' + null)
				system('rm /etc/init.d/softcam.OscamSmartcard' + null)
				system('rm /etc/init.d/cardserver.OscamSmartcard' + null)
				self.initd()
			if getImageDistro() =='openmips' or getImageDistro() =='teamblue':
				system('rm -f /etc/tuxbox/config/oscam.*' + null)
				system('rm /etc/init.d/softcam.OscamSmartcard' + null)
				system('rm /etc/init.d/cardserver.OscamSmartcard' + null)
				self.initd()
			system('rm -rf /tmp/data' + null)
			system('rm -f /tmp/upgrade.log' + null)
			popen('rm -rf /tmp/.oscam' + null)
			self.valuedefaultsettings()
			self.close()
		else:
			return

	def valuedefaultsettings(self):
		config.OscamSmartcard.WebifPort.value = "83"
		config.OscamSmartcard.systemclean.value = True
		config.OscamSmartcard.ConfigPath.value = "/etc/tuxbox/config/oscam-smartcard/"
		config.OscamSmartcard.oscambinary.value = "no_binary_install"
		config.OscamSmartcard.cccam.value = "no_cccam_import"
		config.OscamSmartcard.internalReader0.value = "none"
		config.OscamSmartcard.internalReader1.value = "none"
		config.OscamSmartcard.externalReader0.value = "none"
		config.OscamSmartcard.externalReader1.value = "none"
		config.OscamSmartcard.emu.value = False
		config.OscamSmartcard.hasciplus.value = "no"
		config.OscamSmartcard.save()
		configfile.save()
		return

	def cccamcheck(self):
		cccsrv='';cccuser='';ccconfig='';cccport='12000'
		xc=0;yc=0;zc=0
		if os.path.exists('/etc/CCcam.cfg'):
			i=0;C='C';c='c';y=0; F='F';f='f';l='l';L='L'
			cclines= ('c:','C:')
			camd35lines = ('l:','L:')
			userline = ('f','F')
			datei = open("/etc/CCcam.cfg","r")
			for line in datei.readlines():
				line = line.strip().split('#')[0]
				line = line.split('{')[0]
				if line.startswith((c,C,l,L,F,f,'SERVER LISTEN PORT')):
					line=line.replace("\t"," ").replace(" :",":").replace(": ",":").replace(" :",":").replace(": ",":").replace("  "," ")
					if line.startswith(cclines) or line.startswith(camd35lines):
						if line.startswith(cclines) :protokoll='cccam'
						if line.startswith(camd35lines) :protokoll='cs357x'
						line = line.strip().split(":")
						line = line[1]
						line = line.split()
						if len(line)>3:
							i=i+1
							server = line[0]
							port = line[1];user = line[2];passwd = line[3]
							parts = server.split(".")
							end = str(parts[len(parts)-1])
							if "0" in end or "1" in end or "2" in end or "3" in end or "4" in end or "5" in end or "6" in end or "7" in end or "8" in end or "9" in end:
								servername ="IP"
							else:
								servername =parts[0]
							if protokoll=='cccam':
								xc +=1
								if servername == "IP":
									servername=server.replace(".","-")
								servername =  servername+"_"+str(xc)
								peer = '\n[reader]\nlabel\t\t\t = ' +servername + '\ndescription\t\t = ' + 'CCcam-Server: '+ server + ':' + port + '\nprotocol\t\t = ' + protokoll + '\n' + 'device\t\t\t = '+ server + ',' + port + '\n' +'user\t\t\t = ' + user + '\npassword\t\t = ' + passwd + '\ngroup\t\t\t = 1\ncccversion\t\t = 2.3.0\nccckeepalive\t\t = 1\nccchop\t\t\t = 9\naudisabled\t\t = 1\ndisablecrccws\t\t= 1\ndisablecrccws_only_for\t = 09C4:000000;098C:000000\n'
							if protokoll=='cs357x':
								yc +=1
								if servername == "IP":
									servername=server.replace(".","-")
								servername = servername+"_"+str(yc)
								peer = '\n[reader]\nlabel\t\t\t = ' +servername + '\ndescription\t\t = ' + 'Camd35-Server: ' + server + ':' + port + '\nprotocol\t\t = ' + protokoll + '\n' + 'device\t\t\t = '+ server + ',' + port + '\n' +'user\t\t\t = ' + user + '\npassword\t\t = ' + passwd + '\ngroup\t\t\t = 1\naudisabled\t\t = 1\ndisablecrccws\t\t= 1\ndisablecrccws_only_for\t = 09C4:000000;098C:000000\n'
							cccsrv += peer
					elif line.startswith(userline):
						zc=zc+1
						line = line.strip().split(":")
						line = line[1]
						line = line.split()
						if len(line)>1:
							cuser = line[0];cpass = line[1]
							user= '\n[account]\nuser\t\t\t = ' + line[0] + '\npwd\t\t\t = ' +line[1] + '\nuniq\t\t\t = 3\ngroup\t\t\t = 1\n'
							cccuser += user
					elif line.startswith('SERVER LISTEN PORT'):
						cccport = line.split(':')[1]
					ccconfig = '\n[cccam]\nport\t\t\t = '+cccport+'\nnodeid\t\t\t = \nversion\t\t\t = 2.3.0\nreshare\t\t\t = 2\nstealth\t\t\t = 1\n'
			datei.close()
			h = open(self.oscamsmartcarddata + "cccamconfig.txt","w")
			h.write(ccconfig)
			h.close()
			o = open(self.oscamsmartcarddata + "cccamserver.txt","w")
			o.write(cccsrv)
			o.close()
			p = open(self.oscamsmartcarddata + "cccamuser.txt","w")
			p.write(cccuser)
			p.close()
		return cccsrv,xc,cccuser,yc,ccconfig,zc,cccport

	def initd(self):
		if not fileExists('/etc/init.d/softcam.None'):
			fd = file('/etc/init.d/softcam.None', 'w')
			fd.write('#!/bin/sh\necho "Softcam is deactivated."\n')
			fd.close()
			system('chmod 755 /etc/init.d/softcam.None')
		if not fileExists('/etc/init.d/cardserver.None'):
			fd = file('/etc/init.d/cardserver.None', 'w')
			fd.write('#!/bin/sh\necho "Cardserver is deactivated."\n')
			fd.close()
			system('chmod 755 /etc/init.d/cardserver.None')
		system('rm -f /etc/init.d/softcam')
		system('ln -s /etc/init.d/softcam.None /etc/init.d/softcam')
		system('chmod 755 /etc/init.d/softcam')
		system('rm -f /etc/init.d/cardserver')
		system('ln -s /etc/init.d/cardserver.None /etc/init.d/cardserver')
		system('chmod 755 /etc/init.d/cardserver')
		if fileExists ('/etc/rcS.d/*softcam'):
			os.system('update-rc.d -f softcam remove && update-rc.d -f cardserver remove')
			os.system('rm /etc/rcS.d/*softcam')
			os.system('rm /etc/rcS.d/*cardserver')
		if fileExists ('/etc/rc2.d/*softcam'):
			os.system('update-rc.d -f softcam remove && update-rc.d -f cardserver remove')
		if not fileExists('/etc/rc2.d/*softcam'):
			os.system('update-rc.d softcam defaults 50')
			os.system('update-rc.d cardserver start 95 S .')

	def getIP(self):
		return str(popen('ip route get 8.8.8.8 |cut -d " " -f7').read().strip())

	def getdl(self):
		info  = 'aHR0cDovL2NhbTRtZS5vcmcvb3Blbm1pcHMyL29zY2Ftc21hcnRjYXJkL3ZlcnNpb24uaW5mbw=='
		srv   = 'aHR0cDovL2NhbTRtZS5vcmcvb3Blbm1pcHMyL29zY2Ftc21hcnRjYXJkLw=='
		infoz = 'aHR0cDovL2NhbTRtZS5vcmcvb3Blbm1pcHMyL29zY2Ftc21hcnRjYXJkL3ZlcnNpb24uemlw'
		return info,srv,infoz

	def showNews(self):
		lastinfo =  ""
		x = " : "
                lastinfo += "06-07-2019" + x + _("Adjust runlevels") + "\n"
                lastinfo += "06-06-2019" + x + _("small changes due to disablecrccws") + "\n"
                lastinfo += "02-06-2019" + x + _("Adjust config dir on install") + "\n"
                lastinfo += "02-06-2019" + x + _("Adjust for sfeed and cleanup") + "\n"
                lastinfo += "02-06-2019" + x + _("Fix softcam/cardserver start") + "\n"
		lastinfo += "10-02-2018" + x + _("added bcm arm 64 bit CPU") + "\n"
		lastinfo += "11-07-2018" + x + _("download fix") + "\n"
		lastinfo += "18-02-2018" + x + _("added HD03/04 Support") + "\n"
		lastinfo += "27-01-2018" + x + _("added ORF 650, added 6.2 Support") + "\n"
		lastinfo += "10-12-2016" + x + _("update init.d start/stop") + "\n"
		lastinfo += "17-09-2016" + x + _("update oscamsmartcard code") + "\n"
		lastinfo += "11-09-2016" + x + _("update Redlight HD Card") + "\n"
		lastinfo += "08-09-2016" + x + _("added ORF ICE p410 Card") + "\n"
		lastinfo += "08-09-2016" + x + _("remove reboot from oscamsmartcard") + "\n"
		lastinfo += "08-09-2016" + x + _("this info added") + "\n"
		lastinfo += "17-06-2016" + x + _("added SRG V6 Card") + "\n"
		lastinfo += "09-06-2016" + x + _("added CI+") + "\n"
		self.session.open(MessageBox, lastinfo, MessageBox.TYPE_INFO).setTitle(_("Oscamsmartcard News"))

def main(session, **kwargs):
	session.open(OscamSmartcard,"/usr/lib/enigma2/python/OPENDROID/icons/oscamsmartcard.png")
def OPENDROID(**kwargs):
	return PluginDescriptor(name="Oscam Smartcard v2.4", description=_("Configuration tool for OScam"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)
