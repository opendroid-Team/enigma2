from os import stat, statvfs, makedirs
from os.path import join, isdir
from shlex import split

from enigma import eTimer

from Components.AVSwitch import iAVSwitch
from Components.config import ConfigBoolean, config, configfile
from Components.Console import Console
from Components.Harddisk import harddiskmanager
from Components.SystemInfo import BoxInfo
from Components.Pixmap import Pixmap
from Screens.HelpMenu import ShowRemoteControl
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop, QUIT_RESTART
from Screens.VideoWizard import VideoWizard
from Screens.Wizard import wizardManager, Wizard
from Tools.Directories import fileReadLines, fileWriteLines

MODULE_NAME = __name__.split(".")[-1]

config.misc.firstrun = ConfigBoolean(default=True)
config.misc.videowizardenabled = ConfigBoolean(default=True)
config.misc.wizardLanguageEnabled = ConfigBoolean(default=True)


class StartWizard(Wizard, ShowRemoteControl):
	def __init__(self, session, silent=True, showSteps=False, neededTag=None):
		self.xmlfile = ["startwizard.xml"]
		Wizard.__init__(self, session, showSteps=False)
		ShowRemoteControl.__init__(self)
		self["wizard"] = Pixmap()
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self.setTitle(_("Start Wizard"))

	def markDone(self):
		# setup remote control, all stb have same settings except dm8000 which uses a different settings
		config.misc.rcused.value = 0 if BoxInfo.getItem("machinebuild") == 'dm8000' else 1
		config.misc.rcused.save()
		config.misc.firstrun.value = False
		config.misc.firstrun.save()
		configfile.save()

class WizardLanguage(Wizard, ShowRemoteControl):
	def __init__(self, session, silent=True, showSteps=False, neededTag=None):
		self.xmlfile = ["wizardlanguage.xml"]
		Wizard.__init__(self, session, showSteps=False)
		ShowRemoteControl.__init__(self)
		self.skinName = ["WizardLanguage", "StartWizard"]
		self.oldLanguage = config.osd.language.value
		self.avSwitch = iAVSwitch
		self.mode = "720p"
		self.modeList = [(mode[0], mode[0]) for mode in self.avSwitch.getModeList("HDMI")]
		self["wizard"] = Pixmap()
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self.setTitle(_("Start Wizard"))
		self.resolutionTimer = eTimer()
		self.resolutionTimer.callback.append(self.resolutionTimeout)
		preferred = self.avSwitch.readPreferredModes(saveMode=True)

		if preferred:
			if "2160p50" in preferred:
				self.mode = "2160p"
			elif "2160p30" in preferred:
				self.mode = "2160p30"
			elif "1080p" in preferred:
				self.mode = "1080p"

		self.setMode()

		if not preferred:
			ports = [port for port in self.avSwitch.getPortList() if self.avSwitch.isPortUsed(port)]
			if len(ports) > 1:
				self.resolutionTimer.start(20000)
				print("[WizardLanguage] DEBUG start resolutionTimer")

	def setMode(self):
		print("[WizardLanguage] DEBUG setMode %s" % self.mode)
		if self.mode in ("720p", "1080p") and not BoxInfo.getItem("AmlogicFamily"):
			rate = "multi"
		else:
			rate = self.getVideoRate()
		self.avSwitch.setMode(port="HDMI", mode=self.mode, rate=rate)

	def getVideoRate(self):
		def sortKey(name):
			return {
				"multi": 1,
				"auto": 2
			}.get(name[0], 3)

		rates = []
		for modes in self.avSwitch.getModeList("HDMI"):
			if modes[0] == self.mode:
				for rate in modes[1]:
					if rate == "auto" and not BoxInfo.getItem("have24hz"):
						continue
					rates.append((rate, rate))
		rates.sort(key=sortKey)
		return rates[0][0]

	def resolutionTimeout(self):
		if self.mode == "720p":
			self.mode = "576i"
		if self.mode == "576i":
			self.mode = "480i"
			self.resolutionTimer.stop()
		self.setMode()

	def saveWizardChanges(self):
		self.resolutionTimer.stop()
		config.misc.wizardLanguageEnabled.value = 0
		config.misc.wizardLanguageEnabled.save()
		configfile.save()
		if config.osd.language.value != self.oldLanguage:
			self.session.open(TryQuitMainloop, QUIT_RESTART)
		self.close()

# StartEnigma.py#L528ff - RestoreSettings
if config.misc.firstrun.value:
	wizardManager.registerWizard(WizardLanguage, config.misc.wizardLanguageEnabled.value, priority=0)
wizardManager.registerWizard(VideoWizard, config.misc.videowizardenabled.value, priority=1)
#wizardManager.registerWizard(LocaleWizard, config.misc.languageselected.value, priority=2)
# FrontprocessorUpgrade FPUpgrade priority = 8
# FrontprocessorUpgrade SystemMessage priority = 9
wizardManager.registerWizard(StartWizard, config.misc.firstrun.value, priority=30)
# StartWizard calls InstallWizard
# NetworkWizard priority = 25
