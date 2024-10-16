from __future__ import print_function
from __future__ import absolute_import
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, SCOPE_GUISKIN, resolveFilename
from enigma import *
from enigma import getDesktop
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from OPENDROID.ExtrasList import ExtrasList
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigSelection, getConfigListEntry, config
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Standby import TryQuitMainloop
from boxbranding import getMachineBrand, getMachineName
import sys
import os
import re
import time
from Tools.HardwareInfo import HardwareInfo
import six
import codecs
version='1.2',
author='Dimitrij openPLi',
author_email='dima-73@inbox.lv',
try:
        device_name = HardwareInfo().get_device_name()
except:
        device_name = None

FULLHD = False
if getDesktop(0).size().width() >= 1920:
        FULLHD = True

sfdisk = os.path.exists('/usr/sbin/sfdisk')

def DiskEntry(model, size, removable, rotational, internal):
        if not removable and internal and rotational:
                picture = LoadPixmap(cached=True, path=resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/disk.png"))
        elif internal and not rotational:
                picture = LoadPixmap(cached=True, path=resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/ssddisk.png"))
        else:
                picture = LoadPixmap(cached=True, path=resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/disk.png"));

        return (picture, model, size)

class HddSetup(Screen):
        if FULLHD:
                skin = """
		<screen name="HddSetup" position="center,center" size="560,430" title="Hard Drive Setup">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget source="menu" render="Listbox" position="20,45" size="520,380" scrollbarMode="showOnDemand">
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
        else:
                skin = """
		<screen name="HddSetup" position="center,center" size="560,430" title="Hard Drive Setup">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget source="menu" render="Listbox" position="20,45" size="520,380" scrollbarMode="showOnDemand">
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

        def __init__(self, session, args=0):
                self.session = session
                Screen.__init__(self, session)
                self.disks = list()
                self.mdisks = Disks()
                self.asHDD = False
                for disk in self.mdisks.disks:
                        capacity = "%d MB" % (disk[1] / (1024 * 1024))
                        self.disks.append(DiskEntry(disk[3], capacity, disk[2], disk[6], disk[7]))
                self["menu"] = List(self.disks)
                self["key_red"] = Button(_("Exit"))
                self["key_green"] = Button(_("Info"))
                if sfdisk:
                        self["key_yellow"] = Button(_("Initialize"))
                else:
                        self["key_yellow"] = Button("")
                self["key_blue"] = Button(_("Partitions"))
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                            {
                                                    "blue": self.blue,
                                                    "yellow": self.yellow,
                                                    "green": self.green,
                                                    "red": self.quit,
                                                    "cancel": self.quit,
                                                    }, -2)
                self.onShown.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("Device Manager"))

        def isExt4Supported(self):
                return "ext4" in open("/proc/filesystems").read()

        def mkfs(self):
                self.formatted += 1
                return self.mdisks.mkfs(self.mdisks.disks[self.sindex][0], self.formatted, self.fsresult)

        def refresh(self):
                self.disks = list()
                self.mdisks = Disks()
                for disk in self.mdisks.disks:
                        capacity = "%d MB" % (disk[1] / (1024 * 1024))
                        self.disks.append(DiskEntry(disk[3], capacity, disk[2], disk[6], disk[7]))

                self["menu"].setList(self.disks)

        def checkDefault(self):
                mp = MountPoints()
                mp.read()
                if self.asHDD and not mp.exist("/media/hdd"):
                        mp.add(self.mdisks.disks[self.sindex][0], 1, "/media/hdd")
                        mp.write()
                        mp.mount(self.mdisks.disks[self.sindex][0], 1, "/media/hdd")
                        os.system("mkdir -p /media/hdd/movie")
                        message = _("Fixed mounted first initialized Storage Device to /media/hdd. It needs a system restart in order to take effect.\nRestart your STB now?")
                        mbox = self.session.openWithCallback(self.restartBox, MessageBox, message, MessageBox.TYPE_YESNO)
                        mbox.setTitle(_("Restart %s %s") % (getMachineBrand(), getMachineName()))

        def restartBox(self, answer):
                if answer is True:
                        self.session.open(TryQuitMainloop, 2)

        def format(self, result):
                if result != 0:
                        self.session.open(MessageBox, _("Cannot format partition %d") % (self.formatted), MessageBox.TYPE_ERROR)
                if self.result == 0:
                        if self.formatted > 0:
                                self.checkDefault()
                                self.refresh()
                                return
                elif self.result > 0 and self.result < 3:
                        if self.formatted > 1:
                                self.checkDefault()
                                self.refresh()
                                return
                elif self.result == 3:
                        if self.formatted > 2:
                                self.checkDefault()
                                self.refresh()
                                return
                elif self.result == 4:
                        if self.formatted > 3:
                                self.checkDefault()
                                self.refresh()
                                return
                self.session.openWithCallback(self.format, ExtraActionBox, _("Formatting partition %d") % (self.formatted + 1), _("Initialize disk"), self.mkfs)

        def fdiskEnded(self, result):
                if result == 0:
                        self.format(0)
                elif result == -1:
                        self.session.open(MessageBox, _("Cannot umount current device.\nA record in progress, timeshift or some external tools (like samba, swapfile and nfsd) may cause this problem.\nPlease stop this actions/applications and try again"), MessageBox.TYPE_ERROR)
                else:
                        self.session.open(MessageBox, _("Partitioning failed!"), MessageBox.TYPE_ERROR)

        def fdisk(self):
                return self.mdisks.fdisk(self.mdisks.disks[self.sindex][0], self.mdisks.disks[self.sindex][1], self.result, self.fsresult)

        def initialaze(self, result):
                if not self.isExt4Supported():
                        result += 1
                if result != 6:
                        self.fsresult = result
                        self.formatted = 0
                        mp = MountPoints()
                        mp.read()
                        mp.deleteDisk(self.mdisks.disks[self.sindex][0])
                        mp.write()
                        self.session.openWithCallback(self.fdiskEnded, ExtraActionBox, _("Partitioning..."), _("Initialize disk"), self.fdisk)

        def chooseFSType(self, result):
                if result != 5:
                        self.result = result
                        if self.isExt4Supported():
                                self.session.openWithCallback(self.initialaze, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                              [ [ "Ext4", "partitionmanager.png" ],
                                                                [ "Ext3", "partitionmanager.png" ],
                                                                [ "Ext2", "partitionmanager.png" ],
                                                                [ "NTFS", "partitionmanager.png" ],
                                                                [ "exFAT", "partitionmanager.png" ],
                                                                [ "Fat32", "partitionmanager.png" ],
                                                                [ _("Cancel"), "cancel.png" ],
                                                                ], 1, 6)
                        else:
                                self.session.openWithCallback(self.initialaze, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                              [ [ "Ext3", "partitionmanager.png" ],
                                                                [ "Ext2", "partitionmanager.png" ],
                                                                [ "NTFS", "partitionmanager.png" ],
                                                                [ "exFAT", "partitionmanager.png" ],
                                                                [ "Fat32", "partitionmanager.png" ],
                                                                [ _("Cancel"), "cancel.png" ],
                                                                ], 1, 5)
        def yellow(self):
                self.asHDD = False
                if sfdisk and len(self.mdisks.disks) > 0:
                        list = [(_("No - simple"), "simple"), (_("Yes - fstab entry as /media/hdd"), "as_hdd")]
                        def extraOption(ret):
                                if ret:
                                        if ret[1] == "as_hdd":
                                                self.asHDD = True
                                        self.yellowAswer()
                        self.session.openWithCallback(extraOption, ChoiceBox, title = _("Initialize") + _(" as HDD ?"),list = list)

        def yellowAswer(self):
                if sfdisk and len(self.mdisks.disks) > 0:
                        self.sindex = self['menu'].getIndex()
                        self.session.openWithCallback(self.chooseFSType, ExtraMessageBox, _("Please select your preferred configuration.") + "\n" + _("Or use standard 'Harddisk Setup' to initialize your drive in ext4."), _("Partitioner"),
                                                      [[_("One partition"), "partitionmanager.png"],
                                                       [_("Two partitions (50% - 50%)"), "partitionmanager.png" ],
                                                       [_("Two partitions (75% - 25%)"), "partitionmanager.png" ],
                                                        [_("Three partitions (33% - 33% - 33%)"), "partitionmanager.png" ],
                                                        [_("Four partitions (25% - 25% - 25% - 25%)"), "partitionmanager.png" ],
                                                        [_("Cancel"), "cancel.png" ],
                                                        ], 1, 5)

        def green(self):
                if len(self.mdisks.disks) > 0:
                        self.sindex = self['menu'].getIndex()
                        self.session.open(HddInfo, self.mdisks.disks[self.sindex][0], self.mdisks.disks[self.sindex])

        def blue(self):
                if len(self.mdisks.disks) > 0:
                        self.sindex = self['menu'].getIndex()
                        if len(self.mdisks.disks[self.sindex][5]) == 0:
                                self.session.open(MessageBox, _("You need to initialize your storage device first"), MessageBox.TYPE_ERROR)
                        else:
                                self.session.open(HddPartitions, self.mdisks.disks[self.sindex])

        def quit(self):
                self.close()
##########################################################################################################
FULLHD = False
if getDesktop(0).size().width() >= 1920:
        FULLHD = True

sfdisk = os.path.exists('/usr/sbin/sfdisk')

def PartitionEntry(description, size):
        picture = LoadPixmap(cached = True, path = resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/partitionmanager.png"))
        return (picture, description, size)

class HddPartitions(Screen):
        if FULLHD:
                skin = """
		<screen name="HddPartitions" position="center,center" size="560,430" title="Hard Drive Partitions">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget name="label_disk" position="20,45" font="Regular;20" halign="center" size="520,25" valign="center" />
			<widget source="menu" render="Listbox" position="10,75" size="540,350" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
						MultiContentEntryText(pos = (65, 10), size = (375, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						MultiContentEntryText(pos = (435, 10), size = (125, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 2),
						],
						"fonts": [gFont("Regular", 18)],
						"itemHeight": 50
					}
				</convert>
			</widget>
		</screen>"""
        else:
                skin = """
		<screen name="HddPartitions" position="center,center" size="560,430" title="Hard Drive Partitions">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget name="label_disk" position="20,45" font="Regular;20" halign="center" size="520,25" valign="center" />
			<widget source="menu" render="Listbox" position="20,75" size="520,350" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
						MultiContentEntryText(pos = (65, 10), size = (360, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						MultiContentEntryText(pos = (435, 10), size = (125, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 2),
						],
						"fonts": [gFont("Regular", 18)],
						"itemHeight": 50
					}
				</convert>
			</widget>
		</screen>"""

        def __init__(self, session, disk):
                self.session = session

                Screen.__init__(self, session)
                self.disk = disk
                self.refreshMP(False)

                self["menu"] = List(self.partitions)
                self["menu"].onSelectionChanged.append(self.selectionChanged)
                self["key_red"] = Button(_("Exit"))
                self["key_green"] = Button("")
                self["key_yellow"] = Button("")
                self["key_blue"] = Button("")
                self["label_disk"] = Label("%s - %s" % (self.disk[0], self.disk[3]))
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                            {
                                                    "red": self.quit,
                                                    "yellow": self.yellow,
                                                    "green": self.green,
                                                    "blue": self.blue,
                                                    "cancel": self.quit,
                                                    }, -2)

                self.onShown.append(self.setWindowTitle)

                if len(self.disk[5]) > 0:
                        if self.disk[5][0][3] == "83" or self.disk[5][0][3] == "7" or self.disk[5][0][3] == "b" or self.disk[5][0][3] == "c":
                                self["key_green"].setText(_("Check"))
                                if sfdisk:
                                        self["key_yellow"].setText(_("Format"))
                                mp = self.mountpoints.get(self.disk[0], 1)
                                rmp = self.mountpoints.getRealMount(self.disk[0], 1)
                                if len(mp) > 0 or len(rmp) > 0:
                                        self.mounted = True
                                        self["key_blue"].setText(_("Unmount"))
                                else:
                                        self.mounted = False
                                        self["key_blue"].setText(_("Mount"))

        def setWindowTitle(self):
                self.setTitle(_("Partitions"))

        def selectionChanged(self):
                self["key_green"].setText("")
                self["key_yellow"].setText("")
                self["key_blue"].setText("")

                if len(self.disk[5]) > 0:
                        index = self["menu"].getIndex()
                        if self.disk[5][index][3] == "83" or self.disk[5][index][3] == "7" or self.disk[5][index][3] == "b" or self.disk[5][index][3] == "c":
                                self["key_blue"].setText(_("Check"))
                                if sfdisk:
                                        self["key_yellow"].setText(_("Format"))
                                mp = self.mountpoints.get(self.disk[0], index+1)
                                rmp = self.mountpoints.getRealMount(self.disk[0], index+1)
                                if len(mp) > 0 or len(rmp) > 0:
                                        self.mounted = True
                                        self["key_blue"].setText(_("Unmount"))
                                else:
                                        self.mounted = False
                                        self["key_blue"].setText(_("Mount"))

        def chkfs(self):
                disks = Disks()
                ret = disks.chkfs(self.disk[5][self.index][0][:3], self.index+1, self.fstype)
                if ret == 0:
                        self.session.open(MessageBox, _("Check disk terminated with success"), MessageBox.TYPE_INFO)
                elif ret == -1:
                        self.session.open(MessageBox, _("Cannot umount current drive.\nA record in progress, timeshift or some external tools (like samba, swapfile and nfsd) may cause this problem.\nPlease stop this actions/applications and try again"), MessageBox.TYPE_ERROR)
                else:
                        self.session.open(MessageBox, _("Error checking disk. The disk may be damaged"), MessageBox.TYPE_ERROR)

        def mkfs(self):
                disks = Disks()
                ret = disks.mkfs(self.disk[5][self.index][0][:3], self.index+1, self.fstype)
                if ret == 0:
                        self.session.open(MessageBox, _("Format terminated with success"), MessageBox.TYPE_INFO)
                elif ret == -2:
                        self.session.open(MessageBox, _("Cannot format current drive.\nA record in progress, timeshift or some external tools (like samba, swapfile and nfsd) may cause this problem.\nPlease stop this actions/applications and try again"), MessageBox.TYPE_ERROR)
                else:
                        self.session.open(MessageBox, _("Error formatting disk. The disk may be damaged"), MessageBox.TYPE_ERROR)

        def isExt4Supported(self):
                return "ext4" in open("/proc/filesystems").read()

        def domkfs(self, result):
                if self.disk[5][self.index][3] == "83":
                        if self.isExt4Supported():
                                if result < 3:
                                        self.fstype = result
                                        self.session.open(ExtraActionBox, _("Formatting disk %s") % self.disk[5][self.index][0], _("Formatting disk"), self.mkfs)
                        else:
                                if result < 2:
                                        self.fstype = result == 0 and 1 or 2
                                        self.session.open(ExtraActionBox, _("Formatting disk %s") % self.disk[5][self.index][0], _("Formatting disk"), self.mkfs)
                elif self.disk[5][self.index][3] == "7":
                        if result < 2:
                                self.fstype = result == 0 and 3 or 4
                                self.session.open(ExtraActionBox, _("Formatting disk %s") % self.disk[5][self.index][0], _("Formatting disk"), self.mkfs)
                elif self.disk[5][self.index][3] == "b" or self.disk[5][self.index][3] == "c":
                        if result < 1:
                                self.fstype = 5
                                self.session.open(ExtraActionBox, _("Formatting disk %s") % self.disk[5][self.index][0], _("Formatting disk"), self.mkfs)

        def green(self):
                if len(self.disk[5]) > 0:
                        index = self["menu"].getIndex()
                        if self.disk[5][index][3] == "83" or self.disk[5][index][3] == "7" or self.disk[5][index][3] == "b" or self.disk[5][index][3] == "c":
                                self.index = index
                                if self.disk[5][index][3] == "83":
                                        self.fstype = 0
                                elif self.disk[5][index][3] == "7":
                                        self.fstype = 2
                                elif self.disk[5][index][3] == "b" or self.disk[5][index][3] == "c":
                                        self.fstype = 3
                                self.session.open(ExtraActionBox, _("Checking disk %s") % self.disk[5][index][0], _("Checking disk"), self.chkfs)

        def yellow(self):
                if sfdisk and len(self.disk[5]) > 0:
                        self.index = self["menu"].getIndex()
                        if self.disk[5][self.index][3] == "83":
                                if self.isExt4Supported():
                                        self.session.openWithCallback(self.domkfs, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                                      [["Ext4", "partitionmanager.png"],
                                                                       ["Ext3", "partitionmanager.png"],
                                                                       ["Ext2", "partitionmanager.png"],
                                                                        [_("Cancel"), "cancel.png"],
                                                                        ], 1, 3)
                                else:
                                        self.session.openWithCallback(self.domkfs, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                                      [["Ext3", "partitionmanager.png"],
                                                                       ["Ext2", "partitionmanager.png"],
                                                                       [_("Cancel"), "cancel.png"],
                                                                        ], 1, 2)
                        elif self.disk[5][self.index][3] == "7":
                                self.session.openWithCallback(self.domkfs, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                              [["NTFS", "partitionmanager.png"],
                                                               ["exFAT", "partitionmanager.png"],
                                                               [_("Cancel"), "cancel.png"],
                                                                ], 1, 2)
                        elif self.disk[5][self.index][3] == "b" or self.disk[5][self.index][3] == "c":
                                self.session.openWithCallback(self.domkfs, ExtraMessageBox, _("Format as"), _("Partitioner"),
                                                              [["Fat32", "partitionmanager.png"],
                                                               [_("Cancel"), "cancel.png"],
                                                               ], 1, 1)

        def refreshMP(self, uirefresh=True):
                self.partitions = []
                self.mountpoints = MountPoints()
                self.mountpoints.read()
                count = 1
                for part in self.disk[5]:
                        capacity = "%d MB" % (part[1] / (1024 * 1024))
                        mp = self.mountpoints.get(self.disk[0], count)
                        rmp = self.mountpoints.getRealMount(self.disk[0], count)
                        if len(mp) > 0:
                                self.partitions.append(PartitionEntry(_("P. %d - %s (Fixed: %s)") % (count, part[2], mp), capacity))
                        elif len(rmp) > 0:
                                self.partitions.append(PartitionEntry(_("P. %d - %s (Fast: %s)") % (count, part[2], rmp), capacity))
                        else:
                                self.partitions.append(PartitionEntry("P. %d - %s" % (count, part[2]), capacity))
                        count += 1

                if uirefresh:
                        self["menu"].setList(self.partitions)
                        self.selectionChanged()

        def blue(self):
                if len(self.disk[5]) > 0:
                        index = self["menu"].getIndex()
                        if self.disk[5][index][3] != "83" and self.disk[5][index][3] != "7" and self.disk[5][index][3] != "b" and self.disk[5][index][3] != "c":
                                return

                if len(self.partitions) > 0:
                        self.sindex = self['menu'].getIndex()
                        if self.mounted:
                                mp = self.mountpoints.get(self.disk[0], self.sindex+1)
                                rmp = self.mountpoints.getRealMount(self.disk[0], self.sindex+1)
                                if len(mp) > 0:
                                        if self.mountpoints.isMounted(mp):
                                                if self.mountpoints.umount(mp):
                                                        self.mountpoints.delete(mp)
                                                        self.mountpoints.write()
                                                else:
                                                        self.session.open(MessageBox, _("Cannot umount current device.\nA record in progress, timeshift or some external tools (like samba, swapfile and nfsd) may cause this problem.\nPlease stop this actions/applications and try again"), MessageBox.TYPE_ERROR)
                                        else:
                                                self.mountpoints.delete(mp)
                                                self.mountpoints.write()
                                elif len(rmp) > 0:
                                        self.mountpoints.umount(rmp)
                                self.refreshMP()
                        else:
                                self.session.openWithCallback(self.refreshMP, HddMountDevice, self.disk[0], self.sindex+1)

        def quit(self):
                self.close()
###################################################################################################
FULLHD = False
if getDesktop(0).size().width() >= 1920:
        FULLHD = True

class HddMountDevice(Screen):
        if FULLHD:
                skin = """
		<screen name="HddMountDevice" position="center,center" size="560,430" title="Hard Drive Mount">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget name="menu" position="20,45" scrollbarMode="showOnDemand" size="520,380" transparent="1" />
		</screen>"""
        else:
                skin = """
		<screen name="HddMountDevice" position="center,center" size="560,430" title="Hard Drive Mount">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget name="menu" position="20,45" scrollbarMode="showOnDemand" size="520,380" transparent="1" />
		</screen>"""

        def __init__(self, session, device, partition):
                Screen.__init__(self, session)

                self.device = device
                self.partition = partition
                self.mountpoints = MountPoints()
                self.mountpoints.read()
                self.fast = False

                self.list = []
                self.list.append(_("Mount as main hdd"))
                self.list.append(_("Mount as /media/hdd1"))
                self.list.append(_("Mount as /media/hdd2"))
                self.list.append(_("Mount as /media/hdd3"))
                self.list.append(_("Mount as /media/hdd4"))
                self.list.append(_("Mount as /media/hdd5"))
                self.list.append(_("Mount as /media/usb"))
                self.list.append(_("Mount as /media/usb1"))
                self.list.append(_("Mount as /media/usb2"))
                self.list.append(_("Mount as /media/usb3"))
                self.list.append(_("Mount as /media/usb4"))
                self.list.append(_("Mount as /media/usb5"))
                self.list.append(_("Mount on custom path"))

                self["menu"] = MenuList(self.list)

                self["key_red"] = Button(_("Fixed mount"))
                self["key_green"] = Button(_("Fast mount"))
                self["key_blue"] = Button(_("Exit"))
                self["key_yellow"] = Button("")
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                            {
                                                    "blue": self.quit,
                                                    "green": self.green,
                                                    "red": self.ok,
                                                    "cancel": self.quit,
                                                    }, -2)

                self.onShown.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("Mountpoints"))

        def ok(self):
                self.fast = False
                selected = self["menu"].getSelectedIndex()
                if selected == 0:
                        self.setMountPoint("/media/hdd")
                elif selected == 1:
                        self.setMountPoint("/media/hdd1")
                elif selected == 2:
                        self.setMountPoint("/media/hdd2")
                elif selected == 3:
                        self.setMountPoint("/media/hdd3")
                elif selected == 4:
                        self.setMountPoint("/media/hdd4")
                elif selected == 5:
                        self.setMountPoint("/media/hdd5")
                elif selected == 6:
                        self.setMountPoint("/media/usb")
                elif selected == 7:
                        self.setMountPoint("/media/usb1")
                elif selected == 8:
                        self.setMountPoint("/media/usb2")
                elif selected == 9:
                        self.setMountPoint("/media/usb3")
                elif selected == 10:
                        self.setMountPoint("/media/usb4")
                elif selected == 11:
                        self.setMountPoint("/media/usb5")
                elif selected == 12:
                        self.session.openWithCallback(self.customPath, VirtualKeyBoard, title = (_("Insert mount point:")), text = _("/media/custom"))

        def green(self):
                self.fast = True
                selected = self["menu"].getSelectedIndex()
                if selected == 0:
                        self.setMountPoint("/media/hdd")
                elif selected == 1:
                        self.setMountPoint("/media/hdd1")
                elif selected == 2:
                        self.setMountPoint("/media/hdd2")
                elif selected == 3:
                        self.setMountPoint("/media/hdd3")
                elif selected == 4:
                        self.setMountPoint("/media/hdd4")
                elif selected == 5:
                        self.setMountPoint("/media/hdd5")
                elif selected == 6:
                        self.setMountPoint("/media/usb")
                elif selected == 7:
                        self.setMountPoint("/media/usb1")
                elif selected == 8:
                        self.setMountPoint("/media/usb2")
                elif selected == 9:
                        self.setMountPoint("/media/usb3")
                elif selected == 10:
                        self.setMountPoint("/media/usb4")
                elif selected == 11:
                        self.setMountPoint("/media/usb5")
                elif selected == 12:
                        self.session.openWithCallback(self.customPath, VirtualKeyBoard, title = (_("Insert mount point:")), text = _("/media/custom"))

        def customPath(self, result):
                if result and len(result) > 0:
                        result = result.rstrip("/")
                        os.system("mkdir -p %s" % result)
                        self.setMountPoint(result)

        def setMountPoint(self, path):
                self.cpath = path
                if self.mountpoints.exist(path):
                        self.session.openWithCallback(self.setMountPointCb, ExtraMessageBox, _("Selected mount point is already used by another drive."), _("Mount point exist!"),
                                                      [[_("Change old drive with this new drive"), "ok.png"],
                                                       [_("Keep old drive"), "cancel.png"],
                                                       ])
                else:
                        self.setMountPointCb(0)

        def setMountPointCb(self, result):
                if result == 0:
                        if self.mountpoints.isMounted(self.cpath):
                                if not self.mountpoints.umount(self.cpath):
                                        self.session.open(MessageBox, _("Cannot umount current drive.\nA record in progress, timeshift or some external tools (like samba, swapfile and nfsd) may cause this problem.\nPlease stop this actions/applications and try again"), MessageBox.TYPE_ERROR)
                                        self.close()
                                        return
                        self.mountpoints.delete(self.cpath)
                        if not self.fast:
                                self.mountpoints.add(self.device, self.partition, self.cpath)
                        self.mountpoints.write()
                        if not self.mountpoints.mount(self.device, self.partition, self.cpath):
                                self.session.open(MessageBox, _("Cannot mount new drive.\nPlease check filesystem or format it and try again"), MessageBox.TYPE_ERROR)
                        elif self.cpath == "/media/hdd":
                                os.system("mkdir -p /media/hdd/movie")

                        if not self.fast:
                                message = _("Device Fixed Mount Point change needs a system restart in order to take effect.\nRestart your STB now?")
                                mbox = self.session.openWithCallback(self.restartBox, MessageBox, message, MessageBox.TYPE_YESNO)
                                mbox.setTitle(_("Restart STB"))
                        else:
                                self.close()

        def restartBox(self, answer):
                if answer is True:
                        self.session.open(TryQuitMainloop, 2)
                else:
                        self.close()

        def quit(self):
                self.close()

def MountEntry(description, details):
        picture = LoadPixmap(cached=True, path=resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/diskusb.png"));
        return (picture, description, details)

class HddFastRemove(Screen):
        if FULLHD:
                skin = """
		<screen name="HddFastRemove" position="center,center" size="560,430" title="Hard Drive Fast Umount">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="140,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_blue" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget source="menu" render="Listbox" position="10,55" size="520,380" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
						MultiContentEntryText(pos = (65, 3), size = (190, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						MultiContentEntryText(pos = (165, 27), size = (290, 38), font=1, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 2),
						],
						"fonts": [gFont("Regular", 22), gFont("Regular", 18)],
						"itemHeight": 50
					}
				</convert>
			</widget>
		</screen>"""
        else:
                skin = """
		<screen name="HddFastRemove" position="center,center" size="560,430" title="Hard Drive Fast Umount">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="140,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_blue" position="140,0" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
			<widget source="menu" render="Listbox" position="10,55" size="520,380" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
						MultiContentEntryText(pos = (65, 3), size = (190, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						MultiContentEntryText(pos = (165, 27), size = (290, 38), font=1, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 2),
						],
						"fonts": [gFont("Regular", 22), gFont("Regular", 18)],
						"itemHeight": 50
					}
				</convert>
			</widget>
		</screen>"""

        def __init__(self, session):
                Screen.__init__(self, session)
                self.refreshMP(False)

                self["menu"] = List(self.disks)
                self["key_red"] = Button(_("Unmount"))
                self["key_blue"] = Button(_("Exit"))
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                            {
                                                    "blue": self.quit,
                                                    "red": self.red,
                                                    "cancel": self.quit,
                                                    }, -2)

                self.onShown.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("Fast Mounted Remove"))

        def red(self):
                if len(self.mounts) > 0:
                        self.sindex = self["menu"].getIndex()
                        self.mountpoints.umount(self.mounts[self.sindex]) # actually umount device here - also check both cases possible - for instance error case also check with stay in /e.g. /media/usb folder on telnet
                        self.session.open(MessageBox, _("Fast mounted Media unmounted.\nYou can safely remove the Device now, if no further Partitions (displayed as P.x on Devicelist - where x >=2) are mounted on the same Device.\nPlease unmount Fixed Mounted Devices with Device Manager Panel!"), MessageBox.TYPE_INFO)
                        self.refreshMP(True)

        def refreshMP(self, uirefresh=True):
                self.mdisks = Disks()
                self.mountpoints = MountPoints()
                self.mountpoints.read()
                self.disks = list()
                self.mounts = list()
                for disk in self.mdisks.disks:
                        if disk[2] and not disk[7]:
                                diskname = disk[3]
                                for partition in disk[5]:
                                        mp = ""
                                        rmp = ""
                                        try:
                                                mp = self.mountpoints.get(partition[0][:3], int(partition[0][3:]))
                                                rmp = self.mountpoints.getRealMount(partition[0][:3], int(partition[0][3:]))
                                        except (IOError, OSError) as e:
                                                pass
                                        if len(mp) > 0:
                                                self.disks.append(MountEntry(disk[3], _("P.%s (Fixed: %s)") % (partition[0][3:], mp)))
                                                self.mounts.append(mp)
                                        elif len(rmp) > 0:
                                                self.disks.append(MountEntry(disk[3], _("P.%s (Fast: %s)") % (partition[0][3:], rmp)))
                                                self.mounts.append(rmp)
                if uirefresh:
                        self["menu"].setList(self.disks)

        def quit(self):
                self.close()
##################################################################################################################
import os
import re
from Tools.HardwareInfo import HardwareInfo
try:
        device_name = HardwareInfo().get_device_name()
except:
        device_name = None

BOX_NAME = "none"
MODEL_NAME = "none"
if os.path.exists("/proc/stb/info/boxtype"):
        BOX_NAME = "all"
        try:
                f = open("/proc/stb/info/boxtype")
                MODEL_NAME = f.read().strip()
                f.close()
        except:
                pass
elif os.path.exists("/proc/stb/info/hwmodel"):
        BOX_NAME = "all"
        try:
                f = open("/proc/stb/info/hwmodel")
                MODEL_NAME = f.read().strip()
                f.close()
        except:
                pass
elif os.path.exists("/proc/stb/info/vumodel"):
        BOX_NAME = "vu"
        try:
                f = open("/proc/stb/info/vumodel")
                MODEL_NAME = f.read().strip()
                f.close()
        except:
                pass
elif device_name and device_name.startswith('dm') and os.path.exists("/proc/stb/info/model"):
        BOX_NAME = "dmm"
        try:
                f = open("/proc/stb/info/model")
                MODEL_NAME = f.read().strip()
                f.close()
        except:
                pass
elif os.path.exists("/proc/stb/info/gbmodel"):
        BOX_NAME = "all"
        try:
                f = open("/proc/stb/info/gbmodel")
                MODEL_NAME = f.read().strip()
                f.close()
        except:
                pass

arm_box = MODEL_NAME in ('sf5008','et13000','et1x000','uno4k', 'ultimo4k', 'solo4k', 'hd51', 'hd52', 'dm820', 'dm7080', 'sf4008', 'dm900', 'dm920', 'gb7252', 'dags7252', 'vs1500','8100s')

class Disks:
        ptypes = {'0': 'Empty',
                  '24': 'NEC DOS',
                  '81': 'Minix / old Lin',
                  'bf': 'Solaris',
                  '1': 'FAT12',
                  '39': 'Plan 9',
                  '82': 'Linux swap / Solaris',
                  'c1': 'DRDOS/sec (FAT)',
                  '2': 'XENIX root',
                  '3c': 'PartitionMagic',
                  '83': 'Linux',
                  'c4': 'DRDOS/sec (FAT)',
                  '3': 'XENIX usr',
                  '40': 'Venix 80286',
                  '84': 'OS/2 hidden C:',
                  'c6': 'DRDOS/sec (FAT)',
                  '4': 'FAT16 <32M',
                  '41': 'PPC PReP Boot',
                  '85': 'Linux extended',
                  'c7': 'Syrinx',
                  '5': 'Extended',
                  '42': 'SFS',
                  '86': 'NTFS volume set',
                  'da': 'Non-FS data',
                  '6': 'FAT16',
                  '4d': 'QNX4.x',
                  '87': 'NTFS volume set',
                  'db': 'CP/M / CTOS',
                  '7': 'HPFS/NTFS/exFAT',
                  '4e': 'QNX4.x 2nd part',
                  '88': 'Linux plaintext',
                  'de': 'Dell Utility',
                  '8': 'AIX',
                  '4f': 'QNX4.x 3rd part',
                  '8e': 'Linux LVM',
                  'df': 'BootIt',
                  '9': 'AIX bootable',
                  '50': 'OnTrack DM',
                  '93': 'Amoeba',
                  'e1': 'DOS access',
                  'a': 'OS/2 Boot Manager',
                  '51': 'OnTrack DM6 Aux',
                  '94': 'Amoeba BBT',
                  'e3': 'DOS R/O',
                  'b': 'W95 FAT32',
                  '52': 'CP/M',
                  '9f': 'BSD/OS',
                  'e4': 'SpeedStor',
                  'c': 'W95 FAT32 (LBA)',
                  '53': 'OnTrack DM6 Aux',
                  'a0': 'IBM Thinkpad hi',
                  'eb': 'BeOS fs',
                  'e': 'W95 FAT16 (LBA)',
                  '54': 'OnTrackDM6',
                  'a5': 'FreeBSD',
                  'ee': 'GPT',
                  'f': "W95 Ext'd (LBA)",
                  '55': 'EZ-Drive',
                  'a6': 'OpenBSD',
                  'ef': 'EFI',
                  '10': 'OPUS',
                  '56': 'Golden Bow',
                  'a7': 'NeXTSTEP',
                  'f0': 'Linux/PA-RISC',
                  '11': 'Hidden FAT12',
                  '5c': 'Priam Edisk',
                  'a8': 'Darwin UFS',
                  'f1': 'SpeedStor',
                  '12': 'Compaq diagnostic',
                  '61': 'SpeedStor',
                  'a9': 'NetBSD',
                  'f4': 'SpeedStor',
                  '14': 'Hidden FAT16',
                  '63': 'GNU HURD',
                  'ab': 'Darwin boot',
                  'f2': 'DOS secondary',
                  '16': 'Hidden FAT16',
                  '64': 'Novell Netware',
                  'af': 'HFS / HFS+',
                  'fb': 'VMware VMFS',
                  '17': 'Hidden HPFS/NTFS',
                  '65': 'Novell Netware',
                  'b7': 'BSDI fs',
                  'fc': 'VMware VMKCORE',
                  '18': 'AST SmartSleep',
                  '70': 'DiskSecure Mult',
                  'b8': 'BSDI swap',
                  'fd': 'Linux raid auto',
                  '1b': 'Hidden W95 FAT32',
                  '75': 'PC/IX',
                  'bb': 'Boot Wizard hidden',
                  'fe': 'LANstep',
                  '1c': 'Hidden W95 FAT32',
                  '80': 'Old Minix',
                  'be': 'Solaris boot',
                  'ff': 'BBT',
                  '1e': 'Hidden W95 FAT16'}

        def __init__(self):
                self.disks = []
                self.readDisks()
                self.readPartitions()

        def readDisks(self):
                partitions = open("/proc/partitions")
                for part in partitions:
                        res = re.sub("\\s+", " ", part).strip().split(" ")
                        if res and len(res) == 4:
                                if len(res[3]) == 3 and (res[3][:2] == "sd" or res[3][:3] == "hdb") or len(res[3]) == 7 and (res[3][:6] == "mmcblk" and not arm_box):
                                        self.disks.append([res[3],
                                                           int(res[2]) * 1024,
                                                           self.isRemovable(res[3]),
                                                           self.getModel(res[3]),
                                                           self.getVendor(res[3]),
                                                           [],
                                                           self.isRotational(res[3]),
                                                           self.isInternal(res[3])])

        def readPartitions(self):
                partitions = open("/proc/partitions")
                for part in partitions:
                        res = re.sub("\\s+", " ", part).strip().split(" ")
                        if res and len(res) == 4:
                                if len(res[3]) > 3 and (res[3][:2] == "sd" or res[3][:3] == "hdb") or len(res[3]) > 7 and (res[3][:6] == "mmcblk" and not arm_box):
                                        for i in self.disks:
                                                if i[0] == res[3][:3] or res[3][:7] in i[0]:
                                                        i[5].append([res[3],
                                                                     int(res[2]) * 1024,
                                                                     self.getTypeName(res[3]),
                                                                     self.getType(res[3])])
                                                        break

        def isRemovable(self, device):
                removable = False
                try:
                        data = open('/sys/block/%s/removable' % device, 'r').read().strip()
                        removable = int(data)
                except:
                        pass
                return removable

        def isRotational(self, device):
                try:
                        data = open("/sys/block/%s/queue/rotational" % device, "r").read().strip()
                        rotational = int(data)
                except:
                        rotational = True
                return rotational

        def isInternal(self, device):
                internal = False
                try:
                        phys_path = os.path.realpath(self.sysfsPath('device', device))
                        internal =  "pci" in phys_path or "ahci" in phys_path or "sata" in phys_path
                except:
                        pass
                return internal

        def sysfsPath(self, filename, device):
                return os.path.join('/sys/block/', device, filename)

        def getTypeName(self, device):
                if len(device) > 7:
                        dev = device[:7]
                        n = device[8:]
                else:
                        dev = device[:3]
                        n = device[3:]
                cmd = '/usr/sbin/sfdisk -c /dev/%s %s' % (dev, n)
                fdisk = os.popen(cmd, 'r')
                res = fdisk.read().strip()
                fdisk.close()
                if res in self.ptypes.keys():
                        return self.ptypes[res]
                return res

        def getType(self, device):
                if len(device) > 7:
                        dev = device[:7]
                        n = device[8:]
                else:
                        dev = device[:3]
                        n = device[3:]
                cmd = '/usr/sbin/sfdisk -c /dev/%s %s' % (dev, n) # use --part-type instead -c
                fdisk = os.popen(cmd, 'r')
                res = fdisk.read().strip()
                fdisk.close()
                return res

        def getModel(self, device):
                try:
                        return open("/sys/block/%s/device/model" % device, "r").read().strip()
                except:
                        try:
                                return open("/sys/block/%s/device/name" % device, "r").read().strip()
                        except:
                                try:
                                        return open("/sys/block/%s+p/device/name" % device, "r").read().strip()
                                except:
                                        pass
                return ""

        def getVendor(self, device):
                try:
                        return open("/sys/block/%s/device/vendor" % device, "r").read().strip()
                except:
                        return ""

        def isMounted(self, device):
                mounts = open("/proc/mounts")
                for mount in mounts:
                        res = mount.split(" ")
                        if res and len(res) > 1:
                                if res[0][:8] == '/dev/%s' % device:
                                        mounts.close()
                                        return True
                mounts.close()
                return False

        def isMountedP(self, device, partition):
                mounts = open("/proc/mounts")
                for mount in mounts:
                        res = mount.split(" ")
                        if res and len(res) > 1:
                                if res[0] == '/dev/%s%s' % (device, partition):
                                        mounts.close()
                                        return True
                mounts.close()
                return False

        def getMountedP(self, device, partition):
                mounts = open("/proc/mounts")
                for mount in mounts:
                        res = mount.split(" ")
                        if res and len(res) > 1:
                                if res[0] == "/dev/%s%d" % (device, partition):
                                        mounts.close()
                                        return res[1]
                mounts.close()
                return None

        def umount(self, device):
                mounts = open("/proc/mounts", 'r')
                line = mounts.readlines()
                mounts.close()
                for mnt in line:
                        res = mnt.strip().split()
                        if res and len(res) > 1:
                                if res[0][:8] == "/dev/%s" % device:
                                        print("[DeviceManager] umount %s" % res[0])
                                        if os.system("umount -f %s && sleep 2" % res[0]) != 0:
                                                return False
                mounts = open("/proc/mounts", 'r')
                line = mounts.readlines()
                mounts.close()
                for mnt in line:
                        res = mnt.strip().split()
                        if res and len(res) > 1:
                                if res[0][:8] == "/dev/%s" % device:
                                        print("[DeviceManager] umount %s" % res[0])
                                        if os.system("umount -f %s && sleep 2" % res[3]) != 0:
                                                return False
                return True

        def umountP(self, device, partition):
                if os.system("umount -f /dev/%s%d && sleep 2" % (device, partition)) != 0:
                        return False
                return True

        def mountP(self, device, partition, path):
                if os.system("mount /dev/%s%d %s" % (device, partition, path)) != 0:
                        return False
                return True

        def mount(self, fdevice, path):
                if os.system("mount /dev/%s %s" % (fdevice, path)) != 0:
                        return False
                return True

        def fdisk(self, device, size, type, fstype=0):
                if self.isMounted(device):
                        def mount(self, fdevice, path):
                                print("[DeviceManager] device is mounted... umount")
                if not self.umount(device):
                        def mount(self, fdevice, path):
                                print("[DeviceManager] umount failed!")
                return -1

                if fstype == 0 or fstype == 1 or fstype == 2:
                        ptype = "83"
                elif fstype == 3 or fstype == 4:
                        ptype = "7"
                elif fstype == 5:
                        ptype = "b"
                if type == 0:
                        psize = size / 1048576
                        if psize > 128000:
                                print("[DeviceManager] Detected >128GB disk, using 4k alignment")
                                flow = "8,,%s\n0,0\n0,0\n0,0\nwrite\n" % ptype
                        else:
                                flow = ",,%s\nwrite\n" % ptype
                elif type == 1:
                        psize = size / 1048576 / 2
                        flow = ",%dM,%s\n,,%s\nwrite\n" % (psize, ptype, ptype)
                elif type == 2:
                        psize = size / 1048576 / 4 * 3
                        flow = ",%dM,%s\n,,%s\nwrite\n" % (psize, ptype, ptype)
                elif type == 3:
                        psize = size / 1048576 / 3
                        flow = ",%dM,%s\n,%dM,%s\n,,%s\nwrite\n" % (psize,
                                                                    ptype,
                                                                    psize,
                                                                    ptype,
                                                                    ptype)
                elif type == 4:
                        psize = size / 1048576 / 4
                        flow = ",%dM,%s\n,%dM,%s\n,%dM,%s\n,,%s\nwrite\n" % (psize,
                                                                             ptype,
                                                                             psize,
                                                                             ptype,
                                                                             psize,
                                                                             ptype,
                                                                             ptype)

                cmd = '%s --no-reread -uS /dev/%s' % ('/usr/sbin/sfdisk', device)
                sfdisk = os.popen(cmd, 'w')
                sfdisk.write(flow)
                ret = sfdisk.close()
                print('[DeviceManager]', ret)
                if ret:
                #if ret == 256 and sfdisk_version_bug:
                #	print('[DeviceManager] bug is found ', ret)
                #	return 0
                #else:
                        return -2
                os.system("/sbin/mdev -s")
                return 0

        def chkfs(self, device, partition, fstype=0):
                fdevice = '%s%d' % (device, partition)
                print('[DeviceManager] checking device %s' % fdevice)
                if self.isMountedP(device, partition):
                        oldmp = self.getMountedP(device, partition)
                        print('[DeviceManager] partition is mounted... umount')
                        if not self.umountP(device, partition):
                                print('[DeviceManager] umount failed!')
                                return -1
                else:
                        oldmp = ''
                if self.isMountedP(device, partition):
                        return -1
                if fstype == 0 or fstype == 1:
                        ret = os.system('e2fsck -C 0 -f -p /dev/%s' % fdevice)
                elif fstype == 2:
                        tools = "ntfsfix"
                        data = os.popen("blkid").readlines()
                        for line in data:
                                if fdevice in line and 'exfat' in line:
                                        tools = "exfatfsck"
                        ret = os.system('%s /dev/%s' % (tools, fdevice))
                elif fstype == 3:
                        ret = os.system('dosfsck -a /dev/%s' % fdevice)
                if len(oldmp) > 0:
                        self.mount(fdevice, oldmp)
                if ret == 0:
                        return 0
                return -2

        def mkfs(self, device, partition, fstype=0):
                dev = "%s%d" % (device, partition)
                size = 0
                partitions = open("/proc/partitions")
                for part in partitions:
                        res = re.sub("\s+", " ", part).strip().split(" ")
                        if res and len(res) == 4:
                                if res[3] == dev:
                                        size = int(res[2])
                                        break

                if size == 0:
                        return -1

                if self.isMountedP(device, partition):
                        oldmp = self.getMountedP(device, partition)
                        print("[DeviceManager] partition is mounted... umount")
                        if not self.umountP(device, partition):
                                print("[DeviceManager] umount failed!")
                                return -2
                else:
                        oldmp = ""
                psize = size / 1024
                if fstype == 0:
                        cmd = "mkfs.ext4 -F "
                        if psize > 20000:
                                try:
                                        version = open('/proc/version', 'r').read().split(' ', 4)[2].split('.', 2)[:2]
                                        if version[0] > 3 and version[1] >= 2:
                                                cmd += '-O bigalloc -C 262144 '
                                except:
                                        pass
                        cmd += '-m0 -O dir_index /dev/' + dev
                elif fstype == 1:
                        cmd = "mkfs.ext3 -F "
                        if psize > 250000:
                                cmd += "-T largefile -O sparse_super -N 262144 "
                        elif psize > 16384:
                                cmd += "-T largefile -O sparse_super "
                        elif psize > 2048:
                                cmd += "-T largefile -N %s " % str(psize * 32)
                        cmd += "-m0 -O dir_index /dev/" + dev
                        os.system("opkg update && opkg install kernel-module-ext3")
                elif fstype == 2:
                        cmd = 'mkfs.ext2 -F '
                        if psize > 2048:
                                cmd += '-T largefile '
                        cmd += '-m0 /dev/' + dev
                        os.system("opkg update && opkg install kernel-module-ext2")
                elif fstype == 3:
                        cmd = "mkfs.ntfs -f /dev/" + dev
                elif fstype == 4:
                        cmd = "mkfs.exfat /dev/" + dev
                elif fstype == 5:
                        if psize > 4194304:
                                cmd = 'mkfs.vfat -I -S4096 -F32 /dev/' + dev
                        else:
                                cmd = 'mkfs.vfat -I -F32 /dev/' + dev
                else:
                        if len(oldmp) > 0:
                                self.mount(dev, oldmp)
                        return -3
                ret = os.system(cmd)

                if len(oldmp) > 0:
                        self.mount(dev, oldmp)

                if ret == 0:
                        return 0
                return -3
###########################################################################################################################
class MountPoints():
        def __init__(self):
                self.entries = []
                self.uuids = []
                self.fstab = "/etc/fstab"
                self.blkid = "blkid"

        def read(self):
                rows = open(self.fstab, "r").read().strip().split("\n")
                for row in rows:
                        self.entries.append({
                                "row": row,
                                "data": re.split("\s+", row),
                                "modified": False
                        })

        def write(self):
                conf = open(self.fstab, "w")
                for entry in self.entries:
                        if entry["modified"]:
                                if len(entry["data"]) != 6:
                                        print("[DeviceManager] WARNING: fstab entry with not valid data")
                                        continue
                                conf.write("\t".join(entry["data"]) + "\n")
                        else:
                                conf.write(entry["row"] + "\n")
                conf.close()

        def checkPath(self, path):
                return self.exist(path)

        def isMounted(self, path):
                mounts = open("/proc/mounts")
                for mount in mounts:
                        res = mount.split(" ")
                        if res and len(res) > 1:
                                if res[1] == path:
                                        mounts.close()
                                        return True
                mounts.close()
                return False

        def getRealMount(self, device, partition):
                mounts = open("/proc/mounts")
                for mount in mounts:
                        res = mount.split(" ")
                        if res and len(res) > 1:
                                if res[0] == "/dev/%s%i" % (device, partition):
                                        mounts.close()
                                        return res[1]

                mounts.close()
                return ""

        def umount(self, path):
                return os.system("umount %s" % path) == 0

        def mount(self, device, partition, path):
                return os.system("[ ! -d %s ] && mkdir %s\nmount /dev/%s%d %s" % (path, path, device, partition, path)) == 0

        def exist(self, path):
                for entry in self.entries:
                        if (len(entry["data"]) == 6):
                                if entry["data"][1] == path:
                                        return True
                return False

        def delete(self, path):
                for entry in self.entries:
                        if (len(entry["data"]) == 6):
                                if entry["data"][1] == path:
                                        self.entries.remove(entry)

        def deleteDisk(self, device):
                for i in range(1,4):
                        res = self.get(device, i)
                        if len(res) > 0:
                                self.delete(res)

        def add(self, device, partition, path):
                uuid = self.getUUID(device, partition)
                for entry in self.entries:
                        if (len(entry["data"]) == 6):
                                if entry["data"][0] == "/dev/%s%i" % (device, partition):
                                        self.entries.remove(entry)
                                elif entry["data"][0] == "UUID=" + uuid:
                                        self.entries.remove(entry)
                                elif entry["data"][1] == path:
                                        self.entries.remove(entry)

                self.entries.append({
                        "row": "",
                        "data": ["UUID=" + uuid, path, "auto", "defaults", "1", "1"],
                        "modified": True
                })

        def getUUID(self, device, partition):
                for uuid in self.uuids:
                        if uuid["device"] == device and uuid["partition"] == partition:
                                return uuid["uuid"]

                rows = os.popen(self.blkid).read().strip().split("\n")
                for row in rows:
                        tmp = row.split(":")
                        if len(tmp) < 2:
                                continue

                        if tmp[0] == "/dev/%s%i" % (device, partition):
                                tmp.reverse()
                                key = tmp.pop()
                                tmp.reverse()
                                value = ":".join(tmp)
                                uuid = "00000000"
                                ret = re.search('UUID=\"([\w\-]+)\"', value)
                                if ret:
                                        uuid = ret.group(1)
                                self.uuids.append({
                                        "device": device,
                                        "partition": partition,
                                        "uuid": uuid
                                })
                                return uuid

                return "00000000"

        def get(self, device, partition):
                uuid = self.getUUID(device, partition)
                for entry in self.entries:
                        if (len(entry["data"]) == 6):
                                if entry["data"][0] == "/dev/%s%i" % (device, partition):
                                        return entry["data"][1]
                                elif entry["data"][0] == "UUID=" + uuid:
                                        return entry["data"][1]
                return ""
######################################################################################################################
FULLHD = False
if getDesktop(0).size().width() >= 1920:
        FULLHD = True

class HddInfo(ConfigListScreen, Screen):
        if FULLHD:
                skin = """
		<screen name="HddInfo" position="center,center" size="560,430" title="Hard Drive Info">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget font="Regular;18" halign="left" name="model" position="20,45" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="serial" position="20,75" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="firmware" position="20,105" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="cylinders" position="20,135" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="heads" position="20,165" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="sectors" position="20,195" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="readDisk" position="20,225" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="readCache" position="20,255" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="temp" position="20,285" size="540,25" valign="center" />
			<widget name="config" position="20,325" scrollbarMode="showOnDemand" size="540,30" />
		</screen>"""
        else:
                skin = """
		<screen name="HddInfo" position="center,center" size="560,430" title="Hard Drive Info">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
			<widget font="Regular;18" halign="left" name="model" position="20,45" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="serial" position="20,75" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="firmware" position="20,105" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="cylinders" position="20,135" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="heads" position="20,165" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="sectors" position="20,195" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="readDisk" position="20,225" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="readCache" position="20,255" size="540,25" valign="center" />
			<widget font="Regular;18" halign="left" name="temp" position="20,285" size="540,25" valign="center" />
			<widget name="config" position="20,325" scrollbarMode="showOnDemand" size="540,30" />
		</screen>"""

        def __init__(self, session, device, deviceinfo):
                Screen.__init__(self, session)
                self.device = device
                self.deviceinfo = deviceinfo
                self.list = []
                text = " "
                if self.deviceinfo[2] and not self.deviceinfo[6]:
                        self.list.append(getConfigListEntry(_("Harddisk standby after"), config.usage.hdd_standby))
                        text = _("Save")
                ConfigListScreen.__init__(self, self.list)
                self["key_green"] = Button(text)
                self["key_red"] = Button(_("Exit"))
                self["model"] = Label(_("Model: unknown"))
                self["serial"] = Label(_("Serial: unknown"))
                self["firmware"] = Label(_("Firmware: unknown"))
                self["cylinders"] = Label(_("Cylinders: unknown"))
                self["heads"] = Label(_("Heads: unknown"))
                self["sectors"] = Label(_("Sectors: unknown"))
                self["readDisk"] = Label(_("Read disk speed: unknown"))
                self["readCache"] = Label(_("Read disk cache speed: unknown"))
                self["temp"] = Label(_("Disk temperature: unknown"))
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                            {
                                                    "red": self.keyCancel,
                                                    "green": self.keySave,
                                                    "cancel": self.keyCancel,
                                                    }, -2)

                self.onLayoutFinish.append(self.drawInfo)
                self.onShown.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("Device Details"))

        def drawInfo(self):
                device = "/dev/%s" % self.device
                print("device:", device)
                #regexps
                modelRe = re.compile(r"Model Number:\s*([\w\-]+)")
                serialRe = re.compile(r"Serial Number:\s*([\w\-]+)")
                firmwareRe = re.compile(r"Firmware Revision:\s*([\w\-]+)")
                cylindersRe = re.compile(r"cylinders\s*(\d+)\s*(\d+)")
                headsRe = re.compile(r"heads\s*(\d+)\s*(\d+)")
                sectorsRe = re.compile(r"sectors/track\s*(\d+)\s*(\d+)")
                readDiskRe = re.compile(r"Timing buffered disk reads:\s*(.*)")
                readCacheRe = re.compile(r"Timing buffer-cache reads:\s*(.*)")
                tempRe = re.compile(r"%s:.*:(.*)" % device)

                # wake up disk... disk in standby may cause not correct value
                os.system("/sbin/hdparm -S 0 %s" % device)

                hdparm = os.popen("/sbin/hdparm -I %s" % device)
                for line in hdparm:
                        model = re.findall(modelRe, line)
                        if model:
                                self["model"].setText(_("Model: %s") % model[0].lstrip())
                        serial = re.findall(serialRe, line)
                        if serial:
                                self["serial"].setText(_("Serial: %s") % serial[0].lstrip())
                        firmware = re.findall(firmwareRe, line)
                        if firmware:
                                self["firmware"].setText(_("Firmware: %s") % firmware[0].lstrip())
                        cylinders = re.findall(cylindersRe, line)
                        if cylinders:
                                self["cylinders"].setText(_("Cylinders: %s (max) %s (current)") % (cylinders[0][0].lstrip(), cylinders[0][1].lstrip()))
                        heads = re.findall(headsRe, line)
                        if heads:
                                self["heads"].setText(_("Heads: %s (max) %s (current)") % (heads[0][0].lstrip(), heads[0][1].lstrip()))
                        sectors = re.findall(sectorsRe, line)
                        if sectors:
                                self["sectors"].setText(_("Sectors: %s (max) %s (current)") % (sectors[0][0].lstrip(), sectors[0][1].lstrip()))
                hdparm.close()
                hdparm = os.popen("/sbin/hdparm -t %s" % device)
                for line in hdparm:
                        readDisk = re.findall(readDiskRe, line)
                        if readDisk:
                                self["readDisk"].setText(_("Read speed: %s") % readDisk[0].lstrip())
                hdparm.close()
                hdparm = os.popen("/sbin/hdparm -T %s" % device)
                for line in hdparm:
                        readCache = re.findall(readCacheRe, line)
                        if readCache:
                                self["readCache"].setText(_("Read cache speed: %s") % readCache[0].lstrip())
                hdparm.close()
                if os.path.exists("/tmp/tmpa.txt"):
                        os.remove("/tmp/tmpa.txt")
                else:
                        os.system("touch /tmp/tmpa.txt")
                        time.sleep(1)                        		
                hddtemp = os.popen("/usr/sbin/hddtemp -q %s >/tmp/tmpa.txt" % device)
                time.sleep(1)
                with open("/tmp/tmpa.txt", 'r', encoding='windows-1252') as f:
                        lines = f.readlines()
                for line in lines:
                        temp = re.findall(tempRe, line)
                        if temp:
                                self["temp"].setText("Disk temperature: %s" % temp[0].lstrip())
                f.close()
                if os.path.exists("/tmp/tmpa.txt"):
                        os.remove("/tmp/tmpa.txt")                				
                hddtemp.close()
#######################################################################################################################
FULLHD = False
if getDesktop(0).size().width() >= 1920:
        FULLHD = True

class ExtraActionBox(Screen):
        if FULLHD:
                skin = """
		<screen name="ExtraActionBox" position="center,center" size="560,70" title=" ">
			<widget alphatest="on" name="logo" position="10,10" size="48,48" transparent="1" zPosition="2"/>
			<widget font="Regular;20" halign="center" name="message" position="10,10" size="538,48" valign="center" />
		</screen>"""
        else:
                skin = """
		<screen name="ExtraActionBox" position="center,center" size="560,70" title=" ">
			<widget alphatest="on" name="logo" position="10,10" size="48,48" transparent="1" zPosition="2"/>
			<widget font="Regular;20" halign="center" name="message" position="10,10" size="538,48" valign="center" />
		</screen>"""
        def __init__(self, session, message, title, action):
                Screen.__init__(self, session)
                self.session = session
                self.ctitle = title
                self.caction = action

                self["message"] = Label(message)
                self["logo"] = Pixmap()
                self.timer = eTimer()
                self.timer.callback.append(self.__setTitle)
                self.timer.start(500, 1)

        def __setTitle(self):
                if self["logo"].instance is not None:
                        self["logo"].instance.setPixmapFromFile(resolveFilename(SCOPE_GUISKIN, '/usr/lib/enigma2/python/OPENDROID/icons/run.png'))
                self.setTitle(self.ctitle)
                self.timer = eTimer()
                self.timer.callback.append(self.__start)
                self.timer.start(500, 1)

        def __start(self):
                self.close(self.caction())
#############################################################################################################################
def MessageBoxEntry(name, picture):
        pixmap = LoadPixmap(cached = True, path = resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/" + picture));
        if not pixmap:
                pixmap = LoadPixmap(cached = True, path = resolveFilename(SCOPE_GUISKIN, "/usr/lib/enigma2/python/OPENDROID/icons/empty.png"));

        return (pixmap, name)

class ExtraMessageBox(Screen):
        skin = """
	<screen name="ExtraMessageBox" position="center,center" size="460,430" title=" ">
		<widget name="message" position="10,10" size="440,25" font="Regular;20" />
		<widget source="menu" render="Listbox" position="20,90" size="420,360" scrollbarMode="showOnDemand">
			<convert type="TemplatedMultiContent">
				{"template": [
					MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (48, 48), png = 0),
					MultiContentEntryText(pos = (65, 10), size = (425, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
					],
					"fonts": [gFont("Regular", 22)],
					"itemHeight": 48
				}
			</convert>
		</widget>
		<applet type="onLayoutFinish">
# this should be factored out into some helper code, but currently demonstrates applets.
from enigma import eSize, ePoint

orgwidth = self.instance.size().width()
orgheight = self.instance.size().height()
orgpos = self.instance.position()
textsize = self[&quot;message&quot;].getSize()

# y size still must be fixed in font stuff...
if self[&quot;message&quot;].getText() != &quot;&quot;:
	textsize = (textsize[0] + 80, textsize[1] + 60)
else:
	textsize = (textsize[0] + 80, textsize[1] + 4)

count = len(self.list)
if count &gt; 7:
	count = 7
offset = 48 * count
wsizex = textsize[0] + 80
wsizey = textsize[1] + offset + 20

if (460 &gt; wsizex):
	wsizex = 460
wsize = (wsizex, wsizey)

# resize
self.instance.resize(eSize(*wsize))

# resize label
self[&quot;message&quot;].instance.resize(eSize(*textsize))

# move list
listsize = (wsizex - 20, 48 * count)
self[&quot;menu&quot;].downstream_elements.downstream_elements.instance.move(ePoint(10, textsize[1] + 10))
self[&quot;menu&quot;].downstream_elements.downstream_elements.instance.resize(eSize(*listsize))

# center window
newwidth = wsize[0]
newheight = wsize[1]
self.instance.move(ePoint(orgpos.x() + (orgwidth - newwidth)/2, orgpos.y()  + (orgheight - newheight)/2))
		</applet>
	</screen>"""

        def __init__(self, session, message = "", title = "", menulist = [], type = 0, exitid = -1, default = 0, timeout = 0):
                # type exist for compability... will be ignored
                Screen.__init__(self, session)
                self.session = session
                self.ctitle = title
                self.exitid = exitid
                self.default = default
                self.timeout = timeout
                self.elapsed = 0

                self.list = []
                for item in menulist:
                        self.list.append(MessageBoxEntry(item[0], item[1]))

                self['menu'] = List(self.list)
                self["menu"].onSelectionChanged.append(self.selectionChanged)

                self["message"] = Label(message)
                self["actions"] = ActionMap(["SetupActions"],
                                            {
                                                    "ok": self.ok,
                                                    "cancel": self.cancel
                                                    }, -2)

                self.onLayoutFinish.append(self.layoutFinished)

                self.timer = eTimer()
                self.timer.callback.append(self.timeoutStep)
                if self.timeout > 0:
                        self.timer.start(1000, 1)

        def selectionChanged(self):
                self.timer.stop()
                self.setTitle(self.ctitle)

        def timeoutStep(self):
                self.elapsed += 1
                if self.elapsed == self.timeout:
                        self.ok()
                else:
                        self.setTitle("%s - %d" % (self.ctitle, self.timeout - self.elapsed))
                        self.timer.start(1000, 1)

        def layoutFinished(self):
                if self.timeout > 0:
                        self.setTitle("%s - %d" % (self.ctitle, self.timeout))
                else:
                        self.setTitle(self.ctitle)
                self['menu'].setCurrentIndex(self.default)

        def ok(self):
                index = self['menu'].getIndex()
                self.close(index)

        def cancel(self):
                if self.exitid > -1:
                        self.close(self.exitid)

