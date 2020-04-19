# -*- coding: utf-8 -*-

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from inits import *
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from enigma import eTimer
from Screens.InputBox import InputBox
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Plugins.Extensions.WeatherPlugin.setup import MSNWeatherPluginEntriesListConfigScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import *
from Tools.LoadPixmap import LoadPixmap
from inits import AtileHDInfo, SkinPath
from debug import printDEBUG
from Components.Console import Console as iConsole
try:
        from Screens.SkinSelector import SkinSelector
except:
        from Plugins.SystemPlugins.SkinSelector.plugin import SkinSelector

from os import listdir, remove, rename, system, path, symlink, chdir, rmdir, mkdir
import shutil
import re

config.plugins.AtileHD = ConfigSubsection()

def Plugins(**kwargs):
        return [PluginDescriptor(name=_("%s Setup") % CurrentSkinName, description=_("Personalize your Skin"), where = PluginDescriptor.WHERE_MENU, icon="plugin.png", fnc=menu)]

def menu(menuid, **kwargs):
        for line in open("/etc/enigma2/settings"):
                if menuid == "mainmenu" and not config.skin.primary_skin.value == "Multibox/skin.xml":
                        return [(_("Setup - %s") % CurrentSkinName, main, "atilehd_setup", None)]
                else:
                        pass
                return [ ]

def main(session, **kwargs):
        printDEBUG("Opening Menu ...")
        session.open(AtileHDB_Config)

def isInteger(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False

class AtileHDB_Config(Screen, ConfigListScreen):
	skin = """
	<screen name="AtileHDB_Config" position="82,124" size="1101,376" title="Ultimate Setup" backgroundColor="transparent" flags="wfNoBorder">
		<eLabel position="7,2" size="1091,372" zPosition="-15" backgroundColor="#20000000" />
		<eLabel position="4,51" size="664,238" zPosition="-10" backgroundColor="#20606060" />
		<eLabel position="672,51" size="410,237" zPosition="-10" backgroundColor="#20606060" />
		<eLabel position="6,302" size="240,55" zPosition="-10" backgroundColor="#20b81c46" />
		<eLabel position="284,302" size="240,55" zPosition="-10" backgroundColor="#20009f3c" />
		<eLabel position="564,302" size="240,56" zPosition="-10" backgroundColor="#209ca81b" />
		<eLabel position="843,302" size="240,55" zPosition="-10" backgroundColor="#202673ec" />
		<widget source="Title" render="Label" position="2,4" size="889,43" font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#004e4e4e" transparent="1" />
		<widget name="config" position="6,55" size="657,226" scrollbarMode="showOnDemand" transparent="1" />
		<widget name="Picture" position="676,56" size="400,225" alphatest="blend" />
		<widget name="key_red" position="18,316" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20b81c46" transparent="1" />
		<widget name="key_green" position="299,317" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20009f3c" transparent="1" />
		<widget name="key_yellow" position="578,317" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#209ca81b" transparent="1" />
		<widget name="key_blue" position="854,318" size="210,25" zPosition="0" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#202673ec" transparent="1" />
		</screen>
	"""
	skin_lines = []
	changed_screens = False

	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		self['lab11'] = Label(_('Weather-Setup. Press Menu Button to get to the weather Setup'))
		self['lab12'] = Label(_('press yellow button to select Ultimate Tool'))
		self['lab13'] = Label(_('Help, Skin settings(Weather)'))
		myTitle=_("Ultimate Setup %s") % AtileHDInfo
		self.setTitle(myTitle)
		try:
			self["title"]=StaticText(myTitle)
		except:
			pass
		self.skin_base_dir = SkinPath
		self.currentSkin = CurrentSkinName
		printDEBUG("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, self.currentSkin))
		if self.currentSkin != '':
			self.currentSkin = '_' + self.currentSkin
		if path.exists(resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/VTIPanel/')):
			self.isVTI = True
		else:
			self.isVTI = False

		self.defaultOption = "default"
		self.defaults = (self.defaultOption, _("Default"))
		self.color_file = "skin_user_colors.xml"
		self.user_center_file = "skin_user_center.xml"
		self.user_sb_file = "skin_user_sb.xml"
		self.user_frame_file = "skin_user_frame.xml"
		self.user_lines_file = "skin_user_lines.xml"
		self.user_sbar_file = "skin_user_sbar.xml"
		self.user_wget_file = "skin_user_wget.xml"
		self.user_infobar_file = "skin_user_infobar.xml"
		self.user_sib_file = "skin_user_sib.xml"
		self.user_ch_se_file = "skin_user_ch_se.xml"
		self.user_ev_file = "skin_user_ev.xml"
		self.user_emcsel_file = "skin_user_emcsel.xml"
		self.user_movsel_file = "skin_user_movsel.xml"
		self.user_volume_file = "skin_user_volume.xml"

		if path.exists(self.skin_base_dir):
                        #center
			if path.exists(self.skin_base_dir + self.user_center_file):
				self.default_center_file = path.basename(path.realpath(self.skin_base_dir + self.user_center_file))
				printDEBUG("self.default_center_file = " + self.default_center_file )
			else:
				self.default_center_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/center/"):
				mkdir(self.skin_base_dir + "allScreens/center/")
                        #sb
			if path.exists(self.skin_base_dir + self.user_sb_file):
				self.default_sb_file = path.basename(path.realpath(self.skin_base_dir + self.user_sb_file))
				printDEBUG("self.default_sb_file = " + self.default_sb_file )
			else:
				self.default_sb_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/sb/"):
				mkdir(self.skin_base_dir + "allScreens/sb/")
                        #frame
			if path.exists(self.skin_base_dir + self.user_frame_file):
				self.default_frame_file = path.basename(path.realpath(self.skin_base_dir + self.user_frame_file))
				printDEBUG("self.default_frame_file = " + self.default_frame_file )
			else:
				self.default_frame_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/frame/"):
				mkdir(self.skin_base_dir + "allScreens/frame/")
                        #lines
			if path.exists(self.skin_base_dir + self.user_lines_file):
				self.default_lines_file = path.basename(path.realpath(self.skin_base_dir + self.user_lines_file))
				printDEBUG("self.default_lines_file = " + self.default_lines_file )
			else:
				self.default_lines_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/lines/"):
				mkdir(self.skin_base_dir + "allScreens/lines/")
                        #sbar
			if path.exists(self.skin_base_dir + self.user_sbar_file):
				self.default_sbar_file = path.basename(path.realpath(self.skin_base_dir + self.user_sbar_file))
				printDEBUG("self.default_sbar_file = " + self.default_sbar_file )
			else:
				self.default_sbar_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/sbar/"):
				mkdir(self.skin_base_dir + "allScreens/sbar/")
                        #wget
			if path.exists(self.skin_base_dir + self.user_wget_file):
				self.default_wget_file = path.basename(path.realpath(self.skin_base_dir + self.user_wget_file))
				printDEBUG("self.default_wget_file = " + self.default_wget_file )
			else:
				self.default_wget_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/wget/"):
				mkdir(self.skin_base_dir + "allScreens/wget/")
                        #infobar
			if path.exists(self.skin_base_dir + self.user_infobar_file):
				self.default_infobar_file = path.basename(path.realpath(self.skin_base_dir + self.user_infobar_file))
				printDEBUG("self.default_infobar_file = " + self.default_infobar_file )
			else:
				self.default_infobar_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/infobar/"):
				mkdir(self.skin_base_dir + "allScreens/infobar/")

                        #sib
			if path.exists(self.skin_base_dir + self.user_sib_file):
				self.default_sib_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_sib_file = " + self.default_sib_file )
			else:
				self.default_sib_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/sib/"):
				mkdir(self.skin_base_dir + "allScreens/sib/")
                        #ch_se
			if path.exists(self.skin_base_dir + self.user_ch_se_file):
				self.default_ch_se_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_ch_se_file = " + self.default_ch_se_file )
			else:
				self.default_ch_se_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/ch_se/"):
				mkdir(self.skin_base_dir + "allScreens/ch_se/")
                        #ev
			if path.exists(self.skin_base_dir + self.user_ev_file):
				self.default_ev_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_ev_file = " + self.default_ev_file )
			else:
				self.default_ev_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/ev/"):
				mkdir(self.skin_base_dir + "allScreens/ev/")
                        #emcsel
			if path.exists(self.skin_base_dir + self.user_emcsel_file):
				self.default_emcsel_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_emcsel_file = " + self.default_emcsel_file )
			else:
				self.default_emcsel_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/emcsel/"):
				mkdir(self.skin_base_dir + "allScreens/emcsel/")
                        #movsel
			if path.exists(self.skin_base_dir + self.user_movsel_file):
				self.default_movsel_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_movsel_file = " + self.default_movsel_file )
			else:
				self.default_movsel_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/movsel/"):
				mkdir(self.skin_base_dir + "allScreens/movsel/")
                        #volume
			if path.exists(self.skin_base_dir + self.user_volume_file):
				self.default_volume_file = path.basename(path.realpath(self.skin_base_dir + self.user_volume_file))
				printDEBUG("self.default_volume_file = " + self.default_volume_file )
			else:
				self.default_volume_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/volume/"):
				mkdir(self.skin_base_dir + "allScreens/volume/")
                        #COLORS
			if path.exists(self.skin_base_dir + self.color_file):
				self.default_color_file = path.basename(path.realpath(self.skin_base_dir + self.color_file))
				printDEBUG("self.default_color_file = " + self.default_color_file )
			else:
				self.default_color_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/colors/"):
				mkdir(self.skin_base_dir + "allScreens/colors/")
                        #PREVIEW
			if not path.exists(self.skin_base_dir + "preview"):
				mkdir(self.skin_base_dir + "preview/")
			if path.exists(self.skin_base_dir + "preview"):
				if self.isVTI == False and path.isdir(self.skin_base_dir + "preview"):
					try: rmdir(self.skin_base_dir + "preview")
					except: pass
			else:
				if self.isVTI == True:
					symlink(self.skin_base_dir + "preview", self.skin_base_dir + "preview")
			if path.exists(self.skin_base_dir + "mySkin_off"):
				if not path.exists(self.skin_base_dir + "AtileHD_Selections"):
					chdir(self.skin_base_dir)
					try:
						rename("mySkin_off", "AtileHD_Selections")
					except:
						pass

		current_color = self.getCurrentcolor()[0]
		current_center = self.getCurrentcenter()[0]
		current_sb = self.getCurrentsb()[0]
		current_frame = self.getCurrentframe()[0]
		current_lines = self.getCurrentlines()[0]
		current_sbar = self.getCurrentsbar()[0]
		current_wget = self.getCurrentwget()[0]
		current_infobar = self.getCurrentinfobar()[0]
		current_sib = self.getCurrentsib()[0]
		current_ch_se = self.getCurrentch_se()[0]
		current_ev = self.getCurrentev()[0]
		current_emcsel = self.getCurrentemcsel()[0]
		current_movsel = self.getCurrentmovsel()[0]
		current_volume = self.getCurrentvolume()[0]
		myAtileHD_active = self.getmySkinState()
		self.myAtileHD_active = NoSave(ConfigYesNo(default=myAtileHD_active))
		self.myAtileHD_color = NoSave(ConfigSelection(default=current_color, choices = self.getPossiblecolor()))
		self.myAtileHD_center = NoSave(ConfigSelection(default=current_center, choices = self.getPossiblecenter()))
		self.myAtileHD_sb = NoSave(ConfigSelection(default=current_sb, choices = self.getPossiblesb()))
		self.myAtileHD_frame = NoSave(ConfigSelection(default=current_frame, choices = self.getPossibleframe()))
		self.myAtileHD_lines = NoSave(ConfigSelection(default=current_lines, choices = self.getPossiblelines()))
		self.myAtileHD_sbar = NoSave(ConfigSelection(default=current_sbar, choices = self.getPossiblesbar()))
		self.myAtileHD_wget = NoSave(ConfigSelection(default=current_wget, choices = self.getPossiblewget()))
		self.myAtileHD_infobar = NoSave(ConfigSelection(default=current_infobar, choices = self.getPossibleinfobar()))
		self.myAtileHD_sib = NoSave(ConfigSelection(default=current_sib, choices = self.getPossiblesib()))
		self.myAtileHD_ch_se = NoSave(ConfigSelection(default=current_ch_se, choices = self.getPossiblech_se()))
		self.myAtileHD_ev = NoSave(ConfigSelection(default=current_ev, choices = self.getPossibleev()))
		self.myAtileHD_emcsel = NoSave(ConfigSelection(default=current_emcsel, choices = self.getPossibleemcsel()))
		self.myAtileHD_movsel = NoSave(ConfigSelection(default=current_movsel, choices = self.getPossiblemovsel()))
		self.myAtileHD_volume = NoSave(ConfigSelection(default=current_volume, choices = self.getPossiblevolume()))
		self.myAtileHD_fake_entry = NoSave(ConfigNothing())
		self.LackOfFile = ''
		self.list = []
		ConfigListScreen.__init__(self, self.list, on_change = self.changedEntry)

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
		self["key_yellow"] = Label()
		self["key_blue"] = Label(_("About Weather"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"green": self.keyGreen,
				"red": self.cancel,
				"yellow": self.keyYellow,
				"blue": self.about,
				"cancel": self.cancel,
				"ok": self.keyOk,
				"menu": self.config,
			}, -2)
		self.onLayoutFinish.append(self.opdtext)

		self["Picture"] = Pixmap()

		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)

		self.createConfigList()
		self.updateEntries = False

	def createConfigList(self):
		self.set_color = getConfigListEntry(_("Style:"), self.myAtileHD_color)
		self.set_center = getConfigListEntry(_("Center:"), self.myAtileHD_center)
		self.set_sb = getConfigListEntry(_("ColorSelectedBackground:"), self.myAtileHD_sb)
		self.set_infobar = getConfigListEntry(_("Infobar:"), self.myAtileHD_infobar)
		self.set_sib = getConfigListEntry(_("Secondinfobar:"), self.myAtileHD_sib)
		self.set_ch_se = getConfigListEntry(_("Channelselection:"), self.myAtileHD_ch_se)
		self.set_ev = getConfigListEntry(_("Eventview:"), self.myAtileHD_ev)
		self.set_frame = getConfigListEntry(_("Frame:"), self.myAtileHD_frame)
		self.set_lines = getConfigListEntry(_("Lines:"), self.myAtileHD_lines)
		self.set_sbar = getConfigListEntry(_("Scrollbar:"), self.myAtileHD_sbar)
		self.set_wget = getConfigListEntry(_("Clock_Widget:"), self.myAtileHD_wget)
		self.set_emcsel = getConfigListEntry(_("EMC_Selection:"), self.myAtileHD_emcsel)
		self.set_volume = getConfigListEntry(_("Volume:"), self.myAtileHD_volume)
		self.set_movsel = getConfigListEntry(_("Movie_Selection:"), self.myAtileHD_movsel)
		self.set_myatile = getConfigListEntry(_("Enable skin personalization:"), self.myAtileHD_active)
		self.set_new_skin = getConfigListEntry(_("Change skin"), ConfigNothing())
		self.list = []
		self.list.append(self.set_myatile)
		self.list.append(self.set_color)
		self.list.append(self.set_center)
		self.list.append(self.set_sb)
		self.list.append(self.set_infobar)
		self.list.append(self.set_sib)
		self.list.append(self.set_ch_se)
		self.list.append(self.set_ev)
		self.list.append(self.set_frame)
		self.list.append(self.set_lines)
		self.list.append(self.set_sbar)
		self.list.append(self.set_wget)
		self.list.append(self.set_emcsel)
		self.list.append(self.set_volume)
		self.list.append(self.set_movsel)
		self.list.append(self.set_new_skin)
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		if self.myAtileHD_active.value:
			self["key_yellow"].setText(_("Ultimate Tool"))
		else:
			self["key_yellow"].setText("")
	def config(self):
		self.session.open(MSNWeatherPluginEntriesListConfigScreen)

	def changedEntry(self):
		self.updateEntries = True
		printDEBUG("[AtileHD:changedEntry]")
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHD_color.value)
		elif self["config"].getCurrent() == self.set_center:
			self.setPicture(self.myAtileHD_center.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHD_infobar.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHD_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHD_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHD_ev.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHD_sb.value)
		elif self["config"].getCurrent() == self.set_frame:
			self.setPicture(self.myAtileHD_frame.value)
		elif self["config"].getCurrent() == self.set_lines:
			self.setPicture(self.myAtileHD_lines.value)
		elif self["config"].getCurrent() == self.set_sbar:
			self.setPicture(self.myAtileHD_sbar.value)
		elif self["config"].getCurrent() == self.set_wget:
			self.setPicture(self.myAtileHD_wget.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHD_emcsel.value)
		elif self["config"].getCurrent() == self.set_volume:
			self.setPicture(self.myAtileHD_volume.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHD_movsel.value)
		elif self["config"].getCurrent() == self.set_myatile:
			if self.myAtileHD_active.value:
				self["key_yellow"].setText(_("Ultimate Tool"))
			else:
				self["key_yellow"].setText("")

	def selectionChanged(self):
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHD_color.value)
		elif self["config"].getCurrent() == self.set_center:
			self.setPicture(self.myAtileHD_center.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHD_infobar.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHD_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHD_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHD_ev.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHD_sb.value)
		elif self["config"].getCurrent() == self.set_frame:
			self.setPicture(self.myAtileHD_frame.value)
		elif self["config"].getCurrent() == self.set_lines:
			self.setPicture(self.myAtileHD_lines.value)
		elif self["config"].getCurrent() == self.set_sbar:
			self.setPicture(self.myAtileHD_sbar.value)
		elif self["config"].getCurrent() == self.set_wget:
			self.setPicture(self.myAtileHD_wget.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHD_emcsel.value)
		elif self["config"].getCurrent() == self.set_volume:
			self.setPicture(self.myAtileHD_volume.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHD_movsel.value)
		else:
			self["Picture"].hide()

	def cancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"), MessageBox.TYPE_YESNO, default = False)
		else:
			for x in self["config"].list:
				x[1].cancel()
			if self.changed_screens:
				self.restartGUI()
			else:
				self.close()

	def cancelConfirm(self, result):
		if result is None or result is False:
			printDEBUG("Cancel confirmed.")
		else:
			printDEBUG("Cancel confirmed. Config changes will be lost.")
			for x in self["config"].list:
				x[1].cancel()
			self.close()

	def getPossiblecolor(self):
		color_list = []
		color_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/colors/"):
			return color_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/colors/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('colors_'):
				friendly_name = f.replace("colors_atile_", "").replace("colors_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				color_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('colors_'):
				friendly_name = f.replace("colors_atile_", "").replace("colors_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				color_list.append((f, friendly_name))

		return color_list

	def getPossiblecenter(self):
		center_list = []
		center_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/center/"):
			return center_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/center/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('center_'):
				friendly_name = f.replace("center_atile_", "").replace("center_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				center_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('center_'):
				friendly_name = f.replace("center_atile_", "").replace("center_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				center_list.append((f, friendly_name))

		return center_list

	def getPossiblesb(self):
		sb_list = []
		sb_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/sb/"):
			return sb_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/sb/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('sb_'):
				friendly_name = f.replace("sb_atile_", "").replace("sb_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sb_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('sb_'):
				friendly_name = f.replace("sb_atile_", "").replace("sb_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sb_list.append((f, friendly_name))

		return sb_list

	def getPossibleframe(self):
		frame_list = []
		frame_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/frame/"):
			return frame_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/frame/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('frame_'):
				friendly_name = f.replace("frame_atile_", "").replace("frame_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				frame_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('frame_'):
				friendly_name = f.replace("frame_atile_", "").replace("frame_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				frame_list.append((f, friendly_name))

		return frame_list

	def getPossiblelines(self):
		lines_list = []
		lines_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/lines/"):
			return lines_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/lines/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('lines_'):
				friendly_name = f.replace("lines_atile_", "").replace("lines_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				lines_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('lines_'):
				friendly_name = f.replace("lines_atile_", "").replace("lines_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				lines_list.append((f, friendly_name))

		return lines_list

	def getPossiblesbar(self):
		sbar_list = []
		sbar_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/sbar/"):
			return sbar_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/sbar/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('sbar_'):
				friendly_name = f.replace("sbar_atile_", "").replace("sbar_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sbar_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('sbar_'):
				friendly_name = f.replace("sbar_atile_", "").replace("sbar_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sbar_list.append((f, friendly_name))

		return sbar_list

	def getPossiblewget(self):
		wget_list = []
		wget_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/wget/"):
			return wget_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/wget/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('wget_'):
				friendly_name = f.replace("wget_atile_", "").replace("wget_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				wget_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('wget_'):
				friendly_name = f.replace("wget_atile_", "").replace("wget_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				wget_list.append((f, friendly_name))

		return wget_list

	def getPossibleinfobar(self):
		infobar_list = []
		infobar_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/infobar/"):
			return infobar_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/infobar/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('infobar_'):
				friendly_name = f.replace("infobar_atile_", "").replace("infobar_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				infobar_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('infobar_'):
				friendly_name = f.replace("infobar_atile_", "").replace("infobar_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				infobar_list.append((f, friendly_name))

		return infobar_list

	def getPossiblesib(self):
		sib_list = []
		sib_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/sib/"):
			return sib_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/sib/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('sib_'):
				friendly_name = f.replace("sib_atile_", "").replace("sib_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sib_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('sib_'):
				friendly_name = f.replace("sib_atile_", "").replace("sib_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				sib_list.append((f, friendly_name))

		return sib_list

	def getPossiblech_se(self):
		ch_se_list = []
		ch_se_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/ch_se/"):
			return ch_se_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/ch_se/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('ch_se_'):
				friendly_name = f.replace("ch_se_atile_", "").replace("ch_se_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ch_se_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('ch_se_'):
				friendly_name = f.replace("ch_se_atile_", "").replace("ch_se_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ch_se_list.append((f, friendly_name))

		return ch_se_list

	def getPossibleev(self):
		ev_list = []
		ev_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/ev/"):
			return ev_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/ev/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('ev_'):
				friendly_name = f.replace("ev_atile_", "").replace("ev_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ev_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('ev_'):
				friendly_name = f.replace("ev_atile_", "").replace("ev_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ev_list.append((f, friendly_name))

		return ev_list

	def getPossibleemcsel(self):
		emcsel_list = []
		emcsel_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/emcsel/"):
			return emcsel_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/emcsel/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('emcsel_'):
				friendly_name = f.replace("emcsel_atile_", "").replace("emcsel_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				emcsel_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('emcsel_'):
				friendly_name = f.replace("emcsel_atile_", "").replace("emcsel_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				emcsel_list.append((f, friendly_name))

		return emcsel_list

	def getPossiblemovsel(self):
		movsel_list = []
		movsel_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/movsel/"):
			return movsel_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/movsel/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('movsel_'):
				friendly_name = f.replace("movsel_atile_", "").replace("movsel_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				movsel_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('movsel_'):
				friendly_name = f.replace("movsel_atile_", "").replace("movsel_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				movsel_list.append((f, friendly_name))

		return movsel_list

	def getPossiblevolume(self):
		volume_list = []
		volume_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/volume/"):
			return volume_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/volume/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('volume_'):
				friendly_name = f.replace("volume_atile_", "").replace("volume_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				volume_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('volume_'):
				friendly_name = f.replace("volume_atile_", "").replace("volume_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				volume_list.append((f, friendly_name))

		return volume_list

	def getmySkinState(self):
		chdir(self.skin_base_dir)
		if path.exists("mySkin"):
			return True
		else:
			return False

	def getCurrentcolor(self):
		myfile = self.skin_base_dir + self.color_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/colors/" + self.default_color_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/colors/" + self.default_color_file, self.color_file)
			else:
				return (self.default_color_file, self.default_color_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("colors_atile_", "").replace("colors_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentcenter(self):
		myfile = self.skin_base_dir + self.user_center_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/center/" + self.default_center_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/center/" + self.default_center_file, self.user_center_file)
			else:
				return (self.default_center_file, self.default_center_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("center_atile_", "").replace("center_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentsb(self):
		myfile = self.skin_base_dir + self.user_sb_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/sb/" + self.default_sb_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/sb/" + self.default_sb_file, self.user_sb_file)
			else:
				return (self.default_sb_file, self.default_sb_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("sb_atile_", "").replace("sb_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentframe(self):
		myfile = self.skin_base_dir + self.user_frame_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/frame/" + self.default_frame_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/frame/" + self.default_frame_file, self.user_frame_file)
			else:
				return (self.default_frame_file, self.default_frame_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("frame_atile_", "").replace("frame_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentlines(self):
		myfile = self.skin_base_dir + self.user_lines_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/lines/" + self.default_lines_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/lines/" + self.default_lines_file, self.user_lines_file)
			else:
				return (self.default_lines_file, self.default_lines_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("lines_atile_", "").replace("lines_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentsbar(self):
		myfile = self.skin_base_dir + self.user_sbar_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/sbar/" + self.default_sbar_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/sbar/" + self.default_sbar_file, self.user_sbar_file)
			else:
				return (self.default_sbar_file, self.default_sbar_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("sbar_atile_", "").replace("sbar_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentwget(self):
		myfile = self.skin_base_dir + self.user_wget_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/wget/" + self.default_wget_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/wget/" + self.default_wget_file, self.user_wget_file)
			else:
				return (self.default_wget_file, self.default_wget_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("wget_atile_", "").replace("wget_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentinfobar(self):
		myfile = self.skin_base_dir + self.user_infobar_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/infobar/" + self.default_infobar_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/infobar/" + self.default_infobar_file, self.user_infobar_file)
			else:
				return (self.default_infobar_file, self.default_infobar_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("infobar_atile_", "").replace("infobar_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentsib(self):
		myfile = self.skin_base_dir + self.user_sib_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/sib/" + self.default_sib_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/sib/" + self.default_sib_file, self.user_sib_file)
			else:
				return (self.default_sib_file, self.default_sib_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("sib_atile_", "").replace("sib_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentch_se(self):
		myfile = self.skin_base_dir + self.user_ch_se_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/ch_se/" + self.default_ch_se_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/ch_se/" + self.default_ch_se_file, self.user_ch_se_file)
			else:
				return (self.default_ch_se_file, self.default_ch_se_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("ch_se_atile_", "").replace("ch_se_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentev(self):
		myfile = self.skin_base_dir + self.user_ev_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/ev/" + self.default_ev_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/ev/" + self.default_ev_file, self.user_ev_file)
			else:
				return (self.default_ev_file, self.default_ev_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("ev_atile_", "").replace("ev_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentemcsel(self):
		myfile = self.skin_base_dir + self.user_emcsel_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/emcsel/" + self.default_emcsel_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/emcsel/" + self.default_emcsel_file, self.user_emcsel_file)
			else:
				return (self.default_emcsel_file, self.default_emcsel_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("emcsel_atile_", "").replace("emcsel_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentmovsel(self):
		myfile = self.skin_base_dir + self.user_movsel_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/movsel/" + self.default_movsel_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/movsel/" + self.default_movsel_file, self.user_movsel_file)
			else:
				return (self.default_movsel_file, self.default_movsel_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("movsel_atile_", "").replace("movsel_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)

	def getCurrentvolume(self):
		myfile = self.skin_base_dir + self.user_volume_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/volume/" + self.default_volume_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/volume/" + self.default_volume_file, self.user_volume_file)
			else:
				return (self.default_volume_file, self.default_volume_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("volume_atile_", "").replace("volume_", "")
		friendly_name = friendly_name.replace(".xml", "")
		friendly_name = friendly_name.replace("_", " ")
		return (filename, friendly_name)


	def setPicture(self, f):
		preview = self.skin_base_dir + "preview/"
		if not path.exists(preview):
			mkdir(preview)
		pic = f[:-4]
		if f.startswith("bar_"):
			pic = f + ".png"
		printDEBUG("[AtileHD:setPicture] pic =" + pic + '[jpg|png]')
		previewJPG = preview + "preview_" + picJPG
		if path.exists(preview + "preview_" + pic + '.jpg'):
			self.UpdatePreviewPicture(preview + "preview_" + pic + '.jpg')
		if path.exists(preview + "preview_" + pic + '.png'):
			self.UpdatePreviewPicture(preview + "preview_" + pic + '.png')
		else:
			self["Picture"].hide()

	def setPicture(self, f):
		pic = f[:-4]
		if path.exists(self.skin_base_dir + "preview/preview_" + pic + '.png'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/preview_" + pic + '.png')
		elif path.exists(self.skin_base_dir + "preview/preview_" + pic + '.jpg'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/preview_" + pic + '.jpg')
		elif path.exists(self.skin_base_dir + "preview/" + pic + '.png'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/" + pic + '.png')
		elif path.exists(self.skin_base_dir + "preview/" + pic + '.jpg'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/" + pic + '.jpg')

	def UpdatePreviewPicture(self, PreviewFileName):
		self["Picture"].instance.setScale(1)
		self["Picture"].instance.setPixmap(LoadPixmap(path=PreviewFileName))
		self["Picture"].show()

	def keyYellow(self):
		if self.myAtileHD_active.value:
			if not path.exists(self.skin_base_dir + "AtileHD_Selections"):
				mkdir(self.skin_base_dir + "AtileHD_Selections")
			if not path.exists(self.skin_base_dir + "preview"):
				mkdir(self.skin_base_dir + "preview")
			self.session.openWithCallback(self.AtileHDBScreesnCB, AtileHDBScreens)
		else:
			self["config"].setCurrentIndex(0)

	def keyOk(self):
                sel =  self["config"].getCurrent()
                if sel is not None and sel == self.set_new_skin:
                        self.openSkinSelector()
                else:
                        self.keyGreen()

	def keyGreen(self):
		if self["config"].isChanged() or self.updateEntries == True:
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_color.value=" + self.myAtileHD_color.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_center.value=" + self.myAtileHD_center.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_sb.value=" + self.myAtileHD_sb.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_frame.value=" + self.myAtileHD_frame.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_lines.value=" + self.myAtileHD_lines.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_sbar.value=" + self.myAtileHD_sbar.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_wget.value=" + self.myAtileHD_wget.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_infobar.value=" + self.myAtileHD_infobar.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_sib.value=" + self.myAtileHD_sib.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_ch_se.value=" + self.myAtileHD_ch_se.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_ev.value=" + self.myAtileHD_ev.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_emcsel.value=" + self.myAtileHD_emcsel.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_movsel.value=" + self.myAtileHD_movsel.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_volume.value=" + self.myAtileHD_volume.value)
			for x in self["config"].list:
				x[1].save()
			configfile.save()
			chdir(self.skin_base_dir)
			#center
			if path.exists(self.user_center_file):
				remove(self.user_center_file)
			elif path.islink(self.user_center_file):
				remove(self.user_center_file)
			if path.exists('allScreens/center/' + self.myAtileHD_center.value):
				symlink('allScreens/center/' + self.myAtileHD_center.value, self.user_center_file)
			#sb
			if path.exists(self.user_sb_file):
				remove(self.user_sb_file)
			elif path.islink(self.user_sb_file):
				remove(self.user_sb_file)
			if path.exists('allScreens/sb/' + self.myAtileHD_sb.value):
				symlink('allScreens/sb/' + self.myAtileHD_sb.value, self.user_sb_file)
			#frame
			if path.exists(self.user_frame_file):
				remove(self.user_frame_file)
			elif path.islink(self.user_frame_file):
				remove(self.user_frame_file)
			if path.exists('allScreens/frame/' + self.myAtileHD_frame.value):
				symlink('allScreens/frame/' + self.myAtileHD_frame.value, self.user_frame_file)
			#lines
			if path.exists(self.user_lines_file):
				remove(self.user_lines_file)
			elif path.islink(self.user_lines_file):
				remove(self.user_lines_file)
			if path.exists('allScreens/lines/' + self.myAtileHD_lines.value):
				symlink('allScreens/lines/' + self.myAtileHD_lines.value, self.user_lines_file)
			#sbar
			if path.exists(self.user_sbar_file):
				remove(self.user_sbar_file)
			elif path.islink(self.user_sbar_file):
				remove(self.user_sbar_file)
			if path.exists('allScreens/sbar/' + self.myAtileHD_sbar.value):
				symlink('allScreens/sbar/' + self.myAtileHD_sbar.value, self.user_sbar_file)
			#wget
			if path.exists(self.user_wget_file):
				remove(self.user_wget_file)
			elif path.islink(self.user_wget_file):
				remove(self.user_wget_file)
			if path.exists('allScreens/wget/' + self.myAtileHD_wget.value):
				symlink('allScreens/wget/' + self.myAtileHD_wget.value, self.user_wget_file)
			#infobar
			if path.exists(self.user_infobar_file):
				remove(self.user_infobar_file)
			elif path.islink(self.user_infobar_file):
				remove(self.user_infobar_file)
			if path.exists('allScreens/infobar/' + self.myAtileHD_infobar.value):
				symlink('allScreens/infobar/' + self.myAtileHD_infobar.value, self.user_infobar_file)
			#sib
			if path.exists(self.user_sib_file):
				remove(self.user_sib_file)
			elif path.islink(self.user_sib_file):
				remove(self.user_sib_file)
			if path.exists('allScreens/sib/' + self.myAtileHD_sib.value):
				symlink('allScreens/sib/' + self.myAtileHD_sib.value, self.user_sib_file)
			#ch_se
			if path.exists(self.user_ch_se_file):
				remove(self.user_ch_se_file)
			elif path.islink(self.user_ch_se_file):
				remove(self.user_ch_se_file)
			if path.exists('allScreens/ch_se/' + self.myAtileHD_ch_se.value):
				symlink('allScreens/ch_se/' + self.myAtileHD_ch_se.value, self.user_ch_se_file)
			#ev
			if path.exists(self.user_ev_file):
				remove(self.user_ev_file)
			elif path.islink(self.user_ev_file):
				remove(self.user_ev_file)
			if path.exists('allScreens/ev/' + self.myAtileHD_ev.value):
				symlink('allScreens/ev/' + self.myAtileHD_ev.value, self.user_ev_file)
			#emcsel
			if path.exists(self.user_emcsel_file):
				remove(self.user_emcsel_file)
			elif path.islink(self.user_emcsel_file):
				remove(self.user_emcsel_file)
			if path.exists('allScreens/emcsel/' + self.myAtileHD_emcsel.value):
				symlink('allScreens/emcsel/' + self.myAtileHD_emcsel.value, self.user_emcsel_file)
			#movsel
			if path.exists(self.user_movsel_file):
				remove(self.user_movsel_file)
			elif path.islink(self.user_movsel_file):
				remove(self.user_movsel_file)
			if path.exists('allScreens/movsel/' + self.myAtileHD_movsel.value):
				symlink('allScreens/movsel/' + self.myAtileHD_movsel.value, self.user_movsel_file)
			#ul
			if path.exists(self.user_volume_file):
				remove(self.user_volume_file)
			elif path.islink(self.user_volume_file):
				remove(self.user_volume_file)
			if path.exists('allScreens/volume/' + self.myAtileHD_volume.value):
				symlink('allScreens/volume/' + self.myAtileHD_volume.value, self.user_volume_file)
			#COLORS
			if path.exists(self.color_file):
				remove(self.color_file)
			elif path.islink(self.color_file):
				remove(self.color_file)
			if path.exists("allScreens/colors/" + self.myAtileHD_color.value):
				symlink("allScreens/colors/" + self.myAtileHD_color.value, self.color_file)
			#SCREENS
			if self.myAtileHD_active.value:
				if not path.exists("mySkin") and path.exists("AtileHD_Selections"):
					try:
						symlink("AtileHD_Selections","mySkin")
					except:
						printDEBUG("[AtileHD:keyOK]symlinking myskin exception")
						with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
						destPath = path.join(self.skin_base_dir , "mySkin")
						sourcePath = path.join(self.skin_base_dir , "AtileHD_Selections")
						system("rm -rf %s;ln -sf %s %s" % (destPath , sourcePath ,destPath) )
			else:
				if path.exists("mySkin"):
					if path.exists("AtileHD_Selections"):
						if path.islink("mySkin"):
							remove("mySkin")
						else:
							shutil.rmtree("mySkin")
					else:
						rename("mySkin", "AtileHD_Selections")

			self.update_user_skin()
			self.restartGUI()
		else:
			if self.changed_screens:
				self.update_user_skin()
				self.restartGUI()
			else:
				self.close()

	def openSkinSelector(self):
		self.session.openWithCallback(self.skinChanged, SkinSelector)

	def openSkinSelectorDelayed(self):
		self.delaytimer = eTimer()
		self.delaytimer.callback.append(self.openSkinSelector)
		self.delaytimer.start(200, True)

	def skinChanged(self, ret = None):
		global cur_skin
		cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')
		if cur_skin == "skin.xml":
			self.restartGUI()
		else:
#			self.getInitConfig()
			self.createConfigList()

	def AtileHDBScreesnCB(self):
		self.changed_screens = True
		self["config"].setCurrentIndex(0)

	def restartGUI(self):
		myMessage = ''
		if self.LackOfFile != '':
			printDEBUG("missing components: %s" % self.LackOfFile)
			myMessage += _("Missing components found: %s\n\n") % self.LackOfFile
			myMessage += _("Skin will NOT work properly!!!\n\n")
		myMessage += _("Restart necessary, restart GUI now?")
		restartbox = self.session.openWithCallback(self.restartGUIcb,MessageBox, myMessage, MessageBox.TYPE_YESNO, default = False)
		restartbox.setTitle(_("Message"))

	def keyBlue(self):
		import xml.etree.cElementTree as ET
		from Screens.VirtualKeyBoard import VirtualKeyBoard

		def SaveScreen(ScreenFileName = None):
			if ScreenFileName is not None:
				if not ScreenFileName.endswith('.xml'):
					ScreenFileName += '.xml'
				if not ScreenFileName.startswith('skin_'):
					ScreenFileName = 'skin_' + ScreenFileName
				printDEBUG("Writing %s%s/%s" % (SkinPath, 'allScreens',ScreenFileName))

				for skinScreen in root.findall('screen'):
					if 'name' in skinScreen.attrib:
						if skinScreen.attrib['name'] == self.ScreenSelectedToExport:
							SkinContent = ET.tostring(skinScreen)
							break
				with open("%s%s/%s" % (SkinPath, 'allScreens', ScreenFileName), "w") as f:
					f.write('<skin>\n')
					f.write(SkinContent)
					f.write('</skin>\n')

		def ScreenSelected(ret):
			if ret:
				self.ScreenSelectedToExport = ret[0]
				printDEBUG('Selected: %s' % self.ScreenSelectedToExport)
				self.session.openWithCallback(SaveScreen, VirtualKeyBoard, title=(_("Enter filename")), text = self.ScreenSelectedToExport + '_new')

		ScreensList= []
		root = ET.parse(SkinPath + 'skin.xml').getroot()
		for skinScreen in root.findall('screen'):
			if 'name' in skinScreen.attrib:
				printDEBUG('Found in skin.xml: %s' % skinScreen.attrib['name'])
				ScreensList.append((skinScreen.attrib['name'],skinScreen.attrib['name']))
		if len(ScreensList) > 0:
			ScreensList.sort()
			self.session.openWithCallback(ScreenSelected, ChoiceBox, title = _("Select skin to export:"), list = ScreensList)

	def restartGUIcb(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def update_user_skin(self):
		if self.isVTI == True:
			return
		user_skin_file=resolveFilename(SCOPE_CONFIG, 'skin_user' + self.currentSkin + '.xml')
		if path.exists(user_skin_file):
			remove(user_skin_file)
		if self.myAtileHD_active.value:
                        printDEBUG("update_user_skin.self.myAtileHD_active.value")
                        user_skin = ""
                        if path.exists(self.skin_base_dir + 'skin_user_center.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_center.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_sb.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_sb.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_frame.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_frame.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_lines.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_lines.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_sbar.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_sbar.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_wget.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_wget.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_infobar.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_infobar.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_sib.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_sib.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_ch_se.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_ch_se.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_ev.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_ev.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_emcsel.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_emcsel.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_movsel.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_movsel.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_volume.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_volume.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_colors.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_colors.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_window.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_window.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'mySkin'):
                                for f in listdir(self.skin_base_dir + "mySkin/"):
                                        user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
                        if user_skin != '':
                                user_skin = "<skin>\n" + user_skin
                                user_skin = user_skin + "</skin>\n"
                                with open (user_skin_file, "w") as myFile:
                                        printDEBUG("update_user_skin.self.myAtileHD_active.value write myFile")
                                        myFile.write(user_skin)
                                        myFile.flush()
                                        myFile.close()
                        #checking if all renderers are in system
                        self.checkComponent(user_skin, 'render' , resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
                        self.checkComponent(user_skin, 'pixmap' , resolveFilename(SCOPE_SKIN, '') )

	def checkComponent(self, myContent, look4Component , myPath): #look4Component=render|
		def updateLackOfFile(name, mySeparator =', '):
			printDEBUG("Missing component found:%s\n" % name)
			if self.LackOfFile == '':
				self.LackOfFile = name
			else:
                                self.LackOfFile += mySeparator + name

		r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component , myContent )
		r=list(set(r)) #remove duplicates, no need to check for the same component several times

		printDEBUG("Found %s:\n" % (look4Component))
		print r
		if r:
			for myComponent in set(r):
				#print" [Ultimate] checks if %s exists" % myComponent
				if look4Component == 'pixmap':
					#printDEBUG("%s\n%s\n" % (myComponent,myPath + myComponent))
					if myComponent.startswith('/'):
						if not path.exists(myComponent):
							updateLackOfFile(myComponent, '\n')
					else:
						if not path.exists(myPath + myComponent):
							updateLackOfFile(myComponent)
				else:
					if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py"):
						updateLackOfFile(myComponent)
		return

	def readXMLfile(self, XMLfilename, XMLsection):
		myPath=path.realpath(XMLfilename)
		if not path.exists(myPath):
			remove(XMLfilename)
			return ''
		filecontent = ''
		if XMLsection == 'ALLSECTIONS':
			sectionmarker = True
		else:
			sectionmarker = False
		with open (XMLfilename, "r") as myFile:
			for line in myFile:
				if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
					continue
				if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
					sectionmarker = True
				elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
					sectionmarker = False
					filecontent = filecontent + line
				if sectionmarker == True:
					filecontent = filecontent + line
			myFile.close()
		return filecontent
	def opdtext(self):
		self['lab11'].show()
		self['lab12'].show()
		self['lab13'].show()


	def about(self):
		self.session.open(AtileHDB_About)

class AtileHDB_About(Screen):
	skin = '\n\t<screen position="150,150" size="420,310" title="AtileHD About">\n\t\t<widget name="lab1" position="530,20" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="180,20" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab3" position="1227,880" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab4" position="1225,961" size="100,30" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab5" position="10,332" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab6" position="10,605" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab7" position="10,288" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab8" position="12,560" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab9" position="10,875" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab10" position="10,922" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		self['lab1'] = Label(_('Settings MSN-Wetter'))
		self['lab2'] = Label(_('Skin for OPD Images by stein17'))
		self['lab3'] = Label(_('Extensions/Weather information/Menu, then add green. When you have entered the place, down to location code. Find yellow for code, confirm with green (OK), important again OK. More importantly with red back, otherwise you have to start all over again. Exit now with Exit, Restart user interface, possibly complete restart..'))
		self['lab4'] = Label(_('Menu/ Settings/ Operation and surface/ OSD, *2nd infobar*  on *2nd Infobar INFO* to adjust. Cover the information bag with Event View: Menu/ Settings/ Operation and surface/ Hotkey-Settings/Info Press button,EPG choose, in EPG *Show shipment details* choose. The entry that exists, deactivate by clicking the OK button.'))
		self['lab5'] = Label(_('Settings 2te Infobar With 2x Ok call, Show EventView using the info button'))
		self['lab6'] = Label(_('Skin information'))
		self['lab7'] = Label(_(''))
		self['lab8'] = Label(_(''))
		self['lab9'] = Label(_(''))
		self['lab10'] = Label(_(''))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.keyOk,
			}, -2)
		self.onLayoutFinish.append(self.opdtext)

	def opdtext(self):
		self['lab1'].show()
		self['lab2'].show()
		self['lab3'].show()
		self['lab4'].show()
		self['lab5'].show()
		self['lab6'].show()
		self['lab7'].show()
		self['lab8'].show()
		self['lab9'].show()
		self['lab10'].show()

	def keyOk(self):
		self.close()

	def cancel(self):
		self.close()

class AtileHDBScreens(Screen):
	skin = """
		<screen name="AtileHDBScreens" position="center,center" size="1280,720" title="AtileHD Setup">
			<widget source="Title" render="Label" position="70,47" size="950,43" font="Regular;35" transparent="1" />
			<widget source="menu" render="Listbox" position="70,115" size="700,480" scrollbarMode="showOnDemand" scrollbarWidth="6" scrollbarSliderBorderWidth="1" enableWrapAround="1" transparent="1">
				<convert type="TemplatedMultiContent">
					{"template":
						[
							MultiContentEntryPixmapAlphaTest(pos = (2, 2), size = (54, 54), png = 3),
							MultiContentEntryText(pos = (60, 2), size = (500, 22), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1), # name
							MultiContentEntryText(pos = (55, 24),size = (500, 32), font=1, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2), # info
						],
						"fonts": [gFont("Regular", 22),gFont("Regular", 16)],
						"itemHeight": 60
					}
				</convert>
			</widget>
			<widget name="Picture" position="808,342" size="400,225" alphatest="on" />
			<eLabel position=" 55,675" size="290, 5" zPosition="-10" backgroundColor="red" />
			<eLabel position="350,675" size="290, 5" zPosition="-10" backgroundColor="green" />
			<widget source="key_red" render="Label" position="70,635" size="260,25" zPosition="1" font="Regular;20" halign="left" transparent="1" />
			<widget source="key_green" render="Label" position="365,635" size="260,25" zPosition="1" font="Regular;20" halign="left" transparent="1" />
		</screen>
	"""

	allScreensGroups = [(_("All skins"), "_"),
			(_("ChannelList skins"), "channelselection"),
			(_("Infobar skins"), "infobar"),
			]

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		myTitle=_("Ultimate %s - additional screens") %  AtileHDInfo
		self.setTitle(myTitle)
		try:
                        self["title"]=StaticText(myTitle)
		except:
			pass

		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText(_("on"))

		self["Picture"] = Pixmap()

		menu_list = []
		self["menu"] = List(menu_list)

		self.allScreensGroup = self.allScreensGroups[0][1]

		self["shortcuts"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
		{
			"ok": self.runMenuEntry,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.runMenuEntry,
		}, -2)

		self.currentSkin = CurrentSkinName
		self.skin_base_dir = SkinPath
		#self.screen_dir = "allScreens"
		self.allScreens_dir = "allScreens"
		self.file_dir = "AtileHD_Selections"
		if path.exists("%sAtileHDpics/lock_on.png" % SkinPath):
			printDEBUG("SkinConfig is loading %sAtileHDpics/lock_on.png" % SkinPath)
			self.enabled_pic = LoadPixmap(cached=True, path="%sAtileHDpics/lock_on.png" % SkinPath)
		else:
			self.enabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/AtileHD/pic/lock_on.png"))
		#check if we have preview files
		isPreview=0
		for xpreview in listdir(self.skin_base_dir + "preview/"):
			if len(xpreview) > 4 and  xpreview[-4:] == ".png":
				isPreview += 1
			if isPreview >= 2:
				break
		if self.currentSkin == "Ultimate" and isPreview < 2:
			printDEBUG("no preview files :(")
			if path.exists("%sAtileHDpics/lock_on.png" % SkinPath):
				printDEBUG("SkinConfig is loading %sAtileHDpics/opkg.png" % SkinPath)
				self.disabled_pic = LoadPixmap(cached=True, path="%sAtileHDpics/opkg.png" % SkinPath)
			else:
				self.disabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/AtileHD/pic/opkg.png"))
			self['key_blue'].setText(_('Install from OPKG'))
		else:
			if path.exists("%sAtileHDpics/lock_on.png" % SkinPath):
				printDEBUG("SkinConfig is loading %sAtileHDpics/lock_off.png" % SkinPath)
				self.disabled_pic = LoadPixmap(cached=True, path="%sAtileHDpics/lock_off.png" % SkinPath)
			else:
				self.disabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/AtileHD/pic/lock_off.png"))

		if not self.selectionChanged in self["menu"].onSelectionChanged:
			self["menu"].onSelectionChanged.append(self.selectionChanged)

		self.onLayoutFinish.append(self.createMenuList)

	def selectionChanged(self):
		sel = self["menu"].getCurrent()
		if sel is not None:
			self.setPicture(sel[0])
			if sel[2] == self.enabled_pic:
				self["key_green"].setText(_("off"))
			elif sel[2] == self.disabled_pic:
				self["key_green"].setText(_("on"))

	def createMenuList(self):
		chdir(self.skin_base_dir)
		f_list = []
		if path.exists(self.skin_base_dir + self.allScreens_dir):
			list_dir = sorted(listdir(self.skin_base_dir + self.allScreens_dir), key=str.lower)
			for f in list_dir:
				if f.endswith('.xml') and f.startswith('skin_') and f.lower().find(self.allScreensGroup) > 0:
					friendly_name = f.replace("skin_", "")
					friendly_name = friendly_name.replace(".xml", "")
					friendly_name = friendly_name.replace("_", " ")
					linked_file = self.skin_base_dir + self.file_dir + "/" + f
					if path.exists(linked_file):
						if path.islink(linked_file):
							pic = self.enabled_pic
						else:
							remove(linked_file)
							symlink(self.skin_base_dir + self.allScreens_dir + "/" + f, self.skin_base_dir + self.file_dir + "/" + f)
							pic = self.enabled_pic
					else:
						pic = self.disabled_pic
					f_list.append((f, friendly_name, pic))
		menu_list = [ ]
		for entry in f_list:
			menu_list.append((entry[0], entry[1], entry[2]))
		self["menu"].updateList(menu_list)
		self.selectionChanged()

	def setPicture(self, f):
		pic = f[:-4]
		if path.exists(self.skin_base_dir + "preview/preview_" + pic + '.png'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/preview_" + pic + '.png')
		elif path.exists(self.skin_base_dir + "preview/preview_" + pic + '.jpg'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/preview_" + pic + '.jpg')
		elif path.exists(self.skin_base_dir + "preview/" + pic + '.png'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/" + pic + '.png')
		elif path.exists(self.skin_base_dir + "preview/" + pic + '.jpg'):
			self.UpdatePreviewPicture(self.skin_base_dir + "preview/" + pic + '.jpg')
		else:
			self["Picture"].hide()

	def UpdatePreviewPicture(self, PreviewFileName):
		self["Picture"].instance.setScale(1)
		self["Picture"].instance.setPixmap(LoadPixmap(path=PreviewFileName))
		self["Picture"].show()

	def keyCancel(self):
		self.close()

	def runMenuEntry(self):
		sel = self["menu"].getCurrent()
		if sel[2] == self.enabled_pic:
			remove(self.skin_base_dir + self.file_dir + "/" + sel[0])
		elif sel[2] == self.disabled_pic:
			symlink(self.skin_base_dir + self.allScreens_dir + "/" + sel[0], self.skin_base_dir + self.file_dir + "/" + sel[0])
		self.createMenuList()

