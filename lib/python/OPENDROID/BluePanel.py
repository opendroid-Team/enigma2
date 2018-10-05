from Components.config import config, ConfigSubsection, ConfigText, configfile, getConfigListEntry, ConfigSelection
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Components.MenuList import MenuList
from Components.Label import Label
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Tools.Directories import resolveFilename, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN, fileExists
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from enigma import *
from Components.UsageConfig import config
from twisted.internet import threads
from enigma import eTimer, eConsoleAppContainer
from os import system, listdir, path
from datetime import datetime
from ServiceReference import ServiceReference
from enigma import eTimer, iServiceInformation, getDesktop
import os
from Screens.CCcamInfo import CCcamInfoMain
from Screens.OScamInfo import OscamInfoMenu
from Components.config import config, ConfigSubsection, ConfigText, ConfigSelection, ConfigYesNo
config.OPENDROID_BluePanel = ConfigSubsection()
config.softcam = ConfigSubsection()
config.softcam_actCam = ConfigText(visible_width = 200)
config.softcam_actCam2 = ConfigText(visible_width = 200)
config.softcam_waittime = ConfigSelection([('0',_("dont wait")),('1',_("1 second")), ('5',_("5 seconds")),('10',_("10 seconds")),('15',_("15 seconds")),('20',_("20 seconds")),('30',_("30 seconds"))], default='15')

def Check_Softcam():
	found = True
	if fileExists("/etc/enigma2/noemu"):
		found = False
	else:
		for x in os.listdir('/etc'):
			if x.find('.emu') > -1:
				found = True
				break;
	return found

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

SOFTCAM_SKIN = """<screen name="BluePanel" position="center,center" size="500,450" title="Emu Manager">
	<eLabel font="Regular;22" position="10,10" size="185,25" text="Softcam Selection:" />
	<widget font="Regular;18" name="camcount" position="420,10" size="60,25" />
	<widget name="config" position="10,100" size="400,100" />
	<eLabel backgroundColor="red" position="10,60" size="120,3" zPosition="0" />
	<eLabel backgroundColor="green" position="130,60" size="120,3" zPosition="0" />
	<eLabel backgroundColor="yellow" position="250,60" size="120,3" zPosition="0" />
	<eLabel backgroundColor="blue" position="370,60" size="120,3" zPosition="0" />
	<widget font="Regular;16" halign="center" name="key_red" position="10,62" size="120,35" transparent="1" valign="center" zPosition="2" />
	<widget font="Regular;16" halign="center" name="key_green" position="130,62" size="120,35" transparent="1" valign="center" zPosition="2" />
	<widget font="Regular;16" halign="center" name="key_yellow" position="250,62" size="120,35" transparent="1" valign="center" zPosition="2" />
	<widget font="Regular;16" halign="center" name="key_blue" position="370,62" size="120,35" transparent="1" valign="center" zPosition="2" />
	<eLabel backgroundColor="#56C856" position="0,199" size="500,1" zPosition="0" />
	<widget font="Regular;16" name="actifcam" position="10,205" size="220,32" />
	<widget font="Regular;16" name="actifcam2" position="250,205" size="220,32" />
	<eLabel backgroundColor="#56C856" position="0,225" size="500,1" zPosition="0" />
	<widget font="Regular;16" name="ecminfo" position="10,235" size="480,300" />
</screen>"""


REFRESH = 0
CCCAMINFO = 1
OSCAMINFO = 2

class BluePanel(ConfigListScreen, Screen):
	def __init__(self, session):
		global emuDir
		emuDir = "/etc/"
		self.service = None
		Screen.__init__(self, session)

		self.skin = SOFTCAM_SKIN
		self.onShown.append(self.setWindowTitle)
		self.partyfeed = None
		self.YellowAction = REFRESH

		self.mlist = []
		self["key_green"] = Label(_("ReStart"))
		self["key_red"] = Label(_("Stop"))
		self["key_yellow"] = Label(_("Refresh"))
		self.partyfeed = os.path.exists("/etc/opkg/3rdparty-feed.conf") or os.path.exists("/etc/opkg/3rd-party-feed.conf")
		if self.partyfeed:
			self["key_blue"]= Label(_("Install"))
		else:
			self["key_blue"]= Label(_("Exit"))
		self["ecminfo"] = Label(_("No ECM info"))
		self["actifcam"] = Label(_("no CAM 1 active"))
		self["actifcam2"] = Label(_("no CAM 2 active"))
		self.emuDirlist = []
		self.emuList = []
		self.emuBin = []
		self.emuStart = []
		self.emuStop = []
		self.emuRgui = []
		self.emuDirlist = os.listdir(emuDir)
		self.ecmtel = 0
		self.first = 0
		global count
		count = 0
		print "************ go in the emuloop ************"
		for x in self.emuDirlist:
			if x.find("emu") > -1:
				self.emuList.append(emuDir + x)
				em = open(emuDir + x)
				self.emuRgui.append(0)
				for line in em.readlines():
					line1 = line
					line = line1
					if line.find("startcam") > -1:
						line = line.split("=")
						self.emuStart.append(line[1].strip())

					line = line1
					if line.find("stopcam") > -1:
						line = line.split("=")
						self.emuStop.append(line[1].strip())

					line = line1
					if line.find("restartEnigma2") > -1:
						self.emuRgui[count] = 1

					line = line1
					if line.find("binname") > -1:
						line = line.split("=")
						self.emuBin.append(line[1].strip())
					
				em.close()
				count += 1

		self.maxcount = count
		
		self.onChangedEntry = [ ]
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		self.ReadMenu()
		self.createSetup()
		self["ecminfo"].show()

		self.read_shareinfo()
		self.Timer = eTimer()
		self.Timer.callback.append(self.layoutFinished)
		self.Timer.start(2000, True)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "MenuActions"],
		{
			"cancel": self.Exit,
			"ok": self.ok,
			"blue": self.Blue,
			"red": self.Red,
			"green": self.Green,
			"yellow": self.Yellow,
                        'menu': self.SoftcamSetup,
		}, -1)
		self.onLayoutFinish.append(self.layoutFinished)

	def setWindowTitle(self):
		self.setTitle(_("Emu Manager"))

	def ReadMenu(self):
		self.whichCam()
		
		for x in self.emuDirlist:
			if x.find("emu") > -1:
				self.emuList.append(emuDir + x)
				em = open(emuDir + x)
				self.emuRgui.append(0)
				for line in em.readlines():
					line1 = line
					line = line1
					if line.find("emuname") > -1:
						line = line.split("=")
						self.mlist.append(line[1].strip())
						name = line[1].strip()
				em.close()

		emusel = [_('no cam')]
		for x in self.mlist:
			emusel.append(x)
		self.cam1sel = ConfigSelection(emusel)
		self.cam2sel = ConfigSelection(emusel)
		self.setYellowKey(self.curcam)
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

	def whichCam(self):
		cam = config.softcam_actCam.value
		self.curcam = None
		self.curcamIndex = None
		if cam in self.mlist:
			index = self.mlist.index(cam)
			x = self.emuBin[index]
			if self.isCamrunning(x):
				self.curcam = x
				self.curcamIndex = index

		cam = config.softcam_actCam2.value
		self.curcam2 = None
		self.curcam2Index = None
		if cam in self.mlist:
			index = self.mlist.index(cam)
			x = self.emuBin[index]
			if self.isCamrunning(x):
				self.curcam2 = x
				self.curcam2Index = index

		if not self.curcam and not self.curcam2 and self.mlist:
			print "[SOFTCAMPANEL] try to find a running cam"
			for cam in self.emuBin:
				index = self.emuBin.index(cam)
				if self.isCamrunning(cam):
					self.curcam = cam
					self.curcamIndex = index
					camname = self.mlist[index]
					print"[SOFTCAMPANEL] found %s running" % camname
					self.Save_Settings(camname)
					break

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_("Select Cam 1"), self.cam1sel))
		if len(self.emuStart) > 1:
			self["actifcam2"].show()
			if self.cam1sel.value != _('no cam') or config.softcam_actCam.value != _("no CAM 1 active"):
				self.list.append(getConfigListEntry(_("Select Cam 2"), self.cam2sel))
				if self.cam2sel.value != _('no cam'):
					self.list.append(getConfigListEntry(_("Wait time before start Cam 2"), config.softcam_waittime))
		else:
			self["actifcam2"].hide()
			self.cam2sel.setValue(_('no cam'))

		self["config"].list = self.list
		self["config"].setList(self.list)

	def setYellowKey(self, cam):
		if cam == None or cam == _('no cam'):
			self.YellowAction = REFRESH
			self["key_yellow"].setText(_("Refresh"))
			return
		if cam.upper().startswith('CCCAM'):
			self.YellowAction = CCCAMINFO
			self["key_yellow"].setText(_("CCcamInfo"))
		elif cam.upper().startswith('OSCAM'):
			self.YellowAction = OSCAMINFO
			self["key_yellow"].setText(_("OscamInfo"))
		else:
			self.YellowAction = REFRESH
			self["key_yellow"].setText(_("Refresh"))

	def selectionChanged(self):
		pass

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
		self.selectionChanged()
		self.createSetup()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self["config"].getCurrent() and len(self["config"].getCurrent()) > 2 and self["config"].getCurrent()[2] or ""

	def layoutFinished(self):
		self.Timer.stop()
		if not Check_Softcam():
			self.Exit()
		try:
			self.whichCam()
			global oldcamIndex, oldcam2Index
			oldcamIndex = -1
			oldcam2Index = -1
			tel = 0

			if self.curcam:
				oldcamIndex = self.curcamIndex
				actcam = self.mlist[oldcamIndex]
				if self.first == 0:
					self.cam1sel.setValue(actcam)		
				self["key_green"].setText(_("ReStart"))
				self["actifcam"].setText(_("active CAM 1: ") + actcam )
				print '[SOFTCAM] set active cam 1 to: ' + actcam
			else:
				actcam = _("no CAM 1 active")
				self["actifcam"].setText(actcam)
		
			if self.curcam2:
				oldcam2Index = self.curcam2Index
				actcam = self.mlist[oldcam2Index]
				if self.first == 0:
					self.cam2sel.setValue(actcam)
				self["actifcam2"].setText(_("active CAM 2: ") + actcam )
				print '[SOFTCAM] set active cam 2 to: ' + actcam
			else:
				actcam2 = _("no CAM 2 active")
				self["actifcam2"].setText(actcam2)

			if self.first == 0: 
				self.createSetup()
				self.first = 1
			if not self.curcam and not self.curcam2:
				self["key_green"].setText(_("Start"))
				self.YellowAction = REFRESH
				self["key_yellow"].setText(_("Refresh"))
				if os.path.exists('/tmp/ecm.info') is True:
					os.system("rm /tmp/ecm.info")
				if os.path.exists('/tmp/ecm0.info') is True:
					os.system("rm /tmp/ecm0.info")

		except:
			pass

		if self["config"].getCurrent()[0] == _("Select Cam 1"):
			self.setYellowKey(self.curcam)
		else:
			self.setYellowKey(self.curcam2)
		
		ecmi = ""
		if os.path.exists('/tmp/ecm.info') is True:
			ecmi = self.read_ecm('/tmp/ecm.info')
		elif os.path.exists('/tmp/ecm1.info') is True:
			ecmi = self.read_ecm('/tmp/ecm1.info')
		else:
			ecmi = _("No ECM info")
		ecmold = self["ecminfo"].getText()
		if ecmold == ecmi:
			self.ecmtel += 1
			if self.ecmtel > 5:
				ecmi = _("No new ECM info")
		else:
			self.ecmtel = 0
		self["ecminfo"].setText(ecmi)
		self.Timer.start(2000, True)		

	def read_shareinfo(self):
		self.shareinfo =[]
		if os.path.exists('/tmp/share.info') is True:
			s = open('/tmp/share.info')
			for x in s.readlines():
				self.shareinfo.append(x)
			s.close()

	def read_ecm(self, ecmpath):
		ecmi2 = ''
		Caid = ''
		Prov = ''
		f = open(ecmpath)
		for line in f.readlines():
			line= line.replace('=', '')
			line= line.replace(' ', '', 1)
			if line.find('ECM on CaID') > -1:
				k = line.find('ECM on CaID') + 14
				Caid = line[k:k+4]
			if line.find('prov:') > -1:
				tmpprov = line.split(':')
				Prov = tmpprov[1].strip()
				if Caid <> '' and Prov <> '' and len(self.shareinfo) > 0 :
					for x in self.shareinfo:
						cel = x.split(' ')
						if cel[5][0:4] == Caid and cel[9][3:7] == Prov:
							line = 'Peer: ' + Prov + ' - ' + cel[3] + ' - ' + cel[8] + '\n'
							break
			ecmi2 = ecmi2 + line
		f.close()
		return ecmi2


	def Red(self):
		self.Timer.stop()
		self.Stopcam()
		self.Timer.start(2000, True)		

	def Yellow(self):
		if self.YellowAction == CCCAMINFO:
			self.Timer.stop()
			self.session.openWithCallback(self.ShowSoftcamCallback, CCcamInfoMain)
		elif self.YellowAction == OSCAMINFO:
			self.Timer.stop()
			self.session.openWithCallback(self.ShowSoftcamCallback, OscamInfoMenu)
		else:
			self.first = 0
			self.layoutFinished()

	def Green(self):
		self.Timer.stop()
		self.Startcam()
		self.Timer.start(2000, True)		

	def Exit(self):
		self.Timer.stop()
		self.close()

        def SoftcamSetup(self):
                       self.session.open(SoftcamSetup)

	def Blue(self):
		if not self.partyfeed:
			self.Exit()
		else:
			self.Timer.stop()
			self.session.openWithCallback(self.ShowSoftcamCallback, ShowSoftcamPackages)

	def ShowSoftcamCallback(self):
		self.Timer.start(2000, True)

	def ok(self):
		self.Timer.stop()
		self.Startcam()
		if self.YellowAction == REFRESH:
			self.Yellow()
		self.Timer.start(2000, True)		

	def Stopcam(self):
		global oldcamIndex, oldcam2Index
		if oldcamIndex >= 0:
			oldcam = self.emuBin[oldcamIndex]
		else:
			oldcam = None
		if oldcam2Index >= 0:
			oldcam2 = self.emuBin[oldcam2Index]
		else:
			oldcam2 = None
		import time
		self.container = eConsoleAppContainer()

		if config.softcam_camstartMode.value == "0" or not fileExists('/etc/init.d/softcam'):
			if oldcam:
				print '[SOFTCAM] Python stop cam 1: ' + oldcam
				self.container.execute(self.emuStop[oldcamIndex])

				time.sleep(1) 
				t = 0
				while t < 5:
					p = command('pidof %s |wc -w' % oldcam )
					if not p.isdigit(): p=0
					if int(p) > 0:
						self.container = eConsoleAppContainer()
						self.container.execute('killall -9 ' + oldcam)
						t += 1
						time.sleep(1)
					else:
						t = 5

			if oldcam2:
				print '[SOFTCAM] Python stop cam 2: ' + oldcam2
				self.container.execute(self.emuStop[oldcam2Index])

				time.sleep(1) 
				t = 0
				while t < 5:
					p = command('pidof %s |wc -w' % oldcam2 )
					if not p.isdigit(): p=0
					if int(p) > 0:
						self.container = eConsoleAppContainer()
						self.container.execute('killall -9 ' + oldcam2)
						t += 1
						time.sleep(1)
					else:
						t = 5

		else:
			self.container.execute('/etc/init.d/softcam.cam1 stop')
			self.container.execute('/etc/init.d/softcam.cam2 stop')

		if os.path.exists('/tmp/ecm.info') is True:
			os.system("rm /tmp/ecm.info")
		actcam = _("no CAM 1 active")
		actcam2 = _("no CAM 2 active")
		self["actifcam"].setText(actcam)
		self["actifcam2"].setText(actcam2)
		self["key_green"].setText(_("Start"))
		self["ecminfo"].setText(_("No ECM info"))
		self.Save_Settings(actcam)
		self.Save_Settings2(actcam2)

	def Startcam(self):
		try:
			if count > 0:
				if self.cam1sel.value == self.cam2sel.value:
					self.session.openWithCallback(self.doNothing, MessageBox, _("No Cam started !!\n\nCam 1 must be different from Cam 2"), MessageBox.TYPE_ERROR, simple=True)
					return
				if config.softcam_camstartMode.value == "0":
					self.Stopcam()

				self.camIndex = self.cam1sel.getIndex() -1
				self.cam2Index = self.cam2sel.getIndex() - 1
				if self.camIndex >= 0:
					actcam = self.cam1sel.value
					self["actifcam"].setText(_("active CAM 1: ") + actcam)
					self.Save_Settings(actcam)
					start = self.emuStart[self.camIndex]
					if self.checkBinName(self.emuBin[self.camIndex], start):
						self.session.openWithCallback(self.startcam2, MessageBox, actcam + _(" Not Started !!\n\nCam binname must be in the start command line\nCheck your emu config file"), MessageBox.TYPE_ERROR, simple=True)
						return
					if config.softcam_camstartMode.value == "0":
						print '[SOFTCAM] Python start cam 1: ' + actcam
						self.session.openWithCallback(self.waitTime, MessageBox, _("Starting Cam 1: ") + actcam, MessageBox.TYPE_WARNING, timeout=5, simple=True)
						self.container = eConsoleAppContainer()
						self.container.execute(start)
					else:
						
						self.session.openWithCallback(self.doNothing, MessageBox, _("Creating start scripts and starting the cam"), MessageBox.TYPE_WARNING, timeout=10, simple=True)
						self.Save_Settings2(self.cam2sel.value)

						camname1 = self.emuBin[self.camIndex]
						camname2 = self.emuBin[self.cam2Index]
						self.deleteInit()
						camname = "/usr/bin/" + camname1
						startcmd = self.emuStart[self.camIndex]
						stopcmd = self.emuStop[self.camIndex]							
						self.createInitdscript("cam1", camname, startcmd, stopcmd)
						if self.cam2Index >= 0:
							camname = "/usr/bin/" + camname2
							startcmd = self.emuStart[self.cam2Index]
							stopcmd = self.emuStop[self.cam2Index]							
							self.createInitdscript("cam2", camname, startcmd, stopcmd, config.softcam_waittime.value)

					self["key_green"].setText(_("ReStart"))

		except:
			pass

	def waitTime(self, ret):
		if self.cam2Index >= 0:
			if config.softcam_waittime.value == '0':
				self.startcam2(None)
			else:
				self.session.openWithCallback(self.startcam2, MessageBox, _("Waiting..."), MessageBox.TYPE_WARNING, timeout=int(config.softcam_waittime.value), simple=True)

	def doNothing(self, ret):
		pass

	def startcam2(self, ret):
		camIndex = self.cam2Index
		if camIndex >= 0:
			actcam = self.cam2sel.value
			self["actifcam2"].setText(_("active CAM 2: ") + actcam)
			self.Save_Settings2(actcam)
			start = self.emuStart[camIndex]
			if self.checkBinName(self.emuBin[self.cam2Index], start):
					self.session.open(MessageBox, actcam + _(" Not Started !!\n\nCam binname must be in the start command line\nCheck your emu config file"), MessageBox.TYPE_ERROR, simple=True)
					return
			print '[SOFTCAM] Python start cam 2: ' + actcam
			self.session.open(MessageBox, _("Starting Cam 2: ") + actcam, MessageBox.TYPE_WARNING, timeout=5, simple=True)
			self.container = eConsoleAppContainer()
			self.container.execute(start)

	def Save_Settings(self, cam_name):
		config.softcam_actCam.setValue(cam_name)
		config.softcam.save()
		configfile.save()

	def Save_Settings2(self, cam_name):
		config.softcam_actCam2.setValue(cam_name)
		config.softcam.save()
		configfile.save()

	def isCamrunning(self, cam):
		p = command('pidof ' + cam + ' |wc -w')
		if not p.isdigit(): p=0
		if int(p) > 0:
			return True
		else:
			return False

	def checkBinName(self, binname, start):
		print "[CHECKBINNAME] bin=%s ,start=%s" %(binname,start)
		if start.find(binname + ' ') > -1:
			print "[CHECKBINNAME] OK"
			return False
		else:
			if start[start.rfind('/')+1:] == binname:
				print "[CHECKBINNAME] OK"
				return False
			else:
				print "[CHECKBINNAME] ERROR"
				return True

	def createInitdscript(self, camname, emubin, start, stop, wait=None):
		Adir = "/etc/init.d/softcam." + camname
		softcamfile = []
		softcamfile.append('#!/bin/sh')
		softcamfile.append('DAEMON=%s' % emubin)
		softcamfile.append('STARTCAM="%s"' % start)
		softcamfile.append('STOPCAM="%s"' % stop)
		softcamfile.append('DESC="Softcam"')
		softcamfile.append('')
		softcamfile.append('test -f $DAEMON || exit 0')
		softcamfile.append('set -e')
		softcamfile.append('')
		softcamfile.append('case "$1" in')
		softcamfile.append('	start)')
		softcamfile.append('		echo -n "starting $DESC: $DAEMON... "')
		if wait:
			softcamfile.append('		sleep ' + wait)
		softcamfile.append('		$STARTCAM')
		softcamfile.append('		echo "done."')
		softcamfile.append('		;;')
		softcamfile.append('	stop)')
		softcamfile.append('		echo -n "stopping $DESC: $DAEMON... "')
		softcamfile.append('		$STOPCAM')
		softcamfile.append('		echo "done."')
		softcamfile.append('		;;')
		softcamfile.append('	restart)')
		softcamfile.append('		echo "restarting $DESC: $DAEMON... "')
		softcamfile.append('		$0 stop')
		softcamfile.append('		echo "wait..."')
		softcamfile.append('		sleep 5')
		softcamfile.append('		$0 start')
		softcamfile.append('		echo "done."')
		softcamfile.append('		;;')
		softcamfile.append('	*)')
		softcamfile.append('		echo "Usage: $0 {start|stop|restart}"')
		softcamfile.append('		exit 1')
		softcamfile.append('		;;')
		softcamfile.append('esac')
		softcamfile.append('')
		softcamfile.append('exit 0')

		f = open( Adir, "w" )
		for x in softcamfile:
			f.writelines(x + '\n')
		f.close()

		self.container = eConsoleAppContainer()
		os.chmod(Adir,0755)
		if not os.path.exists("/etc/rc2.d/S20softcam." + camname):
			self.container.execute('update-rc.d -f softcam.' + camname + ' defaults')
		import time
		time.sleep (3) 

		if self.isCamrunning(emubin):
			self.container.execute('/etc/init.d/softcam.' + camname + ' restart')
		else:
			self.container.execute('/etc/init.d/softcam.' + camname + ' start')

	def deleteInit(self):
		if os.path.exists("/etc/rc2.d/S20softcam.cam1"):
			print "Delete Symbolink link"
			self.container = eConsoleAppContainer()
			self.container.execute('update-rc.d -f softcam.cam1 defaults')
		if os.path.exists("/etc/init.d/softcam.cam1"):
			print "Delete softcam init script cam1"
			os.system("rm /etc/init.d/softcam.cam1")
			
		if os.path.exists("/etc/rc2.d/S20softcam.cam2"):
			print "Delete Symbolink link"
			self.container = eConsoleAppContainer()
			self.container.execute('update-rc.d -f softcam.cam2 defaults')
		if os.path.exists("/etc/init.d/softcam.cam2"):
			print "Delete softcam init script cam2"
			os.system("rm /etc/init.d/softcam.cam2")

class ShowSoftcamPackages(Screen):
	skin = """
		<screen name="ShowSoftcamPackages" position="center,center" size="630,500" title="Install Softcams" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
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
		}, -1)
		
		self.list = []
		self.statuslist = []
		self["list"] = List(self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Reload"))
		self["key_ok"] = StaticText(_("Install"))

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
##################################################################
isBusy = None
CFG = "/usr/keys/CCcam.cfg"

def CamCheck():
    global campoller, POLLTIME
    POLLTIME = int(config.OPENDROID_frozencheck.list.value) * 60
    if campoller is None:
        campoller = CamCheckPoller()
    campoller.start()

def CamCheckStop():
    try:
        campoller.stop()
    except:
        print"CamCheck not running, so no need to stop it !! "

def confPath():
	search_dirs = [ "/usr", "/var", "/etc" ]
	sdirs = " ".join(search_dirs)
	cmd = 'find %s -name "CCcam.cfg" | head -n 1' % sdirs
	res = popen(cmd).read()
	if res == "":
		return None
	else:
		return res.replace("\n", "")

def getConfigValue(l):
	list = l.split(":")
	ret = ""

	if len(list) > 1:
		ret = (list[1]).replace("\n", "").replace("\r", "")
		if ret.__contains__("#"):
			idx = ret.index("#")
			ret = ret[:idx]
		while ret.startswith(" "):
			ret = ret[1:]
		while ret.endswith(" "):
			ret = ret[:-1]

	return ret

class CamCheckPoller:
    def __init__(self):
        self.timer = eTimer()
        self.onClose = []

    def start(self):
        global isBusy
        if isBusy:
            return
        isBusy = True
        if self.camcheck not in self.timer.callback:
            self.timer.callback.append(self.camcheck)
        self.timer.startLongTimer(60)

    def stop(self):
        global isBusy
        if self.camcheck in self.timer.callback:
            self.timer.callback.remove(self.camcheck)
        self.timer.stop()
        isBusy = None

    def camcheck(self):
        global isBusy
        isBusy = True
        threads.deferToThread(self.JobTask)
        self.timer.startLongTimer(POLLTIME)

    def JobTask(self):
        self.doCheck()
        self.timer.startLongTimer(POLLTIME)


    def FrozenCCcam(self, cam):
        if not cam.upper().startswith('CCCAM'):
            print "[CAMSCHECK] exit Frozen CCcam check, softcam is not CCcam"
            return False
        if path.exists(CFG):
            self.cfg = CFG
        else:
            self.cfg = confPath()
        if not self.cfg:
            print "[CAMSCHECK] exit Frozen CCcam check, CCcam.cfg not found"
            return False
        self.readConfig()
        ff = system('wget -s ' + self.url + ' 2>/dev/null')
        if ff > 0:
            print "[CAMSCHECK] Frozen CCcam detected"
            return True
        else:
            print "[CAMSCHECK] CCcam OK"
            return False

    def readConfig(self):
        self.url = "http://127.0.0.1:16001"
        username = None
        password = None

        try:
            f = open(self.cfg, 'r')
            for l in f:
                if l.startswith('WEBINFO LISTEN PORT :'):
                    port = getConfigValue(l)
                    if port != "":
                        self.url = self.url.replace('16001', port)
                elif l.startswith('WEBINFO USERNAME :'):
                    username = getConfigValue(l)
                elif l.startswith('WEBINFO PASSWORD :'):
                    password = getConfigValue(l)

            f.close()
        except:
            pass

        if (username is not None) and (password is not None) and (username != "") and (password != ""):
            self.url = self.url.replace('http://', ("http://%s:%s@" % (username, password)))

    def doCheck(self):
        emuDir = "/etc/"
        self.emuList = []
        self.mlist = []
        self.emuDirlist = []
        self.emuBin = []
        self.emuStart = []
        self.emuStop = []
        self.emuDirlist = listdir(emuDir)
        cam_name = config.softcam_actCam.value
        cam_name2 = config.softcam_actCam2.value
        if (cam_name == "no CAM 1 active" or cam_name == "") and (cam_name2 == "no CAM 2 active" or cam_name2 == ""):
            print "[CAMSCHECK] No Cam to Check, Exit"
            global isBusy
            isBusy = None
            return


        for x in self.emuDirlist:
            if x.find("emu") > -1:
                self.emuList.append(emuDir + x)
                em = open(emuDir + x)
                for line in em.readlines():
                    line1 = line
                    if line.find("emuname") > -1:
                        line = line.split("=")
                        self.mlist.append(line[1].strip())
                    line = line1
                    if line.find("binname") > -1:
                        line = line.split("=")
                        self.emuBin.append(line[1].strip())
                    line = line1
                    if line.find("startcam") > -1:
                        line = line.split("=")
                        self.emuStart.append(line[1].strip())
                    line = line1
                    if line.find("stopcam") > -1:
                        line = line.split("=")
                        self.emuStop.append(line[1].strip())

                em.close()

        camrunning = 0
        camfound = 0
        camfrozen = 0
        indexcam = -1
        camrunning2 = 0
        camfound2 = 0
        camfrozen2 = 0
        indexcam2 = -1
        tel = 0

        for x in self.mlist:
            if x == cam_name:
                camfound = 1
                indexcam = tel
                cam_bin = self.emuBin[tel]
                p = system('pidof %s' % cam_bin)
                if p != '':
                    if int(p) == 0:
                        actcam = self.mlist[tel]
                        print datetime.now()
                        print '[CAMSTARTER] CAM 1 is Running, active cam 1: ' + actcam
                        camrunning = 1
                        if self.FrozenCCcam(actcam):
                            camfrozen = 1
                tel +=1
            elif x == cam_name2:
                camfound2 = 1
                indexcam2 = tel
                cam_bin = self.emuBin[tel]
                p = system('pidof %s' % cam_bin)
                if p != '':
                    if int(p) == 0:
                        actcam = self.mlist[tel]
                        print datetime.now()
                        print '[CAMSTARTER] CAM 2 is Running, active cam 2: ' + actcam
                        camrunning2 = 1
                        if self.FrozenCCcam(actcam):
                            camfrozen2 = 1
                tel +=1
            else:
                tel +=1
        try:

            if camrunning == 0 or camfrozen == 1 or (camfound2 == 1 and camrunning2 == 0 or camfrozen2 == 1):
                if camfound == 1:
                    stop = self.emuStop[indexcam]
                    print "[CAMSTARTER] CAM 1 not running, stop " + stop
                    self.container = eConsoleAppContainer()
                    self.container.execute(stop)

                    start = self.emuStart[indexcam]
                    print "[CAMSTARTER] no CAM 1 active, starting " + start
                    system("echo %s Started cam 1 at: %s >> /tmp/camcheck.txt" % (start, datetime.now()))
                    self.container = eConsoleAppContainer()
                    self.container.execute(start)
                    if camrunning2 == 0 or camfrozen2 == 1:
                        if camfound2 == 1:
                            stop = self.emuStop[indexcam2]
                            print "[CAMSTARTER] CAM 2 not running, stop " + stop
                            self.container = eConsoleAppContainer()
                            self.container.execute(stop)
                            
                            import time
                            time.sleep (int(config.softcam_waittime.value))
                            start = self.emuStart[indexcam2]
                            print "[CAMSTARTER] no CAM 2 active, starting " + start
                            system("echo %s Started cam 2 at: %s >> /tmp/camcheck.txt" % (start, datetime.now()))
                            self.container = eConsoleAppContainer()
                            self.container.execute(start)
            else:
                if camfound == 0:
                    print "[CAMSTARTER] No Cam found to start"

        except:
            print "[CAMSCHECK] Error, can not start Cam"

        global isBusy
        isBusy = None

campoller = None

##################################################################

config.softcam_restartRunning = ConfigYesNo(default=True)
config.softcam_restartAttempts =  ConfigSelection(
                    [
                    ("0", _("0 (disabled)")),
                    ("1", _("1")),
                    ("3", _("3")),
                    ("5", _("5 (default)")),
                    ("10", _("10")),
                    ], "5")
config.softcam_restartTime = ConfigSelection(
                    [
                    ("5", _("5")),
                    ("10", _("10 (default)")),
                    ("20", _("20")),
                    ("30", _("30")),
                    ("60", _("60")),
                    ("120", _("120")),
                    ("240", _("240")),
                    ], "10")
config.softcam_camstartMode =  ConfigSelection(
                    [
                    ("0", _("Python Camstarter (default)")),
                    ("1", _("Init.d")),
                    ], "0")

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

class CamStart(Screen):
	skin = """
	<screen name="CamStart" position="center,center" size="484, 150" title="Starting Softcam">
		<widget name="connect" position="217, 0" size="64,64" zPosition="2" pixmaps="/usr/share/enigma2/oDreamy-FHD/opendroid/sc1.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc2.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc3.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc4.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc5.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc6.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc7.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc8.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc9.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc10.png,/usr/share/enigma2/oDreamy-FHD/opendroid/sc11.png"  transparent="1" alphatest="blend"/>
		<widget name="lab1" position="10, 80" halign="center" size="460, 60" zPosition="1" font="Regular;20" valign="top" transparent="1"/>
	</screen>"""
	def __init__(self, session):
		self.count = 0
		self.timerTime = 2
		Screen.__init__(self, session)
		self.session = session
		self.timer = eTimer()
		self.timer.timeout.get().append(self.timerEvent)
		self.list.append(getConfigListEntry(_("Start Mode"), config.softcam_camstartMode))
		if config.softcam_camstartMode.value == "0":
		        self.list.append(getConfigListEntry(_("Start attempts"), config.softcam_restartAttempts))
		        self.list.append(getConfigListEntry(_("Time between start attempts (sec.)"), config.softcam_restartTime))
		        self.list.append(getConfigListEntry(_("Stop check when cam is running"), config.softcam_restartRunning))
		        self.list.append(getConfigListEntry(_("Wait time before start Cam 2"), config.softcam_waittime))
		self.service = None

	def startTimer(self):
		if self.timer.isActive():
			pass
		else:
			self.timer.startLongTimer(self.timerTime)

	def StopTimer(self, result):
		if result:
			self.timer.stop()
			self.service = None

	def timerEvent(self):
		if config.softcam_restartAttempts.value == "0":
			return
		self.timerTime = int(config.softcam_restartTime.value)
		emuDir = "/etc/"
		self.emuList = []
		self.mlist = []
		self.emuDirlist = []
		self.emuBin = []
		self.emuStart = []
		self.emuDirlist = os.listdir(emuDir)
		cam_name = config.softcam_actCam.value
		cam_name2 = config.softcam_actCam2.value
		if (cam_name == "no CAM 1 active" or cam_name == "") and (cam_name2 == "no CAM 1 active" or cam_name2 == ""):
			self.timer.stop()
			self.service = None
			print "[CAMSTARTER] No Cam to Start, Exit"
		else:
			self.count += 1
			print '[CAMSTARTER] Start/Check: ' + str(self.count)
			for x in self.emuDirlist:
				if x.find("emu") > -1:
					self.emuList.append(emuDir + x)
					em = open(emuDir + x)
					for line in em.readlines():
						line1 = line
						if line.find("emuname") > -1:
							line = line.split("=")
							self.mlist.append(line[1].strip())
						line = line1
						if line.find("binname") > -1:
							line = line.split("=")
							self.emuBin.append(line[1].strip())
						line = line1
						if line.find("startcam") > -1:
							line = line.split("=")
							self.emuStart.append(line[1].strip())

					em.close()

			camrunning = 0
			camfound = 0
			indexcam = -1
			camrunning2 = 0
			camfound2 = 0
			indexcam2 = -1
			tel = 0
			for x in self.mlist:
				if x == cam_name:
					camfound = 1
					indexcam = tel
					cam_bin = self.emuBin[tel]
					p = command('pidof %s |wc -w' % cam_bin)
					if p != '':
						if int(p) > 0:
							actcam = self.mlist[tel]
							print datetime.datetime.now()
							print '[CAMSTARTER] CAM 1 is Running, active cam 1: ' + actcam
							camrunning = 1
					tel +=1
				elif x == cam_name2:
					camfound2 = 1
					indexcam2 = tel
					cam_bin = self.emuBin[tel]
					p = command('pidof %s |wc -w' % cam_bin)
					if p != '':
						if int(p) > 0:
							actcam = self.mlist[tel]
							print datetime.datetime.now()
							print '[CAMSTARTER] CAM 2 is Running, active cam 2: ' + actcam
							camrunning2 = 1
					tel +=1
				else:
					tel +=1
			try:
				if camrunning == 0:
					if camfound == 1:
						start = self.emuStart[indexcam]
						print "[CAMSTARTER] no CAM active, starting " + start
						os.system("echo Start attempts cam 1: " + str(self.count) + " cmd=" + start + " > " + "/tmp/camstarter.txt")
						self.container = eConsoleAppContainer()
						self.container.execute(start)
						if camrunning2 == 0:
							if camfound2 == 1:
								import time
								time.sleep (int(config.softcam_waittime.value))
								start = self.emuStart[indexcam2]
								print "[CAMSTARTER] no CAM active, starting " + start
								os.system("echo Start attempts cam 2: " + str(self.count) + " cmd=" + start + " >> " + "/tmp/camstarter.txt")
								self.container = eConsoleAppContainer()
								self.container.execute(start)
				else:
					if camfound == 0:
						print "[CAMSTARTER] No Cam found to start"
				
				if config.softcam_restartRunning.value and camrunning == 1:
					if camfound2 == 1:
						if camrunning2 == 1:
							print "[CAMSTARTER] Cam is running, exit camstarter"
							self.count = 0
							return
					else:
						print "[CAMSTARTER] Cam is running, exit camstarter"
						self.count = 0
						return

			except:
				pass

			if self.count < int(config.softcam_restartAttempts.value):
				self.startTimer()
			else:
				self.count = 0

timerInstance = None

class SoftcamSetup(ConfigListScreen, Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = "Setup"
		Screen.setTitle(self, _("Softcam-Setup") + "...")
		self.setup_title = _("Softcam-Setup") + "..."
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self["status"] = StaticText()
		self["footnote"] = Label()
		self["description"] = Label("")
		self["labelExitsave"] = Label("[Exit] = " +_("Cancel") +"              [Ok] =" +_("Save"))
		CamCheckStop()

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
		self["key_green"] = StaticText(_("Save"))
		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_("Start Mode"), config.softcam_camstartMode))
		if config.softcam_camstartMode.value == "0":
			self.list.append(getConfigListEntry(_("Start attempts"), config.softcam_restartAttempts))
			self.list.append(getConfigListEntry(_("Time between start attempts (sec.)"), config.softcam_restartTime))
			self.list.append(getConfigListEntry(_("Stop check when cam is running"), config.softcam_restartRunning))
		self.list.append(getConfigListEntry(_("Show CCcamInfo in Extensions Menu"), config.cccaminfo.showInExtensions))
		self.list.append(getConfigListEntry(_("Show OscamInfo in Extensions Menu"), config.oscaminfo.showInExtensions))
		self.list.append(getConfigListEntry(_("Wait time before start Cam 2"), config.softcam_waittime))
		
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
		self.createSetup()

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
		if config.softcam_camstartMode.value == "0":
			if os.path.exists("/etc/rc2.d/S20softcam.cam1"):
				print"Delete Symbolink link"
				self.container = eConsoleAppContainer()
				self.container.execute('update-rc.d -f softcam.cam1 defaults')
			if os.path.exists("/etc/init.d/softcam.cam1"):
				print"Delete softcam init script cam1"
				os.system("rm /etc/init.d/softcam.cam1")
				
			if os.path.exists("/etc/rc2.d/S20softcam.cam2"):
				print"Delete Symbolink link"
				self.container = eConsoleAppContainer()
				self.container.execute('update-rc.d -f softcam.cam2 defaults')
			if os.path.exists("/etc/init.d/softcam.cam2"):
				print"Delete softcam init script cam2"
				os.system("rm /etc/init.d/softcam.cam2")
			
		for x in self["config"].list:
			x[1].save()
		configfile.save()

	def keySave(self):
		self.saveAll()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x[1].cancel()

	def keyCancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"))
		self.close()
