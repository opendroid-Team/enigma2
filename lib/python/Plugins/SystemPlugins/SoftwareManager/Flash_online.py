from Plugins.Extensions.OPDBoot.plugin import *
from os import W_OK, access, listdir, major, makedirs, minor, mkdir, remove, sep, stat, statvfs, unlink, walk
from os.path import exists, isdir, isfile, islink, ismount, splitext, join as pathjoin
from shutil import rmtree
import zipfile
from Components.config import config
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.Task import Task, Job, job_manager, Condition
from Components.Sources.StaticText import StaticText
from Components.SystemInfo import BoxInfo
from Components.ProgressBar import ProgressBar
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.MultiBootManager import MultiBootManager
from Components.Console import Console
from Tools.BoundFunction import boundFunction
from Tools.MultiBoot import MultiBoot
from Screens.HelpMenu import HelpableScreen
from enigma import eTimer, fbClass
import json
import os
import shutil
import ssl
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import urllib.error
from os import path, popen
from Components.Pixmap import Pixmap
from Components.About import about
from json import load
from boxbranding import getImageType, getImageDistro, getImageVersion, getImageBuild, getImageDevBuild, getImageFolder, getImageFileSystem, getBrandOEM, getMachineBrand, getMachineName, getMachineBuild, getMachineMake, getMachineMtdRoot, getMachineRootFile, getMachineMtdKernel, getMachineKernelFile, getMachineMKUBIFS, getMachineUBINIZE
machinebuild = BoxInfo.getItem("machinebuild")

feedurl = 'https://opendroid.org/'
imagecat = [7.1, 7.0]

FEED_URLS = {
	"EGAMI": ("http://image.egami-image.com/json/%s", "machinebuild"),
	"OpenATV": ("http://images.mynonpublic.com/openatv/json/%s", "machinebuild"),
	"OpenBH": ("https://images.openbh.net/json/%s", "model"),
	"OpenPLi": ("http://downloads.openpli.org/json/%s", "model"),
	"OpenVisionE2": ("https://images.openvision.dedyn.io/json/%s", "model"),
	"OpenViX": ("https://www.openvix.co.uk/json/%s", "machinebuild"),
	"TeamBlue": ("https://images.teamblue.tech/json/%s", "machinebuild"),
	"OpenHDF": ("https://flash.hdfreaks.cc/openhdf/json/%s", "machinebuild"),
	"Open8eIGHT": ("http://openeight.de/json/%s", "machinebuild"),
	"OpenDROID": ("https://opendroid.org/json/%s", "machinebuild")
}


def checkimagefiles(files):
	return len([x for x in files if "kernel" in x and ".bin" in x or x in ("zImage", "uImage", "root_cfe_auto.bin", "root_cfe_auto.jffs2", "oe_kernel.bin", "oe_rootfs.bin", "e2jffs2.img", "rootfs.tar.bz2", "rootfs.ubi", "rootfs.bin")]) >= 2

def my_requests(url):
	req = Request(url, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
	context = ssl._create_unverified_context()
	response = urlopen(req, context=context)
	link = response.read().decode('utf-8')
	response.close()
	return link

class FlashOnline(Screen, HelpableScreen):
	skin = """
	<screen name="FlashOnline" position="center,center" size="550,400">
		<widget name="list" position="fill" scrollbarMode="showOnDemand"/>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		HelpableScreen.__init__(self)
		self.skinName = ["FlashOnline"]
		self.imageFeed = "OpenPLi"
		self.selection = 0
		self.imagesList = {}
		self.expanded = []
		self.setIndex = 0
		Screen.setTitle(self, _("Flash On the Fly"))

		self["actions"] = HelpableActionMap(self, ["CancelSaveActions", "OkActions", "OkCancelActions", "NavigationActions", "ColorActions", "DirectionActions", "TimerEditActions", "SetupActions"],
						    {
							    "ok": self.keyOk,
							    "cancel": boundFunction(self.close, None),
							    "red": boundFunction(self.close, None),
							    "green": self.keyOk,
							    "yellow": (self.keyDistribution, _("Select a distribution from where images are to be obtained")),
							    "blue": self.keyDelete,
							    "up": self.keyUp,
							    "down": self.keyDown,
							    "left": self.keyLeft,
							    "right": self.keyRight,
							    "upRepeated": self.keyUp,
							    "downRepeated": self.keyDown,
							    "leftRepeated": self.keyLeft,
							    "rightRepeated": self.keyRight,
							    "menu": boundFunction(self.close, True),
							    }, prio=-1)
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText()
		self["key_yellow"] = StaticText(_("Distribution"))
		self["key_blue"] = StaticText()
		self["description"] = StaticText()
		self["list"] = ChoiceList(list=[ChoiceEntryComponent("", ((_("Retrieving image list - Please wait...")), "Loading"))])
		self.delay = eTimer()
		self.callLater(self.getImagesList)
		self.delay.start(0, True)

	def getImagesList(self):
		def getImages(path, files):
			for file in [x for x in files if splitext(x)[1] == ".zip" and box in x]:
				try:
					if checkimagefiles([x.split(sep)[-1] for x in zipfile.ZipFile(file).namelist()]):
						imageType = _("Downloaded images")
						if "backup" in file.split(sep)[-1]:
							imageType = _("Backup images")
						if imageType not in self.imagesList:
							self.imagesList[imageType] = {}
						self.imagesList[imageType][file] = {
							"link": str(file),
							"name": str(file.split(sep)[-1])
						}
				except Exception:
					print("[FlashOnline] Error: Unable to extract file list from Zip file '%s'!" % file)

		if not self.imagesList:
			try:
				feedURL, boxInfoField = FEED_URLS.get(self.imageFeed, ("http://images.mynonpublic.com/openatv/json/%s", "BoxName"))
				self.box = BoxInfo.getItem(boxInfoField, "")
				url = feedURL % self.box
				req = Request(url, None, {"User-agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"})
				self.imagesList = dict(load(urlopen(req)))
			except Exception:
				print("[FlashOnline] Error: Unable to load json data from URL '%s'!" % url)
			box = getBoxType()
			brand = getMachineBrand()
			version = getImageVersion()
			for version in reversed(sorted(imagecat)):
				newversion = _("Image Version %s") %version
				the_page =""
				url = '%s/%s/%s/%s' % (feedurl, version,brand,box)
				try:
					req = my_requests(url)
				except urllib.error.URLError as e:
					print("URL ERROR: %s\n%s" % (e, url))
					continue

				try:
					the_page = req
				except urllib.error.URLError as e:
					print("HTTP download ERROR: %s" % e.code)
					continue

				lines = the_page.split('\n')
				tt = len(box)
				b = len(brand)
				countimage = []
				for line in lines:
					if line.find('<a href="o') > -1:
						t = line.find('<a href="o')
						e = line.find('zip"')
						countimage.append(line[t + 9:e + 3])
					if line.find('recovery_emmc.zip"') > -1:
						x = line.find('recovery_emmc.zip"')
						countimage.remove(line[t + 9:e + 3])
				if len(countimage) >= 1:
					self.imagesList[newversion] = {}
					for image in countimage:
						self.imagesList[newversion][image] = {}
						self.imagesList[newversion][image]["name"] = image
						self.imagesList[newversion][image]["link"] = '%s/%s/%s/%s/%s' % (feedurl, version, brand, box, image)

			for media in ["/media/%s" % x for x in listdir("/media")] + (["/media/net/%s" % x for x in listdir("/media/net")] if isdir("/media/net") else []):
				print("[FlashOnline] OLD DEBUG: media='%s'." % media)
				if not(BoxInfo.getItem("HasMMC") and "/mmc" in media) and isdir(media):
					getImages(media, [pathjoin(media, x) for x in listdir(media) if splitext(x)[1] == ".zip" and box in x])
					for folder in ["images", "downloaded_images", "imagebackups"]:
						if folder in listdir(media):
							subfolder = pathjoin(media, folder)
							print("[FlashOnline] OLD DEBUG: subfolder='%s'." % subfolder)
							if isdir(subfolder) and not islink(subfolder) and not ismount(subfolder):
								print("[FlashOnline] OLD DEBUG: Next subfolder='%s'." % subfolder)
								getImages(subfolder, [pathjoin(subfolder, x) for x in listdir(subfolder) if splitext(x)[1] == ".zip" and box in x])
								for dir in [dir for dir in [pathjoin(subfolder, dir) for dir in listdir(subfolder)] if isdir(dir) and splitext(dir)[1] == ".unzipped"]:
#									shutil.rmtree(dir)
									try:
										rmtree(dir)
									except (IOError, OSError) as err:
										print("[FlashOnline] Error %d: Unable to remove directory '%s'!  (%s)" % (err.errno, dir, err.strerror))
		imageList = []
		for catagory in reversed(sorted(self.imagesList.keys())):
			if catagory in self.expanded:
				imageList.append(ChoiceEntryComponent("expanded", ((str(catagory)), "Expanded")))
				for image in reversed(sorted(list(self.imagesList[catagory].keys()), key=lambda x: x.split(sep)[-1])):
					imageList.append(ChoiceEntryComponent("verticalline", ((self.imagesList[catagory][image]["name"]), self.imagesList[catagory][image]["link"])))
			else:
				for image in self.imagesList[catagory].keys():
					imageList.append(ChoiceEntryComponent("expandable", ((catagory), "Expanded")))
					break
		if imageList:
			self["list"].setList(imageList)
			if self.setIndex:
				self["list"].moveToIndex(self.setIndex if self.setIndex < len(imageList) else len(imageList) - 1)
				if self["list"].l.getCurrentSelection()[0][1] == "Expanded":
					self.setIndex -= 1
					if self.setIndex:
						self["list"].moveToIndex(self.setIndex if self.setIndex < len(imageList) else len(imageList) - 1)
				self.setIndex = 0
			self.selectionChanged()
		else:
			self.session.openWithCallback(self.close, MessageBox, _("Error: Cannot find any images!"), type=MessageBox.TYPE_ERROR, timeout=3)

	def keyOk(self):
		currentSelection = self["list"].l.getCurrentSelection()
		if currentSelection[0][1] == "Expanded":
			if currentSelection[0][0] in self.expanded:
				self.expanded.remove(currentSelection[0][0])
			else:
				self.expanded.append(currentSelection[0][0])
			self.getImagesList()
		elif currentSelection[0][1] != "Loading":
			self.session.openWithCallback(self.getImagesList, FlashImage, currentSelection[0][0], currentSelection[0][1])

	def keyDistribution(self):
		default = 0
		distributionList = []
		for index, distribution in enumerate(sorted(FEED_URLS.keys())):
			distributionList.append((distribution, distribution))
			if distribution == self.imageFeed:
				default = index
		message = _("Please select a distribution from which you would like to flash an image:")
		self.session.openWithCallback(self.keyDistributionCallback, MessageBox, message, default=default, list=distributionList, windowTitle=_("Flash Online"))

	def keyDistributionCallback(self, distribution):
		self.imageFeed = distribution
		self.setTitle(_("Flash OnLine - %s Images") % self.imageFeed)
		self.imagesList = {}
		self.expanded = []
		self.setIndex = 0
		self.getImagesList()
		self["list"].moveToIndex(self.setIndex)

	def keyDelete(self):
		currentSelection = self["list"].l.getCurrentSelection()[0][1]
		if not("://" in currentSelection or currentSelection in ["Expanded", "Loading"]):
			try:
				remove(currentSelection)
				currentSelection = ".".join([currentSelection[:-4], "unzipped"])
				if isdir(currentSelection):
					rmtree(currentSelection)
				self.setIndex = self["list"].getSelectedIndex()
				self.imagesList = {}
				self.getImagesList()
			except (IOError, OSError) as err:
				self.session.open(MessageBox, _("Error %d: Unable to delete downloaded image '%s'!  (%s)" % (err.errno, currentSelection, err.strerror)), MessageBox.TYPE_ERROR, timeout=3)

	def selectionChanged(self):
		currentSelection = self["list"].l.getCurrentSelection()[0]
		self["key_blue"].setText("" if "://" in currentSelection[1] or currentSelection[1] in ["Expanded", "Loading"] else _("Delete Image"))
		if currentSelection[1] == "Loading":
			self["key_green"].setText("")
		else:
			if currentSelection[1] == "Expanded":
				self["key_green"].setText(_("Collapse") if currentSelection[0] in self.expanded else _("Expand"))
				self["description"].setText("")
			else:
				self["key_green"].setText(_("Flash Image"))
				self["description"].setText(_("Location: %s") % currentSelection[1][:currentSelection[1].rfind(sep) + 1])

	def keyLeft(self):
		self["list"].instance.moveSelection(self["list"].instance.moveTop)
		self.selectionChanged()
		self["list"].instance.moveSelection(self["list"].instance.pageUp)
		self.selectionChanged()

	def keyRight(self):
		self["list"].instance.moveSelection(self["list"].instance.pageDown)
		self.selectionChanged()

	def keyUp(self):
		self["list"].instance.moveSelection(self["list"].instance.moveUp)
		self.selectionChanged()

	def keyDown(self):
		self["list"].instance.moveSelection(self["list"].instance.moveDown)
		self.selectionChanged()


class FlashImage(Screen):
	skin = """
	<screen position="center,center" size="1200,600" flags="wfNoBorder" backgroundColor="#54242424">
		<widget name="header" position="5,10" size="e-10,50" font="Regular;40" backgroundColor="#54242424"/>
		<widget name="info" position="5,60" size="e-10,130" font="Regular;24" backgroundColor="#54242424"/>
		<widget name="progress" position="5,e-39" size="e-10,24" backgroundColor="#54242424"/>
	</screen>"""

	def __init__(self, session, imagename, source):
		Screen.__init__(self, session)
		self.containerbackup = None
		self.containerofgwrite = None
		self.getImageList = None
		self.saveImageList = None
		self.downloader = None
		self.source = source
		self.imagename = imagename
#		self["key_red"] = Label(_("Cancel"))
#		self["key_green"] = Label(_("ok"))
		self["header"] = Label(_("Backup settings"))
		self["info"] = Label(_("Save settings and EPG data"))
		self["summary_header"] = StaticText(self["header"].getText())
		self["actions"] = HelpableActionMap(self, ["OkCancelActions"], {
			"cancel": (self.abort, _("Add help text")),
			"ok": (self.ok, _("Add help text"))
			}, prio=-1)
		self["progress"] = ProgressBar()
		self["progress"].setRange((0, 100))
		self["progress"].setValue(0)
#		self["actions"] = HelpableActionMap(["OkCancelActions", "ColorActions"],
#		self["actions"] = HelpableActionMap(self, ["OkCancelActions"], {
#			"cancel": (self.abort, _("Add help text")),
#			"ok": (self.ok, _("Add help text"))
#		}, prio=-1)
		self.delay = eTimer()
		self.delay.callback.append(self.confirmation)
		self.delay.start(0, True)
		self.hide()

	def confirmation(self):
		self.message = _("Do you want to flash image\n%s") % self.imagename
		if MultiBoot.canMultiBoot():
			self.getImageList = MultiBoot.getSlotImageList(self.getImagelistCallback)
		else:
			self.checkMedia(True)

	def getImagelistCallback(self, imagedict):
		self.saveImageList = imagedict
		self.getImageList = None
		choices = []
		for item in imagedict.copy():
			if not item.isdecimal():
				imagedict.pop(item)
		currentimageslot = int(MultiBoot.getCurrentSlotCode())
		print("[FlashOnline] Current image slot %s." % currentimageslot)
		for slotCode in imagedict.keys():
			print("[FlashOnline] Image Slot %s: %s" % (slotCode, str(imagedict)))
			choices.append(((_("slot%s - %s (current image)") if slotCode == currentimageslot else _("slot%s - %s")) % (slotCode, imagedict[slotCode]["imagename"]), (slotCode, True)))
		choices.append((_("No, do not flash an image"), False))
		self.session.openWithCallback(self.checkMedia, MessageBox, self.message, list=choices, default=currentimageslot - 1)

	def backupQuestionCB(self, retval=True):
		if retval:
			self.checkMedia("backup")
		else:
			self.checkMedia("no_backup")

	def checkMedia(self, retval):
		if retval:
			if not "backup" in str(retval):
				if MultiBoot.canMultiBoot():
					self.multibootslot = retval[0]
				self.session.openWithCallback(self.backupQuestionCB, MessageBox, _("Backup Settings") + "?", default=True, timeout=10)
				return

			def findmedia(paths):
				def avail(path):
					if not "/mmc" in path and isdir(path) and access(path, W_OK):
						try:
							fs = statvfs(path)
							return (fs.f_bavail * fs.f_frsize) / (1 << 20)
						except:
							pass
					return 0

				def checkIfDevice(path, diskstats):
					st_dev = stat(path).st_dev
					return (major(st_dev), minor(st_dev)) in diskstats

				diskstats = [(int(x[0]), int(x[1])) for x in [x.split()[0:3] for x in open("/proc/diskstats").readlines()] if x[2].startswith("sd")]
				for path in paths:
					if isdir(path) and checkIfDevice(path, diskstats) and avail(path) > 500:
						return (path, True)
				mounts = []
				devices = []
				for path in ["/media/%s" % x for x in listdir("/media")] + (["/media/net/%s" % x for x in listdir("/media/net")] if isdir("/media/net") else []):
					if checkIfDevice(path, diskstats):
						devices.append((path, avail(path)))
					else:
						mounts.append((path, avail(path)))
				devices.sort(key=lambda x: x[1], reverse=True)
				mounts.sort(key=lambda x: x[1], reverse=True)
				return ((devices[0][1] > 500 and (devices[0][0], True)) if devices else mounts and mounts[0][1] > 500 and (mounts[0][0], False)) or (None, None)

			self.destination, isDevice = findmedia(["/media/hdd", "/media/usb"])

			if self.destination:

				destination = pathjoin(self.destination, "images")
				self.zippedimage = "://" in self.source and pathjoin(destination, self.imagename) or self.source
				self.unzippedimage = pathjoin(destination, "%s.unzipped" % self.imagename[:-4])

				try:
					if isfile(destination):
						remove(destination)
					if not isdir(destination):
						mkdir(destination)
					if isDevice or "no_backup" == retval:
						self.startBackupsettings(retval)
					else:
						self.session.openWithCallback(self.startBackupsettings, MessageBox, _("Can only find a network drive to store the backup this means after the flash the autorestore will not work. Alternatively you can mount the network drive after the flash and perform a manufacturer reset to autorestore"))
				except:
					self.session.openWithCallback(self.abort, MessageBox, _("Unable to create the required directories on the media (e.g. USB stick or Harddisk) - Please verify media and try again!"), type=MessageBox.TYPE_ERROR)
			else:
				self.session.openWithCallback(self.abort, MessageBox, _("Could not find suitable media - Please remove some downloaded images or insert a media (e.g. USB stick) with sufficient free space and try again!"), type=MessageBox.TYPE_ERROR)
		else:
			self.abort()

	def startBackupsettings(self, retval):
		if retval:
			if "backup" == retval or True == retval:
				from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen
				self.session.openWithCallback(self.flashPostAction, BackupScreen, runBackup=True)
			else:
				self.flashPostAction()
		else:
			self.abort()

	def flashPostAction(self, retval=True):
		if retval:
			self.recordcheck = False
			title = _("Please select what to do after flashing the image:\n(In addition, if it exists, a local script will be executed as well at /media/hdd/images/config/myrestore.sh)")
			choices = ((_("Upgrade (Backup, Flash & Restore All)"), "restoresettingsandallplugins"),
				   (_("Clean (Just flash and start clean)"), "wizard"),
				   (_("Backup, flash and restore settings and no plugins"), "restoresettingsnoplugin"),
				   (_("Backup, flash and restore settings and selected plugins (ask user)"), "restoresettings"),
				   (_("Do not flash image"), "abort"))
			self.session.openWithCallback(self.postFlashActionCallback, ChoiceBox, title=title, list=choices, selection=self.SelectPrevPostFlashAction())
		else:
			self.abort()

	def SelectPrevPostFlashAction(self):
		index = 1
		if exists("/media/hdd/images/config/settings"):
			index = 3
			if exists("/media/hdd/images/config/noplugins"):
				index = 2
			if exists("/media/hdd/images/config/plugins"):
				index = 0
		return index

	def recordWarning(self, answer):
		if answer:
			self.postFlashActionCallback(self.answer)
		else:
			self.abort()

	def postFlashActionCallback(self, answer):
		if answer is not None:
			rootFolder = "/media/hdd/images/config"
			if answer[1] != "abort" and not self.recordcheck:
				self.recordcheck = True
				rec = self.session.nav.RecordTimer.isRecording()
				next_rec_time = self.session.nav.RecordTimer.getNextRecordingTime()
				if rec or (next_rec_time > 0 and (next_rec_time - time()) < 360):
					self.answer = answer
					self.session.openWithCallback(self.recordWarning, MessageBox, _("Recording(s) are in progress or coming up in few seconds!") + "\n" + _("Really reflash your %s %s and reboot now?") % (BoxInfo.getItem("displaybrand"), BoxInfo.getItem("displaymodel")), default=False)
					return
			restoreSettings = ("restoresettings" in answer[1])
			restoreSettingsnoPlugin = (answer[1] == "restoresettingsnoplugin")
			restoreAllPlugins = (answer[1] == "restoresettingsandallplugins")
			if restoreSettings:
				self.SaveEPG()
			if answer[1] != "abort":
				filestocreate = []
				try:
					if not exists(rootFolder):
						makedirs(rootFolder)
				except (IOError, OSError) as err:
					print("[FlashOnline] postFlashActionCallback: Error %d: Failed to create '%s' folder! (%s)" % (err.errno, rootFolder, err.strerror))

				if restoreSettings:
					filestocreate.append("settings")
				if restoreAllPlugins:
					filestocreate.append("plugins")
				if restoreSettingsnoPlugin:
					filestocreate.append("noplugins")

				for fileName in ["settings", "plugins", "noplugins"]:
					if fileName in filestocreate:
						path = pathjoin(rootFolder, fileName)
						try:
							open(path, "w").close()
						except (IOError, OSError) as err:
							print("[FlashOnline] postFlashActionCallback: Error %d: failed to create %s! (%s)" % (err.errno, path, err.strerror))
					else:
						if exists(path):
							unlink(path)

				if restoreSettings:
					if config.plugins.softwaremanager.restoremode.value is not None:
						try:
							for fileName in ["slow", "fast", "turbo"]:
								path = pathjoin(rootFolder, fileName)
								if fileName == config.plugins.softwaremanager.restoremode.value:
									if not exists(path):
										open(path, "w").close()
								else:
									if exists(path):
										unlink(path)
						except (IOError, OSError) as err:
							print("[FlashOnline] postFlashActionCallback: Error %d: failed to create restore mode flagfile! (%s)" % (err.errno, err.strerror))
				self.startDownload()
			else:
				self.abort()
		else:
			self.abort()

	def SaveEPG(self):
		from enigma import eEPGCache
		epgcache = eEPGCache.getInstance()
		epgcache.save()

	def startDownload(self, reply=True):
		self.show()
		if reply:
			if "://" in self.source:
				from Tools.Downloader import downloadWithProgress
				self["header"].setText(_("Downloading Image ... Please wait"))
				self["info"].setText(self.imagename)
				self["summary_header"].setText(self["header"].getText())
				self.downloader = downloadWithProgress(self.source, self.zippedimage)
				self.downloader.addProgress(self.downloadProgress)
				self.downloader.addEnd(self.downloadEnd)
				self.downloader.addError(self.downloadError)
				self.downloader.start()
			else:
				self.unzip()
		else:
			self.abort()

	def downloadProgress(self, current, total):
		self["progress"].setValue(int(100 * current / total))

	def downloadError(self, reason, status):
		self.downloader.stop()
		self.session.openWithCallback(self.abort, MessageBox, _("Error during downloading image\n%s\n%s") % (self.imagename, reason), type=MessageBox.TYPE_ERROR)

	def downloadEnd(self):
		self.downloader.stop()
		self.unzip()

	def unzip(self):
		self["header"].setText(_("Unzipping Image"))
		self["summary_header"].setText(self["header"].getText())
		self["info"].setText("%s\n%s" % (self.imagename, _("Please wait")))
		self["progress"].hide()
		self.delay.callback.remove(self.confirmation)
		self.delay.callback.append(self.doUnzip)
		self.delay.start(0, True)

	def doUnzip(self):
		try:
			zipfile.ZipFile(self.zippedimage, "r").extractall(self.unzippedimage)
			self.doFlashImage()
		except:
			self.session.openWithCallback(self.abort, MessageBox, _("Error during unzipping image\n%s") % self.imagename, type=MessageBox.TYPE_ERROR)

	def doFlashImage(self):
		self["header"].setText(_("Flashing Image"))
		self["summary_header"].setText(self["header"].getText())

		def findimagefiles(path):
			for path, subdirs, files in walk(path):
				if not subdirs and files:
					return checkimagefiles(files) and path
		imagefiles = findimagefiles(self.unzippedimage)
		if imagefiles:
			self.ROOTFSSUBDIR = "none"
			bootSlots = MultiBoot.getBootSlots()
			if bootSlots:
				self.MTDKERNEL = bootSlots[self.multibootslot]["kernel"].split("/")[2]
				if bootSlots[self.multibootslot].get("ubi"):
					self.MTDROOTFS = bootSlots[self.multibootslot]["device"]
				else:
					self.MTDROOTFS = bootSlots[self.multibootslot]["device"].split("/")[2]
				if MultiBoot.hasRootSubdir():
					self.ROOTFSSUBDIR = bootSlots[self.multibootslot]["rootsubdir"]
			else:
				self.MTDKERNEL = getMachineMtdKernel()
				self.MTDROOTFS = getMachineMtdRoot()
			if getMachineBuild() in ("dm820", "dm7080"): # temp solution ofgwrite autodetection not ready
				CMD = "/usr/bin/ofgwrite -rmmcblk0p1 '%s'" % imagefiles
			elif self.MTDKERNEL == self.MTDROOTFS:	# receiver with kernel and rootfs on one partition
				CMD = "/usr/bin/ofgwrite -r '%s'" % imagefiles
			else:
				CMD = "/usr/bin/ofgwrite -r -k '%s'" % imagefiles	#normal non multiboot receiver
			if MultiBoot.canMultiBoot():
				if (self.ROOTFSSUBDIR) is None:	# receiver with SD card multiboot
					CMD = "/usr/bin/ofgwrite -r%s -k%s -m0 '%s'" % (self.MTDROOTFS, self.MTDKERNEL, imagefiles)
				else:
					CMD = "/usr/bin/ofgwrite -r -k -m%s '%s'" % (self.multibootslot, imagefiles)
			self.containerofgwrite = Console()
			self.containerofgwrite.ePopen(CMD, self.flashImageDone)
			fbClass.getInstance().lock()
		else:
			self.session.openWithCallback(self.abort, MessageBox, _("Image to install is invalid\n%s") % self.imagename, type=MessageBox.TYPE_ERROR)

	def flashImageDone(self, data, retval, extra_args):
		fbClass.getInstance().unlock()
		self.containerofgwrite = None
		if retval == 0:
			self["header"].setText(_("Flashing image successful"))
			self["summary_header"].setText(self["header"].getText())
			self["info"].setText(_("%s\nPress ok for multiboot selection\nPress exit to close") % self.imagename)
		else:
			self.session.openWithCallback(self.abort, MessageBox, _("Flashing image was not successful\n%s") % self.imagename, type=MessageBox.TYPE_ERROR)

	def abort(self, reply=None):
		if self.getImageList or self.containerofgwrite:
			return 0
		if self.downloader:
			self.downloader.stop()
		self.close()

	def ok(self):
		fbClass.getInstance().unlock()
		if self["header"].text == _("Flashing image successful"):
			if MultiBoot.canMultiBoot():
				self.session.openWithCallback(self.abort, MultiBootManager)
			else:
				self.close()
		else:
			return 0
