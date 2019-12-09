from enigma import eTimer, eConsoleAppContainer
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.Button import Button
from Components.PluginComponent import plugins
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Label import Label
from Components.MenuList import MenuList
from Components.PluginList import PluginList
from Screens.Console import Console
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from enigma import getDesktop

####################################################################################
#                                     ManualPanel                                  #
####################################################################################
class ManualPanel(Screen):
	skin = """
		<screen name="ManualPanel" position="center,60" size="800,635" title="OPENDROID Addons Manager" >
		<widget name="list" position="80,100" size="810,350" zPosition="2" scrollbarMode="showOnDemand" transparent="1"/>
		<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="red" backgroundColor="red" transparent="1" />		
		<widget name="key_green" position="400,600" zPosition="1" size="100,45" font="Regular;18" foregroundColor="green" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list=[]
		self.entrylist = []  #List reset
		self.entrylist.append((_("bh.tgz, tar.gz, nab.tgz installer"), "Plg", "/usr/lib/enigma2/python/OPENDROID/icons/tar.png"))
		self.entrylist.append((_("ipk packets installer"), "Pcs-HDD", "/usr/lib/enigma2/python/OPENDROID/icons/ipk1.png"))
		self.entrylist.append((_("advanced ipk packets installer"), "Pcs-USB", "/usr/lib/enigma2/python/OPENDROID/icons/ipk2.png"))
		self.entrylist.append((_("install extensions all feed"), "Stg", "/usr/lib/enigma2/python/OPENDROID/icons/down.png"))
		self.entrylist.append((_("ipk packets remover"), "Sks", "/usr/lib/enigma2/python/OPENDROID/icons/ipk.png"))
		self.entrylist.append((_("clear /tmp"), "Logo","/usr/lib/enigma2/python/OPENDROID/icons/clear.png"))
		self['list'] = PluginList(self.list)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Restart E2"))
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{
			'ok': self.KeyOk,
			"red": self.close,
			'back': self.close,
			'green': self.RestartE2,
			
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

	def RestartE2(self):
		os.system("killall -9 enigma2")

	def KeyOk(self):
		selection = self["list"].getCurrent()[0][1]
		print selection
		if (selection == "Plg"):
			self.title = 'bh.tgz, tar.gz, nab.tgz installer'
			self.session.open(PanelTGzInstaller, self.title)
		elif (selection == "Pcs-HDD"):
			self.title = 'ipk packets installer'
			self.session.open(PanelIPKInstaller, self.title)
		elif (selection == "Pcs-USB"):
			self.title = 'advanced ipk packets installer'
			self.session.open(AdvInstallIpk, self.title)
		elif (selection == "Stg"):
			self.title = 'install extensions all feed'
			self.session.open(downfeed, self.title)
		elif (selection == "Sks"):
			self.title = 'ipk packets remover'
			self.session.open(RemoveIPK, self.title)
		elif (selection == "Logo"):
			self.title = 'clear /tmp'
			os.system("rm /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.ipk /tmp/*.nab.tgz")
			self.mbox = self.session.open(MessageBox,_("*.tar.gz & *.bh.tgz & *.ipk removed"), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.messpopup("Selection error")

	def messpopup(self,msg):
		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO)

	def updateList(self):
		for i in self.entrylist:
				res = [i]
				res.append(MultiContentEntryText(pos=(110, 13), size=(700, 50), font=0, text=i[0]))
				picture=LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
				res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 13), size=(100, 40), png=picture))
				self.list.append(res)
		self['list'].l.setList(self.list)
####################################################################################
#                                   PanelTGzInstaller                              #
####################################################################################
class PanelTGzInstaller(Screen):
	skin = """
		<screen name="PanelTGzInstaller" position="80,95" size="620,450" title="Select install files" >
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
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.nab.tgz")
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "/usr/lib/enigma2/python/OPENDROID/icons/plugin.png"))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], png))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % name])
		except:
			pass
			
	def okInstAll(self):
			ipklist = os.popen("ls -1  /tmp/*.tar.gz /tmp/*.bh.tgz")#posizione ipk
			self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/*.tar.gz", "tar -C/ -xzpvf /tmp/*.bh.tgz", "tar -C/ -xzpvf /tmp/*.nab.tgz"])

	def cancel(self):
		self.close()
####################################################################################
#                                   PanelIPKInstaller                              #
####################################################################################
class PanelIPKInstaller(Screen):
	skin = """
		<screen name="PanelIPKInstaller" position="80,95" size="620,450" title="Select install files" >
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
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")#cerca ipk
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, '/usr/lib/enigma2/python/OPENDROID/icons/plugin.png'))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], png))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		except:
			pass
			
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		
	def cancel(self):
		self.close()
####################################################################################
#                                     AdvInstallIpk                                #
####################################################################################
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
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")#cerca ipk
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, '/usr/lib/enigma2/python/OPENDROID/icons/plugin.png'))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], png))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		except:
			pass
		
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		
	def cancel(self):
		self.close()
####################################################################################
#                                     RemoveIPK                                    #
####################################################################################
class RemoveIPK(Screen):
	skin = """
		<screen name="RemoveIPK" position="80,95" size="620,450" title="Select install files" >
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
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnInstall"))
		self["key_yellow"] = StaticText(_("Adv. UnInstall"))
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
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "/usr/lib/enigma2/python/OPENDROID/icons/plugin.png"))
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0]) + 2
				self.list.append((dstring[0], line[endstr:], png))
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
####################################################################################
#                                     DownFeed                                     #
####################################################################################
class downfeed(Screen):
	skin = """
		<screen name="downfeed" position="center,center" size="560,430" title="Select install files">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget source="menu" render="Listbox" position="15,10" size="720,500" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
						MultiContentEntryText(pos = (65, 10), size = (330, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						MultiContentEntryText(pos = (405, 10), size = (125, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 2),
						],
						"fonts": [gFont("Regular", 22)],
						"itemHeight": 50
					}
				</convert>
			</widget>
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
				"ok": self.setup,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		
	def nList(self):
		self.list = []
		os.system("opkg update")#Downloading di tutti i feed 
		try:
			ipklist = os.popen("opkg list")
		except:
			pass
		png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "/usr/lib/enigma2/python/OPENDROID/icons/plugin.png"))
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0] + dstring[1]+ dstring[2]+dstring[3]) + 4

				self.list.append((dstring[0]  + " " + dstring[1] + " " + dstring[2], line[endstr:], png))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def setup(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg install -force-reinstall %s" % name)
		msg  = _("%s is installed" % name)
		self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout = 4 )
##############################################################################
#                              InstallFeed                                   #
##############################################################################
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
