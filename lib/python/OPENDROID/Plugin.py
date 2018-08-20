from enigma import eTimer, eConsoleAppContainer
from Screens.InputBox import InputBox
from Screens.Setup import Setup
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap,NumberActionMap
from Components.ScrollLabel import *
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.ConfigList import ConfigListScreen
from Components.FileList import *
from Components.MenuList import MenuList
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, configfile
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir, statvfs, listdir
from os import rename, remove, stat as mystat
from Plugins.Plugin import PluginDescriptor
#import time
#import datetime
import Screens.MessageBox
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.PluginList import PluginList
from Screens.ChoiceBox import ChoiceBox
import stat, os, time ,datetime
from Components.Button import Button
from Components.Sources.StaticText import StaticText
mypanel = None


###########################
# Manual Pannel installer #
###########################

class ManualPanel(Screen):
	skin = """<screen name="ManualPanel" position="80,95" size="620,450" title="OPENDROID IPK Tools Panel" >
		  <widget name="list" position="20,20" size="510,400" zPosition="10" scrollbarMode="showOnDemand"  transparent="1"/>
		  </screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list=[]
		self.entrylist = []  #List reset
		self.entrylist.append((_("TarGz packages installer"), "one", "/usr/lib/enigma2/python/OPENDROID/icons/File_Archive.png"))
		self.entrylist.append((_("Ipk packages installer"), "two", "/usr/lib/enigma2/python/OPENDROID/icons/File_Archive.png"))
                self.entrylist.append((_("Advanced ipk packages installer"), "tree", "/usr/lib/enigma2/python/OPENDROID/icons/File_Archive.png"))	
		self.entrylist.append((_("Ipk remove"), "four", "/usr/lib/enigma2/python/OPENDROID/icons/File_Archive.png"))	
		self['list'] = PluginList(self.list)
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{"ok": self.OK,
		 "back": self.exit,
		})
		self.onLayoutFinish.append(self.updateList)
	def exit(self):
		self.close()
	def OK(self):
		selection = self["list"].getCurrent()[0][1]
		if (selection == "one"):
			self.session.open(PanelTGzInstaller)
		elif (selection== "two"):
			self.session.open(PanelIPKInstaller)
		elif (selection== "tree"):
			self.session.open(AdvInstallIpk)
		elif (selection== "four"):
			self.session.open(RemoveIPK)
		else:
			self.messpopup("Selection error")
			
	def messpopup(self,msg):
		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO)

	def updateList(self):
		for i in self.entrylist:
				res = [i]
				res.append(MultiContentEntryText(pos=(50, 5), size=(800, 32), font=0, text=i[0]))
				picture=LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
				res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(34, 34), png=picture))
				self.list.append(res)
		self['list'].l.setList(self.list)	

#################
# Ipk Installer #
#################
class PanelIPKInstaller(Screen):
	skin = """
		<screen name="PanelIPKInstaller" position="80,95" size="620,450" title="Manual Install Ipk Packages" >
		<widget source="list" render="Listbox" position="10,10" size="600,300" scrollbarMode="showOnDemand" >
		<convert type="StringList" />
		</widget>	
		<widget name="key_red" position="90,350" zPosition="1" size="110,60" font="Regular;20"  foregroundColor="red" transparent="1" />		  
		<widget name="key_green" position="290,350" zPosition="1" size="110,60" font="Regular;20" foregroundColor="green" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Install ipk'))
		self.flist = []
		idx = 0
		pkgs = listdir('/tmp')
		for fil in pkgs:
			if fil.find('.ipk') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
				continue
		self['list'] = List(self.flist)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
		{'ok': self.KeyOk, 
		 'red':self.close, 
		 'green':self.KeyOk, 
		 'back': self.close})

	def KeyOk(self):
		self.sel = self['list'].getCurrent()
		if self.sel:
			self.sel
			self.sel = self.sel[0]
			message = 'Do you want to install the Addon:\n ' + self.sel + ' ?'
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle('Installation Confirm')
		else:
			self.sel

	def installadd2(self, answer):
		if answer is True:
			dest = '/tmp/' + self.sel
			mydir = getcwd()
			chdir('/')
			cmd = 'opkg install -force-overwrite ' + dest
			cmd2 = 'rm -f ' + dest
			self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd, cmd2])
			chdir(mydir)
			
#####################################################################################################
# Tar.Gz Installer
####################################################################################################
class PanelTGzInstaller(Screen):
	skin = """
		<screen name="PanelTGzInstaller" position="80,95" size="620,450" title="Manual Install Tgz Packages" >
		<widget source="list" render="Listbox" position="10,10" size="600,300" scrollbarMode="showOnDemand" >
		<convert type="StringList" />
		</widget>	
		<widget name="key_red" position="90,350" zPosition="1" size="110,60" font="Regular;20" foregroundColor="red" transparent="1" />		  
		<widget name="key_green" position="290,350" zPosition="1" size="110,60" font="Regular;20" foregroundColor="green" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Install Tgz'))
		self.flist = []
		idx = 0
		pkgs = listdir('/tmp')
		for fil in pkgs:
			if fil.find('.tgz') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
				continue
		self['list'] = List(self.flist)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
		{'ok': self.KeyOk, 
		 'red':self.close,
		 'green':self.KeyOk,  
		 'back': self.close})

	def KeyOk(self):
		self.sel = self['list'].getCurrent()
		if self.sel:
			self.sel
			self.sel = self.sel[0]
			message = 'Do you want to install the Addon:\n ' + self.sel + ' ?'
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle('Installation Confirm')
		else:
			self.sel

	def installadd2(self, answer):
		if answer is True:
			dest = '/tmp/' + self.sel
			mydir = getcwd()
			chdir('/')
			cmd = 'tar -C/ -xzpvf ' + dest
			cmd2 = 'rm -f ' + dest
			self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd, cmd2])
			chdir(mydir)
			
				

	def Restart(self, answer):
		rc = system('killall -9 enigma2')



######################################################################################################
# Advance ipk Installer
######################################################################################################
class AdvInstallIpk(Screen):
	skin = """
		<screen name="AdvInstallIpk" position="80,95" size="620,450" title="Select install files" >
		<widget source="menu" render="Listbox" position="10,10" size="600,300" scrollbarMode="showOnDemand">
		<convert type="StringList" />
		</widget>
		<widget source="key_red" render="Label" position="40,360" zPosition="2" size="170,30" font="Regular;20" foregroundColor="red" transparent="1" />
		<widget source="key_green" render="Label" position="220,360" zPosition="2" size="170,30" font="Regular;20" foregroundColor="green" transparent="1" />
		<widget source="key_yellow" render="Label" position="400,360" zPosition="2" size="170,30" font="Regular;20" foregroundColor="yellow" transparent="1" />
		</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.okInstAll,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_('Exit'))
		self["key_green"] = Label(_("Install"))
		self["key_yellow"] = Label(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0]))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		except:
			pass
		
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		
	def cancel(self):
		self.close()
######################################################################################################
# Ipk Remove
######################################################################################################
class RemoveIPK(Screen):
	skin = """
		<screen name="RemoveIPK" position="center,100" size="750,520" title="Panel Ipk remove" >
		<widget source="menu" position="15,10" render="Listbox" size="720,420">
		<convert type="StringList" />
		</widget>
		<widget source="key_red" render="Label" position="30,475" zPosition="2" size="170,30" font="Regular;20" foregroundColor="red" transparent="1" />
		<widget source="key_green" render="Label" position="210,475" zPosition="2" size="170,30" font="Regular;20" foregroundColor="green" transparent="1" />
		<widget source="key_yellow" render="Label" position="360,475" zPosition="2" size="200,30" font="Regular;20" foregroundColor="yellow" transparent="1" />
		</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("UnInstall"))
		self["key_yellow"] = Label(_("Force UnInstall"))
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.Remove,
				"green": self.Remove,
				"red": self.cancel,
				"yellow": self.ARemove,
			},-1)
		
	def nList(self):
		self.list = []
		ipklist = os.popen("opkg list-installed")
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0]) + 2
				self.list.append((dstring[0], line[endstr:]))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def Remove(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg remove %s" % item[0])
		self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

	def ARemove(self):
		item = self["menu"].getCurrent()
		os.system("opkg remove -force-remove %s" % item[0])
		self.mbox = self.session.open(MessageBox,_("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()
#####################################################################################
# DownFeed
####################################################################################
class InstallFeed(Screen):
	skin = """
		<screen name="InstallFeed" position="center,center" size="750,560" title="Insatall extensions from feed" >
		<widget source="list" render="Listbox" position="15,10" size="720,450" scrollbarMode="showOnDemand">
		<convert type="StringList" />
		</widget>
		<widget source="key_red" render="Label" position="65,510" zPosition="2" size="170,30" font="Regular;20" foregroundColor="red" transparent="1" />
		<widget source="key_green" render="Label" position="315,510" zPosition="2" size="170,30" font="Regular;20" foregroundColor="green" transparent="1" />
		</screen>"""
	  
	def __init__(self, session):
		Screen.__init__(self, session)

		self["key_green"] = Label(_("Addons"))
		self["key_red"] = Label(_("Software-Manager"))
		self.list = []
		self["list"] = List(self.list)
		self.updateList()

		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.runPlug,
			"back": self.close,
			"red": self.keyRed,
			"green": self.keyGreen,
			
		}, -1)

	def runPlug(self):
		mysel = self["list"].getCurrent()
		if mysel:
			plugin = mysel[3]
			plugin(session=self.session)

	def updateList(self):
		self.list = [ ]
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "/usr/lib/enigma2/python/OPENDROID/icons/plugin.png"))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png, plugin)
			self.list.append(res)

		self["list"].list = self.list

	def keyRed(self):
		from Plugins.SystemPlugins.SoftwareManager.plugin import UpdatePluginMenu
		self.session.open(UpdatePluginMenu)

	def keyGreen(self):
		from Screens.PluginBrowser import PluginDownloadBrowser
		self.session.open(PluginDownloadBrowser)

from HddSetup import HddSetup, HddFastRemove
from Plugins.Plugin import PluginDescriptor
import os

def supportExtFat():
	if not os.path.isfile("/sbin/mkexfatfs"):
		arch = os.popen("uname -m").read()
		if 'mips' in arch and os.path.isfile("/usr/lib/enigma2/python/OPENDROID/bin/mips/mkexfatfs"):
			os.system("cp /usr/lib/enigma2/python/OPENDROID/bin/mips/mkexfatfs /sbin/mkexfatfs && chmod 755 /sbin/mkexfatfs && ln /sbin/mkexfatfs /sbin/mkfs.exfat")
			os.system("cp /usr/lib/enigma2/python/OPENDROID/bin/mips/exfatfsck /sbin/exfatfsck && chmod 755 /sbin/exfatfsck")
		elif 'armv7l' in arch and os.path.isfile("/usr/lib/enigma2/python/OPENDROID/bin/armv7l/mkexfatfs"):
			os.system("cp /usr/lib/enigma2/python/OPENDROID/bin/armv7l/mkexfatfs /sbin/mkexfatfs && chmod 755 /sbin/mkexfatfs && ln /sbin/mkexfatfs /sbin/mkfs.exfat")
			os.system("cp /usr/lib/enigma2/python/OPENDROID/bin/armv7l/exfatfsck /sbin/exfatfsck && chmod 755 /sbin/exfatfsck")
	if "exfat-fuse" in open("/etc/filesystems").read():
		pass
	else:
		os.system("echo exfat-fuse >> /etc/filesystems && opkg update && opkg install fuse-exfat")

def deviceManagerMain(session, **kwargs):
	supportExtFat()
	session.open(HddSetup)

def deviceManagerSetup(menuid, **kwargs):
	if menuid != "system":
		return []
	return [(_("Device Manager"), deviceManagerMain, "device_manager", None)]

def deviceManagerFastRemove(session, **kwargs):
	session.open(HddFastRemove)


def Plugins(**kwargs):
	return [PluginDescriptor(name = _("Device Manager"), description = _("Format/Partition your Devices and manage Mountpoints"), where = PluginDescriptor.WHERE_MENU, fnc = deviceManagerSetup),
			PluginDescriptor(name = _("Device Manager - Fast Mounted Remove"), description = _("Quick and safe remove for your mounted devices "), where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = deviceManagerFastRemove)]
