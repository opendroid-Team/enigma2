from boxbranding import getImageVersion
import os
from enigma import eTimer
from os import system, listdir, chdir, getcwd, remove as os_remove
import os
import urllib
from urllib2 import Request, urlopen, URLError, HTTPError
from Screens.Screen import Screen
from Components.PluginList import PluginList, PluginEntryComponent, PluginCategoryComponent, PluginDownloadComponent
from Components.Harddisk import harddiskmanager
from Components.Sources.StaticText import StaticText
from Components import Ipkg
from Components.config import config, ConfigSubsection, ConfigYesNo, getConfigListEntry, configfile, ConfigText
from Screens.Ipkg import Ipkg as Ipkg_1
from Components.config import config
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_ACTIVE_SKIN
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Screens.InputBox import InputBox, PinInput
from Screens.ChoiceBox import ChoiceBox
from enigma import eTimer, eConsoleAppContainer
from enigma import eConsoleAppContainer, eDVBDB
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.FileList import FileList
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import PluginList
from Components.Button import Button
from Components.Input import Input
from Plugins.Plugin import PluginDescriptor
from Tools.BoundFunction import boundFunction
from ServiceReference import ServiceReference
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_SKIN_IMAGE, fileExists, pathExists, createDir, SCOPE_PLUGINS
from Tools import Notifications
from Tools.NumericalTextInput import NumericalTextInput
from twisted.web.client import getPage, downloadPage
import os
from Components.Button import Button
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView
from ServiceReference import ServiceReference
import os, sys
from os import listdir
from twisted.web.client import downloadPage 
import urllib
from enigma import *
import sys,os
from Tools.LoadPixmap import LoadPixmap
from Components.Ipkg import IpkgComponent
from Components.ScrollLabel import ScrollLabel
from os import popen, system, remove, listdir, chdir, getcwd, statvfs, mkdir, path, walk
from Components.ProgressBar import ProgressBar
def getVarSpaceKb():
    try:
        s = statvfs('/')
    except OSError:
        return (0, 0)

    return (float(s.f_bfree * (s.f_bsize / 1024)), float(s.f_blocks * (s.f_bsize / 1024)))

class AddonsUtility(Screen):
	skin = """
		<screen name="AddonsUtility" position="center,60" size="800,635" title="OPENDROID Addons Manager" >
		<widget name="list" position="80,100" size="710,350" zPosition="2" scrollbarMode="showOnDemand" transparent="1"/>
		<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="red" backgroundColor="red" transparent="1" />		
		<widget name="key_green" position="400,600" zPosition="1" size="100,45" font="Regular;18" foregroundColor="green" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list=[]
		self.entrylist = []  #List reset
		self.entrylist.append((_("Plugin"), "Plg", "/usr/lib/enigma2/python/OPENDROID/icons/Plugin.png"))
		self.entrylist.append((_("Picons-HDD"), "Pcs-HDD", "/usr/lib/enigma2/python/OPENDROID/icons/Picons-HDD.png"))
		self.entrylist.append((_("Picons-USB"), "Pcs-USB", "/usr/lib/enigma2/python/OPENDROID/icons/Picons-USB.png"))
		self.entrylist.append((_("Setting"), "Stg", "/usr/lib/enigma2/python/OPENDROID/icons/Setting_list.png"))
		self.entrylist.append((_("Skin"), "Sks", "/usr/lib/enigma2/python/OPENDROID/icons/Skins.png"))
		self.entrylist.append((_("BootLogo"), "Logo","/usr/lib/enigma2/python/OPENDROID/icons/BootLogo.png"))
		self['list'] = PluginList(self.list)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Remove"))
		self["key_yellow"] = Label(_("Restart E2"))
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{
			'ok': self.KeyOk,
			"red": self.close,
			'back': self.close,
			'green': self.Remove,
			'yellow' : self.RestartE2,
			
		})
		self.onLayoutFinish.append(self.updateList)
		
	
	def Remove(self):
		self.session.open(AddonsRemove)
	def RestartE2(self):
		msg="Do you want Restart GUI now ?" 
		self.session.openWithCallback(self.Finish, MessageBox, msg, MessageBox.TYPE_YESNO)
	def Finish(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()
	def KeyOk(self):
		selection = self["list"].getCurrent()[0][1]
		print selection
		if (selection == "Plg"):
			addons = 'Plugins'
			self.title = ' OPENDROID Downloader Plugins'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Pcs-HDD"):
			addons = 'Picons-HDD'
			self.title = 'Picons-HDD'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Pcs-USB"):
			addons = 'Picons-USB'
			self.title = 'Picons-USB'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Stg"):
			addons = 'Settings'
			self.title = ' OPENDROID Downloader Settings '
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Sks"):
			addons = 'Skins'
			self.title = ' OPENDROID Downloader Skins '
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Logo"):
			addons = 'BootLogo'
			self.title = ' OPENDROID Downloader BootLogo '
			self.session.open(Connection_Server, addons, self.title)
		else:
			self.messpopup("Selection error")

	def messpopup(self,msg):
		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO)
	
	def updateList(self):
		for i in self.entrylist:
				res = [i]
				res.append(MultiContentEntryText(pos=(60, 5), size=(300, 48), font=0, text=i[0]))
				picture=LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
				res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(48, 48), png=picture))
				self.list.append(res)
		self['list'].l.setList(self.list)


###################################################################################
#Remove Addons
###################################################################################
class	AddonsRemove(Screen):
	
	skin = """
		<screen name="AddonsRemove" position="80,160" size="1100,450" title="Remove Plugins">
				<widget name="list" position="5,0" size="560,300" itemHeight="49" foregroundColor="white" backgroundColor="black" transparent="1" scrollbarMode="showOnDemand" zPosition="2" enableWrapAround="1" />
				<widget name="status" position="580,43" size="518,300" font="Regular;16" halign="center" noWrap="1" transparent="1" />
				<eLabel name="" position="580,6" size="517,30" font="Regular; 22"text="List of plugins to uninstall" zPosition="3" halign="center" />
				<widget name="text" position="580,345" size="519,60" zPosition="1" font="Regular;20" halign="center" valign="center" foregroundColor="green" transparent="1" />
				<widget name="key_green" render="Label" position="46,366" zPosition="2" size="190,22" valign="center" halign="left" font="Regular;21" transparent="1" backgroundColor="foreground" />
				<ePixmap position="5,365" size="35,27" pixmap="/usr/share/enigma2/skin_default/buttons/key_green.png" alphatest="blend" zPosition="2" />
				<widget name="key_red" render="Label" position="360,366" zPosition="2" size="190,22" valign="center" halign="left" font="Regular;21" transparent="1" backgroundColor="foreground" />
				<ePixmap position="320,365" size="35,27" pixmap="/usr/share/enigma2/skin_default/buttons/key_blue.png" alphatest="blend" zPosition="2" />
				<eLabel name="new eLabel" position="570,0" size="2,400" zPosition="5" foregroundColor="unc0c0c0" backgroundColor="darkgrey" />
				<eLabel name="spaceused" text="% Flash Used..." position="45,414" size="150,20" font="Regular;19" halign="left" foregroundColor="white" backgroundColor="black" transparent="1" zPosition="5" />
				<widget name="spaceused" position="201,415" size="894,20" foregroundColor="white" backgroundColor="blue" zPosition="3" />
			</screen>"""
	
	REMOVE = 1		  
	DOWNLOAD = 0
	PLUGIN_PREFIX = 'enigma2-plugin-'
	lastDownloadDate = None

	def __init__(self, session, type = 1, needupdate = True):
		Screen.__init__(self, session)
		global pluginfiles
		self.type = type
		self.needupdate = needupdate
		self.container = eConsoleAppContainer()
		self.container.appClosed.append(self.runFinished)
		self.container.dataAvail.append(self.dataAvail)
		self.onLayoutFinish.append(self.startRun)
		self.onShown.append(self.setWindowTitle)
		self.setuplist = []

		self.list = []
		self["list"] = PluginList(self.list)
		self.pluginlist = []
		self.expanded = []
		self.installedplugins = []
		self.plugins_changed = False
		self.reload_settings = False
		self.check_settings = False
		self.check_bootlogo = False
		self.install_settings_name = ''
		self.remove_settings_name = ''
		self['spaceused'] = ProgressBar()		
		self["status"] = ScrollLabel()
		self['key_green']  = Label(_('Remove'))	
		self['key_red']  = Label(_('Exit'))
		
		if self.type == self.DOWNLOAD:
			self["text"] = Label(_("Downloading plugin information. Please wait..."))
		self.run = 0
		self.remainingdata = ""
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.go,
			"back": self.requestClose,
			"green": self.install,
			"red": self.close,
			
		})
		if os.path.isfile('/usr/bin/opkg'):
			self.ipkg = '/usr/bin/opkg'
			self.ipkg_install = self.ipkg + ' install --force-overwrite'
			self.ipkg_remove =  self.ipkg + ' remove --autoremove --force-depends'
		else:
			self.ipkg = 'ipkg'
			self.ipkg_install = 'ipkg install --force-overwrite -force-defaults'
			self.ipkg_remove =  self.ipkg + ' remove --autoremove --force-depends'

	def go(self):
		sel = self["list"].l.getCurrentSelection()
		if sel is None:
			return

		sel = sel[0]
		if isinstance(sel, str): 

			if sel in self.expanded:

				self.expanded.remove(sel)
			else:
				self.expanded.append(sel)
			self.updateList()

		else:
			pluginfiles = ""
			if self.type == self.DOWNLOAD:
				if sel.name in self.setuplist:
					self.setuplist.remove("%s" % sel.name)
					if not self.setuplist:
						pluginfiles += "no Plugin select"
						self.listplugininfo(pluginfiles)
					else:
						list = self.setuplist
						for item in list:
							pluginfiles += item
							pluginfiles += "\n" 
							self.listplugininfo(pluginfiles)
							self.list = []
				else:
					self.setuplist.append("%s" % sel.name)
					list = self.setuplist
					for item in list:
						pluginfiles += item
						pluginfiles += "\n"
						self.listplugininfo(pluginfiles)
						self.list = []

			elif self.type == self.REMOVE:
				if sel.name in self.setuplist:
					self.setuplist.remove("%s" % sel.name)
					if not self.setuplist:
						pluginfiles += "no Plugin select"
						self.listplugininfo(pluginfiles)
					else:
						list = self.setuplist
						for item in list:
							pluginfiles += item
							pluginfiles += "\n" 
							self.listplugininfo(pluginfiles)
							self.list = []
				else:
					self.setuplist.append("%s" % sel.name)
					list = self.setuplist
					for item in list:
						pluginfiles += item
						pluginfiles += "\n"
						self.listplugininfo(pluginfiles)
						self.list = []

	def install(self):
		PLUGIN_PREFIX = 'enigma2-plugin-'
		cmdList = []
		for item in self.setuplist:
			cmdList.append((IpkgComponent.CMD_REMOVE, { "package": PLUGIN_PREFIX + item }))
		self.session.open(Ipkg_1, cmdList = cmdList)
	
		
	def listplugininfo(self, pluginfiles):
		try:
			pluginfiles.split("/n")	
			self["status"].setText(pluginfiles)
		except:
			self["status"].setText("")



	def requestClose(self):
		if self.plugins_changed:
			plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		if self.reload_settings:
			self["text"].setText(_("Reloading bouquets and services..."))
			eDVBDB.getInstance().reloadBouquets()
			eDVBDB.getInstance().reloadServicelist()
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.container.appClosed.remove(self.runFinished)
		self.container.dataAvail.remove(self.dataAvail)
		self.close()

	def resetPostInstall(self):
		try:
			del self.postInstallCall
		except:
			pass

	def installDestinationCallback(self, result):
		if result is not None:
			dest = result[1]
			if dest.startswith('/'):
				
				dest = os.path.normpath(dest)
				extra = '--add-dest %s:%s -d %s' % (dest,dest,dest)
				Ipkg.opkgAddDestination(dest)
			else:
				extra = '-d ' + dest
			self.doInstall(self.installFinished, pluginnames + ' ' + extra)
		else:
			self.resetPostInstall()

	def runInstall(self, val):
		if val:
			if self.type == self.DOWNLOAD:
				if pluginnames.startswith("enigma2-plugin-picons-"):
					supported_filesystems = frozenset(('vfat','ext4', 'ext3', 'ext2', 'reiser', 'reiser4', 'jffs2', 'ubifs', 'rootfs'))
					candidates = []
					import Components.Harddisk
					mounts = Components.Harddisk.getProcMounts()
					for partition in harddiskmanager.getMountedPartitions(False, mounts):
						if partition.filesystem(mounts) in supported_filesystems:
							candidates.append((partition.description, partition.mountpoint))
					if candidates:
						from Components.Renderer import Picon
						self.postInstallCall = Picon.initPiconPaths
						self.session.openWithCallback(self.installDestinationCallback, ChoiceBox, title=_("Install picons on"), list=candidates)
					return
				elif pluginnames.startswith("enigma2-plugin-display-picon"):
					supported_filesystems = frozenset(('vfat','ext4', 'ext3', 'ext2', 'reiser', 'reiser4', 'jffs2', 'ubifs', 'rootfs'))
					candidates = []
					import Components.Harddisk
					mounts = Components.Harddisk.getProcMounts()
					for partition in harddiskmanager.getMountedPartitions(False, mounts):
						if partition.filesystem(mounts) in supported_filesystems:
							candidates.append((partition.description, partition.mountpoint))
					if candidates:
						from Components.Renderer import LcdPicon
						self.postInstallCall = LcdPicon.initLcdPiconPaths
						self.session.openWithCallback(self.installDestinationCallback, ChoiceBox, title=_("Install lcd picons on"), list=candidates)
					return
				self.install_settings_name = pluginnames
				self.install_bootlogo_name = pluginnames
				if pluginnames.startswith('enigma2-plugin-settings-'):
					self.check_settings = True
					self.startIpkgListInstalled(self.PLUGIN_PREFIX + 'settings-*')
				elif pluginnames.startswith('enigma2-plugin-bootlogo-'):
					self.check_bootlogo = True
					self.startIpkgListInstalled(self.PLUGIN_PREFIX + 'bootlogo-*')
				else:
					self.runSettingsInstall()
			elif self.type == self.REMOVE:
				self.doRemove(self.installFinished, pluginnames + " --force-remove --force-depends")

	def doRemove(self, callback, pkgname):
		self.session.openWithCallback(callback, Console, cmdlist = [self.ipkg_remove + Ipkg.opkgExtraDestinations() + " " + self.PLUGIN_PREFIX + pkgname, "sync"], closeOnSuccess = True)
					
	def doInstall(self, callback, pkgname):
		self.session.openWithCallback(callback, Console, cmdlist = [self.ipkg_install + " " + self.PLUGIN_PREFIX + pkgname, "sync"], closeOnSuccess = True)

	def runSettingsRemove(self, val):
		if val:
			self.doRemove(self.runSettingsInstall, self.remove_settings_name)

	def runBootlogoRemove(self, val):
		if val:
			self.doRemove(self.runSettingsInstall, self.remove_bootlogo_name + " --force-remove --force-depends")

	def runSettingsInstall(self):
		self.doInstall(self.installFinished, self.install_settings_name)

	def ConvertSize(self, size):
		size = int(size)
		if size >= 1073741824:
			Size = '%0.2f TB' % (size / 1073741824.0)
		elif size >= 1048576:
			Size = '%0.2f GB' % (size / 1048576.0)
		elif size >= 1024:
			Size = '%0.2f MB' % (size / 1024.0)
		else:
			Size = '%0.2f KB' % size
		return str(Size)

	def setWindowTitle(self):
		diskSpace = getVarSpaceKb()
		percFree = int(diskSpace[0] / diskSpace[1] * 100)
		percUsed = int((diskSpace[1] - diskSpace[0]) / diskSpace[1] * 100)
		self.setTitle('%s - %s: %s (%d%%)' % (_('Remove plugins'),
		 _('Free'),
		 self.ConvertSize(int(diskSpace[0])),
		 percFree))
		self['spaceused'].setValue(percUsed)

	def startIpkgListInstalled(self, pkgname = PLUGIN_PREFIX + '*'):
		self.container.execute(self.ipkg + Ipkg.opkgExtraDestinations() + " list_installed '%s'" % pkgname)

	def startIpkgListAvailable(self):
		self.container.execute(self.ipkg + Ipkg.opkgExtraDestinations() + " list '" + self.PLUGIN_PREFIX + "*'")

	def startRun(self):
		listsize = self["list"].instance.size()
		self["list"].instance.hide()
		self.listWidth = listsize.width()
		self.listHeight = listsize.height()
		if self.type == self.DOWNLOAD:
			self.container.execute(self.ipkg + " update")
		elif self.type == self.REMOVE:
			self.run = 1
			self.startIpkgListInstalled()			

	def installFinished(self):
		if hasattr(self, 'postInstallCall'):
			try:
				self.postInstallCall()
			except Exception, ex:
				print "[PluginBrowser] postInstallCall failed:", ex
			self.resetPostInstall()
		try:
			os.unlink('/tmp/opkg.conf')
		except:
			pass
		for plugin in self.pluginlist:
			if plugin[3] == pluginnames:
				self.pluginlist.remove(plugin)
				break
		self.plugins_changed = True
		if pluginnames.startswith("enigma2-plugin-settings-"):
			self.reload_settings = True
		self.expanded = []
		self.updateList()
		self["list"].moveToIndex(0)

	def runFinished(self, retval):
		if self.check_settings:
			self.check_settings = False
			self.runSettingsInstall()
			return
		if self.check_bootlogo:
			self.check_bootlogo = False
			self.runSettingsInstall()
			return
		self.remainingdata = ""
		if self.run == 0:
			self.run = 1
			if self.type == self.DOWNLOAD:
				self.startIpkgListInstalled()
		elif self.run == 1 and self.type == self.DOWNLOAD:
			self.run = 2
			from Components import opkg
			pluginlist = []
			self.pluginlist = pluginlist
			for plugin in opkg.enumPlugins(self.PLUGIN_PREFIX):
				if plugin[0] not in self.installedplugins:
					pluginlist.append(plugin + (plugin[0][15:],))
			if pluginlist:
				pluginlist.sort()
				self.updateList()
				self["list"].instance.show()
			else:
				self["text"].setText(_("No new plugins found"))
		else:
			if self.pluginlist:
				self.updateList()
				self["list"].instance.show()
			else:
				if self.type == self.DOWNLOAD:
					self["text"].setText(_("Sorry feeds are down for maintenance"))

	def dataAvail(self, str):
		if self.type == self.DOWNLOAD and ('wget returned 1' or 'wget returned 255' or '404 Not Found') in str:
			self.run = 3
			return

		
		str = self.remainingdata + str
		
		lines = str.split('\n')
		
		if len(lines[-1]):
			
			self.remainingdata = lines[-1]
			lines = lines[0:-1]
		else:
			self.remainingdata = ""

		if self.check_settings:
			self.check_settings = False
			self.remove_settings_name = str.split(' - ')[0].replace(self.PLUGIN_PREFIX, '')
			self.session.openWithCallback(self.runSettingsRemove, MessageBox, _('You already have a channel list installed,\nwould you like to remove\n"%s"?') % self.remove_settings_name)
			return

		if self.check_bootlogo:
			self.check_bootlogo = False
			self.remove_bootlogo_name = str.split(' - ')[0].replace(self.PLUGIN_PREFIX, '')
			self.session.openWithCallback(self.runBootlogoRemove, MessageBox, _('You already have a bootlogo installed,\nwould you like to remove\n"%s"?') % self.remove_bootlogo_name)
			return

		if self.run == 1:
			for x in lines:
				plugin = x.split(" - ", 2)
				
				if len(plugin) >= 2:
					if not plugin[0].endswith('-dev') and not plugin[0].endswith('-staticdev') and not plugin[0].endswith('-dbg') and not plugin[0].endswith('-doc'):
						if plugin[0] not in self.installedplugins:
							if self.type == self.DOWNLOAD:
								self.installedplugins.append(plugin[0])
							else:
								if len(plugin) == 2:
									plugin.append('')
								plugin.append(plugin[0][15:])
								self.pluginlist.append(plugin)
			self.pluginlist.sort()

	def updateList(self):
		list = []
		expandableIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/expandable-plugins.png"))
		expandedIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/expanded-plugins.png"))
		verticallineIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/verticalline-plugins.png"))

		self.plugins = {}
		for x in self.pluginlist:
			split = x[3].split('-', 1)
			if len(split) < 2:
				continue
			if not self.plugins.has_key(split[0]):
				self.plugins[split[0]] = []

			self.plugins[split[0]].append((PluginDescriptor(name = x[3], description = x[2], icon = verticallineIcon), split[1], x[1]))

		temp = self.plugins.keys()
		if config.usage.sort_pluginlist.value:
			temp.sort()
		for x in temp:
			if x in self.expanded:
				list.append(PluginCategoryComponent(x, expandedIcon, self.listWidth))
				list.extend([PluginDownloadComponent(plugin[0], plugin[1], plugin[2], self.listWidth) for plugin in self.plugins[x]])
			else:
				list.append(PluginCategoryComponent(x, expandableIcon, self.listWidth))
		self.list = list
		self["list"].l.setList(list)
		self["text"] = Label(_("Downloading plugin information complete."))
			
###################
#Download Addons
###################
class Connection_Server(Screen):
	try:
		s = statvfs('/')
	except OSError:
		return (0, 0)

	return (float(s.f_bfree * (s.f_bsize / 1024)), float(s.f_blocks * (s.f_bsize / 1024)))

class RSList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		try:
			font = skin.fonts.get("RSList", ("Regular", 35, 50))
			self.l.setFont(0, gFont(font[0], font[1]))
			self.l.setItemHeight(font[2])
		except:
			self.l.setFont(0, gFont("Regular", 35))
			self.l.setItemHeight(50)

##############################################################################

def RSListEntry(download, state):
	res = [(download)]
	try:
		x, y, w, h , x1, y1, w1, h1 = skin.parameters.get("RSList",(60, 0, 1920, 38, 5, 6, 38, 38))
	except:
		x = 50
		y = 0
		w = 820
		h = 38
		x1 = 8
		y1 = 10
		w1 = 38
		h1 = 38
	res.append(MultiContentEntryText(pos=(x, y), size=(w, h), font=0, text=download))
	if state == 0:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(x1, y1), size=(w1,h1), png=LoadPixmap(cached=True, desktop=getDesktop(0), path=resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/buttons/button_green.png"))))
	else:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(x1, y1), size=(w1,h1), png=LoadPixmap(cached=True, desktop=getDesktop(0), path=resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/buttons/button_red.png"))))

	print "res =", res
	return res


class AddonsUtility(Screen):
	skin = """
		<screen name="AddonsUtility" position="center,60" size="800,635" title="OPENDROID Addons Manager" >
		<widget name="list" position="80,100" size="710,350" zPosition="2" scrollbarMode="showOnDemand" transparent="1"/>
		<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="red" backgroundColor="red" transparent="1" />		
		<widget name="key_green" position="400,600" zPosition="1" size="100,45" font="Regular;18" foregroundColor="green" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list=[]
		self.entrylist = []  #List reset
		self.entrylist.append((_("Plugin"), "Plg", "/usr/lib/enigma2/python/OPENDROID/icons/Plugin.png"))
		self.entrylist.append((_("Picons-HDD"), "Pcs-HDD", "/usr/lib/enigma2/python/OPENDROID/icons/Picons-HDD.png"))
		self.entrylist.append((_("Picons-USB"), "Pcs-USB", "/usr/lib/enigma2/python/OPENDROID/icons/Picons-USB.png"))
		self.entrylist.append((_("Setting"), "Stg", "/usr/lib/enigma2/python/OPENDROID/icons/Setting_list.png"))
		self.entrylist.append((_("Skin"), "Sks", "/usr/lib/enigma2/python/OPENDROID/icons/Skins.png"))
		self.entrylist.append((_("BootLogo"), "Logo","/usr/lib/enigma2/python/OPENDROID/icons/BootLogo.png"))
		self['list'] = PluginList(self.list)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Remove"))
		self["key_yellow"] = Label(_("Restart E2"))
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{
			'ok': self.KeyOk,
			"red": self.close,
			'back': self.close,
			'green': self.Remove,
			'yellow' : self.RestartE2,
			
		})
		self.onLayoutFinish.append(self.updateList)
		
	
	def Remove(self):
		self.session.open(AddonsRemove)
	def RestartE2(self):
		msg="Do you want Restart GUI now ?" 
		self.session.openWithCallback(self.Finish, MessageBox, msg, MessageBox.TYPE_YESNO)
	def Finish(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()
	def KeyOk(self):
		selection = self["list"].getCurrent()[0][1]
		print selection
		if (selection == "Plg"):
			addons = 'Plugins'
			self.title = ' OPENDROID Downloader Plugins'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Pcs-HDD"):
			addons = 'Picons-HDD'
			self.title = 'Picons-HDD'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Pcs-USB"):
			addons = 'Picons-USB'
			self.title = 'Picons-USB'
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Stg"):
			addons = 'Settings'
			self.title = ' OPENDROID Downloader Settings '
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Sks"):
			addons = 'Skins'
			self.title = ' OPENDROID Downloader Skins '
			self.session.open(Connection_Server, addons, self.title)
		elif (selection == "Logo"):
			addons = 'BootLogo'
			self.title = ' OPENDROID Downloader BootLogo '
			self.session.open(Connection_Server, addons, self.title)
		else:
			self.messpopup("Selection error")

	def messpopup(self,msg):
		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO)
	
	def updateList(self):
		for i in self.entrylist:
				res = [i]
				res.append(MultiContentEntryText(pos=(60, 5), size=(300, 48), font=0, text=i[0]))
				picture=LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
				res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(48, 48), png=picture))
				self.list.append(res)
		self['list'].l.setList(self.list)


###################################################################################
#Remove Addons
###################################################################################
class	AddonsRemove(Screen):
	
	skin = """
		<screen name="AddonsRemove" position="80,160" size="1100,450" title="Remove Plugins">
				<widget name="list" position="5,0" size="560,300" itemHeight="49" foregroundColor="white" backgroundColor="black" transparent="1" scrollbarMode="showOnDemand" zPosition="2" enableWrapAround="1" />
				<widget name="status" position="580,43" size="518,300" font="Regular;16" halign="center" noWrap="1" transparent="1" />
				<eLabel name="" position="580,6" size="517,30" font="Regular; 22"text="List of plugins to uninstall" zPosition="3" halign="center" />
				<widget name="text" position="580,345" size="519,60" zPosition="1" font="Regular;20" halign="center" valign="center" foregroundColor="green" transparent="1" />
				<widget name="key_green" render="Label" position="46,366" zPosition="2" size="190,22" valign="center" halign="left" font="Regular;21" transparent="1" backgroundColor="foreground" />
				<ePixmap position="5,365" size="35,27" pixmap="/usr/share/enigma2/skin_default/buttons/key_green.png" alphatest="blend" zPosition="2" />
				<widget name="key_red" render="Label" position="360,366" zPosition="2" size="190,22" valign="center" halign="left" font="Regular;21" transparent="1" backgroundColor="foreground" />
				<ePixmap position="320,365" size="35,27" pixmap="/usr/share/enigma2/skin_default/buttons/key_blue.png" alphatest="blend" zPosition="2" />
				<eLabel name="new eLabel" position="570,0" size="2,400" zPosition="5" foregroundColor="unc0c0c0" backgroundColor="darkgrey" />
				<eLabel name="spaceused" text="% Flash Used..." position="45,414" size="150,20" font="Regular;19" halign="left" foregroundColor="white" backgroundColor="black" transparent="1" zPosition="5" />
				<widget name="spaceused" position="201,415" size="894,20" foregroundColor="white" backgroundColor="blue" zPosition="3" />
			</screen>"""
	
	REMOVE = 1		  
	DOWNLOAD = 0
	PLUGIN_PREFIX = 'enigma2-plugin-'
	lastDownloadDate = None

	def __init__(self, session, type = 1, needupdate = True):
		Screen.__init__(self, session)
		global pluginfiles
		self.type = type
		self.needupdate = needupdate
		self.container = eConsoleAppContainer()
		self.container.appClosed.append(self.runFinished)
		self.container.dataAvail.append(self.dataAvail)
		self.onLayoutFinish.append(self.startRun)
		self.onShown.append(self.setWindowTitle)
		self.setuplist = []

		self.list = []
		self["list"] = PluginList(self.list)
		self.pluginlist = []
		self.expanded = []
		self.installedplugins = []
		self.plugins_changed = False
		self.reload_settings = False
		self.check_settings = False
		self.check_bootlogo = False
		self.install_settings_name = ''
		self.remove_settings_name = ''
		self['spaceused'] = ProgressBar()		
		self["status"] = ScrollLabel()
		self['key_green']  = Label(_('Remove'))	
		self['key_red']  = Label(_('Exit'))
		
		if self.type == self.DOWNLOAD:
			self["text"] = Label(_("Downloading plugin information. Please wait..."))
		self.run = 0
		self.remainingdata = ""
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.go,
			"back": self.requestClose,
			"green": self.install,
			"red": self.close,
			
		})
		if os.path.isfile('/usr/bin/opkg'):
			self.ipkg = '/usr/bin/opkg'
			self.ipkg_install = self.ipkg + ' install --force-overwrite'
			self.ipkg_remove =  self.ipkg + ' remove --autoremove --force-depends'
		else:
			self.ipkg = 'ipkg'
			self.ipkg_install = 'ipkg install --force-overwrite -force-defaults'
			self.ipkg_remove =  self.ipkg + ' remove --autoremove --force-depends'

	def go(self):
		sel = self["list"].l.getCurrentSelection()
		if sel is None:
			return

		sel = sel[0]
		if isinstance(sel, str): 

			if sel in self.expanded:

				self.expanded.remove(sel)
			else:
				self.expanded.append(sel)
			self.updateList()

		else:
			pluginfiles = ""
			if self.type == self.DOWNLOAD:
				if sel.name in self.setuplist:
					self.setuplist.remove("%s" % sel.name)
					if not self.setuplist:
						pluginfiles += "no Plugin select"
						self.listplugininfo(pluginfiles)
					else:
						list = self.setuplist
						for item in list:
							pluginfiles += item
							pluginfiles += "\n" 
							self.listplugininfo(pluginfiles)
							self.list = []
				else:
					self.setuplist.append("%s" % sel.name)
					list = self.setuplist
					for item in list:
						pluginfiles += item
						pluginfiles += "\n"
						self.listplugininfo(pluginfiles)
						self.list = []

			elif self.type == self.REMOVE:
				if sel.name in self.setuplist:
					self.setuplist.remove("%s" % sel.name)
					if not self.setuplist:
						pluginfiles += "no Plugin select"
						self.listplugininfo(pluginfiles)
					else:
						list = self.setuplist
						for item in list:
							pluginfiles += item
							pluginfiles += "\n" 
							self.listplugininfo(pluginfiles)
							self.list = []
				else:
					self.setuplist.append("%s" % sel.name)
					list = self.setuplist
					for item in list:
						pluginfiles += item
						pluginfiles += "\n"
						self.listplugininfo(pluginfiles)
						self.list = []

	def install(self):
		PLUGIN_PREFIX = 'enigma2-plugin-'
		cmdList = []
		for item in self.setuplist:
			cmdList.append((IpkgComponent.CMD_REMOVE, { "package": PLUGIN_PREFIX + item }))
		self.session.open(Ipkg_1, cmdList = cmdList)
	
		
	def listplugininfo(self, pluginfiles):
		try:
			pluginfiles.split("/n")	
			self["status"].setText(pluginfiles)
		except:
			self["status"].setText("")



	def requestClose(self):
		if self.plugins_changed:
			plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		if self.reload_settings:
			self["text"].setText(_("Reloading bouquets and services..."))
			eDVBDB.getInstance().reloadBouquets()
			eDVBDB.getInstance().reloadServicelist()
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.container.appClosed.remove(self.runFinished)
		self.container.dataAvail.remove(self.dataAvail)
		self.close()

	def resetPostInstall(self):
		try:
			del self.postInstallCall
		except:
			pass

	def installDestinationCallback(self, result):
		if result is not None:
			dest = result[1]
			if dest.startswith('/'):
				
				dest = os.path.normpath(dest)
				extra = '--add-dest %s:%s -d %s' % (dest,dest,dest)
				Ipkg.opkgAddDestination(dest)
			else:
				extra = '-d ' + dest
			self.doInstall(self.installFinished, pluginnames + ' ' + extra)
		else:
			self.resetPostInstall()

	def runInstall(self, val):
		if val:
			if self.type == self.DOWNLOAD:
				if pluginnames.startswith("enigma2-plugin-picons-"):
					supported_filesystems = frozenset(('vfat','ext4', 'ext3', 'ext2', 'reiser', 'reiser4', 'jffs2', 'ubifs', 'rootfs'))
					candidates = []
					import Components.Harddisk
					mounts = Components.Harddisk.getProcMounts()
					for partition in harddiskmanager.getMountedPartitions(False, mounts):
						if partition.filesystem(mounts) in supported_filesystems:
							candidates.append((partition.description, partition.mountpoint))
					if candidates:
						from Components.Renderer import Picon
						self.postInstallCall = Picon.initPiconPaths
						self.session.openWithCallback(self.installDestinationCallback, ChoiceBox, title=_("Install picons on"), list=candidates)
					return
				elif pluginnames.startswith("enigma2-plugin-display-picon"):
					supported_filesystems = frozenset(('vfat','ext4', 'ext3', 'ext2', 'reiser', 'reiser4', 'jffs2', 'ubifs', 'rootfs'))
					candidates = []
					import Components.Harddisk
					mounts = Components.Harddisk.getProcMounts()
					for partition in harddiskmanager.getMountedPartitions(False, mounts):
						if partition.filesystem(mounts) in supported_filesystems:
							candidates.append((partition.description, partition.mountpoint))
					if candidates:
						from Components.Renderer import LcdPicon
						self.postInstallCall = LcdPicon.initLcdPiconPaths
						self.session.openWithCallback(self.installDestinationCallback, ChoiceBox, title=_("Install lcd picons on"), list=candidates)
					return
				self.install_settings_name = pluginnames
				self.install_bootlogo_name = pluginnames
				if pluginnames.startswith('enigma2-plugin-settings-'):
					self.check_settings = True
					self.startIpkgListInstalled(self.PLUGIN_PREFIX + 'settings-*')
				elif pluginnames.startswith('enigma2-plugin-bootlogo-'):
					self.check_bootlogo = True
					self.startIpkgListInstalled(self.PLUGIN_PREFIX + 'bootlogo-*')
				else:
					self.runSettingsInstall()
			elif self.type == self.REMOVE:
				self.doRemove(self.installFinished, pluginnames + " --force-remove --force-depends")

	def doRemove(self, callback, pkgname):
		self.session.openWithCallback(callback, Console, cmdlist = [self.ipkg_remove + Ipkg.opkgExtraDestinations() + " " + self.PLUGIN_PREFIX + pkgname, "sync"], closeOnSuccess = True)
					
	def doInstall(self, callback, pkgname):
		self.session.openWithCallback(callback, Console, cmdlist = [self.ipkg_install + " " + self.PLUGIN_PREFIX + pkgname, "sync"], closeOnSuccess = True)

	def runSettingsRemove(self, val):
		if val:
			self.doRemove(self.runSettingsInstall, self.remove_settings_name)

	def runBootlogoRemove(self, val):
		if val:
			self.doRemove(self.runSettingsInstall, self.remove_bootlogo_name + " --force-remove --force-depends")

	def runSettingsInstall(self):
		self.doInstall(self.installFinished, self.install_settings_name)

	def ConvertSize(self, size):
		size = int(size)
		if size >= 1073741824:
			Size = '%0.2f TB' % (size / 1073741824.0)
		elif size >= 1048576:
			Size = '%0.2f GB' % (size / 1048576.0)
		elif size >= 1024:
			Size = '%0.2f MB' % (size / 1024.0)
		else:
			Size = '%0.2f KB' % size
		return str(Size)

	def setWindowTitle(self):
		diskSpace = getVarSpaceKb()
		percFree = int(diskSpace[0] / diskSpace[1] * 100)
		percUsed = int((diskSpace[1] - diskSpace[0]) / diskSpace[1] * 100)
		self.setTitle('%s - %s: %s (%d%%)' % (_('Remove plugins'),
		 _('Free'),
		 self.ConvertSize(int(diskSpace[0])),
		 percFree))
		self['spaceused'].setValue(percUsed)

	def startIpkgListInstalled(self, pkgname = PLUGIN_PREFIX + '*'):
		self.container.execute(self.ipkg + Ipkg.opkgExtraDestinations() + " list_installed '%s'" % pkgname)

	def startIpkgListAvailable(self):
		self.container.execute(self.ipkg + Ipkg.opkgExtraDestinations() + " list '" + self.PLUGIN_PREFIX + "*'")

	def startRun(self):
		listsize = self["list"].instance.size()
		self["list"].instance.hide()
		self.listWidth = listsize.width()
		self.listHeight = listsize.height()
		if self.type == self.DOWNLOAD:
			self.container.execute(self.ipkg + " update")
		elif self.type == self.REMOVE:
			self.run = 1
			self.startIpkgListInstalled()			

	def installFinished(self):
		if hasattr(self, 'postInstallCall'):
			try:
				self.postInstallCall()
			except Exception, ex:
				print "[PluginBrowser] postInstallCall failed:", ex
			self.resetPostInstall()
		try:
			os.unlink('/tmp/opkg.conf')
		except:
			pass
		for plugin in self.pluginlist:
			if plugin[3] == pluginnames:
				self.pluginlist.remove(plugin)
				break
		self.plugins_changed = True
		if pluginnames.startswith("enigma2-plugin-settings-"):
			self.reload_settings = True
		self.expanded = []
		self.updateList()
		self["list"].moveToIndex(0)

	def runFinished(self, retval):
		if self.check_settings:
			self.check_settings = False
			self.runSettingsInstall()
			return
		if self.check_bootlogo:
			self.check_bootlogo = False
			self.runSettingsInstall()
			return
		self.remainingdata = ""
		if self.run == 0:
			self.run = 1
			if self.type == self.DOWNLOAD:
				self.startIpkgListInstalled()
		elif self.run == 1 and self.type == self.DOWNLOAD:
			self.run = 2
			from Components import opkg
			pluginlist = []
			self.pluginlist = pluginlist
			for plugin in opkg.enumPlugins(self.PLUGIN_PREFIX):
				if plugin[0] not in self.installedplugins:
					pluginlist.append(plugin + (plugin[0][15:],))
			if pluginlist:
				pluginlist.sort()
				self.updateList()
				self["list"].instance.show()
			else:
				self["text"].setText(_("No new plugins found"))
		else:
			if self.pluginlist:
				self.updateList()
				self["list"].instance.show()
			else:
				if self.type == self.DOWNLOAD:
					self["text"].setText(_("Sorry feeds are down for maintenance"))

	def dataAvail(self, str):
		if self.type == self.DOWNLOAD and ('wget returned 1' or 'wget returned 255' or '404 Not Found') in str:
			self.run = 3
			return

		
		str = self.remainingdata + str
		
		lines = str.split('\n')
		
		if len(lines[-1]):
			
			self.remainingdata = lines[-1]
			lines = lines[0:-1]
		else:
			self.remainingdata = ""

		if self.check_settings:
			self.check_settings = False
			self.remove_settings_name = str.split(' - ')[0].replace(self.PLUGIN_PREFIX, '')
			self.session.openWithCallback(self.runSettingsRemove, MessageBox, _('You already have a channel list installed,\nwould you like to remove\n"%s"?') % self.remove_settings_name)
			return

		if self.check_bootlogo:
			self.check_bootlogo = False
			self.remove_bootlogo_name = str.split(' - ')[0].replace(self.PLUGIN_PREFIX, '')
			self.session.openWithCallback(self.runBootlogoRemove, MessageBox, _('You already have a bootlogo installed,\nwould you like to remove\n"%s"?') % self.remove_bootlogo_name)
			return

		if self.run == 1:
			for x in lines:
				plugin = x.split(" - ", 2)
				
				if len(plugin) >= 2:
					if not plugin[0].endswith('-dev') and not plugin[0].endswith('-staticdev') and not plugin[0].endswith('-dbg') and not plugin[0].endswith('-doc'):
						if plugin[0] not in self.installedplugins:
							if self.type == self.DOWNLOAD:
								self.installedplugins.append(plugin[0])
							else:
								if len(plugin) == 2:
									plugin.append('')
								plugin.append(plugin[0][15:])
								self.pluginlist.append(plugin)
			self.pluginlist.sort()

	def updateList(self):
		list = []
		expandableIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/expandable-plugins.png"))
		expandedIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/expanded-plugins.png"))
		verticallineIcon = LoadPixmap(resolveFilename(SCOPE_ACTIVE_SKIN, "icons/verticalline-plugins.png"))

		self.plugins = {}
		for x in self.pluginlist:
			split = x[3].split('-', 1)
			if len(split) < 2:
				continue
			if not self.plugins.has_key(split[0]):
				self.plugins[split[0]] = []

			self.plugins[split[0]].append((PluginDescriptor(name = x[3], description = x[2], icon = verticallineIcon), split[1], x[1]))

		temp = self.plugins.keys()
		if config.usage.sort_pluginlist.value:
			temp.sort()
		for x in temp:
			if x in self.expanded:
				list.append(PluginCategoryComponent(x, expandedIcon, self.listWidth))
				list.extend([PluginDownloadComponent(plugin[0], plugin[1], plugin[2], self.listWidth) for plugin in self.plugins[x]])
			else:
				list.append(PluginCategoryComponent(x, expandableIcon, self.listWidth))
		self.list = list
		self["list"].l.setList(list)
		self["text"] = Label(_("Downloading plugin information complete."))
			
###################
#Download Addons
###################
class Connection_Server(Screen):


	skin = """
		<screen position="center,center" size="800,500" title=" " >
			<widget name="text" position="100,20" size="200,30" font="Regular;20" halign="left" />
			<ePixmap position="300,25"   zPosition="2" size="140,40" pixmap="skin_default/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="list" position="50,80" size="730,300" scrollbarMode="showOnDemand" />

			<ePixmap name="red"    position="0,460"   zPosition="2" size="140,40" pixmap="skin_default/buttons/button_red.png" transparent="1" alphatest="on" />
			<ePixmap name="green"  position="140,460" zPosition="2" size="140,40" pixmap="skin_default/buttons/button_green.png" transparent="1" alphatest="on" />

			<widget name="key_red" position="0,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
			<widget name="key_green" position="140,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 

			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="100,230" zPosition="4" size="300,25" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
		</screen>"""

	def __init__(self, session, addons, title):

		self.skin = Connection_Server.skin
		Screen.__init__(self, session)

		self.list = []
		self["text"] = Label()
		self["list"] = List(self.list)
		self["list"] = RSList([])
		self['lab1'] = Label(_("It is recommended !!\nto mount the appropriate device before downloading.\nOtherwise\nPress OK to continue"))
		self["info"] = Label()
		self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
			"red": self.close,
			"green": self.okClicked,
		}, -1)
		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		self.mytitle = title
		self.addon = addons
		self["title"] = Button(title)
		self.icount = 0
		self.names = []
		self.onLayoutFinish.append(self.openTest)

	def openTest(self):
		self["info"].setText("Downloading list...")
		testno = 1

		xurl = 'http://images.opendroid.org/Addons/'+ self.addon + '/list'
		print "xurl =", xurl
		getPage(xurl).addCallback(self.gotPage).addErrback(self.getfeedError)

	def gotPage(self, html):
		print "html = ", html 
		self.data = []
		icount = 0
		self.data = html.splitlines()
		list = []
		for line in self.data:
			ipkname = self.data[icount] 
			print "gotPage icount, ipk name =", icount, ipkname 
			remname = ipkname
			state = self.getstate(ipkname)
			print "gotPage state, remname = ", state, remname
			list.append(RSListEntry(remname, state))
			icount = icount+1
			self["list"].setList(list)
			print 'self["list"] A =', self["list"] 
			self["info"].setText("")

	def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error


	def getstate(self, ipkname):
		item = "/etc/ipkinst/" + ipkname
		if os.path.exists(item):
			state = 1
			return state
		else:
			state = 0
			return state

	def okClicked(self):
		print "Here in okClicked A"
		sel = self["list"].getSelectionIndex()
		ipk = self.data[sel]
		addon = self.addon
		ipkinst = Installer_Addons(self.session, ipk, addon)
		ipkinst.openTest()

	def keyLeft(self):
		self["text"].left()
	
	def keyRight(self):
		self["text"].right()
	
	def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)

class Installer_Addons(Screen):
	skin = """
		<screen position="center,center" size="800,500" title="Play Options" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,20" size="750,350" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="50,50" zPosition="4" size="500,400" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="left" valign="top" />
			<ePixmap name="red"    position="0,450"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
			<ePixmap name="green"  position="140,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
			<ePixmap name="yellow" position="280,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
			<!--ePixmap name="blue"   position="420,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /--> 
			<widget name="key_red" position="0,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
			<widget name="key_green" position="140,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
			<!--widget name="key_yellow" position="280,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
			<widget name="key_blue" position="420,450" size="140,50" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /-->
		</screen>"""
 
	def __init__(self, session, ipk, addon):
		Screen.__init__(self, session)
		self.skin = Installer_Addons.skin
		title = "Addon Install"
		self.setTitle(title)
		self["list"] = MenuList([])
		self["info"] = Label()
		self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Install"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			"red": self.close,
			"green": self.okClicked,
			"yellow": self.install,
			"cancel": self.cancel,
			"ok": self.close,
		}, -2)
		print "Installer_Addons : ipk =", ipk
		self.icount = 0
		self.ipk = ipk
		self.addon = addon
		self.onLayoutFinish.append(self.openTest)
		txt = "You have selected\n\n" + ipk + "\n\n\nPlease press Download"
		self["info"].setText(txt)
		self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
		self.onLayoutFinish.append(self.openTest)
	def openTest(self):
		if not os.path.exists("/etc/ipkinst"): 
			cmd = "mkdir -p /etc/ipkinst"
			os.system(cmd)
		xurl1 = 'http://images.opendroid.org/Addons/' + self.addon + '/'
		print "xurl1 =", xurl1
		xurl2 = xurl1 + self.ipk
		print "xurl2 =", xurl2
		xdest = "/tmp/" + self.ipk
		print "xdest =", xdest
		self.cmd1 = 'wget -O "' + xdest + '" "' + xurl2 + '"'
		self.cmd2 = "opkg install --force-overwrite /tmp/" + self.ipk
		self.cmd3 = "touch /etc/ipkinst/" + self.ipk + " &"
		self.okClicked()    
	def okClicked(self):
		plug = self.ipk
		title = _("Installing addon %s" %(plug))
		cmd = self.cmd1 + " && " + self.cmd2 + " && " + self.cmd3
		self.session.open(Console,_(title),[cmd])
	def LastJobView(self):
		currentjob = None
		for job in JobManager.getPendingJobs():
			currentjob = job

		if currentjob is not None:
			self.session.open(JobView, currentjob)
 
	def install(self):
		cmd = "opkg install --force-overwrite /tmp/" + self.ipk + ">/tmp/ipk.log"
		print "cmd =", cmd
		title = _("Installing addon %s" %(plug))
		self.session.open(Console,_(title),[cmd])
		self.endinstall()

	def viewLog(self):
		self["info"].setText("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n       Press Exit to continue...")
		if os.path.isfile("/tmp/ipk.log")is not True :
			cmd = "touch /tmp/ipk.log"
			os.system(cmd)
		else:	
			myfile = file(r"/tmp/ipk.log")
			icount = 0
			data = []
			for line in myfile.readlines():
				data.append(icount)
				print line
				num = len(line)
				data[icount] = (line[:-1])
				print data[icount]
				icount = icount + 1
			self["list"].setList(data)
			self.endinstall()

	def endinstall(self):
		path="/tmp"
		tmplist = []
		ipkname = 0  
		tmplist=os.listdir(path)
		print "files in /tmp", tmplist
		icount = 0
		for name in tmplist:
			nipk = tmplist[icount]
			if (nipk[-3:]=="ipk"):
				ipkname = nipk
			icount = icount+1       

		if ipkname != 0:
			print "endinstall ipk name =", ipkname 
			ipos = ipkname.find("_")
			remname = ipkname[:ipos]
			print "endinstall remname =", remname
			f=open('/etc/ipklist_installed', 'a')
			f1= remname + "\n"
			f.write(f1)
			cmd = "rm /tmp/*.ipk"
			os.system(cmd)

	def cancel(self):
		self.close()

	def keyLeft(self):
		self["text"].left()
	
	def keyRight(self):
		self["text"].right()

	def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)        
 
class downloadJob(Job):
	def __init__(self, toolbox, cmdline, filename, filetitle):
		Job.__init__(self, _("Downloading"))
		self.toolbox = toolbox
		self.retrycount = 0
		
		downloadTask(self, cmdline, filename, filetitle)

	def retry(self):
		assert self.status == self.FAILED
		self.retrycount += 1
		self.restart()
	
class downloadTask(Task):
	ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
	def __init__(self, job, cmdline, filename, filetitle):
		Task.__init__(self, job, filetitle)
		self.setCmdline(cmdline)
		self.filename = filename
		self.toolbox = job.toolbox
		self.error = None
		self.lasterrormsg = None
		
	def processOutput(self, data):
		try:
			if data.endswith('%)'):
				startpos = data.rfind("sec (")+5
				if startpos and startpos != -1:
					self.progress = int(float(data[startpos:-4]))
			elif data.find('%') != -1:
				tmpvalue = data[:data.find("%")]
				tmpvalue = tmpvalue[tmpvalue.rfind(" "):].strip()
				tmpvalue = tmpvalue[tmpvalue.rfind("(")+1:].strip()
				self.progress = int(float(tmpvalue))
			else:
				Task.processOutput(self, data)
		except Exception, errormsg:
			print "Error processOutput: " + str(errormsg)
			Task.processOutput(self, data)

	def processOutputLine(self, line):
			self.error = self.ERROR_SERVER
			
	def afterRun(self):
		pass

class downloadTaskPostcondition(Condition):
	RECOVERABLE = True
	def check(self, task):
		if task.returncode == 0 or task.error is None:
			return True
		else:
			return False

	def getErrorMessage(self, task):
		return {
			task.ERROR_CORRUPT_FILE: _("Video Download Failed!Corrupted Download File:%s" % task.lasterrormsg),
			task.ERROR_RTMP_ReadPacket: _("Video Download Failed!Could not read RTMP-Packet:%s" % task.lasterrormsg),
			task.ERROR_SEGFAULT: _("Video Download Failed!Segmentation fault:%s" % task.lasterrormsg),
			task.ERROR_SERVER: _("Download Failed!-Server error:"),
			task.ERROR_UNKNOWN: _("Download Failed!Unknown Error:%s" % task.lasterrormsg)
		}[task.error]
