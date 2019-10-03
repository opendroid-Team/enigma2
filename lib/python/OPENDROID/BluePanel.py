from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.config import ConfigSelection, getConfigListEntry, ConfigAction
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN, fileExists
from Tools.GetEcmInfo import GetEcmInfo
from Components.Sources.StaticText import StaticText
from OPENDROID.OscamSmartcard import *
import os
import enigma
from ServiceReference import ServiceReference
from enigma import eTimer, iServiceInformation, getDesktop
from Components.config import config, ConfigSubsection, ConfigText, ConfigSelection, ConfigYesNo
from enigma import eTimer, eConsoleAppContainer

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
	
	if text[-1:] == '\n': text = text[:-1]
	comandline = text
	os.system("rm /tmp/command.txt")
	return comandline


class BluePanel(Screen, ConfigListScreen):
	skin = """
	<screen name="BluePanel" position="center,center" size="560,450" >
		<widget name="config" position="5,10" size="550,90" />
		<widget name="info" position="5,100" size="550,300" font="Fixed;18" />
		<ePixmap name="red" position="0,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap name="green" position="140,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<widget objectTypes="key_red,StaticText" source="key_red" render="Label" position="0,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget objectTypes="key_green,StaticText" source="key_green" render="Label" position="140,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget objectTypes="key_blue,StaticText" source="key_blue" render="Label"  position="420,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1"/>
		<widget objectTypes="key_blue,StaticText" source="key_blue" render="Pixmap" pixmap="skin_default/buttons/blue.png"  position="420,410" zPosition="1" size="140,40" transparent="1" alphatest="on">
			<convert type="ConditionalShowHide"/>
		</widget>
	</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)

		self.setup_title = _("Softcam setup")
		self.setTitle(self.setup_title)

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
			{
				"cancel": self.cancel,
				"green": self.save,
				"red": self.cancel,
                                "yellow": self.Yellow,
				"blue": self.ppanelShortcut,
			},-1)

		self.list = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)

		self.softcam = CamControl('softcam')
		self.cardserver = CamControl('cardserver')
		self.ecminfo = GetEcmInfo()
		(newEcmFound, ecmInfo) = self.ecminfo.getEcm()
		self["info"] = ScrollLabel("".join(ecmInfo))
		self.EcmInfoPollTimer = eTimer()
		self.EcmInfoPollTimer.callback.append(self.setEcmInfo)
		self.EcmInfoPollTimer.start(1000)
                self.Timer = eTimer()
		self.partyfeed = os.path.exists("/etc/opkg/3rdparty-feed.conf") or os.path.exists("/etc/opkg/3rd-party-feed.conf")
		if self.partyfeed:
			self["key_yellow"]= Label(_("Install"))
		else:
			self["key_yellow"]= Label(_("Exit"))
		try:
			service = self.session.nav.getCurrentService()
		        info = service and service.info()
		        videosize = str(info.getInfo(iServiceInformation.sVideoWidth)) + 'x' + str(info.getInfo(iServiceInformation.sVideoHeight))
		        aspect = info.getInfo(iServiceInformation.sAspect)
		        if aspect in (1, 2, 5, 6, 9, 10, 13, 14):
				aspect = '4:3'
		        else:
		                aspect = '16:9'
		                provider = info.getInfoString(iServiceInformation.sProvider)
		                chname = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
		                self['lb_provider'] = Label(_('Provider: ') + provider)
		                self['lb_channel'] = Label(_('Name: ') + chname)
		                self['lb_aspectratio'] = Label(_('Aspect Ratio: ') + aspect)
		                self['lb_videosize'] = Label(_('Video Size: ') + videosize)
		except:
		                self['lb_provider'] = Label(_('Provider: n/a'))
		                self['lb_channel'] = Label(_('Name: n/a'))
		                self['lb_aspectratio'] = Label(_('Aspect Ratio: n/a'))
		                self['lb_videosize'] = Label(_('Video Size: n/a'))
		softcams = self.softcam.getList()
		cardservers = self.cardserver.getList()

		self.softcams = ConfigSelection(choices = softcams)
		self.softcams.value = self.softcam.current()

		self.softcams_text = _("Select Softcam")
		self.list.append(getConfigListEntry(self.softcams_text, self.softcams))
		if cardservers:
			self.cardservers = ConfigSelection(choices = cardservers)
			self.cardservers.value = self.cardserver.current()
			self.list.append(getConfigListEntry(_("Select Card Server"), self.cardservers))

		self.list.append(getConfigListEntry(_("Restart softcam"), ConfigAction(self.restart, "s")))
		if cardservers:
			self.list.append(getConfigListEntry(_("Restart cardserver"), ConfigAction(self.restart, "c")))
			self.list.append(getConfigListEntry(_("Restart both"), ConfigAction(self.restart, "sc")))

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
                self["key_yellow"] = Label(_("Install"))
		self["key_blue"] = Label(_("Info"))
		self.onShown.append(self.blueButton)

	def changedEntry(self):
		if self["config"].getCurrent()[0] == self.softcams_text:
			self.blueButton()

	def blueButton(self):
		if self.softcams.value and self.softcams.value.lower() != "none":
			self["key_blue"].setText(_("Info"))
		else:
			self["key_blue"].setText("")
	def Yellow(self):
		if not self.partyfeed:
			self.Exit()
		else:
			self.Timer.stop()
			self.session.open(ShowSoftcamPackages)


	def setEcmInfo(self):
		(newEcmFound, ecmInfo) = self.ecminfo.getEcm()
		if newEcmFound:
			self["info"].setText("".join(ecmInfo))

        def getCurrentValue(self):
                return str(self["config"].getCurrent()[1].getText())

	def ppanelShortcut(self):
		ppanelFileName = '/etc/ppanels/' + self.softcams.value + '.xml'
		if "oscam" in self.softcams.value.lower() and os.path.isfile('/usr/lib/enigma2/python/Screens/OScamInfo.pyo'):
			from Screens.OScamInfo import OscamInfoMenu
			self.session.open(OscamInfoMenu)
		elif "cccam" in self.softcams.value.lower() and os.path.isfile('/usr/lib/enigma2/python/Screens/CCcamInfo.pyo'):
			from Screens.CCcamInfo import CCcamInfoMain
			self.session.open(CCcamInfoMain)
		elif "ncam" in self.softcams.value.lower() and os.path.isfile('/usr/lib/enigma2/python/Screens/OScamInfo.pyo'):
			from Screens.OScamInfo import OscamInfoMenu
			self.session.open(OscamInfoMenu)
		elif os.path.isfile(ppanelFileName) and os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/PPanel/plugin.pyo'):
			from Plugins.Extensions.PPanel.ppanel import PPanel
			self.session.open(PPanel, name = self.softcams.value + ' PPanel', node = None, filename = ppanelFileName, deletenode = None)
		else:
			return 0

	def restart(self, what):
		self.what = what
		if "s" in what:
			if "c" in what:
				msg = _("Please wait, restarting softcam and cardserver.")
			else:
				msg  = _("Please wait, restarting softcam.")
		elif "c" in what:
			msg = _("Please wait, restarting cardserver.")
		self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.doStop)
		self.activityTimer.start(100, False)

	def doStop(self):
		self.activityTimer.stop()
		if "c" in self.what:
			self.cardserver.command('stop')
		if "s" in self.what:
			self.softcam.command('stop')
		self.oldref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
		self.session.nav.stopService()
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.doStart)
		self.activityTimer.start(1000, False)

	def doStart(self):
		self.activityTimer.stop()
		del self.activityTimer
		if "c" in self.what:
			self.cardserver.select(self.cardservers.value)
			self.cardserver.command('start')
		if "s" in self.what:
			self.softcam.select(self.softcams.value)
			self.softcam.command('start')
		if self.mbox:
			self.mbox.close()
		self.close()
		self.session.nav.playService(self.oldref, adjust=False)

	def restartCardServer(self):
		if hasattr(self, 'cardservers'):
			self.restart("c")

	def restartSoftcam(self):
		self.restart("s")

	def save(self):
		what = ''
		if hasattr(self, 'cardservers') and (self.cardservers.value != self.cardserver.current()):
			what = 'sc'
		elif self.softcams.value != self.softcam.current():
			what = 's'
		if what:
			self.restart(what)
		else:
			self.close()

	def cancel(self):
		self.close()

class CamControl:
	'''CAM convention is that a softlink named /etc/init.c/softcam.* points
	to the start/stop script.'''
	def __init__(self, name):
		self.name = name
		self.link = '/etc/init.d/' + name
		if not os.path.exists(self.link):
			print "[CamControl] No softcam link?", self.link

	def getList(self):
		result = []
		prefix = self.name + '.'
		for f in os.listdir("/etc/init.d"):
			if f.startswith(prefix):
				result.append(f[len(prefix):])
		return result

	def current(self):
		try:
			l = os.readlink(self.link)
			prefix = self.name + '.'
			return os.path.split(l)[1].split(prefix, 2)[1]
		except:
			pass
		return None

	def command(self, cmd):
		if os.path.exists(self.link):
			print "Executing", self.link + ' ' + cmd
			enigma.eConsoleAppContainer().execute(self.link + ' ' + cmd)

	def select(self, which):
		print "Selecting CAM:", which
		if not which:
			which = "None"
		dst = self.name + '.' + which
		if not os.path.exists('/etc/init.d/' + dst):
			print "[CamControl] init script does not exist:", dst
			return 
		try:
			os.unlink(self.link)
		except:
			pass
		try:
			os.symlink(dst, self.link);
		except:
			print "Failed to create symlink for softcam:", dst
			import sys
			print sys.exc_info()[:2]


class ShowSoftcamPackages(Screen):
	skin = """
		<screen name="ShowSoftcamPackages" position="center,center" size="630,500" title="Install Softcams" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red,StaticText" source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green,StaticText" source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow,StaticText" source="key_yellow" render="Label" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue,StaticText" source="key_blue" render="Label" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget source="key_ok" render="Label" position="240,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget source="list" render="Listbox" position="5,50" size="620,420" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (5, 1), size = (540, 28), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 0 is the name
							MultiContentEntryText(pos = (5, 26), size = (540, 20), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 2 is the description
							MultiContentEntryPixmapAlphaBlend(pos = (545, 2), size = (48, 48), png = 4), # index 4 is the status pixmap
							MultiContentEntryPixmapAlphaBlend(pos = (5, 50), size = (510, 2), png = 5), # index 4 is the div pixmap
						],
					"fonts": [gFont("Regular", 22),gFont("Regular", 14)],
					"itemHeight": 52
					}
				</convert>
			</widget>
		</screen>"""
	
	def __init__(self, session, args = None):
		Screen.__init__(self, session)
		self.session = session
		
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
		{
			"red": self.exit,
			"ok": self.go,
			"cancel": self.exit,
			"green": self.startupdateList,
                        "yellow": self.oscamsmartcard,
		}, -1)
		
		self.list = []
		self.statuslist = []
		self["list"] = List(self.list)
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("Reload"))
		self["key_ok"] = Label(_("Install"))
                self["key_yellow"] = Label(_("oscamsmartcard"))
		self.oktext = _("\nPress OK on your remote control to continue.")
		self.onShown.append(self.setWindowTitle)
		self.setStatus('list')
		self.Timer1 = eTimer()
		self.Timer1.callback.append(self.rebuildList)
		self.Timer1.start(1000, True)
		self.Timer2 = eTimer()
		self.Timer2.callback.append(self.updateList)

	def go(self, returnValue = None):
		cur = self["list"].getCurrent()
		if cur:
			status = cur[3]
			self.package = cur[2]
			if status == "installable":
				self.session.openWithCallback(self.runInstall, MessageBox, _("Do you want to install the package:\n") + self.package + "\n" + self.oktext)

	def runInstall(self, result):
		if result:
			self.session.openWithCallback(self.runInstallCont, Console, cmdlist = ['opkg install ' + self.package], closeOnSuccess = True)

	def runInstallCont(self):
			ret = command('opkg list-installed | grep ' + self.package + ' | cut -d " " -f1')

			if ret != self.package:
				self.session.open(MessageBox, _("Install Failed !!"), MessageBox.TYPE_ERROR, timeout = 10)
			else:
				self.session.open(MessageBox, _("Install Finished."), MessageBox.TYPE_INFO, timeout = 10)
				self.setStatus('list')
				self.Timer1.start(1000, True)

	def UpgradeReboot(self, result):
		if result is None:
			return
		
	def exit(self):
		self.close()

	def oscamsmartcard(self):
		self.session.open(OscamSmartcard)
			
	def setWindowTitle(self):
		self.setTitle(_("Install Softcams"))

	def setStatus(self,status = None):
		if status:
			self.statuslist = []
			divpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/div-h.png"))
			if status == 'update':
				statuspng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "/usr/lib/enigma2/python/OPENDROID/icons/upgrade.png"))
				self.statuslist.append(( _("Package list update"), '', _("Trying to download a new updatelist. Please wait..." ),'', statuspng, divpng ))
				self['list'].setList(self.statuslist)
			if status == 'list':
				statuspng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "/usr/lib/enigma2/python/OPENDROID/icons/upgrade.png"))
				self.statuslist.append(( _("Package list"), '', _("Getting Softcam list. Please wait..." ),'', statuspng, divpng ))
				self['list'].setList(self.statuslist)
			elif status == 'error':
				statuspng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "/usr/lib/enigma2/python/OPENDROID/icons/remove.png"))
				self.statuslist.append(( _("Error"), '', _("There was an error downloading the updatelist. Please try again." ),'', statuspng, divpng ))
				self['list'].setList(self.statuslist)				

	def startupdateList(self):
		self.setStatus('update')
		self.Timer2.start(1000, True)

	def updateList(self):
		self.container = eConsoleAppContainer()
		self.container.appClosed.append(self.doneupdateList)
		self.setStatus('list')
		self.container.execute('opkg update')

	def doneupdateList(self, answer):
		self.container.appClosed.remove(self.doneupdateList)
		self.Timer1.start(1000, True)

	def rebuildList(self):
		self.list = []
		self.Flist = []
		self.Elist = []
		t = command('opkg list | grep "enigma2-plugin-softcams-"')
		self.Flist = t.split('\n')
		tt = command('opkg list-installed | grep "enigma2-plugin-softcams-"')
		self.Elist = tt.split('\n')

		if len(self.Flist) > 0:
			self.buildPacketList()
		else:
			self.setStatus('error')

	def buildEntryComponent(self, name, version, description, state):
		divpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/div-h.png"))
		if not description:
			description = ""
		installedpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "/usr/lib/enigma2/python/OPENDROID/icons/installed.png"))
		return((name, version, _(description), state, installedpng, divpng))

	def buildPacketList(self):
		fetchedList = self.Flist
		excludeList = self.Elist

		if len(fetchedList) > 0:
			for x in fetchedList:
				x_installed = False
				Fx = x.split(' - ')
				try:
					if Fx[0].find('-softcams-') > -1:
						for exc in excludeList:
							Ex = exc.split(' - ')
							if Fx[0] == Ex[0]:
								x_installed = True
								break
						if x_installed == False:
							self.list.append(self.buildEntryComponent(Fx[2], Fx[1], Fx[0], "installable"))
				except:
					pass

			self['list'].setList(self.list)
	
		else:
			self.setStatus('error')
