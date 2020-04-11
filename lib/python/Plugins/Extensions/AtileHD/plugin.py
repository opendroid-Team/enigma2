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
                if menuid == "mainmenu" and not config.skin.primary_skin.value == "Ultimate/skin.xml":
                        return [(_("Setup - %s") % CurrentSkinName, main, "atilehd_setup", None)]
                else:
                        pass
                return [ ]

def main(session, **kwargs):
        printDEBUG("Opening Menu ...")
        session.open(AtileHD_Config)

def isInteger(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False

class AtileHD_Config(Screen, ConfigListScreen):
	skin = """
	<screen name="AtileHD_Config" position="82,124" size="1101,376" title="Multibox Setup" backgroundColor="transparent" flags="wfNoBorder">
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
		self['lab11'] = Label(_('Weather Setup .... Press Menu Button to get to the weather plugin'))
		self['lab12'] = Label(_('press yellow button to select Multibox Tool'))
		self['lab13'] = Label(_('Help, Skin settings(Weather, Own user logo )'))
		myTitle=_("Multibox Setup %s") % AtileHDInfo
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
		self.user_background_file = "skin_user_background.xml"
		self.user_sb_file = "skin_user_sb.xml"
		self.user_clock_file = "skin_user_clock.xml"
		self.user_infobar_file = "skin_user_infobar.xml"
		self.user_sib_file = "skin_user_sib.xml"
		self.user_ch_se_file = "skin_user_ch_se.xml"
		self.user_ev_file = "skin_user_ev.xml"
		self.user_emcsel_file = "skin_user_emcsel.xml"
		self.user_movsel_file = "skin_user_movsel.xml"
		self.user_ul_file = "skin_user_ul.xml"

		if path.exists(self.skin_base_dir):
                        #background
			if path.exists(self.skin_base_dir + self.user_background_file):
				self.default_background_file = path.basename(path.realpath(self.skin_base_dir + self.user_background_file))
				printDEBUG("self.default_background_file = " + self.default_background_file )
			else:
				self.default_background_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/background/"):
				mkdir(self.skin_base_dir + "allScreens/background/")
                        #sb
			if path.exists(self.skin_base_dir + self.user_sb_file):
				self.default_sb_file = path.basename(path.realpath(self.skin_base_dir + self.user_sb_file))
				printDEBUG("self.default_sb_file = " + self.default_sb_file )
			else:
				self.default_sb_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/sb/"):
				mkdir(self.skin_base_dir + "allScreens/sb/")
                        #clock
			if path.exists(self.skin_base_dir + self.user_clock_file):
				self.default_clock_file = path.basename(path.realpath(self.skin_base_dir + self.user_clock_file))
				printDEBUG("self.default_clock_file = " + self.default_clock_file )
			else:
				self.default_clock_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/clock/"):
				mkdir(self.skin_base_dir + "allScreens/clock/")
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
                        #ul
			if path.exists(self.skin_base_dir + self.user_ul_file):
				self.default_ul_file = path.basename(path.realpath(self.skin_base_dir + self.user_sib_file))
				printDEBUG("self.default_ul_file = " + self.default_ul_file )
			else:
				self.default_ul_file = self.defaultOption
			if not path.exists(self.skin_base_dir + "allScreens/ul/"):
				mkdir(self.skin_base_dir + "allScreens/ul/")
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

		current_color = self.getCurrentColor()[0]
		current_background = self.getCurrentbackground()[0]
		current_sb = self.getCurrentsb()[0]
		current_clock = self.getCurrentclock()[0]
		current_infobar = self.getCurrentinfobar()[0]
		current_sib = self.getCurrentsib()[0]
		current_ch_se = self.getCurrentch_se()[0]
		current_ev = self.getCurrentev()[0]
		current_emcsel = self.getCurrentemcsel()[0]
		current_movsel = self.getCurrentmovsel()[0]
		current_ul = self.getCurrentul()[0]
		myAtileHD_active = self.getmySkinState()
		self.myAtileHD_active = NoSave(ConfigYesNo(default=myAtileHD_active))
		self.myAtileHD_background = NoSave(ConfigSelection(default=current_background, choices = self.getPossiblebackground()))
		self.myAtileHD_sb = NoSave(ConfigSelection(default=current_sb, choices = self.getPossiblesb()))
		self.myAtileHD_clock = NoSave(ConfigSelection(default=current_clock, choices = self.getPossibleclock()))
		self.myAtileHD_infobar = NoSave(ConfigSelection(default=current_infobar, choices = self.getPossibleinfobar()))
		self.myAtileHD_sib = NoSave(ConfigSelection(default=current_sib, choices = self.getPossiblesib()))
		self.myAtileHD_ch_se = NoSave(ConfigSelection(default=current_ch_se, choices = self.getPossiblech_se()))
		self.myAtileHD_ev = NoSave(ConfigSelection(default=current_ev, choices = self.getPossibleev()))
		self.myAtileHD_emcsel = NoSave(ConfigSelection(default=current_emcsel, choices = self.getPossibleemcsel()))
		self.myAtileHD_movsel = NoSave(ConfigSelection(default=current_movsel, choices = self.getPossiblemovsel()))
		self.myAtileHD_ul = NoSave(ConfigSelection(default=current_ul, choices = self.getPossibleul()))
		self.myAtileHD_style = NoSave(ConfigSelection(default=current_color, choices = self.getPossibleColor()))
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
		self.set_color = getConfigListEntry(_("Style:"), self.myAtileHD_style)
		self.set_sb = getConfigListEntry(_("ColorSelectedBackground:"), self.myAtileHD_sb)
		self.set_clock = getConfigListEntry(_("Clock:"), self.myAtileHD_clock)
		self.set_infobar = getConfigListEntry(_("Infobar:"), self.myAtileHD_infobar)
		self.set_background = getConfigListEntry(_("Background:"), self.myAtileHD_background)
		self.set_sib = getConfigListEntry(_("Secondinfobar:"), self.myAtileHD_sib)
		self.set_ch_se = getConfigListEntry(_("Channelselection:"), self.myAtileHD_ch_se)
		self.set_ev = getConfigListEntry(_("Eventview:"), self.myAtileHD_ev)
		self.set_emcsel = getConfigListEntry(_("EMC_Selection:"), self.myAtileHD_emcsel)
		self.set_movsel = getConfigListEntry(_("Movie_Selection:"), self.myAtileHD_movsel)
		self.set_ul = getConfigListEntry(_("Userlogo:"), self.myAtileHD_ul)
		self.set_myatile = getConfigListEntry(_("Enable skin personalization:"), self.myAtileHD_active)
		self.set_new_skin = getConfigListEntry(_("Change skin"), ConfigNothing())
		self.list = []
		self.list.append(self.set_myatile)
		self.list.append(self.set_color)
		self.list.append(self.set_sb)
		self.list.append(self.set_clock)
		self.list.append(self.set_infobar)
		self.list.append(self.set_background)
		self.list.append(self.set_sib)
		self.list.append(self.set_ch_se)
		self.list.append(self.set_ev)
		self.list.append(self.set_emcsel)
		self.list.append(self.set_movsel)
		self.list.append(self.set_ul)
		self.list.append(self.set_new_skin)

		self["config"].list = self.list
		self["config"].l.setList(self.list)
		if self.myAtileHD_active.value:
			self["key_yellow"].setText(_("Multibox Tool"))
		else:
			self["key_yellow"].setText("")
	def config(self):
		self.session.open(MSNWeatherPluginEntriesListConfigScreen)

	def changedEntry(self):
		self.updateEntries = True
		printDEBUG("[AtileHD:changedEntry]")
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHD_style.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHD_sb.value)
		elif self["config"].getCurrent() == self.set_clock:
			self.setPicture(self.myAtileHD_clock.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHD_infobar.value)
		elif self["config"].getCurrent() == self.set_background:
			self.setPicture(self.myAtileHD_background.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHD_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHD_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHD_ev.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHD_emcsel.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHD_movsel.value)
		elif self["config"].getCurrent() == self.set_ul:
			self.setPicture(self.myAtileHD_ul.value)
		elif self["config"].getCurrent() == self.set_myatile:
			if self.myAtileHD_active.value:
				self["key_yellow"].setText(_("Multibox Tool"))
			else:
				self["key_yellow"].setText("")

	def selectionChanged(self):
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHD_style.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHD_sb.value)
		elif self["config"].getCurrent() == self.set_clock:
			self.setPicture(self.myAtileHD_clock.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHD_infobar.value)
		elif self["config"].getCurrent() == self.set_background:
			self.setPicture(self.myAtileHD_background.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHD_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHD_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHD_ev.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHD_emcsel.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHD_movsel.value)
		elif self["config"].getCurrent() == self.set_ul:
			self.setPicture(self.myAtileHD_ul.value)
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

	def getPossibleColor(self):
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

	def getPossiblebackground(self):
		background_list = []
		background_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/background/"):
			return background_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/background/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('background_'):
				friendly_name = f.replace("background_atile_", "").replace("background_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				background_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('background_'):
				friendly_name = f.replace("background_atile_", "").replace("background_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				background_list.append((f, friendly_name))

		return background_list

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

	def getPossibleclock(self):
		clock_list = []
		clock_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/clock/"):
			return clock_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/clock/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('clock_'):
				friendly_name = f.replace("clock_atile_", "").replace("clock_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				clock_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('clock_'):
				friendly_name = f.replace("clock_atile_", "").replace("clock_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				clock_list.append((f, friendly_name))

		return clock_list

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

	def getPossibleul(self):
		ul_list = []
		ul_list.append(self.defaults)

		if not path.exists(self.skin_base_dir + "allScreens/ul/"):
			return ul_list

		for f in sorted(listdir(self.skin_base_dir + "allScreens/ul/"), key=str.lower):
			if f.endswith('.xml') and f.startswith('ul_'):
				friendly_name = f.replace("ul_atile_", "").replace("ul_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ul_list.append((f, friendly_name))

		for f in sorted(listdir(self.skin_base_dir), key=str.lower):
			if f.endswith('.xml') and f.startswith('ul_'):
				friendly_name = f.replace("ul_atile_", "").replace("ul_", "")
				friendly_name = friendly_name.replace(".xml", "")
				friendly_name = friendly_name.replace("_", " ")
				ul_list.append((f, friendly_name))

		return ul_list

	def getmySkinState(self):
		chdir(self.skin_base_dir)
		if path.exists("mySkin"):
			return True
		else:
			return False

	def getCurrentColor(self):
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

	def getCurrentbackground(self):
		myfile = self.skin_base_dir + self.user_background_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/background/" + self.default_background_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/background/" + self.default_background_file, self.user_background_file)
			else:
				return (self.default_background_file, self.default_background_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("background_atile_", "").replace("background_", "")
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

	def getCurrentclock(self):
		myfile = self.skin_base_dir + self.user_clock_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/clock/" + self.default_clock_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/clock/" + self.default_clock_file, self.user_clock_file)
			else:
				return (self.default_clock_file, self.default_clock_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("clock_atile_", "").replace("clock_", "")
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

	def getCurrentul(self):
		myfile = self.skin_base_dir + self.user_ul_file
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + "allScreens/ul/" + self.default_ul_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink("allScreens/ul/" + self.default_ul_file, self.user_ul_file)
			else:
				return (self.default_ul_file, self.default_ul_file)
		filename = path.realpath(myfile)
		filename = path.basename(filename)
		friendly_name = filename.replace("ul_atile_", "").replace("ul_", "")
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
			self.session.openWithCallback(self.AtileHDScreesnCB, AtileHDScreens)
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
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_background.value=" + self.myAtileHD_background.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_sb.value=" + self.myAtileHD_sb.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_clock.value=" + self.myAtileHD_clock.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_infobar.value=" + self.myAtileHD_infobar.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_sib.value=" + self.myAtileHD_sib.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_ch_se.value=" + self.myAtileHD_ch_se.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_ev.value=" + self.myAtileHD_ev.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_emcsel.value=" + self.myAtileHD_emcsel.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_movsel.value=" + self.myAtileHD_movsel.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_ul.value=" + self.myAtileHD_ul.value)
			printDEBUG("[AtileHD:keyOk] self.myAtileHD_style.value=" + self.myAtileHD_style.value)
			for x in self["config"].list:
				x[1].save()
			configfile.save()
			chdir(self.skin_base_dir)
			#background
			if path.exists(self.user_background_file):
				remove(self.user_background_file)
			elif path.islink(self.user_background_file):
				remove(self.user_background_file)
			if path.exists('allScreens/background/' + self.myAtileHD_background.value):
				symlink('allScreens/background/' + self.myAtileHD_background.value, self.user_background_file)
			#sb
			if path.exists(self.user_sb_file):
				remove(self.user_sb_file)
			elif path.islink(self.user_sb_file):
				remove(self.user_sb_file)
			if path.exists('allScreens/sb/' + self.myAtileHD_sb.value):
				symlink('allScreens/sb/' + self.myAtileHD_sb.value, self.user_sb_file)
			#clock
			if path.exists(self.user_clock_file):
				remove(self.user_clock_file)
			elif path.islink(self.user_clock_file):
				remove(self.user_clock_file)
			if path.exists('allScreens/clock/' + self.myAtileHD_clock.value):
				symlink('allScreens/clock/' + self.myAtileHD_clock.value, self.user_clock_file)
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
			if path.exists(self.user_ul_file):
				remove(self.user_ul_file)
			elif path.islink(self.user_ul_file):
				remove(self.user_ul_file)
			if path.exists('allScreens/ul/' + self.myAtileHD_ul.value):
				symlink('allScreens/ul/' + self.myAtileHD_ul.value, self.user_ul_file)
			#COLORS
			if path.exists(self.color_file):
				remove(self.color_file)
			elif path.islink(self.color_file):
				remove(self.color_file)
			if path.exists("allScreens/colors/" + self.myAtileHD_style.value):
				symlink("allScreens/colors/" + self.myAtileHD_style.value, self.color_file)
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

	def AtileHDScreesnCB(self):
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
                        if path.exists(self.skin_base_dir + 'skin_user_background.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_background.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_sb.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_sb.xml' , 'ALLSECTIONS')
                        if path.exists(self.skin_base_dir + 'skin_user_clock.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_clock.xml' , 'ALLSECTIONS')
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
                        if path.exists(self.skin_base_dir + 'skin_user_ul.xml'):
                                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + 'skin_user_ul.xml' , 'ALLSECTIONS')
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
				#print" [Multibox] checks if %s exists" % myComponent
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
		self.session.open(AtileHD_About)

class AtileHD_About(Screen):
	skin = '\n\t<screen position="150,150" size="420,310" title="AtileHD About">\n\t\t<widget name="lab1" position="530,20" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="180,20" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab3" position="1227,880" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab4" position="1225,961" size="100,30" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab5" position="10,332" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab6" position="10,605" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab7" position="10,288" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab8" position="12,560" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab9" position="10,875" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<widget name="lab10" position="10,922" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" transparent="1"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		self['lab1'] = Label(_('*Multibox FHD*  FHD Skin for OPD Images by stein17'))
		self['lab2'] = Label(_('Skin information'))
		self['lab3'] = Label(_('*Multibox* FHD Skin for OPD Images by stein17'))
		self['lab4'] = Label(_('Support: https://droidsat.org/forum/'))
		self['lab5'] = Label(_('In the skin there is the possibility to integrate your own user logos. The logo should not be bigger than 150x48 pixels. Scale your logo to this size and save it as User_Logo.png. Then copy the logo with FTP to usr / share / enigma2 / Multibox / Skinparts /, this will overwrite the original. Anyone who has requests regarding a user logo, can sign up in the forum. PN s are ignored.'))
		self['lab6'] = Label(_('Google DNS Server: The IP addresses of the Google service\nIP addresses for the Internet Protocol version 4 (IPv4)\nPreferred DNS server: 8.8.8.8\nAlternative DNS server: 8.8.4.4IP addresses for the Internet Protocol version 6 (IPv6)\nPreferred DNS server: 2001:4860:4860:8888\nAlternative DNS server: 2001:4860:4860:8844'))
		self['lab7'] = Label(_('Instructions User logo'))
		self['lab8'] = Label(_('If no weather is displayed, it may help to change the DNS address'))
		self['lab9'] = Label(_('DNS server fast and secure: Super fast DNS server from Cloudflare'))
		self['lab10'] = Label(_('Preferred DNSv4-Server die IP 1.1.1.1\nAlternative DNSv4-Server die IP 1.0.0.1'))
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

class AtileHDScreens(Screen):
	skin = """
		<screen name="AtileHDScreens" position="center,center" size="1280,720" title="Multibox Setup">
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

		myTitle=_("Multibox %s - additional screens") %  AtileHDInfo
		self.setTitle(myTitle)
		try:
                        self["title"]=StaticText(myTitle)
		except:
			pass

		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText("on")

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
		if self.currentSkin == "Multibox" and isPreview < 2:
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

