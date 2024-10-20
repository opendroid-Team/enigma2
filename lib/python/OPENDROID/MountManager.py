from __future__ import print_function
from Screens.Screen import Screen
from enigma import eTimer
from boxbranding import getMachineBrand, getMachineName, getBoxType, getMachineBuild
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigSelection, NoSave, configfile
from Components.Console import Console
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Tools.LoadPixmap import LoadPixmap
from os import system, rename, path, mkdir, remove
from time import sleep
from re import search
import six


class DeviceManager(Screen):
	skin = """
	<screen position="center,center" size="640,460" title="Devices Manager">
		<ePixmap pixmap="skin_default/buttons/red.png" position="25,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="175,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="325,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/blue.png" position="475,0" size="140,40" alphatest="on" />
		<widget name="key_red" position="25,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="175,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="325,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="key_blue" position="475,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
		<widget source="list" render="Listbox" position="10,50" size="620,450" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
				{"template": [
				 MultiContentEntryText(pos = (90, 0), size = (600, 30), font=0, text = 0),
				 MultiContentEntryText(pos = (110, 30), size = (600, 50), font=1, flags = RT_VALIGN_TOP, text = 1),
				 MultiContentEntryPixmapAlphaBlend(pos = (0, 0), size = (80, 80), png = 2),
				],
				"fonts": [gFont("Regular", 24),gFont("Regular", 20)],
				"itemHeight": 85
				}
			</convert>
		</widget>
		<widget name="lab1" zPosition="2" position="50,90" size="600,40" font="Regular;22" halign="center" transparent="1"/>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Devices Manager"))
		self['key_red'] = StaticText(" ")
		self['key_green'] = Label(_("Setup Mounts"))
		self['key_yellow'] = Label(_("Unmount"))
		self['key_blue'] = Label(_("Mount"))
		self['lab1'] = Label()
		self.onChangedEntry = []
		self.list = []
		self['list'] = List(self.list)
		self["list"].onSelectionChanged.append(self.selectionChanged)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions', "MenuActions"], {'back': self.close, 'green': self.SetupMounts, 'red': self.saveMypoints, 'yellow': self.Unmount, 'blue': self.Mount, "menu": self.close})
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.updateList2)
		self.updateList()

	def createSummary(self):
		return DevicesPanelSummary

	def selectionChanged(self):
		if len(self.list) == 0:
			return
		self.sel = self['list'].getCurrent()
		mountp = self.sel[3]
		if mountp.find('/media/hdd') < 0:
			self["key_red"].setText(_("Use as HDD"))
		else:
			self["key_red"].setText(" ")

		if self.sel:
			try:
				name = str(self.sel[0])
				desc = str(self.sel[1].replace('\t', '  '))
			except:
				name = ""
				desc = ""
		else:
			name = ""
			desc = ""
		for cb in self.onChangedEntry:
			cb(name, desc)

	def updateList(self, result=None, retval=None, extra_args=None):
		scanning = _("Wait please while scanning for devices...")
		self['lab1'].setText(scanning)
		self.activityTimer.start(10)

	def updateList2(self):
		self.activityTimer.stop()
		self.list = []
		list2 = []
		f = open('/proc/partitions', 'r')
		for line in f.readlines():
			parts = line.strip().split()
			if not parts:
				continue
			device = parts[3]
			if not search('sd[a-z][1-9]', device) and not search('mmcblk[0-9]p[1-9]', device):
				continue
			if getMachineBuild() in ('multibox', 'multiboxse', 'dagsmv200', 'gbmv200', 'v8plus', 'hd60', 'hd61', 'pulse4k', 'pulse4kmini', 'vuduo4k', 'vuduo4kse', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'sf8008', 'sf8008m', 'sf8008opt', 'cc1', 'dags72604', 'u51', 'u52', 'u53', 'u532', 'u533', 'u54', 'u56', 'u57', 'u571', 'vuzero4k', 'u5', 'sf5008', 'et13000', 'et1x000', 'vuuno4k', 'vuuno4kse', 'vuultimo4k', 'vusolo4k', 'hd51', 'hd52', 'dm820', 'dm7080', 'sf4008', 'dm900', 'dm920', 'gb7252', 'gb72604', 'dags7252', 'vs1500', '8100s') and search('mmcblk0p[1-9]', device):
				continue
			if getMachineBuild() in ('xc7439', 'osmio4k', 'osmio4kplus', 'osmini4k') and search('mmcblk1p[1-9]', device):
				continue
			if device in list2:
				continue
			self.buildMy_rec(device)
			list2.append(device)

		f.close()
		self['list'].list = self.list
		self['lab1'].hide()

	def buildMy_rec(self, device):
		device2 = ''
		try:
			if device.find('1') > 1:
				device2 = device.replace('1', '')
		except:
			device2 = ''
		try:
			if device.find('2') > 1:
				device2 = device.replace('2', '')
		except:
			device2 = ''
		try:
			if device.find('3') > 1:
				device2 = device.replace('3', '')
		except:
			device2 = ''
		try:
			if device.find('4') > 1:
				device2 = device.replace('4', '')
		except:
			device2 = ''
		try:
			if device.find('5') > 1:
				device2 = device.replace('5', '')
		except:
			device2 = ''
		try:
			if device.find('6') > 1:
				device2 = device.replace('6', '')
		except:
			device2 = ''
		try:
			if device.find('7') > 1:
				device2 = device.replace('7', '')
		except:
			device2 = ''
		try:
			if device.find('8') > 1:
				device2 = device.replace('8', '')
		except:
			device2 = ''
		try:
			if device.find('p1') > 1:
				device2 = device.replace('p1', '')
		except:
			device2 = ''
		try:
			if device.find('p2') > 1:
				device2 = device.replace('p2', '')
		except:
			device2 = ''
		try:
			if device.find('p3') > 1:
				device2 = device.replace('p3', '')
		except:
			device2 = ''
		try:
			if device.find('p4') > 1:
				device2 = device.replace('p4', '')
		except:
			device2 = ''
		try:
			if device.find('p5') > 1:
				device2 = device.replace('p5', '')
		except:
			device2 = ''
		try:
			if device.find('p6') > 1:
				device2 = device.replace('p6', '')
		except:
			device2 = ''
		try:
			if device.find('p7') > 1:
				device2 = device.replace('p7', '')
		except:
			device2 = ''
		try:
			if device.find('p8') > 1:
				device2 = device.replace('p8', '')
		except:
			device2 = ''
		devicetype = path.realpath('/sys/block/' + device2 + '/device')
		d2 = device
		name = 'USB: '
		mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_usb.png'
		if device2.startswith('mmcblk'):
			try:
				model = open('/sys/block/' + device2 + '/device/name').read()
			except:
				model = ''
			mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_mmc.png'
			name = 'MMC: '
		else:
			try:
				model = open('/sys/block/' + device2 + '/device/model').read()
			except:
				model = ''
		model = str(model).replace('\n', '')
		des = ''
		if devicetype.find('/devices/pci') != -1 or devicetype.find('ahci') != -1:
			name = _("HARD DISK: ")
			mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_hdd.png'
		name = name + model
		self.Console = Console()
		self.Console.ePopen("sfdisk -l | grep swap | awk '{print $(NF-9)}' >/tmp/devices.tmp")
		sleep(0.5)
		try:
			f = open('/tmp/devices.tmp', 'r')
			swapdevices = f.read()
			f.close()
		except:
			swapdevices = ' '
		if path.exists('/tmp/devices.tmp'):
			remove('/tmp/devices.tmp')
		swapdevices = swapdevices.replace('\n', '')
		swapdevices = swapdevices.split('/')
		f = open('/proc/mounts', 'r')
		for line in f.readlines():
			if line.find(device) != -1:
				parts = line.strip().split()
				d1 = parts[1]
				dtype = parts[2]
				rw = parts[3]
				break
				continue
			else:
				if device in swapdevices:
					parts = line.strip().split()
					d1 = _("None")
					dtype = 'swap'
					rw = _("None")
					break
					continue
				else:
					d1 = _("None")
					dtype = _("unavailable")
					rw = _("None")
		f.close()
		f = open('/proc/partitions', 'r')
		for line in f.readlines():
			if line.find(device) != -1:
				parts = line.strip().split()
				size = int(parts[2])
				if (((float(size) / 1024) / 1024) / 1024) > 1:
					des = _("Size: ") + str(round((((float(size) / 1024) / 1024) / 1024), 2)) + _("TB")
				elif ((size / 1024) / 1024) > 1:
					des = _("Size: ") + str(round(((float(size) / 1024) / 1024), 2)) + _("GB")
				else:
					des = _("Size: ") + str(round((float(size) / 1024), 2)) + _("MB")
			else:
				try:
					size = open('/sys/block/' + device2 + '/' + device + '/size').read()
					size = str(size).replace('\n', '')
					size = int(size)
				except:
					size = 0
				if ((((float(size) / 2) / 1024) / 1024) / 1024) > 1:
					des = _("Size: ") + str(round(((((float(size) / 2) / 1024) / 1024) / 1024), 2)) + _("TB")
				elif (((size / 2) / 1024) / 1024) > 1:
					des = _("Size: ") + str(round((((float(size) / 2) / 1024) / 1024), 2)) + _("GB")
				else:
					des = _("Size: ") + str(round(((float(size) / 2) / 1024), 2)) + _("MB")
		f.close()
		if des != '':
			if rw.startswith('rw'):
				rw = ' R/W'
			elif rw.startswith('ro'):
				rw = ' R/O'
			else:
				rw = ""
			des += '\t' + _("Mount: ") + d1 + '\n' + _("Device: ") + '/dev/' + device + '\t' + _("Type: ") + dtype + rw
			png = LoadPixmap(mypixmap)
			mountP = d1
			deviceP = '/dev/' + device
			res = (name, des, png, mountP, deviceP)
			self.list.append(res)

	def SetupMounts(self):
		self.session.openWithCallback(self.updateList, DeviceManager_Setup)

	def Mount(self):
		sel = self['list'].getCurrent()
		if sel:
			mountp = sel[3]
			device = sel[4]
			system('mount ' + device)
			mountok = False
			f = open('/proc/mounts', 'r')
			for line in f.readlines():
				if line.find(device) != -1:
					mountok = True
			if not mountok:
				self.session.open(MessageBox, _("Mount failed"), MessageBox.TYPE_INFO, timeout=5)
			self.updateList()

	def Unmount(self):
		sel = self['list'].getCurrent()
		if sel:
			mountp = sel[3]
			device = sel[4]
			system('umount ' + mountp)
			try:
				mounts = open("/proc/mounts")
			except IOError:
				return -1
			mountcheck = mounts.readlines()
			mounts.close()
			for line in mountcheck:
				parts = line.strip().split(" ")
				if path.realpath(parts[0]).startswith(device):
					self.session.open(MessageBox, _("Can't unmount partiton, make sure it is not being used for swap or record/timeshift paths"), MessageBox.TYPE_INFO)
			self.updateList()

	def saveMypoints(self):
		sel = self['list'].getCurrent()
		if sel:
			self.mountp = sel[3]
			self.device = sel[4]
			if self.mountp.find('/media/hdd') < 0:
				self.Console.ePopen('umount ' + self.device)
				if not path.exists('/media/hdd'):
					mkdir('/media/hdd', 0o755)
				else:
					self.Console.ePopen('umount /media/hdd')
				self.Console.ePopen('mount ' + self.device + ' /media/hdd')
				self.Console.ePopen("/sbin/blkid | grep " + self.device, self.add_fstab, [self.device, self.mountp])
			else:
				self.session.open(MessageBox, _("This Device is already mounted as HDD."), MessageBox.TYPE_INFO, timeout=10, close_on_any_key=True)

	def add_fstab(self, result=None, retval=None, extra_args=None):
		self.device = extra_args[0]
		self.mountp = extra_args[1]
		self.device_uuid_tmp = six.ensure_str(result).split('UUID=')
		self.device_uuid_tmp = self.device_uuid_tmp[1].replace('"', "")
		self.device_uuid_tmp = self.device_uuid_tmp.replace('\n', "")
		self.device_uuid_tmp = self.device_uuid_tmp.split()[0]
		self.device_uuid = 'UUID=' + self.device_uuid_tmp
		if not path.exists(self.mountp):
			mkdir(self.mountp, 0o755)
		open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if '/media/hdd' not in l])
		rename('/etc/fstab.tmp', '/etc/fstab')
		open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device not in l])
		rename('/etc/fstab.tmp', '/etc/fstab')
		open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device_uuid not in l])
		rename('/etc/fstab.tmp', '/etc/fstab')
		out = open('/etc/fstab', 'a')
		line = self.device_uuid + '\t/media/hdd\tauto\tdefaults\t0 0\n'
		out.write(line)
		out.close()
		self.Console.ePopen('mount /media/hdd', self.updateList)

	def restBo(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 2)
		else:
			self.updateList()
			self.selectionChanged()


class DeviceManager_Setup(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="640,460" title="Choose where to mount your devices to:">
		<ePixmap pixmap="skin_default/buttons/red.png" position="25,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="175,0" size="140,40" alphatest="on" />
		<widget name="key_red" position="25,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="175,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="config" position="30,60" size="580,275" scrollbarMode="showOnDemand"/>
		<widget name="Linconn" position="30,375" size="580,20" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313"/>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.list = []
		self.device_type = 'auto'
		self.device_uuid = ""
		ConfigListScreen.__init__(self, self.list)
		Screen.setTitle(self, _("Choose where to mount your devices to:"))
		self['key_green'] = Label(_("Save"))
		self['key_red'] = Label(_("Cancel"))
		self['Linconn'] = Label(_("Wait please while scanning your %s %s devices...") % (getMachineBrand(), getMachineName()))
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.saveMypoints, 'red': self.close, 'back': self.close})
		self.updateList()

	def updateList(self):
		self.list = []
		list2 = []
		self.Console = Console()
		self.Console.ePopen("sfdisk -l | grep swap | awk '{print $(NF-9)}' >/tmp/devices.tmp")
		sleep(0.5)
		f = open('/tmp/devices.tmp', 'r')
		swapdevices = f.read()
		f.close()
		if path.exists('/tmp/devices.tmp'):
			remove('/tmp/devices.tmp')
		swapdevices = swapdevices.replace('\n', '')
		swapdevices = swapdevices.split('/')
		f = open('/proc/partitions', 'r')
		for line in f.readlines():
			parts = line.strip().split()
			if not parts:
				continue
			device = parts[3]
			if not search('sd[a-z][1-9]', device) and not search('mmcblk[0-9]p[1-9]', device):
				continue
			if getMachineBuild() in ('dagsmv200', 'gbmv200', 'multibox', 'multiboxse', 'v8plus', 'hd60', 'hd61', 'pulse4k', 'pulse4kmini', 'vuduo4k', 'vuduo4kse', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'sf8008', 'sf8008m', 'sf8008opt', 'cc1', 'dags72604', 'u51', 'u52', 'u53', 'u532', 'u533', 'u54', 'u56', 'u57', 'u571', 'vuzero4k', 'u5', 'sf5008', 'et13000', 'et1x000', 'vuuno4k', 'vuuno4kse', 'vuultimo4k', 'vusolo4k', 'hd51', 'hd52', 'dm820', 'dm7080', 'sf4008', 'dm900', 'dm920', 'gb7252', 'gb72604', 'dags7252', 'vs1500', '8100s') and search('mmcblk0p[1-9]', device):
				continue
			if getMachineBuild() in ('xc7439', 'osmio4k', 'osmio4kplus', 'osmini4k') and search('mmcblk1p[1-9]', device):
				continue
			if device in list2:
				continue
			if device in swapdevices:
				continue
			self.buildMy_rec(device)
			list2.append(device)
		f.close()
		self['config'].list = self.list
		self['config'].l.setList(self.list)
		self['Linconn'].hide()

	def buildMy_rec(self, device):
		try:
			if device.find('1') > 1:
				device2 = device.replace('1', '')
		except:
			device2 = ''
		try:
			if device.find('2') > 1:
				device2 = device.replace('2', '')
		except:
			device2 = ''
		try:
			if device.find('3') > 1:
				device2 = device.replace('3', '')
		except:
			device2 = ''
		try:
			if device.find('4') > 1:
				device2 = device.replace('4', '')
		except:
			device2 = ''
		try:
			if device.find('5') > 1:
				device2 = device.replace('5', '')
		except:
			device2 = ''
		try:
			if device.find('6') > 1:
				device2 = device.replace('6', '')
		except:
			device2 = ''
		try:
			if device.find('7') > 1:
				device2 = device.replace('7', '')
		except:
			device2 = ''
		try:
			if device.find('8') > 1:
				device2 = device.replace('8', '')
		except:
			device2 = ''
		try:
			if device.find('p1') > 1:
				device2 = device.replace('p1', '')
		except:
			device2 = ''
		try:
			if device.find('p2') > 1:
				device2 = device.replace('p2', '')
		except:
			device2 = ''
		try:
			if device.find('p3') > 1:
				device2 = device.replace('p3', '')
		except:
			device2 = ''
		try:
			if device.find('p4') > 1:
				device2 = device.replace('p4', '')
		except:
			device2 = ''
		try:
			if device.find('p5') > 1:
				device2 = device.replace('p5', '')
		except:
			device2 = ''
		try:
			if device.find('p6') > 1:
				device2 = device.replace('p6', '')
		except:
			device2 = ''
		try:
			if device.find('p7') > 1:
				device2 = device.replace('p7', '')
		except:
			device2 = ''
		try:
			if device.find('p8') > 1:
				device2 = device.replace('p8', '')
		except:
			device2 = ''
		devicetype = path.realpath('/sys/block/' + device2 + '/device')
		d2 = device
		name = 'USB: '
		mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_usb.png'
		if device2.startswith('mmcblk'):
			model = open('/sys/block/' + device2 + '/device/name').read()
			mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_mmc.png'
			name = 'MMC: '
		else:
			model = open('/sys/block/' + device2 + '/device/model').read()
		model = str(model).replace('\n', '')
		des = ''
		print("test:")
		if devicetype.find('/devices/pci') != -1 or devicetype.find('ahci') != -1:
			name = _("HARD DISK: ")
			mypixmap = '/usr/lib/enigma2/python/OPENDROID/icons/dev_hdd.png'
		name = name + model
		f = open('/proc/mounts', 'r')
		for line in f.readlines():
			if line.find(device) != -1:
				parts = line.strip().split()
				d1 = parts[1]
				dtype = parts[2]
				break
				continue
			else:
				d1 = _("None")
				dtype = _("unavailable")
		f.close()
		f = open('/proc/partitions', 'r')
		for line in f.readlines():
			if line.find(device) != -1:
				parts = line.strip().split()
				size = int(parts[2])
				if (((float(size) / 1024) / 1024) / 1024) > 1:
					des = _("Size: ") + str(round((((float(size) / 1024) / 1024) / 1024), 2)) + _("TB")
				elif ((size / 1024) / 1024) > 1:
					des = _("Size: ") + str((size / 1024) / 1024) + _("GB")
				else:
					des = _("Size: ") + str(size / 1024) + _("MB")
			else:
				try:
					size = open('/sys/block/' + device2 + '/' + device + '/size').read()
					size = str(size).replace('\n', '')
					size = int(size)
				except:
					size = 0
				if ((((float(size) / 2) / 1024) / 1024) / 1024) > 1:
					des = _("Size: ") + str(round(((((float(size) / 2) / 1024) / 1024) / 1024), 2)) + _("TB")
				elif (((size / 2) / 1024) / 1024) > 1:
					des = _("Size: ") + str(((size / 2) / 1024) / 1024) + _("GB")
				else:
					des = _("Size: ") + str((size / 2) / 1024) + _("MB")
		f.close()
		item = NoSave(ConfigSelection(default='/media/' + device, choices=[('/media/' + device, '/media/' + device),
		('/media/hdd', '/media/hdd'),
		('/media/hdd2', '/media/hdd2'),
		('/media/hdd3', '/media/hdd3'),
		('/media/usb', '/media/usb'),
		('/media/usb2', '/media/usb2'),
		('/media/usb3', '/media/usb3'),
		('/media/mmc', '/media/mmc'),
		('/media/mmc2', '/media/mmc2'),
		('/media/mmc3', '/media/mmc3'),
		('/usr', '/usr')]))
		if dtype == 'Linux':
			dtype = 'ext3'
		else:
			dtype = 'auto'
		item.value = d1.strip()
		text = name + ' ' + des + ' /dev/' + device
		res = getConfigListEntry(text, item, device, dtype)

		if des != '' and self.list.append(res):
			pass

	def saveMypoints(self):
		self.Console = Console()
		mycheck = False
		for x in self['config'].list:
			self.device = x[2]
			self.mountp = x[1].value
			self.type = x[3]
			self.Console.ePopen('umount ' + self.device)
			self.Console.ePopen("/sbin/blkid | grep " + self.device, self.add_fstab, [self.device, self.mountp])
		message = _("Updating mount locations.")
		ybox = self.session.openWithCallback(self.delay, MessageBox, message, type=MessageBox.TYPE_INFO, timeout=5, enable_input=False)
		ybox.setTitle(_("Please wait."))

	def delay(self, val):
		message = _("Changes need a system restart to take effect.\nRestart your %s %s now?") % (getMachineBrand(), getMachineName())
		ybox = self.session.openWithCallback(self.restartBox, MessageBox, message, MessageBox.TYPE_YESNO)
		ybox.setTitle(_("Restart %s %s.") % (getMachineBrand(), getMachineName()))

	def add_fstab(self, result=None, retval=None, extra_args=None):
		self.device = extra_args[0]
		self.mountp = extra_args[1]
		if len(result) == 0:
			print("[MountManager] error get UUID for device %s" % self.device)
			return
		self.device_tmp = six.ensure_str(result).split(' ')
		if self.device_tmp[0].startswith('UUID='):
			self.device_uuid = self.device_tmp[0].replace('"', "")
			self.device_uuid = self.device_uuid.replace('\n', "")
		elif self.device_tmp[1].startswith('UUID='):
			self.device_uuid = self.device_tmp[1].replace('"', "")
			self.device_uuid = self.device_uuid.replace('\n', "")
		elif self.device_tmp[2].startswith('UUID='):
			self.device_uuid = self.device_tmp[2].replace('"', "")
			self.device_uuid = self.device_uuid.replace('\n', "")
		elif self.device_tmp[3].startswith('UUID='):
			self.device_uuid = self.device_tmp[3].replace('"', "")
			self.device_uuid = self.device_uuid.replace('\n', "")
		try:
			if self.device_tmp[0].startswith('TYPE='):
				self.device_type = self.device_tmp[0].replace('TYPE=', "")
				self.device_type = self.device_type.replace('"', "")
				self.device_type = self.device_type.replace('\n', "")
			elif self.device_tmp[1].startswith('TYPE='):
				self.device_type = self.device_tmp[1].replace('TYPE=', "")
				self.device_type = self.device_type.replace('"', "")
				self.device_type = self.device_type.replace('\n', "")
			elif self.device_tmp[2].startswith('TYPE='):
				self.device_type = self.device_tmp[2].replace('TYPE=', "")
				self.device_type = self.device_type.replace('"', "")
				self.device_type = self.device_type.replace('\n', "")
			elif self.device_tmp[3].startswith('TYPE='):
				self.device_type = self.device_tmp[3].replace('TYPE=', "")
				self.device_type = self.device_type.replace('"', "")
				self.device_type = self.device_type.replace('\n', "")
			elif self.device_tmp[4].startswith('TYPE='):
				self.device_type = self.device_tmp[4].replace('TYPE=', "")
				self.device_type = self.device_type.replace('"', "")
				self.device_type = self.device_type.replace('\n', "")
		except:
			self.device_type = 'auto'

		if self.device_type.startswith('ext'):
			self.device_type = 'auto'

		if not path.exists(self.mountp):
			mkdir(self.mountp, 0o755)
		open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device not in l])
		rename('/etc/fstab.tmp', '/etc/fstab')
		open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device_uuid not in l])
		rename('/etc/fstab.tmp', '/etc/fstab')
		out = open('/etc/fstab', 'a')
		line = self.device_uuid + '\t' + self.mountp + '\t' + self.device_type + '\tdefaults\t0 0\n'
		out.write(line)
		out.close()

	def restartBox(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 2)
		else:
			self.close()


class DevicesPanelSummary(Screen):
	def __init__(self, session, parent):
		Screen.__init__(self, session, parent=parent)
		self["entry"] = StaticText("")
		self["desc"] = StaticText("")
		self.onShow.append(self.addWatcher)
		self.onHide.append(self.removeWatcher)

	def addWatcher(self):
		self.parent.onChangedEntry.append(self.selectionChanged)
		self.parent.selectionChanged()

	def removeWatcher(self):
		self.parent.onChangedEntry.remove(self.selectionChanged)

	def selectionChanged(self, name, desc):
		self["entry"].text = name
		self["desc"].text = desc


class UsbFormat(Screen):
	skin = '\n\t<screen position="center,center" size="580,350" title="Usb Format Wizard">\n\t\t<widget name="lab1" position="10,10" size="560,280" font="Regular;20" valign="top" transparent="1"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="100,300" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="340,300" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="100,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="340,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _('USB Disk Format Wizard'))
		msg = _('This wizard will help you to format Usb mass storage devices for Linux.\n\n')
		msg += _('Please be sure that your usb drive is NOT CONNECTED to your %s %s box before you continue.\n') % (getMachineBrand(), getMachineName())
		msg += _('If your usb drive is connected and mounted you have to poweroff your box, remove the usb device and reboot.\n\n')
		msg += _('Press Red button to continue, when you are ready and your usb is disconnected.\n')
		self['key_red'] = Label(_('Continue ->'))
		self['key_green'] = Label(_('Cancel'))
		self['lab1'] = Label(msg)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.checkClose, 'red': self.step_Bump, 'green': self.checkClose})
		self.step = 1
		self.devices = []
		self.device = None
		self.totalpartitions = 1
		self.totalsize = self.p1size = self.p2size = self.p3size = self.p4size = '0'
		self.canclose = True
		return

	def stepOne(self):
		msg = _('Connect your usb storage to your %s %s box\n\n') % (getMachineBrand(), getMachineName())
		msg += _('Press Red button to continue when ready.\n\n')
		msg += _('Warning: If your usb is already connected\n')
		msg += _('to the box you have to unplug it, press\n')
		msg += _('the Green button and restart the wizard.\n')
		rc = system('/etc/init.d/autofs stop')
		self.devices = self.get_Devicelist()
		self['lab1'].setText(msg)
		self.step = 2

	def stepTwo(self):
		msg = _('The wizard will now try to identify your connected usb device.')
		msg += _('Press Red button to continue.')
		self['lab1'].setText(msg)
		self.step = 3

	def stepThree(self):
		newdevices = self.get_Devicelist()
		for d in newdevices:
			if d not in self.devices:
				self.device = d

		if self.device is None:
			self.wizClose(_('Sorry, no new usb storage device detected.\nBe sure to follow the wizard instructions.'))
		else:
			msg = self.get_Deviceinfo(self.device)
			self['lab1'].setText(msg)
			self.step = 4
		return

	def stepFour(self):
		myoptions = [['1', '1'],
		['2', '2'],
		['3', '3'],
		['4', '4']]
		self.session.openWithCallback(self.partSize1, ChoiceBox, title=_('Select number of partitions:'), list=myoptions)

	def partSize1(self, total):
		self.totalpartitions = int(total[1])
		if self.totalpartitions > 1:
			self.session.openWithCallback(self.partSize2, InputBox, title=_('Enter the size in Megabyte of the first partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
		else:
			self.writePartFile()

	def partSize2(self, psize):
		if psize is None:
			psize = '100'
		self.p1size = psize
		if self.totalpartitions > 2:
			self.session.openWithCallback(self.partSize3, InputBox, title=_('Enter the size in Megabyte of the second partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
		else:
			self.writePartFile()
		return

	def partSize3(self, psize):
		if psize is None:
			psize = '100'
		self.p2size = psize
		if self.totalpartitions > 3:
			self.session.openWithCallback(self.partSize4, InputBox, title=_('Enter the size in Megabyte of the third partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
		else:
			self.writePartFile()
		return

	def partSize4(self, psize):
		if psize is None:
			psize = '100'
		self.p3size = psize
		self.writePartFile()
		return

	def writePartFile(self):
		p1 = p2 = p3 = p4 = '0'
		device = '/dev/' + self.device
		out0 = '#!/bin/sh\n\nsfdisk %s << EOF\n' % device
		msg = _('Total Megabyte Available: \t') + str(self.totalsize)
		msg += _('\nPartition scheme:\n')
		p1 = self.p1size
		out1 = ',%sM\n' % self.p1size
		if self.totalpartitions == 1:
			p1 = str(self.totalsize)
			out1 = ';\n'
		msg += '%s1 \t size:%s M\n' % (device, p1)
		if self.totalpartitions > 1:
			p2 = self.p2size
			out2 = ',%sM\n' % self.p2size
			if self.totalpartitions == 2:
				p2 = self.totalsize - int(self.p1size)
				out2 = ';\n'
			msg += '%s2 \t size:%s M\n' % (device, p2)
		if self.totalpartitions > 2:
			p3 = self.p3size
			out3 = ',%sM\n' % self.p3size
			if self.totalpartitions == 3:
				p3 = self.totalsize - (int(self.p1size) + int(self.p2size))
				out3 = ';\n'
			msg += '%s3 \t size:%s M\n' % (device, p3)
		if self.totalpartitions > 3:
			p4 = self.totalsize - (int(self.p1size) + int(self.p2size) + int(self.p3size))
			out4 = ';\n'
			msg += '%s4 \t size:%s M\n' % (device, p4)
		msg += _('\nWarning: all the data will be lost.\nAre you sure you want to format this device?\n')
		out = open('/tmp/sfdisk.tmp', 'w')
		out.write(out0)
		out.write(out1)
		if self.totalpartitions > 1:
			out.write(out2)
		if self.totalpartitions > 2:
			out.write(out3)
		if self.totalpartitions > 3:
			out.write(out4)
		out.write('EOF\n')
		out.close()
		system('chmod 0755 /tmp/sfdisk.tmp')
		self['lab1'].setText(msg)
		if int(self.p1size) + int(self.p2size) + int(self.p3size) + int(self.p4size) > self.totalsize:
			self.wizClose(_('Sorry, your partition(s) sizes are bigger than total device size.'))
		else:
			self.step = 5

	def do_Part(self):
		self.do_umount()
		self.canclose = False
		self['key_green'].hide()
		device = '/dev/%s' % self.device
		cmd = "echo -e 'Partitioning: %s \n\n'" % device
		cmd2 = '/tmp/sfdisk.tmp'
		self.session.open(ConsoleScreen, title=_('Partitioning...'), cmdlist=[cmd, cmd2], finishedCallback=self.partDone, closeOnSuccess=True)

	def partDone(self):
		msg = _('The device has been partitioned.\nPartitions will be now formatted.')
		self['lab1'].setText(msg)
		self.step = 6

	def choiceBoxFstype(self):
		menu = []
		menu.append((_('ext2 - recommended for USB flash memory'), 'ext2'))
		menu.append((_('ext3 - recommended for HARD Disks'), 'ext3'))
		menu.append((_('ext4 - recommended for OPDBoot'), 'ext4'))
		menu.append((_('vfat - use only for media-files'), 'vfat'))
		self.session.openWithCallback(self.choiceBoxFstypeCB, ChoiceBox, title=_('Choice filesystem.'), list=menu)

	def choiceBoxFstypeCB(self, choice):
		if choice is None:
			return
		else:
			newfstype = choice[1]
			if newfstype == 'ext4':
				self.formatcmd = '/sbin/mkfs.ext4 -F -O extent,flex_bg,large_file,uninit_bg -m1'
			elif newfstype == 'ext3':
				self.formatcmd = '/sbin/mkfs.ext3 -F -m0'
			elif newfstype == 'ext2':
				self.formatcmd = '/sbin/mkfs.ext2 -F -m0'
			elif newfstype == 'vfat':
				self.formatcmd = '/sbin/mkfs.vfat'
			self.do_Format()
			return

	def do_Format(self):
		self.do_umount()
		os_remove('/tmp/sfdisk.tmp')
		cmds = ['sleep 1']
		device = '/dev/%s1' % self.device
		cmd = '%s %s' % (self.formatcmd, device)
		cmds.append(cmd)
		if self.totalpartitions > 1:
			device = '/dev/%s2' % self.device
			cmd = '%s %s' % (self.formatcmd, device)
			cmds.append(cmd)
		if self.totalpartitions > 2:
			device = '/dev/%s3' % self.device
			cmd = '%s %s' % (self.formatcmd, device)
			cmds.append(cmd)
		if self.totalpartitions > 3:
			device = '/dev/%s4' % self.device
			cmd = '%s %s' % (self.formatcmd, device)
			cmds.append(cmd)
		self.session.open(ConsoleScreen, title=_('Formatting...'), cmdlist=cmds, finishedCallback=self.succesS)

	def step_Bump(self):
		if self.step == 1:
			self.stepOne()
		elif self.step == 2:
			self.stepTwo()
		elif self.step == 3:
			self.stepThree()
		elif self.step == 4:
			self.stepFour()
		elif self.step == 5:
			self.do_Part()
		elif self.step == 6:
			self.choiceBoxFstype()

	def get_Devicelist(self):
		devices = []
		folder = listdir('/sys/block')
		for f in folder:
			if f.find('sd') != -1:
				devices.append(f)

		return devices

	def get_Deviceinfo(self, device):
		info = vendor = model = size = ''
		filename = '/sys/block/%s/device/vendor' % device
		if fileExists(filename):
			vendor = file(filename).read().strip()
			filename = '/sys/block/%s/device/model' % device
			model = file(filename).read().strip()
			filename = '/sys/block/%s/size' % device
			size = int(file(filename).read().strip())
			cap = size / 1000 * 512 / 1024
			size = '%d.%03d GB' % (cap / 1000, cap % 1000)
			self.totalsize = cap
		info = _('Model: ') + vendor + ' ' + model + '\n' + _('Size: ') + size + '\n' + _('Device: ') + '/dev/' + device
		return info

	def do_umount(self):
		f = open('/proc/mounts', 'r')
		for line in f.readlines():
			if line.find('/dev/sd') != -1:
				parts = line.split()
				cmd = 'umount -l ' + parts[0]
				system(cmd)

		f.close()

	def checkClose(self):
		if self.canclose == True:
			self.close()

	def wizClose(self, msg):
		self.session.openWithCallback(self.close, MessageBox, msg, MessageBox.TYPE_INFO)

	def succesS(self):
		text = _("The %s %s will be now restarted to generate a new device UID.\nDon't forget to remap your device after the reboot.\nPress OK to continue") % (getMachineBrand(), getMachineName())
		mybox = self.session.openWithCallback(self.hreBoot, MessageBox, text, MessageBox.TYPE_INFO)

	def hreBoot(self, answer):
		self.session.open(TryQuitMainloop, 2)

