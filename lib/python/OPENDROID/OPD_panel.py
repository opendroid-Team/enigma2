from Plugins.Plugin import PluginDescriptor
from Screens.PluginBrowser import *
from Screens.Ipkg import Ipkg
from Screens.HarddiskSetup import HarddiskSetup
from Components.ProgressBar import ProgressBar
from Components.SelectionList import SelectionList
from Screens.NetworkSetup import *
from enigma import *
from Screens.Standby import *
from Screens.LogManager import *
from Screens.MessageBox import MessageBox
from Plugins.SystemPlugins.SoftwareManager.Flash_online import FlashOnline
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Screens.Screen import Screen
from Screens.TaskView import JobView
from Components.Task import Task, Job, job_manager, Condition
from GlobalActions import globalActionMap
from Screens.ChoiceBox import ChoiceBox
from Tools.BoundFunction import boundFunction
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, fileExists, pathExists
from Components.MenuList import MenuList
from Components.FileList import FileList
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.config import ConfigSubsection, ConfigInteger, ConfigText, getConfigListEntry, ConfigSelection, ConfigIP, ConfigYesNo, ConfigSequence, ConfigNumber, NoSave, ConfigEnableDisable, configfile
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.Sources.StaticText import StaticText
from Components.Sources.Progress import Progress
from Components.Button import Button
from Components.ActionMap import ActionMap
from Components.SystemInfo import SystemInfo
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from OPENDROID.OscamSmartcard import *
from enigma import eConsoleAppContainer
from Tools.Directories import fileExists
from Tools.Downloader import downloadWithProgress
from boxbranding import getBoxType, getMachineName, getMachineBrand, getBrandOEM
from boxbranding import getBoxType, getMachineBuild, getMachineBrand, getMachineName, getImageVersion, getImageBuild, getDriverDate, getOEVersion, getImageType
from enigma import getDesktop
from Screens.InputBox import PinInput
import string
from random import Random

import os
import sys
import re, string
font = "Regular;16"
import ServiceReference
import time
import datetime
inOPD_panel = None

config.OPENDROID_redpanel = ConfigSubsection()

def Check_Softcam():
	found = False
	if fileExists("/etc/enigma2/noemu"):
		found = False
	else:
		for cam in os.listdir("/etc/init.d"):
			if cam.startswith('softcam.') and not cam.endswith('None'):
				found = True
				break
			elif cam.startswith('cardserver.') and not cam.endswith('None'):
				found = True
				break
	return found

def Check_SysSoftcam():
	syscam="none"
	if os.path.isfile('/etc/init.d/softcam'):
		if (os.path.islink('/etc/init.d/softcam') and not os.readlink('/etc/init.d/softcam').lower().endswith('none')):
			try:
				syscam = os.readlink('/etc/init.d/softcam').rsplit('.', 1)[1]
				if syscam.lower().startswith('oscam'):
					syscam="oscam"
				if syscam.lower().startswith('ncam'):
					syscam="ncam"
				if syscam.lower().startswith('cccam'):
					syscam="cccam"
			except:
				pass
	return syscam


if Check_Softcam():
	redSelection = [('0',_("Default (Instant Record)")), ('1',_("OPD_panel")),('2',_("Timer List")),('3',_("Show Movies")), ('4',_("SoftcamSetup"))]
else:
	redSelection = [('0',_("Default (Instant Record)")), ('1',_("OPD_panel")),('2',_("Timer List")),('3',_("Show Movies"))]

def timerEvent():
	pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
	for p in pluginlist:
		redSelection.append((p.name, _(p.name)))
	if getBoxType() == "dm800":
		config.OPENDROID_redpanel.selection = ConfigSelection(redSelection, default='0')
		config.OPENDROIDl_redpanel.selectionLong = ConfigSelection(redSelection, default='1')
	else:
		config.OPENDROID_redpanel.selection = ConfigSelection(redSelection, default='1')
		config.OPENDROID_redpanel.selectionLong = ConfigSelection(redSelection, default='2')
timer = eTimer()
timer.timeout.get().append(timerEvent)
timer.startLongTimer(1)

from OPENDROID.HddSetup import *
from OPENDROID.BluePanel import *
from Screens.CronTimer import *
from OPENDROID.ScriptRunner import *
from OPENDROID.MountManager import *
from OPENDROID.SwapManager import Swap, SwapAutostart
from OPENDROID.SoftwarePanel import SoftwarePanel
from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen, RestoreScreen, BackupSelection, getBackupPath, getBackupFilename
SystemInfo["SoftCam"] = Check_Softcam()

if config.usage.keymap.value != eEnv.resolve("${datadir}/enigma2/keymap.xml"):
	if not os.path.isfile(eEnv.resolve("${datadir}/enigma2/keymap.usr")) and config.usage.keymap.value == eEnv.resolve("${datadir}/enigma2/keymap.usr"):
		setDefaultKeymap()
	if not os.path.isfile(eEnv.resolve("${datadir}/enigma2/keymap.ntr")) and config.usage.keymap.value == eEnv.resolve("${datadir}/enigma2/keymap.ntr"):
		setDefaultKeymap()
	if not os.path.isfile(eEnv.resolve("${datadir}/enigma2/keymap.u80")) and config.usage.keymap.value == eEnv.resolve("${datadir}/enigma2/keymap.u80"):
		setDefaultKeymap()
def setDefaultKeymap():
	print "[Info-Panel] Set Keymap to Default"
	config.usage.keymap.value = eEnv.resolve("${datadir}/enigma2/keymap.xml")
	config.save()

def command(comandline, strip=1):
  comandline = comandline + " >/tmp/command.txt"
  os.system(comandline)
  text = ""
  if os.path.exists("/tmp/command.txt") is True:
    file = open("/tmp/command.txt", "r")
    if strip == 1:
      for line in file:
        text = text + line.strip() + '\n'
    else:
      for line in file:
        text = text + line
        if text[-1:] != '\n': text = text + "\n"
    file.close()
  # if one or last line then remove linefeed
  if text[-1:] == '\n': text = text[:-1]
  comandline = text
  os.system("rm /tmp/command.txt")
  return comandline

boxversion = getBoxType()
machinename = getMachineName()
machinebrand = getMachineBrand()
OEMname = getBrandOEM()
OPD_panel_Version = 'OPD PANEL V1.5 (By OPD-Team)'
print "[OPD_panel] machinebrand: %s"  % (machinebrand)
print "[OPD_panel] machinename: %s"  % (machinename)
print "[OPD_panel] oem name: %s"  % (OEMname)
print "[OPD_panel] boxtype: %s"  % (boxversion)
panel = open("/tmp/OPD_panel.ver", "w")
panel.write(OPD_panel_Version + '\n')
panel.write("Machinebrand: %s " % (machinebrand)+ '\n')
panel.write("Machinename: %s " % (machinename)+ '\n')
panel.write("oem name: %s " % (OEMname)+ '\n')
panel.write("Boxtype: %s " % (boxversion)+ '\n')
try:
	panel.write("Keymap: %s " % (config.usage.keymap.value)+ '\n')
except:
	panel.write("Keymap: keymap file not found !!" + '\n')
panel.close()
ExitSave = "[Exit] = " +_("Cancel") +"              [Ok] =" +_("Save")

class ConfigPORT(ConfigSequence):

	def __init__(self, default):
		ConfigSequence.__init__(self, seperator = ".", limits = [(1,65535)], default = default)

def main(session, **kwargs):
		session.open(OPD_panel)
def Apanel(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("OPD_panel"), main, "OPD_panel", 3)]
	else:
		return []



def Plugins(**kwargs):
	return [
	PluginDescriptor(name='OPD_panel', description='OPD_panel GUI 16/5/2016', where=PluginDescriptor.WHERE_MENU, fnc=Apanel),
	PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=camstart),
	PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=SwapAutostart),
	PluginDescriptor(name='OPD_panel', description='OPD_panel GUI 16/5/2016', where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]


MENU_SKIN = '<screen position="center,center" size="950,470" title="OPD Panel - Main Menu" >\n\t<ePixmap pixmap="/usr/lib/enigma2/python/OPENDROID/icons/redlogo.png" position="0,380" size="950,84" alphatest="on" zPosition="1"/>\n\t<ePixmap pixmap="/usr/lib/enigma2/python/OPENDROID/icons/opendroid_info.png" position="510,11" size="550,354" alphatest="on" zPosition="1"/>\n\t\t<widget source="global.CurrentTime" render="Label" position="450, 340" size="500,24" font="Regular;20" foregroundColor="#FFFFFF" halign="right" transparent="1" zPosition="5">\n\t\t<convert type="ClockToText">>Format%H:%M:%S</convert>\n\t</widget>\n\t<eLabel backgroundColor="#56C856" position="0,330" size="950,1" zPosition="0" />\n <widget name="Mlist" position="70,110" size="705,260" itemHeight="50" scrollbarMode="showOnDemand" transparent="1" zPosition="0" />\n\t<widget name="label1" position="10,340" size="490,25" font="Regular;20" transparent="1" foregroundColor="#f2e000" halign="left" />\n</screen>'
CONFIG_SKIN = '<screen position="center,center" size="600,440" title="PANEL Config" >\n\t<widget name="config" position="10,10" size="580,377" enableWrapAround="1" scrollbarMode="showOnDemand" />\n\t<widget name="labelExitsave" position="90,410" size="420,25" halign="center" font="Regular;20" transparent="1" foregroundColor="#f2e000" />\n</screen>'
INFO_SKIN = '<screen name="OPD_panel"  position="center,center" size="730,400" title="OPD_panel" >\n\t<widget name="label2" position="0,10" size="730,25" font="Regular;20" transparent="1" halign="center" foregroundColor="#f2e000" />\n\t<widget name="label1" position="10,45" size="710,350" font="Console;20" zPosition="1" backgroundColor="#251e1f20" transparent="1" />\n</screen>'
INFO_SKIN2 = '<screen name="OPD_panel"  position="center,center" size="530,400" title="OPD_panel" backgroundColor="#251e1f20">\n\t<widget name="label1" position="10,50" size="510,340" font="Regular;15" zPosition="1" backgroundColor="#251e1f20" transparent="1" />\n</screen>'

class PanelList(MenuList):
	if (getDesktop(0).size().width() == 1920):
		def __init__(self, list, font0 = 38, font1 = 28, itemHeight = 60, enableWrapAround = True):
			MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
			self.l.setFont(0, gFont("Regular", font0))
			self.l.setFont(1, gFont("Regular", font1))
			self.l.setItemHeight(itemHeight)
	else:
		def __init__(self, list, font0 = 24, font1 = 16, itemHeight = 50, enableWrapAround = True):	        
			MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
			self.l.setFont(0, gFont("Regular", font0))
			self.l.setFont(1, gFont("Regular", font1))
			self.l.setItemHeight(itemHeight)

def MenuEntryItem(entry):
	if (getDesktop(0).size().width() == 1920):
		res = [entry]
		res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 10), size=(60, 60), png=entry[0]))  
		res.append(MultiContentEntryText(pos=(110, 5), size=(690, 50), font=0, text=entry[1]))  
		return res
	else:
		res = [entry]
		res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 5), size=(100, 40), png=entry[0]))  
		res.append(MultiContentEntryText(pos=(110, 10), size=(440, 40), font=0, text=entry[1]))  
		return res

from Screens.PiPSetup import PiPSetup
from Screens.InfoBarGenerics import InfoBarPiP

def InfoEntryComponent(file):
	png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'icons/' + file + '.png'))
	if png == None:
		png = LoadPixmap('/usr/lib/enigma2/python/OPENDROID/icons/' + file + '.png')
		if png == None:
			png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'icons/default.png'))
			if png == None:
				png = LoadPixmap('/usr/lib/enigma2/python/OPENDROID/icons/default.png')
	res = png
	return res


class OPD_panel(Screen, InfoBarPiP):
	servicelist = None

	def __init__(self, session, services = None):
		global menu
		global inOPD_panel
		global pluginlist
		global INFOCONF
		Screen.__init__(self, session)
		self.session = session
		self.skin = MENU_SKIN
		self.onShown.append(self.setWindowTitle)
		self.service = None
		INFOCONF = 0
		pluginlist="False"
		try:
			print '[OPD_panel] SHOW'
			OPD_panel = self
		except:
			print '[OPD_Panel] Error Hide'

		if services is not None:
			self.servicelist = services
		else:
			self.servicelist = None
		self.list = []
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
			{
				"cancel": self.Exit,
				"upUp": self.up,
				"downUp": self.down,
				"ok": self.ok,
			}, 1)
		
		self['label1'] = Label(OPD_panel_Version)
		self["summary_description"] = StaticText("")

		self.Mlist = []
		if Check_Softcam():
			self.Mlist.append(MenuEntryItem((InfoEntryComponent('SoftcamSetup'), _("Softcam-Setup"), 'SoftcamSetup')))
		if Check_SysSoftcam() is "oscam":
			self.Mlist.append(MenuEntryItem((InfoEntryComponent('OScamInfo'), _("OScamInfo"), 'OScamInfo')))
		if Check_SysSoftcam() is "ncam":
			self.Mlist.append(MenuEntryItem((InfoEntryComponent('OScamInfo'), _("NcamInfo"), 'OScamInfo')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('ImageFlash'), _('Image-Flasher'), 'ImageFlash')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('opdBootLogoSelector'), _('opdBootLogo-Setup'), 'opdBootLogoSelector')))
                self.Mlist.append(MenuEntryItem((InfoEntryComponent('ClearMem'), _('ClearMem-Setup'), 'ClearMem')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('LogManager'), _('Log-Manager'), 'LogManager')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('KeymapSel'), _("Keymap Selection"), 'KeymapSel')))	
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('SoftwareManager'), _('Software-Manager'), 'software-manager')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('services'), _('services'), 'services')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('Infos'), _('Infos'), 'Infos')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('Infobar_Setup'), _('Infobar_Setup'), 'Infobar_Setup')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('Decoding_Setup'), _('Decoding_Setup'), 'Decoding_Setup')))
		self.onChangedEntry = []
		self["Mlist"] = PanelList([])
		self["Mlist"].l.setList(self.Mlist)
		menu = 0
		self["Mlist"].onSelectionChanged.append(self.selectionChanged)

	def getCurrentEntry(self):
		if self['Mlist'].l.getCurrentSelection():
			selection = self['Mlist'].l.getCurrentSelection()[0]
			self["summary_description"].text = selection[1]
			if (selection[0] is not None):
				return selection[0]

	def selectionChanged(self):
		item = self.getCurrentEntry()

	def setWindowTitle(self):
		self.setTitle(_("OPD-Main Menu"))

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		pass

	def right(self):
		pass

	def Red(self):
		self.showExtensionSelection1(Parameter="run")

	def Green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

	def Exit(self):
		global menu
		global inOPD_panel
		if menu == 0:
			try:
				self.service = self.session.nav.getCurrentlyPlayingServiceReference()
				service = self.service.toCompareString()
				servicename = ServiceReference.ServiceReference(service).getServiceName().replace('\xc2\x87', '').replace('\xc2\x86', '').ljust(16)
				print '[OPD_panel] HIDE'
				inOPD_panel = None
			except:
				print '[OPD_panel] Error Hide'
			self.close()
		elif menu == 1:
			self["Mlist"].moveToIndex(0)
			self["Mlist"].l.setList(self.oldmlist)
			menu = 0
			self["label1"].setText(OPD_panel_Version)
		elif menu == 2:
			self["Mlist"].moveToIndex(0)
			self["Mlist"].l.setList(self.oldmlist1)
			menu = 1
			self["label1"].setText(_("Infos"))
		else:
			pass

	def ok(self):
		global INFOCONF
		menu = self['Mlist'].l.getCurrentSelection()[0][2]
		print '[OPD_panel] MenuItem: ' + menu
		if menu == "services":
			self.services()
		elif menu == "Pluginbrowser":
			self.session.open(PluginBrowser)
		elif menu == "Infos":
			self.Infos()
		elif menu == "Info":
			self.session.open(Info, "SystemInfo")
		elif menu == "ImageVersion":
			self.session.open(Info, "ImageVersion")
		elif menu == "FreeSpace":
			self.session.open(Info, "FreeSpace")
		elif menu == "Network":
			self.session.open(Info, "Network")
		elif menu == "Mounts":
			self.session.open(Info, "Mounts")
		elif menu == "Kernel":
			self.session.open(Info, "Kernel")
		elif menu == "Ram":
			self.session.open(Info, "Free")
		elif menu == "Cpu":
			self.session.open(Info, "Cpu")
		elif menu == "Top":
			self.session.open(Info, "Top")
		elif menu == "MemInfo":
			self.session.open(Info, "MemInfo")
		elif menu == "Module":
			self.session.open(Info, "Module")
		elif menu == "Mtd":
			self.session.open(Info, "Mtd")
		elif menu == "Partitions":
			self.session.open(Info, "Partitions")
		elif menu == "Swap":
			self.session.open(Info, "Swap")
		elif menu == "SystemInfo":
			self.System()
		elif menu == "CronTimer":
			self.session.open(CronTimers)
		elif menu == "Infobar_Setup":
			from OPENDROID.GreenPanel import InfoBarSetup
			self.session.open(InfoBarSetup)
		elif menu == "Decoding_Setup":
			from OPENDROID.GreenPanel import DecodingSetup
			self.session.open(DecodingSetup)
		elif menu == "opdBootLogoSelector":
			from OPENDROID.OPD_Bootlogo import opdBootLogoSelector
			self.session.open(opdBootLogoSelector)
                elif menu == "ClearMem":
			from OPENDROID.ClearMem import ClearMem
			self.session.open(ClearMem)
		elif menu == "JobManager":
			self.session.open(ScriptRunner)
		elif menu == "software-manager":
			self.Software_Manager()
		elif menu == "OScamInfo":
			from Screens.OScamInfo import OscamInfoMenu
			self.session.open(OscamInfoMenu)
		elif menu == "SoftcamSetup":
			self.session.open(BluePanel)
		elif menu == "software-manager":
			self.Software_Manager()
		elif menu == "software-update":
			self.session.open(SoftwarePanel)
		elif menu == "Password-Change":
			self.session.open(PasswdScreen)
		elif menu == "backup-settings":
			self.session.openWithCallback(self.backupDone,BackupScreen, runBackup = True)
		elif menu == "restore-settings":
			self.backuppath = getBackupPath()
			self.backupfile = getBackupFilename()
			self.fullbackupfilename = self.backuppath + "/" + self.backupfile
			if os_path.exists(self.fullbackupfilename):
				self.session.openWithCallback(self.startRestore, MessageBox, _("Are you sure you want to restore your STB backup?\nSTB will restart after the restore"), default = False)
			else:
				self.session.open(MessageBox, _("Sorry no backups found!"), MessageBox.TYPE_INFO, timeout = 10)
		elif menu == "backup-files":
			self.session.open(BackupSelection,title=_("Default files/folders to backup"),configBackupDirs=config.plugins.configurationbackup.backupdirs_default,readOnly=True)
		elif menu == "backup-files-additional":
			self.session.open(BackupSelection,title=_("Additional files/folders to backup"),configBackupDirs=config.plugins.configurationbackup.backupdirs,readOnly=False)
		elif menu == "backup-files-excluded":
			self.session.open(BackupSelection,title=_("Files/folders to exclude from backup"),configBackupDirs=config.plugins.configurationbackup.backupdirs_exclude,readOnly=False)
		elif menu == "MultiQuickButton":
			self.session.open(MultiQuickButton)
		elif menu == "MountManager":
			self.session.open(DeviceManager)
		elif menu == "HddSetup":
			self.session.open(HddSetup)
		elif menu == "OscamSmartcard":
			self.session.open(OscamSmartcard)
		elif menu == "SwapManager":
			self.session.open(Swap)
		elif menu == "KeymapSel":
			self.session.open(KeymapSel)
		elif menu == "Edid":
			self.session.open(Info, "Edid")
		elif menu == "LogManager":
			self.session.open(LogManager)
		elif menu == "ImageFlash":
			self.session.open(FlashOnline)
		elif menu == "Samba":
			self.session.open(NetworkSamba)

	def services(self):
		global menu
		menu = 1
		self["label1"].setText(_("services"))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Password-Change'), _("Password-Change"), 'Password-Change')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('MountManager'), _("MountManager"), 'MountManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('HddSetup'), _("HddSetup"), 'HddSetup')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('CronTimer'), _("CronManager"), 'CronTimer')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('JobManager'), _("JobManager"), 'JobManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('SwapManager'), _("SwapManager"), 'SwapManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('OscamSmartcard'), _("OscamSmartcard"), 'OscamSmartcard')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Samba'), _("Samba"), 'Samba')))

		if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/plugin.pyo') is True:
			self.tlist.append(MenuEntryItem((InfoEntryComponent('MultiQuickButton'), _('MultiQuickButton'), 'MultiQuickButton')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)

	def Infos(self):
		global menu
		menu = 1
		self["label1"].setText(_("Infos"))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist1 = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('ImageVersion'), _("Image-Version"), 'ImageVersion')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('FreeSpace'), _("FreeSpace"), 'FreeSpace')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Kernel'), _("Kernel"), 'Kernel')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Mounts'), _("Mounts"), 'Mounts')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Network'), _("Network"), 'Network')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Ram'), _("Ram"), 'Ram')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('SystemInfo'), _("SystemInfo"), 'SystemInfo')))
		if SystemInfo["HAVEEDIDDECODE"]:
			self.tlist.append(MenuEntryItem((InfoEntryComponent('Edid'), _("EDID decode"), 'Edid')))
		self["Mlist"].moveToIndex(0)
		self["Mlist"].l.setList(self.tlist)
		self.oldmlist1 = self.tlist

	def System(self):
		global menu
		menu = 2
		self["label1"].setText(_("System Info"))
		self.tlist = []
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Cpu'), _("Cpu"), 'Cpu')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('MemInfo'), _("MemInfo"), 'MemInfo')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Mtd'), _("Mtd"), 'Mtd')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Module'), _("Module"), 'Module')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Partitions'), _("Partitions"), 'Partitions')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Swap'), _("Swap"), 'Swap')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Top'), _("Top"), 'Top')))
		self["Mlist"].moveToIndex(0)
		self["Mlist"].l.setList(self.tlist)

	def System_main(self):
		global menu
		menu = 1
		self["label1"].setText(_("System"))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Info'), _("Info"), 'Info')))
		self["Mlist"].moveToIndex(0)
		self["Mlist"].l.setList(self.tlist)

	def Software_Manager(self):
		global menu
		menu = 1
		self["label1"].setText(_("Software Manager"))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("SoftwareManager" ), _("Software update"), ("software-update"))))
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("BackupSettings" ), _("Backup Settings"), ("backup-settings"))))
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("RestoreSettings" ), _("Restore Settings"), ("restore-settings"))))
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("BackupFiles" ), _("Show default backup files"), ("backup-files"))))
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("BackupFilesAdditional" ), _("Select additional backup files"), ("backup-files-additional"))))
		self.tlist.append(MenuEntryItem((InfoEntryComponent ("BackupFilesExcluded" ), _("Select excluded backup files"), ("backup-files-excluded"))))
		self["Mlist"].moveToIndex(0)
		self["Mlist"].l.setList(self.tlist)

	def backupDone(self,retval = None):
		if retval is True:
			self.session.open(MessageBox, _("Backup done."), MessageBox.TYPE_INFO, timeout = 10)
		else:
			self.session.open(MessageBox, _("Backup failed."), MessageBox.TYPE_INFO, timeout = 10)

	def startRestore(self, ret = False):
		if (ret == True):
			self.exe = True
			self.session.open(RestoreScreen, runRestore = True)

class KeymapSel(ConfigListScreen, Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = ["SetupInfo", "Setup" ]
		Screen.setTitle(self, _("Keymap Selection") + "...")
		self.setup_title =  _("Keymap Selection") + "..."
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self["status"] = StaticText()
		self["footnote"] = Label()
		self["description"] = Label("")

		usrkey = eEnv.resolve("${datadir}/enigma2/keymap.usr")
		ntrkey = eEnv.resolve("${datadir}/enigma2/keymap.ntr")
		u80key = eEnv.resolve("${datadir}/enigma2/keymap.u80")
		self.actkeymap = self.getKeymap(config.usage.keymap.value)
		keySel = [ ('keymap.xml',_("Default  (keymap.xml)"))]
		if os.path.isfile(usrkey):
			keySel.append(('keymap.usr',_("User  (keymap.usr)")))
		if os.path.isfile(ntrkey):
			keySel.append(('keymap.ntr',_("Neutrino  (keymap.ntr)")))
		if os.path.isfile(u80key):
			keySel.append(('keymap.u80',_("UP80  (keymap.u80)")))
		if self.actkeymap == usrkey and not os.path.isfile(usrkey):
			setDefaultKeymap()
		if self.actkeymap == ntrkey and not os.path.isfile(ntrkey):
			setDefaultKeymap()
		if self.actkeymap == u80key and not os.path.isfile(u80key):
			setDefaultKeymap()
		self.keyshow = ConfigSelection(keySel)
		self.keyshow.value = self.actkeymap

		self.onChangedEntry = [ ]
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		self.createSetup()
		self["actions"] = ActionMap(["SetupActions", 'ColorActions'],
		{
			"ok": self.keySave,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.keySave,
			"menu": self.keyCancel,
		}, -2)

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_("Use Keymap"), self.keyshow))
		
		self["config"].list = self.list
		self["config"].setList(self.list)
		if config.usage.sort_settings.value:
			self["config"].list.sort()

	def selectionChanged(self):
		self["status"].setText(self["config"].getCurrent()[0])

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
		self.selectionChanged()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self["config"].getCurrent() and len(self["config"].getCurrent()) > 2 and self["config"].getCurrent()[2] or ""

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def saveAll(self):
		config.usage.keymap.value = eEnv.resolve("${datadir}/enigma2/" + self.keyshow.value)
		config.usage.keymap.save()
		configfile.save()
		if self.actkeymap != self.keyshow.value:
			self.changedFinished()

	def keySave(self):
		self.saveAll()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def keyCancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"))
		else:
			self.close()

	def getKeymap(self, file):
		return file[file.rfind('/') +1:]

	def changedFinished(self):
		self.session.openWithCallback(self.ExecuteRestart, MessageBox, _("Keymap changed, you need to restart the GUI") +"\n"+_("Do you want to restart now?"), MessageBox.TYPE_YESNO)
		self.close()

	def ExecuteRestart(self, result):
		if result:
			quitMainloop(3)
		else:
			self.close()

class Info(Screen):
	def __init__(self, session, info):
		self.service = None
		Screen.__init__(self, session)
		self.skin = INFO_SKIN
		self["label2"] = Label("INFO")
		self["label1"] =  ScrollLabel()
		if info == "SystemInfo":
			self.SystemInfo()
		elif info == "ImageVersion":
			self.ImageVersion()
		elif info == "FreeSpace":
			self.FreeSpace()
		elif info == "Mounts":
			self.Mounts()
		elif info == "Network":
			self.Network()
		elif info == "Kernel":
			self.Kernel()
		elif info == "Free":
			self.Free()
		elif info == "Cpu":
			self.Cpu()
		elif info == "Top":
			self.Top()
		elif info == "MemInfo":
			self.MemInfo()
		elif info == "Module":
			self.Module()
		elif info == "Mtd":
			self.Mtd()
		elif info == "Partitions":
			self.Partitions()
		elif info == "Swap":
			self.Swap()
		elif info == "Edid":
			self.Edid()

		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"],
		{
			"cancel": self.Exit,
			"ok": self.ok,
			"up": self.Up,
			"down": self.Down,
		}, -1)

	def Exit(self):
		self.close()

	def ok(self):
		self.close()

	def Down(self):
		self["label1"].pageDown()

	def Up(self):
		self["label1"].pageUp()

	def SystemInfo(self):
		try:
			self["label2"].setText(_("Image Info"))
			info1 = self.Do_cmd("cat", "/etc/version", None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def ImageVersion(self):
		try:
			self["label2"].setText(_("Image Version"))
			now = datetime.datetime.now()
			info1 = 'Date = ' + now.strftime("%d-%B-%Y") + "\n"
			info2 = 'Time = ' + now.strftime("%H:%M:%S") + "\n"
			info3 = self.Do_cmd("uptime", None, None)
			tmp = info3.split(",")
			info3 = 'Uptime = ' + tmp[0].lstrip() + "\n"
			info4 = self.Do_cmd("cat", "/etc/image-version", " | head -n 1")
			info4 = info4[9:]
			info4 = 'Imagetype = ' + info4 + "\n"
			info5 = 'Load = ' + self.Do_cmd("cat", "/proc/loadavg", None)
			info6 = self.Do_cut(info1 + info2 + info3 + info4 + info5)
			self["label1"].setText(info6)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def FreeSpace(self):
		try:
			self["label2"].setText(_("FreeSpace"))
			info1 = self.Do_cmd("df", None, "-h")
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Mounts(self):
		try:
			self["label2"].setText(_("Mounts"))
			info1 = self.Do_cmd("mount", None, None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Network(self):
		try:
			self["label2"].setText(_("Network"))
			info1 = self.Do_cmd("ifconfig", None, None) + '\n'
			info2 = self.Do_cmd("route", None, "-n")
			info3 = self.Do_cut(info1 + info2)
			self["label1"].setText(info3)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Kernel(self):
		try:
			self["label2"].setText(_("Kernel"))
			info0 = self.Do_cmd("cat", "/proc/version", None)
			info = info0.split('(')
			info1 = "Name = " + info[0] + "\n"
			info2 =  "Owner = " + info[1].replace(')','') + "\n"
			info3 =  "Mainimage = " + info[2][0:info[2].find(')')] + "\n"
			info4 = "Date = " + info[3][info[3].find('SMP')+4:len(info[3])]
			info5 = self.Do_cut(info1 + info2 + info3 + info4)
			self["label1"].setText(info5)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Free(self):
		try:
			self["label2"].setText(_("Ram"))
			info1 = self.Do_cmd("free", None, None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Cpu(self):
		try:
			self["label2"].setText(_("Cpu"))
			info1 = self.Do_cmd("cat", "/proc/cpuinfo", None, " | sed 's/\t\t/\t/'")
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Top(self):
		try:
			self["label2"].setText(_("Top"))
			info1 = self.Do_cmd("top", None, "-b -n1")
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def MemInfo(self):
		try:
			self["label2"].setText(_("MemInfo"))
			info1 = self.Do_cmd("cat", "/proc/meminfo", None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Module(self):
		try:
			self["label2"].setText(_("Module"))
			info1 = self.Do_cmd("cat", "/proc/modules", None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Mtd(self):
		try:
			self["label2"].setText(_("Mtd"))
			info1 = self.Do_cmd("cat", "/proc/mtd", None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Partitions(self):
		try:
			self["label2"].setText(_("Partitions"))
			info1 = self.Do_cmd("cat", "/proc/partitions", None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Swap(self):
		try:
			self["label2"].setText(_("Swap"))
			info0 = self.Do_cmd("cat", "/proc/swaps", None, " | sed 's/\t/ /g; s/[ ]* / /g'")
			info0 = info0.split("\n");
			info1 = ""
			for l in info0[1:]:
				l1 = l.split(" ")
				info1 = info1 + "Name: " + l1[0] + '\n'
				info1 = info1 + "Type: " + l1[1] + '\n'
				info1 = info1 + "Size: " + l1[2] + '\n'
				info1 = info1 + "Used: " + l1[3] + '\n'
				info1 = info1 + "Prio: " + l1[4] + '\n\n'
			if info1[-1:] == '\n': info1 = info1[:-1]
			if info1[-1:] == '\n': info1 = info1[:-1]
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))

	def Edid(self):
		try:
			self["label2"].setText(_("EDID decode"))
			info1 = self.Do_cmd("cat /proc/stb/hdmi/raw_edid | edid-decode", None, None)
			info1 = self.Do_cut(info1)
			self["label1"].setText(info1)
		except:
			self["label1"].setText(_("an internal error has occur"))


	def Do_find(self, text, search):
		text = text + ' '
		ret = ""
		pos = text.find(search)
		pos1 = text.find(" ", pos)
		if pos > -1:
			ret = text[pos + len(search):pos1]
		return ret

	def Do_cut(self, text):
		text1 = text.split("\n")
		text = ""
		for line in text1:
			text = text + line[:95] + "\n"
		if text[-1:] == '\n': text = text[:-1]
		return text

	def Do_cmd(self, cmd , file, arg , pipe = ""):
		try:
			if file != None:
				if os.path.exists(file) is True:
					o = command(cmd + ' ' + file + pipe, 0)
				else:
					o = "File not found: \n" + file
			else:
				if arg == None:
					o = command(cmd, 0)
				else:
					o = command(cmd + ' ' + arg, 0)
			return o
		except:
			o = ''
			return o

####################################################################################################################################
def getStbArch():
    if about.getChipSetString() in ('7366', '7376', '5272s', '7252', '7251', '7251S', '7252', '7252S'):
        return 'armv7ahf'
    elif about.getChipSetString() in 'pnx8493':
        return 'armv7a-vfp'
    elif about.getChipSetString() in ('meson-6', 'meson-64'):
        return 'cortexa9hf'
    elif about.getChipSetString() in ('7162', '7111'):
        return 'sh40'
    else:
        return 'mipsel'

def runBackCmd(cmd):
    eConsoleAppContainer().execute(cmd)


def getRealName(string):
    if string.startswith(' '):
        while string.startswith(' '):
            string = string[1:]

    return string


def hex_str2dec(str):
    ret = 0
    try:
        ret = int(re.sub('0x', '', str), 16)
    except:
        pass

    return ret


def norm_hex(str):
    return '%04x' % hex_str2dec(str)


def loadcfg(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    return wartosc


def loadbool(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    if wartosc == '1':
        return True
    else:
        return False


def unload_modules(name):
    try:
        from sys import modules
        del modules[name]
    except:
        pass


def wyszukaj_in(zrodlo, szukana_fraza):
    wyrazenie = string.strip(szukana_fraza)
    for linia in zrodlo.xreadlines():
        if wyrazenie in linia:
            return True

    return False


def wyszukaj_re(szukana_fraza):
    wyrazenie = re.compile(string.strip(szukana_fraza), re.IGNORECASE)
    zrodlo = open('/usr/share/enigma2/' + config.skin.primary_skin.value, 'r')
    for linia in zrodlo.xreadlines():
        if re.search(wyrazenie, linia) != None:
            return True

    zrodlo.close()
    return False


class FileDownloadJob(Job):

    def __init__(self, url, filename, file):
        Job.__init__(self, _('Downloading %s' % file))
        FileDownloadTask(self, url, filename)


class DownloaderPostcondition(Condition):

    def check(self, task):
        return task.returncode == 0

    def getErrorMessage(self, task):
        return self.error_message


class FileDownloadTask(Task):

    def __init__(self, job, url, path):
        Task.__init__(self, job, _('Downloading'))
        self.postconditions.append(DownloaderPostcondition())
        self.job = job
        self.url = url
        self.path = path
        self.error_message = ''
        self.last_recvbytes = 0
        self.error_message = None
        self.download = None
        self.aborted = False
        return

    def run(self, callback):
        self.callback = callback
        self.download = downloadWithProgress(self.url, self.path)
        self.download.addProgress(self.download_progress)
        self.download.start().addCallback(self.download_finished).addErrback(self.download_failed)
        print '[FileDownloadTask] downloading', self.url, 'to', self.path

    def abort(self):
        print '[FileDownloadTask] aborting', self.url
        if self.download:
            self.download.stop()
        self.aborted = True

    def download_progress(self, recvbytes, totalbytes):
        if recvbytes - self.last_recvbytes > 10000:
            self.progress = int(100 * (float(recvbytes) / float(totalbytes)))
            self.name = _('Downloading') + ' ' + '%d of %d kBytes' % (recvbytes / 1024, totalbytes / 1024)
            self.last_recvbytes = recvbytes

    def download_failed(self, failure_instance = None, error_message = ''):
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        Task.processFinished(self, 1)
        return

    def download_finished(self, string = ''):
        if self.aborted:
            self.finish(aborted=True)
        else:
            Task.processFinished(self, 0)
class PasswdScreen(Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        self.title = _('Change Root Password')
        try:
            self['title'] = StaticText(self.title)
        except:
            print 'self["title"] was not found in skin'

        self.user = 'root'
        self.output_line = ''
        self.list = []
        self['passwd'] = ConfigList(self.list)
        self['key_red'] = StaticText(_('Close'))
        self['key_green'] = StaticText(_('Set Password'))
        self['key_yellow'] = StaticText(_('new Random'))
        self['key_blue'] = StaticText(_('virt. Keyboard'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': self.close,
         'green': self.SetPasswd,
         'yellow': self.newRandom,
         'blue': self.bluePressed,
         'cancel': self.close}, -1)
        self.buildList(self.GeneratePassword())
        self.onShown.append(self.setWindowTitle)

    def newRandom(self):
        self.buildList(self.GeneratePassword())

    def buildList(self, password):
        self.password = password
        self.list = []
        self.list.append(getConfigListEntry(_('Enter new Password'), ConfigText(default=self.password, fixed_size=False)))
        self['passwd'].setList(self.list)

    def GeneratePassword(self):
        passwdChars = string.letters + string.digits
        passwdLength = 8
        return ''.join(Random().sample(passwdChars, passwdLength))

    def SetPasswd(self):
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.processOutputLine)
        retval = self.container.execute('passwd %s' % self.user)
        if retval == 0:
            self.session.open(MessageBox, _('Sucessfully changed password for root user to:\n%s ' % self.password), MessageBox.TYPE_INFO)
        else:
            self.session.open(MessageBox, _('Unable to change/reset password for root user'), MessageBox.TYPE_ERROR)

    def dataAvail(self, data):
        self.output_line += data
        if self.output_line.find('password changed.') == -1:
            if self.output_line.endswith('new UNIX password: '):
                print '1password:%s\n' % self.password
                self.processOutputLine(self.output_line[:1])

    def processOutputLine(self, line):
        if line.find('new UNIX password: '):
            print '2password:%s\n' % self.password
            self.container.write('%s\n' % self.password)
            self.output_line = ''

    def runFinished(self, retval):
        del self.container.dataAvail[:]
        del self.container.appClosed[:]
        del self.container
        self.close()

    def bluePressed(self):
        self.session.openWithCallback(self.VirtualKeyBoardTextEntry, VirtualKeyBoard, title=_('Enter your password here:'), text=self.password)

    def VirtualKeyBoardTextEntry(self, callback = None):
        if callback is not None:
            self.buildList(callback)
        return

    def setWindowTitle(self, title = None):
        if not title:
            title = self.title
        try:
            self['title'] = StaticText(title)
        except:
            pass   
