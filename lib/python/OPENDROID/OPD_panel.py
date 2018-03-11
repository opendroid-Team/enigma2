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
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS
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
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from OPENDROID.OscamSmartcard import *
from enigma import eConsoleAppContainer
from Tools.Directories import fileExists
from Tools.Downloader import downloadWithProgress
from boxbranding import getBoxType, getMachineName, getMachineBrand, getBrandOEM
from enigma import getDesktop
from Screens.InputBox import PinInput
import string
from random import Random
import os
import sys
import re, string
font = 'Regular;16'
import ServiceReference
import time
import datetime
inOPD_panel = None
config.softcam = ConfigSubsection()
config.softcam.actCam = ConfigText(visible_width=200)
config.softcam.actCam2 = ConfigText(visible_width=200)
config.softcam.waittime = ConfigSelection([('0',_("dont wait")),('1',_("1 second")), ('5',_("5 seconds")),('10',_("10 seconds")),('15',_("15 seconds")),('20',_("20 seconds")),('30',_("30 seconds"))], default='15')

if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/plugin.pyo') is True:
	try:
		from Plugins.Extensions.MultiQuickButton.plugin import *
	except:
		pass

from OPENDROID.BluePanel import *
from OPENDROID.CronManager import *
from OPENDROID.ScriptRunner import *
from OPENDROID.MountManager import *
from OPENDROID.SwapManager import Swap, SwapAutostart
from OPENDROID.SoftwarePanel import SoftwarePanel
from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen, RestoreScreen, BackupSelection, getBackupPath, getBackupFilename
import gettext

def _(txt):
	t = gettext.dgettext("OPD_panel", txt)
	if t == txt:
		print "[OPD_panel] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t
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
OPD_panel_Version = 'OPD PANEL V1.4 (By OPD-Team)'
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
		pluginlist = 'False'
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
		self['actions'] = ActionMap(['OkCancelActions', 'DirectionActions', 'ColorActions'], {'cancel': self.Exit,
                                                                                                      'upUp': self.up,
                                                                                              'downUp': self.down,
                                                                                              'ok': self.ok}, 1)
		self['label1'] = Label(OPD_panel_Version)
		self.Mlist = []
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('ImageFlash'), _('Image-Flasher'), 'ImageFlash')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('LogManager'), _('Log-Manager'), 'LogManager')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('SoftwareManager'), _('Software-Manager'), 'software-manager')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('services'), _('services'), 'services')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('Infos'), _('Infos'), 'Infos')))
		self.Mlist.append(MenuEntryItem((InfoEntryComponent('Infobar_Setup'), _('Infobar_Setup'), 'Infobar_Setup')))
		self.onChangedEntry = []
		self["Mlist"] = PanelList([])
		self["Mlist"].l.setList(self.Mlist)
		menu = 0
		self['Mlist'].onSelectionChanged.append(self.selectionChanged)

	def getCurrentEntry(self):
		if self['Mlist'].l.getCurrentSelection():
			selection = self['Mlist'].l.getCurrentSelection()[0]
			if selection[0] is not None:
				return selection[0]
		return

	def selectionChanged(self):
		item = self.getCurrentEntry()

	def setWindowTitle(self):
		self.setTitle(_('OPD-Main Menu'))

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		pass

	def right(self):
		pass

	def Red(self):
		self.showExtensionSelection1(Parameter='run')

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
			self['Mlist'].moveToIndex(0)
			self['Mlist'].l.setList(self.oldmlist)
			menu = 0
			self['label1'].setText(OPD_panel_Version)
		elif menu == 2:
			self['Mlist'].moveToIndex(0)
			self['Mlist'].l.setList(self.oldmlist1)
			menu = 1
			self['label1'].setText('Infos')
		return

	def ok(self):
		menu = self['Mlist'].l.getCurrentSelection()[0][2]
		print '[OPD_panel] MenuItem: ' + menu
		if menu == 'services':
			self.services()
		elif menu == 'Pluginbrowser':
			self.session.open(PluginBrowser)
		elif menu == 'Infos':
			self.Infos()
		elif menu == 'Service_Team':
			self.session.open(Info, 'Service_Team')
		elif menu == 'Info':
			self.session.open(Info, 'SystemInfo')
		elif menu == 'ImageVersion':
			self.session.open(Info, 'ImageVersion')
		elif menu == 'FreeSpace':
			self.session.open(Info, 'FreeSpace')
		elif menu == 'Network':
			self.session.open(Info, 'Network')
		elif menu == 'Mounts':
			self.session.open(Info, 'Mounts')
		elif menu == 'Kernel':
			self.session.open(Info, 'Kernel')
		elif menu == 'Ram':
			self.session.open(Info, 'Free')
		elif menu == 'Cpu':
			self.session.open(Info, 'Cpu')
		elif menu == 'Top':
			self.session.open(Info, 'Top')
		elif menu == 'MemInfo':
			self.session.open(Info, 'MemInfo')
		elif menu == 'Module':
			self.session.open(Info, 'Module')
		elif menu == 'Mtd':
			self.session.open(Info, 'Mtd')
		elif menu == 'Partitions':
			self.session.open(Info, 'Partitions')
		elif menu == 'Swap':
			self.session.open(Info, 'Swap')
		elif menu == 'SystemInfo':
			self.System()
		elif menu == 'CronManager':
			self.session.open(CronManager)
		elif menu == 'Infobar_Setup':
			from OPENDROID.GreenPanel import InfoBarSetup
			self.session.open(InfoBarSetup)
		elif menu == 'Decoding_Setup':
			from OPENDROID.GreenPanel import DecodingSetup
			self.session.open(DecodingSetup)
		elif menu == 'JobManager':
			self.session.open(ScriptRunner)
		elif menu == 'software-manager':
			self.Software_Manager()
		elif menu == 'software-update':
			self.session.open(SoftwarePanel)
		elif menu == 'backup-settings':
			self.session.openWithCallback(self.backupDone, BackupScreen, runBackup=True)
		elif menu == 'restore-settings':
			self.backuppath = getBackupPath()
			self.backupfile = getBackupFilename()
			self.fullbackupfilename = self.backuppath + '/' + self.backupfile
			if os_path.exists(self.fullbackupfilename):
				self.session.openWithCallback(self.startRestore, MessageBox, _('Are you sure you want to restore your STB backup?\nSTB will restart after the restore'))
			else:
				self.session.open(MessageBox, _('Sorry no backups found!'), MessageBox.TYPE_INFO, timeout=10)
		elif menu == 'backup-files':
			self.session.openWithCallback(self.backupfiles_choosen, BackupSelection)
		elif menu == 'MultiQuickButton':
			self.session.open(MultiQuickButton)
		elif menu == 'MountManager':
			self.session.open(DeviceManager)
		elif menu == 'OscamSmartcard':
			self.session.open(OscamSmartcard)
		elif menu == 'SwapManager':
			self.session.open(Swap)
		elif menu == 'RedPanel':
			self.session.open(RedPanel)
		elif menu == 'Yellow-Key-Action':
			self.session.open(YellowPanel)
		elif menu == 'LogManager':
			self.session.open(LogManager)
		elif menu == 'ImageFlash':
			self.session.open(FlashOnline)
		elif menu == 'Samba':
			self.session.open(NetworkSamba)

	def services(self):
		global menu
		menu = 1
		self['label1'].setText(_('services'))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('MountManager'), _('MountManager'), 'MountManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('CronManager'), _('CronManager'), 'CronManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('JobManager'), _('JobManager'), 'JobManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('SwapManager'), _('SwapManager'), 'SwapManager')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('OscamSmartcard'), _('OscamSmartcard'), 'OscamSmartcard')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Samba'), _('Samba'), 'Samba')))

		if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/plugin.pyo') is True:
			self.tlist.append(MenuEntryItem((InfoEntryComponent('MultiQuickButton'), _('MultiQuickButton'), 'MultiQuickButton')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)

	def Infos(self):
		global menu
		menu = 1
		self['label1'].setText(_('Infos'))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist1 = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Service_Team'), _('Service_Team'), 'Service_Team')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('ImageVersion'), _('Image-Version'), 'ImageVersion')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('FreeSpace'), _('FreeSpace'), 'FreeSpace')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Kernel'), _('Kernel'), 'Kernel')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Mounts'), _('Mounts'), 'Mounts')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Network'), _('Network'), 'Network')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Ram'), _('Ram'), 'Ram')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('SystemInfo'), _('SystemInfo'), 'SystemInfo')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)
		self.oldmlist1 = self.tlist

	def System(self):
		global menu
		menu = 2
		self['label1'].setText(_('System Info'))
		self.tlist = []
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Cpu'), _('Cpu'), 'Cpu')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('MemInfo'), _('MemInfo'), 'MemInfo')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Mtd'), _('Mtd'), 'Mtd')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Module'), _('Module'), 'Module')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Partitions'), _('Partitions'), 'Partitions')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Swap'), _('Swap'), 'Swap')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Top'), _('Top'), 'Top')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)

	def System_main(self):

		global menu
		menu = 1
		self["label1"].setText(_("Image/Remote Setup"))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Red-Key-Action'), _("Red Panel"), 'Red-Key-Action')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Blue-Key-Action'), _("Blue Panel"), 'Blue-Key-Action')))
		self["Mlist"].moveToIndex(0)
		self["Mlist"].l.setList(self.tlist)
	def System_main(self):
		global menu
		menu = 1
		self['label1'].setText(_('System'))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('Info'), _('Info'), 'Info')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)

	def Software_Manager(self):
		global menu
		menu = 1
		self['label1'].setText(_('Software Manager'))
		self.tlist = []
		self.oldmlist = []
		self.oldmlist = self.Mlist
		self.tlist.append(MenuEntryItem((InfoEntryComponent('SoftwareManager'), _('Software update'), 'software-update')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('BackupSettings'), _('Backup Settings'), 'backup-settings')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('RestoreSettings'), _('Restore Settings'), 'restore-settings')))
		self.tlist.append(MenuEntryItem((InfoEntryComponent('BackupFiles'), _('Choose backup files'), 'backup-files')))
		self['Mlist'].moveToIndex(0)
		self['Mlist'].l.setList(self.tlist)

	def backupfiles_choosen(self, ret):
		config.plugins.configurationbackup.backupdirs.save()
		config.plugins.configurationbackup.save()
		config.save()

	def backupDone(self, retval = None):
		if retval is True:
			self.session.open(MessageBox, _('Backup done.'), MessageBox.TYPE_INFO, timeout=10)
		else:
			self.session.open(MessageBox, _('Backup failed.'), MessageBox.TYPE_INFO, timeout=10)

	def startRestore(self, ret = False):
		if ret == True:
			self.exe = True
			self.session.open(RestoreScreen, runRestore=True)


class RedPanel(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = 'Setup'
		Screen.setTitle(self, _('RedPanel') + '...')
		self.setup_title = _('RedPanel') + '...'
		self['HelpWindow'] = Pixmap()
		self['HelpWindow'].hide()
		self['status'] = StaticText()
		self['footnote'] = Label('')
		self['description'] = Label(_(''))
		self['labelExitsave'] = Label('[Exit] = ' + _('Cancel') + '              [Ok] =' + _('Save'))
		self.onChangedEntry = []
		self.list = []
		ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
		self.createSetup()
		self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.keySave,
                                                                               'cancel': self.keyCancel,
                                                                       'red': self.keyCancel,
                                                                       'green': self.keySave,
         'menu': self.keyCancel}, -2)
		self['key_red'] = StaticText(_('Cancel'))
		self['key_green'] = StaticText(_('OK'))
		if self.selectionChanged not in self['config'].onSelectionChanged:
			self['config'].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_('Show OPD_panel Red-key'), config.plugins.OPD_panel_redpanel.enabled))
		self.list.append(getConfigListEntry(_('Show Softcam-Panel Red-key long'), config.plugins.OPD_panel_redpanel.enabledlong))
		self['config'].list = self.list
		self['config'].setList(self.list)
		if config.usage.sort_settings.value:
			self['config'].list.sort()
		return

	def selectionChanged(self):
		self['status'].setText(self['config'].getCurrent()[0])

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

		self.selectionChanged()

	def getCurrentEntry(self):
		return self['config'].getCurrent()[0]

	def getCurrentValue(self):
		return str(self['config'].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self['config'].getCurrent() and len(self['config'].getCurrent()) > 2 and self['config'].getCurrent()[2] or ''

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def saveAll(self):
		for x in self['config'].list:
			x[1].save()

		configfile.save()

	def keySave(self):
		self.saveAll()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self['config'].list:
			x[1].cancel()

		self.close()

	def keyCancel(self):
		if self['config'].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving settings?'))
		else:
			self.close()


class YellowPanel(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = 'Setup'
		Screen.setTitle(self, _('Yellow Key Action') + '...')
		self.setup_title = _('Yellow Key Action') + '...'
		self['HelpWindow'] = Pixmap()
		self['HelpWindow'].hide()
		self['status'] = StaticText()
		self['footnote'] = Label('')
		self['description'] = Label('')
		self['labelExitsave'] = Label('[Exit] = ' + _('Cancel') + '              [Ok] =' + _('Save'))
		self.onChangedEntry = []
		self.list = []
		ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
		self.createSetup()
		self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.keySave,
                                                                               'cancel': self.keyCancel,
                                                                       'red': self.keyCancel,
                                                                       'green': self.keySave,
         'menu': self.keyCancel}, -2)
		self['key_red'] = StaticText(_('Cancel'))
		self['key_green'] = StaticText(_('OK'))
		if self.selectionChanged not in self['config'].onSelectionChanged:
			self['config'].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_('Yellow Key Action'), config.plugins.OPD_panel_yellowkey.list))
		self['config'].list = self.list
		self['config'].setList(self.list)
		if config.usage.sort_settings.value:
			self['config'].list.sort()
		return

	def selectionChanged(self):
		self['status'].setText(self['config'].getCurrent()[0])

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

		self.selectionChanged()

	def getCurrentEntry(self):
		return self['config'].getCurrent()[0]

	def getCurrentValue(self):
		return str(self['config'].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self['config'].getCurrent() and len(self['config'].getCurrent()) > 2 and self['config'].getCurrent()[2] or ''

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def saveAll(self):
		for x in self['config'].list:
			x[1].save()

		configfile.save()

	def keySave(self):
		self.saveAll()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self['config'].list:
			x[1].cancel()

		self.close()

	def keyCancel(self):
		if self['config'].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving settings?'))
		else:
			self.close()

class Info(Screen):

	def __init__(self, session, info):
		self.service = None
		Screen.__init__(self, session)
		self.skin = INFO_SKIN
		self['label2'] = Label('INFO')
		self['label1'] = ScrollLabel()
		if info == 'Service_Team':
			self.Service_Team()
		if info == 'SystemInfo':
			self.SystemInfo()
		elif info == 'ImageVersion':
			self.ImageVersion()
		elif info == 'FreeSpace':
			self.FreeSpace()
		elif info == 'Mounts':
			self.Mounts()
		elif info == 'Network':
			self.Network()
		elif info == 'Kernel':
			self.Kernel()
		elif info == 'Free':
			self.Free()
		elif info == 'Cpu':
			self.Cpu()
		elif info == 'Top':
			self.Top()
		elif info == 'MemInfo':
			self.MemInfo()
		elif info == 'Module':
			self.Module()
		elif info == 'Mtd':
			self.Mtd()
		elif info == 'Partitions':
			self.Partitions()
		elif info == 'Swap':
			self.Swap()
		self['actions'] = ActionMap(['OkCancelActions', 'DirectionActions'], {'cancel': self.Exit,
                                                                                      'ok': self.ok,
                                                                              'up': self.Up,
                                                                              'down': self.Down}, -1)
		return

	def Exit(self):
		self.close()

	def ok(self):
		self.close()

	def Down(self):
		self['label1'].pageDown()

	def Up(self):
		self['label1'].pageUp()

	def Service_Team(self):
		try:
			self['label2'].setText('INFO')
			info1 = self.Do_cmd('cat', '/etc/motd', None)
			if info1.find('wElc0me') > -1:
				info1 = info1[info1.find('wElc0me'):len(info1)] + '\n'
				info1 = info1.replace('|', '')
			else:
				info1 = info1[info1.find('INFO'):len(info1)] + '\n'
			info2 = self.Do_cmd('cat', '/etc/image-version', None)
			info3 = self.Do_cut(info1 + info2)
			self['label1'].setText(info3)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def SystemInfo(self):
		try:
			self['label2'].setText(_('Image Info'))
			info1 = self.Do_cmd('cat', '/etc/version', None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def ImageVersion(self):
		try:
			self['label2'].setText(_('Image Version'))
			now = datetime.now()
			info1 = 'Date = ' + now.strftime('%d-%B-%Y') + '\n'
			info2 = 'Time = ' + now.strftime('%H:%M:%S') + '\n'
			info3 = self.Do_cmd('uptime', None, None)
			tmp = info3.split(',')
			info3 = 'Uptime = ' + tmp[0].lstrip() + '\n'
			info4 = self.Do_cmd('cat', '/etc/image-version', ' | head -n 1')
			info4 = info4[9:]
			info4 = 'Imagetype = ' + info4 + '\n'
			info5 = 'Load = ' + self.Do_cmd('cat', '/proc/loadavg', None)
			info6 = self.Do_cut(info1 + info2 + info3 + info4 + info5)
			self['label1'].setText(info6)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def FreeSpace(self):
		try:
			self['label2'].setText(_('FreeSpace'))
			info1 = self.Do_cmd('df', None, '-h')
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Mounts(self):
		try:
			self['label2'].setText(_('Mounts'))
			info1 = self.Do_cmd('mount', None, None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Network(self):
		try:
			self['label2'].setText(_('Network'))
			info1 = self.Do_cmd('ifconfig', None, None) + '\n'
			info2 = self.Do_cmd('route', None, '-n')
			info3 = self.Do_cut(info1 + info2)
			self['label1'].setText(info3)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Kernel(self):
		try:
			self['label2'].setText(_('Kernel'))
			info0 = self.Do_cmd('cat', '/proc/version', None)
			info = info0.split('(')
			info1 = 'Name = ' + info[0] + '\n'
			info2 = 'Owner = ' + info[1].replace(')', '') + '\n'
			info3 = 'Mainimage = ' + info[2][0:info[2].find(')')] + '\n'
			info4 = 'Date = ' + info[3][info[3].find('SMP') + 4:len(info[3])]
			info5 = self.Do_cut(info1 + info2 + info3 + info4)
			self['label1'].setText(info5)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Free(self):
		try:
			self['label2'].setText(_('Ram'))
			info1 = self.Do_cmd('free', None, None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Cpu(self):
		try:
			self['label2'].setText(_('Cpu'))
			info1 = self.Do_cmd('cat', '/proc/cpuinfo', None, " | sed 's/\t\t/\t/'")
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Top(self):
		try:
			self['label2'].setText(_('Top'))
			info1 = self.Do_cmd('top', None, '-b -n1')
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def MemInfo(self):
		try:
			self['label2'].setText(_('MemInfo'))
			info1 = self.Do_cmd('cat', '/proc/meminfo', None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Module(self):
		try:
			self['label2'].setText(_('Module'))
			info1 = self.Do_cmd('cat', '/proc/modules', None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Mtd(self):
		try:
			self['label2'].setText(_('Mtd'))
			info1 = self.Do_cmd('cat', '/proc/mtd', None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Partitions(self):
		try:
			self['label2'].setText(_('Partitions'))
			info1 = self.Do_cmd('cat', '/proc/partitions', None)
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Swap(self):
		try:
			self['label2'].setText(_('Swap'))
			info0 = self.Do_cmd('cat', '/proc/swaps', None, " | sed 's/\t/ /g; s/[ ]* / /g'")
			info0 = info0.split('\n')
			info1 = ''
			for l in info0[1:]:
				l1 = l.split(' ')
				info1 = info1 + 'Name: ' + l1[0] + '\n'
				info1 = info1 + 'Type: ' + l1[1] + '\n'
				info1 = info1 + 'Size: ' + l1[2] + '\n'
				info1 = info1 + 'Used: ' + l1[3] + '\n'
				info1 = info1 + 'Prio: ' + l1[4] + '\n\n'

			if info1[-1:] == '\n':
				info1 = info1[:-1]
			if info1[-1:] == '\n':
				info1 = info1[:-1]
			info1 = self.Do_cut(info1)
			self['label1'].setText(info1)
		except:
			self['label1'].setText(_('an internal error has occur'))

		return

	def Do_find(self, text, search):
		text = text + ' '
		ret = ''
		pos = text.find(search)
		pos1 = text.find(' ', pos)
		if pos > -1:
			ret = text[pos + len(search):pos1]
		return ret

	def Do_cut(self, text):
		text1 = text.split('\n')
		text = ''
		for line in text1:
			text = text + line[:95] + '\n'

		if text[-1:] == '\n':
			text = text[:-1]
		return text

	def Do_cmd(self, cmd, file, arg, pipe = ''):
		try:
			if file != None:
				if os.path.exists(file) is True:
					o = command(cmd + ' ' + file + pipe, 0)
				else:
					o = 'File not found: \n' + file
			elif arg == None:
				o = command(cmd, 0)
			else:
				o = command(cmd + ' ' + arg, 0)
			return o
		except:
			o = ''
			return o

		return
####################################################################################################################################
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


