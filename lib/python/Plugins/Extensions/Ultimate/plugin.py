# -*- coding: utf-8 -*-

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from enigma import eTimer
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigSelection, ConfigYesNo, NoSave, ConfigNothing, ConfigNumber
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.SkinSelector import SkinSelector
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import *
from Tools.LoadPixmap import LoadPixmap
from Plugins.Extensions.WeatherPlugin.setup import MSNWeatherPluginEntriesListConfigScreen
from Tools import Notifications
from os import listdir, remove, rename, system, path, symlink, chdir, makedirs, mkdir
import shutil
cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')

# Atile
config.plugins.AtileHDB = ConfigSubsection()

def Plugins(**kwargs):
	return [PluginDescriptor(name=_("%s Setup") % cur_skin, description=_("Personalize your Skin"), where = PluginDescriptor.WHERE_MENU, icon="plugin.png", fnc=menu)]

def menu(menuid, **kwargs):
	if menuid == "mainmenu" and not config.skin.primary_skin.value == "Multibox/skin.xml":
		return [(_("Setup - %s") % cur_skin, main, "atilehdb_setup", None)]
	else:
		pass
	return [ ]

def main(session, **kwargs):
	print "[%s]: Config ..." % cur_skin
	session.open(AtileHDB_Config)

def isInteger(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False


class AtileHDB_Config(Screen, ConfigListScreen):

	skin = """
		<screen name="AtileHDB_Config" position="center,center" size="1280,720" title="AtileHD Setup" >
			<widget source="Title" render="Label" position="70,47" size="950,43" font="Regular;35" transparent="1" />
			<widget name="config" position="70,115" size="700,480" scrollbarMode="showOnDemand" scrollbarWidth="6" transparent="1" />
			<widget name="Picture" position="808,342" size="400,225" alphatest="on" />
			<eLabel position=" 55,675" size="290, 5" zPosition="-10" backgroundColor="red" />
			<eLabel position="350,675" size="290, 5" zPosition="-10" backgroundColor="green" />
			<eLabel position="645,675" size="290, 5" zPosition="-10" backgroundColor="yellow" />
			<eLabel position="940,675" size="290, 5" zPosition="-10" backgroundColor="blue" />
			<widget name="key_red" position="70,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="foreground" transparent="1" />
			<widget name="key_green" position="365,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="foreground" transparent="1" />
			<widget name="key_yellow" position="660,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="foreground" transparent="1" />
			<widget name="key_blue" position="955,635" size="260,25" zPosition="0" font="Regular;20" halign="left" foregroundColor="foreground" transparent="1" />
		</screen>
	"""

	def __init__(self, session, args = 0):
		self.session = session
		self.skin_lines = []
		self.changed_screens = False
		Screen.__init__(self, session)
		self['lab11'] = Label(_('press yellow button to select SkinParts'))
		self['lab12'] = Label(_('Weather Setup .... Press Menu Button to get to the weather plugin'))
		self['lab13'] = Label(_('Help, Skin settings(Weather, Own user logo )'))
		self.start_skin = config.skin.primary_skin.value

		if self.start_skin != "skin.xml":
			self.getInitConfig()
		
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)

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

		if self.start_skin == "skin.xml":
			self.onLayoutFinish.append(self.openSkinSelectorDelayed)
		else:
			self.createConfigList()

	def getInitConfig(self):
		global cur_skin
		self.is_atile = False
		if cur_skin == 'AtileHDB':
			self.is_atile = True
		self.title = _("%s - Setup") % cur_skin
		self.skin_base_dir = "/usr/share/enigma2/%s/" % cur_skin
		if self.is_atile:
			self.default_font_file = "font_atile_Roboto.xml"
			self.default_color_file = "colors_atile_Grey_transparent.xml"
		else:
			self.default_center_file = "center_Original.xml"
			self.default_color_file = "colors_Original.xml"
		self.default_infobar_file = "infobar_Original.xml"
		self.default_sib_file = "sib_Original.xml"
		self.default_ch_se_file = "ch_se_Original.xml"
		self.default_ev_file = "ev_Original.xml"
		self.default_sb_file = "sb_Original.xml"
		self.default_frame_file = "frame_Original.xml"
		self.default_lines_file = "lines_Original.xml"
		self.default_sbar_file = "sbar_Original.xml"
		self.default_wget_file = "wget_Original.xml"
		self.default_emcsel_file = "emcsel_Original.xml"
		self.default_volume_file = "volume_Original.xml"
		self.default_movsel_file = "movsel_Original.xml"

		self.color_file = "skin_user_colors.xml"
		self.center_file = "skin_user_center.xml"
		self.infobar_file = "skin_user_infobar.xml"
		self.sib_file = "skin_user_sib.xml"
		self.ch_se_file = "skin_user_ch_se.xml"
		self.ev_file = "skin_user_ev.xml"
		self.sb_file = "skin_user_sb.xml"
		self.frame_file = "skin_user_frame.xml"
		self.lines_file = "skin_user_lines.xml"
		self.sbar_file = "skin_user_sbar.xml"
		self.wget_file = "skin_user_wget.xml"
		self.emcsel_file = "skin_user_emcsel.xml"
		self.volume_file = "skin_user_volume.xml"
		self.movsel_file = "skin_user_movsel.xml"

		# color
		current, choices = self.getSettings(self.default_color_file, self.color_file)
		self.myAtileHDB_color = NoSave(ConfigSelection(default=current, choices = choices))
		# center
		current, choices = self.getSettings(self.default_center_file, self.center_file)
		self.myAtileHDB_center = NoSave(ConfigSelection(default=current, choices = choices))
		# infobar
		current, choices = self.getSettings(self.default_infobar_file, self.infobar_file)
		self.myAtileHDB_infobar = NoSave(ConfigSelection(default=current, choices = choices))
		# sib
		current, choices = self.getSettings(self.default_sib_file, self.sib_file)
		self.myAtileHDB_sib = NoSave(ConfigSelection(default=current, choices = choices))
		# ch_se
		current, choices = self.getSettings(self.default_ch_se_file, self.ch_se_file)
		self.myAtileHDB_ch_se = NoSave(ConfigSelection(default=current, choices = choices))
		# ev
		current, choices = self.getSettings(self.default_ev_file, self.ev_file)
		self.myAtileHDB_ev = NoSave(ConfigSelection(default=current, choices = choices))
		# sb
		current, choices = self.getSettings(self.default_sb_file, self.sb_file)
		self.myAtileHDB_sb = NoSave(ConfigSelection(default=current, choices = choices))
		# frame
		current, choices = self.getSettings(self.default_frame_file, self.frame_file)
		self.myAtileHDB_frame = NoSave(ConfigSelection(default=current, choices = choices))
		# lines
		current, choices = self.getSettings(self.default_lines_file, self.lines_file)
		self.myAtileHDB_lines = NoSave(ConfigSelection(default=current, choices = choices))
		# sbar
		current, choices = self.getSettings(self.default_sbar_file, self.sbar_file)
		self.myAtileHDB_sbar = NoSave(ConfigSelection(default=current, choices = choices))
		# wget
		current, choices = self.getSettings(self.default_wget_file, self.wget_file)
		self.myAtileHDB_wget = NoSave(ConfigSelection(default=current, choices = choices))
		# emcsel
		current, choices = self.getSettings(self.default_emcsel_file, self.emcsel_file)
		self.myAtileHDB_emcsel = NoSave(ConfigSelection(default=current, choices = choices))
		# volume
		current, choices = self.getSettings(self.default_volume_file, self.volume_file)
		self.myAtileHDB_volume = NoSave(ConfigSelection(default=current, choices = choices))
		# movsel
		current, choices = self.getSettings(self.default_movsel_file, self.movsel_file)
		self.myAtileHDB_movsel = NoSave(ConfigSelection(default=current, choices = choices))
		# myatile
		myatile_active = self.getmyAtileState()
		self.myAtileHDB_active = NoSave(ConfigYesNo(default=myatile_active))
		self.myAtileHDB_fake_entry = NoSave(ConfigNothing())

	def getSettings(self, default_file, user_file):
		# default setting
		default = ("default", _("Default"))

		# search typ
		styp = default_file.replace('_Original.xml','')
		if self.is_atile:
			search_str = '%s_atile_' %styp
		else:
			search_str = '%s_' %styp

		# possible setting
		choices = []
		files = listdir(self.skin_base_dir)
		if path.exists(self.skin_base_dir + 'allScreens/%s/' %styp):
			files += listdir(self.skin_base_dir + 'allScreens/%s/' %styp)
		for f in sorted(files, key=str.lower):
			if f.endswith('.xml') and f.startswith(search_str):
				friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
				if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp,f)):
					choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp,f), friendly_name))
				else:
					choices.append((self.skin_base_dir + f, friendly_name))
		choices.append(default)

		# current setting
		myfile = self.skin_base_dir + user_file
		current = ''
		if not path.exists(myfile):
			if path.exists(self.skin_base_dir + default_file):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink(default_file, user_file)
			elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file)):
				if path.islink(myfile):
					remove(myfile)
				chdir(self.skin_base_dir)
				symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
			else:
				current = None
		if current is None:
			current = default
		else:
			filename = path.realpath(myfile)
			friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
			current = (filename, friendly_name)

		return current[0], choices

	def createConfigList(self):
		self.set_color = getConfigListEntry(_("Style:"), self.myAtileHDB_color)
		self.set_center = getConfigListEntry(_("Center:"), self.myAtileHDB_center)
		self.set_sb = getConfigListEntry(_("ColorSelectedBackground:"), self.myAtileHDB_sb)
		self.set_infobar = getConfigListEntry(_("Infobar:"), self.myAtileHDB_infobar)
		self.set_sib = getConfigListEntry(_("Secondinfobar:"), self.myAtileHDB_sib)
		self.set_ch_se = getConfigListEntry(_("Channelselection:"), self.myAtileHDB_ch_se)
		self.set_ev = getConfigListEntry(_("Eventview:"), self.myAtileHDB_ev)
		self.set_frame = getConfigListEntry(_("Frame:"), self.myAtileHDB_frame)
		self.set_lines = getConfigListEntry(_("Lines:"), self.myAtileHDB_lines)
		self.set_sbar = getConfigListEntry(_("Scrollbar:"), self.myAtileHDB_sbar)
		self.set_wget = getConfigListEntry(_("Clock_Widget:"), self.myAtileHDB_wget)
		self.set_emcsel = getConfigListEntry(_("EMC_Selection:"), self.myAtileHDB_emcsel)
		self.set_volume = getConfigListEntry(_("Volume:"), self.myAtileHDB_volume)
		self.set_movsel = getConfigListEntry(_("Movie_Selection:"), self.myAtileHDB_movsel)
		self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.myAtileHDB_active)
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
		#if not config.skin.primary_skin.value == "oDreamy-FHD/skin.xml":
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		if self.myAtileHDB_active.value:
			self["key_yellow"].setText("%s pro" % cur_skin)
		else:
			self["key_yellow"].setText("")
	def config(self):
		self.session.open(MSNWeatherPluginEntriesListConfigScreen)


	def changedEntry(self):
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHDB_color.value)
		elif self["config"].getCurrent() == self.set_center:
			self.setPicture(self.myAtileHDB_center.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHDB_infobar.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHDB_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHDB_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHDB_ev.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHDB_sb.value)
		elif self["config"].getCurrent() == self.set_frame:
			self.setPicture(self.myAtileHDB_frame.value)
		elif self["config"].getCurrent() == self.set_lines:
			self.setPicture(self.myAtileHDB_lines.value)
		elif self["config"].getCurrent() == self.set_sbar:
			self.setPicture(self.myAtileHDB_sbar.value)
		elif self["config"].getCurrent() == self.set_wget:
			self.setPicture(self.myAtileHDB_wget.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHDB_emcsel.value)
		elif self["config"].getCurrent() == self.set_volume:
			self.setPicture(self.myAtileHDB_volume.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHDB_movsel.value)
		elif self["config"].getCurrent() == self.set_myatile:
			if self.myAtileHDB_active.value:
				self["key_yellow"].setText("%s pro" % cur_skin)
			else:
				self["key_yellow"].setText("")

	def selectionChanged(self):
		if self["config"].getCurrent() == self.set_color:
			self.setPicture(self.myAtileHDB_color.value)
		elif self["config"].getCurrent() == self.set_center:
			self.setPicture(self.myAtileHDB_center.value)
		elif self["config"].getCurrent() == self.set_infobar:
			self.setPicture(self.myAtileHDB_infobar.value)
		elif self["config"].getCurrent() == self.set_sib:
			self.setPicture(self.myAtileHDB_sib.value)
		elif self["config"].getCurrent() == self.set_ch_se:
			self.setPicture(self.myAtileHDB_ch_se.value)
		elif self["config"].getCurrent() == self.set_ev:
			self.setPicture(self.myAtileHDB_ev.value)
		elif self["config"].getCurrent() == self.set_sb:
			self.setPicture(self.myAtileHDB_sb.value)
		elif self["config"].getCurrent() == self.set_frame:
			self.setPicture(self.myAtileHDB_frame.value)
		elif self["config"].getCurrent() == self.set_lines:
			self.setPicture(self.myAtileHDB_lines.value)
		elif self["config"].getCurrent() == self.set_sbar:
			self.setPicture(self.myAtileHDB_sbar.value)
		elif self["config"].getCurrent() == self.set_wget:
			self.setPicture(self.myAtileHDB_wget.value)
		elif self["config"].getCurrent() == self.set_emcsel:
			self.setPicture(self.myAtileHDB_emcsel.value)
		elif self["config"].getCurrent() == self.set_volume:
			self.setPicture(self.myAtileHDB_volume.value)
		elif self["config"].getCurrent() == self.set_movsel:
			self.setPicture(self.myAtileHDB_movsel.value)
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
			print "[%s]: Cancel confirmed." % cur_skin
		else:
			print "[%s]: Cancel confirmed. Config changes will be lost." % cur_skin
			for x in self["config"].list:
				x[1].cancel()
			self.close()

	def getmyAtileState(self):
		chdir(self.skin_base_dir)
		if path.exists("mySkin"):
			return True
		else:
			return False

	def setPicture(self, f):
		pic = f.split('/')[-1].replace(".xml", ".png")
		preview = self.skin_base_dir + "preview/preview_" + pic
		if path.exists(preview):
			self["Picture"].instance.setPixmapFromFile(preview)
			self["Picture"].show()
		else:
			self["Picture"].hide()

	def keyYellow(self):
		if self.myAtileHDB_active.value:
			self.session.openWithCallback(self.AtileHDBScreenCB, AtileHDBScreens)
		else:
			self["config"].setCurrentIndex(0)

	def keyOk(self):
		sel =  self["config"].getCurrent()
		if sel is not None and sel == self.set_new_skin:
			self.openSkinSelector()
		else:
			self.keyGreen()

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
			self.getInitConfig()
			self.createConfigList()

	def keyGreen(self):
		if self["config"].isChanged():
			for x in self["config"].list:
				x[1].save()
			chdir(self.skin_base_dir)

			# color
			self.makeSettings(self.myAtileHDB_color, self.color_file)
			# background
			self.makeSettings(self.myAtileHDB_center, self.center_file)
			# infobar
			self.makeSettings(self.myAtileHDB_infobar, self.infobar_file)
			# sib
			self.makeSettings(self.myAtileHDB_sib, self.sib_file)
			# ch_se
			self.makeSettings(self.myAtileHDB_ch_se, self.ch_se_file)
			# ev
			self.makeSettings(self.myAtileHDB_ev, self.ev_file)
			# sb
			self.makeSettings(self.myAtileHDB_sb, self.sb_file)
			# frame
			self.makeSettings(self.myAtileHDB_frame, self.frame_file)
			# lines
			self.makeSettings(self.myAtileHDB_lines, self.lines_file)
			# sbar
			self.makeSettings(self.myAtileHDB_sbar, self.sbar_file)
			# wget
			self.makeSettings(self.myAtileHDB_wget, self.wget_file)
			# emcsel
			self.makeSettings(self.myAtileHDB_emcsel, self.emcsel_file)
			# volume
			self.makeSettings(self.myAtileHDB_volume, self.volume_file)
			# movsel
			self.makeSettings(self.myAtileHDB_movsel, self.movsel_file)

			if not path.exists("mySkin_off"):
				mkdir("mySkin_off")
				print "makedir mySkin_off"
			if self.myAtileHDB_active.value:
				if not path.exists("mySkin") and path.exists("mySkin_off"):
						symlink("mySkin_off","mySkin")
			else:
				if path.exists("mySkin"):
					if path.exists("mySkin_off"):
						if path.islink("mySkin"):
							remove("mySkin")
						else:
							shutil.rmtree("mySkin")
					else:
						rename("mySkin", "mySkin_off")
			self.restartGUI()
		elif  config.skin.primary_skin.value != self.start_skin:
			self.restartGUI()
		else:
			if self.changed_screens:
				self.restartGUI()
			else:
				self.close()

	def makeSettings(self, config_entry, user_file):
		if path.exists(user_file) or path.islink(user_file):
			remove(user_file)
		if config_entry.value != 'default':
			symlink(config_entry.value, user_file)

	def AtileHDBScreenCB(self):
		self.changed_screens = True
		self["config"].setCurrentIndex(0)

	def restartGUI(self):
		restartbox = self.session.openWithCallback(self.restartGUIcb,MessageBox,_("Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Message"))

	def about(self):
		self.session.open(AtileHDB_About)

	def opdtext(self):
		self['lab11'].show()
		self['lab12'].show()
		self['lab13'].show()

	def restartGUIcb(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

class AtileHDB_About(Screen):
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

class AtileHDBScreens(Screen):

	skin = """
		<screen name="AtileHDBScreens" position="center,center" size="1280,720" title="AtileHD Setup">
			<widget source="Title" render="Label" position="70,47" size="950,43" font="Regular;35" transparent="1" />
			<widget source="menu" render="Listbox" position="70,115" size="700,480" scrollbarMode="showOnDemand" scrollbarWidth="6" scrollbarSliderBorderWidth="1" enableWrapAround="1" transparent="1">
				<convert type="TemplatedMultiContent">
					{"template":
						[
							MultiContentEntryPixmapAlphaTest(pos = (2, 2), size = (25, 24), png = 2),
							MultiContentEntryText(pos = (35, 4), size = (500, 24), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
						],
						"fonts": [gFont("Regular", 22),gFont("Regular", 16)],
						"itemHeight": 30
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

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		
		global cur_skin
		self.is_atile = False
		if cur_skin == 'AtileHDB':
			self.is_atile = True

		self.title = _("%s additional screens") % cur_skin
		try:
			self["title"]=StaticText(self.title)
		except:
			print 'self["title"] was not found in skin'
		
		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText(_("on"))
		
		self["Picture"] = Pixmap()
		
		menu_list = []
		self["menu"] = List(menu_list)
		
		self["shortcuts"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
		{
			"ok": self.runMenuEntry,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.runMenuEntry,
		}, -2)
		
		self.skin_base_dir = "/usr/share/enigma2/%s/" % cur_skin
		self.screen_dir = "allScreens"
		self.skinparts_dir = "skinparts"
		self.file_dir = "mySkin_off"
		my_path = resolveFilename(SCOPE_SKIN, "%s/icons/lock_on.png" % cur_skin)
		if not path.exists(my_path):
			my_path = resolveFilename(SCOPE_SKIN, "skin_default/icons/lock_on.png")
		self.enabled_pic = LoadPixmap(cached = True, path = my_path)
		my_path = resolveFilename(SCOPE_SKIN, "%s/icons/lock_off.png" % cur_skin)
		if not path.exists(my_path):
			my_path = resolveFilename(SCOPE_SKIN, "skin_default/icons/lock_off.png")
		self.disabled_pic = LoadPixmap(cached = True, path = my_path)
		
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
		dir_path = self.skin_base_dir + self.screen_dir
		if not path.exists(dir_path):
			makedirs(dir_path)
		dir_skinparts_path = self.skin_base_dir + self.skinparts_dir
		if not path.exists(dir_skinparts_path):
			makedirs(dir_skinparts_path)
		file_dir_path = self.skin_base_dir + self.file_dir
		if not path.exists(file_dir_path):
			makedirs(file_dir_path)
		dir_global_skinparts = resolveFilename(SCOPE_SKIN, "skinparts")
		if path.exists(dir_global_skinparts):
			for pack in listdir(dir_global_skinparts):
				if path.isdir(dir_global_skinparts + "/" + pack):
					for f in listdir(dir_global_skinparts + "/" + pack):
						if path.exists(dir_global_skinparts + "/" + pack + "/" + f + "/" + f + "_Atile.xml"):
							if not path.exists(dir_path + "/skin_" + f + ".xml"):
								symlink(dir_global_skinparts + "/" + pack + "/" + f + "/" + f + "_Atile.xml", dir_path + "/skin_" + f + ".xml")
							if not path.exists(dir_skinparts_path + "/" + f):
								symlink(dir_global_skinparts + "/" + pack + "/" + f, dir_skinparts_path + "/" + f)
		list_dir = sorted(listdir(dir_path), key=str.lower)
		for f in list_dir:
			if f.endswith('.xml') and f.startswith('skin_'):
				if (not path.islink(dir_path + "/" + f)) or os.path.exists(os.readlink(dir_path + "/" + f)):
					friendly_name = f.replace("skin_", "")
					friendly_name = friendly_name.replace(".xml", "")
					friendly_name = friendly_name.replace("_", " ")
					linked_file = file_dir_path + "/" + f
					if path.exists(linked_file):
						if path.islink(linked_file):
							pic = self.enabled_pic
						else:
							remove(linked_file)
							symlink(dir_path + "/" + f, file_dir_path + "/" + f)
							pic = self.enabled_pic
					else:
						pic = self.disabled_pic
					f_list.append((f, friendly_name, pic))
				else:
					if path.islink(dir_path + "/" + f):
						remove(dir_path + "/" + f)
		menu_list = [ ]
		for entry in f_list:
			menu_list.append((entry[0], entry[1], entry[2]))
		self["menu"].updateList(menu_list)
		self.selectionChanged()

	def setPicture(self, f):
		pic = f.replace(".xml", ".png")
		preview = self.skin_base_dir + "preview/preview_" + pic
		if path.exists(preview):
			self["Picture"].instance.setPixmapFromFile(preview)
			self["Picture"].show()
		else:
			self["Picture"].hide()
	
	def keyCancel(self):
		self.close()

	def runMenuEntry(self):
		sel = self["menu"].getCurrent()
		if sel is not None:
			if sel[2] == self.enabled_pic:
				remove(self.skin_base_dir + self.file_dir + "/" + sel[0])
			elif sel[2] == self.disabled_pic:
				symlink(self.skin_base_dir + self.screen_dir + "/" + sel[0], self.skin_base_dir + self.file_dir + "/" + sel[0])
			self.createMenuList()
