from GlobalActions import globalActionMap
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Button import Button
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.SystemInfo import SystemInfo
from Components.config import config, ConfigSubsection, ConfigText, ConfigYesNo
from Components.PluginComponent import plugins
from Components.Sources.StaticText import StaticText
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.BoundFunction import boundFunction
from ServiceReference import ServiceReference
from enigma import eServiceReference, eActionMap
from Components.Label import Label
from boxbranding import getHaveHDMIinHD, getHaveHDMIinFHD, getHaveCI
import os
def getButtonSetupKeys():
	return [(_("Red"), "red", "Infobar/openSingleServiceEPG"),
		(_("Red long"), "red_long", "Infobar/activateRedButton"),
		(_("Green"), "green", "Module/OPENDROID.GreenPanel/GreenPanel"),
		(_("Green long"), "green_long", "Infobar/showAutoTimerList"),
		(_("Yellow"), "yellow", "Infobar/showExtensionSelection"),
		(_("Yellow long"), "yellow_long", ""),
		(_("Blue"), "blue", "Module/OPENDROID.BluePanel/BluePanel"),
		(_("Blue long"), "blue_long", ""),
		(_("Info (EPG)"), "info", "Infobar/InfoPressed/1"),
		(_("Info (EPG) Long"), "info_long", "Infobar/showEventInfoPlugins/1"),
		(_("Epg/Guide"), "epg", "Infobar/EPGPressed/1"),
		(_("Epg/Guide long"), "epg_long", "Infobar/showEventGuidePlugins/1"),
		(_("Left"), "cross_left", ""),
		(_("Right"), "cross_right", ""),
		(_("Left long"), "cross_left_long", ""),
		(_("Right long"), "cross_right_long", "Infobar/seekFwdVod"),
		(_("Up"), "cross_up", ""),
		(_("Down"), "cross_down", ""),
		(_("PageUp"), "pageup", ""),
		(_("PageUp long"), "pageup_long", ""),
		(_("PageDown"), "pagedown", ""),
		(_("PageDown long"), "pagedown_long", ""),
		(_("Channel up"), "channelup", ""),
		(_("Channel down"), "channeldown", ""),
		(_("TV"), "showTv", "Infobar/showTv"),
		(_("Radio"), "radio", "Infobar/showRadio"),
		(_("Rec"), "rec", ""),
		(_("Rec long"), "rec_long", ""),
		(_("Teletext"), "text", ""),
		(_("Subtitle"), "subtitle", ""),
		(_("Subtitle long"), "subtitle_long", ""),
		(_("Menu"), "mainMenu", ""),
		(_("List/Fav"), "list", ""),
		(_("List/Fav long"), "list_long", ""),
		(_("PVR"), "pvr", ""),
		(_("PVR long"), "pvr_long", ""),
		(_("Favorites"), "favorites", ""),
		(_("Favorites long"), "favorites_long", ""),
		(_("File"), "file", ""),
		(_("File long"), "file_long", ""),
		(_("OK long"), "ok_long", ""),
		(_("Media"), "media", ""),
		(_("Media long"), "media_long", ""),
		(_("Open"), "open", ""),
		(_("Open long"), "open_long", ""),
		(_("Option"), "option", ""),
		(_("Option long"), "option_long", ""),
		(_("Www"), "www", ""),
		(_("Www long"), "www_long", ""),
		(_("Directory"), "directory", ""),
		(_("Directory long"), "directory_long", ""),
		(_("Back/Recall"), "back", ""),
		(_("Back/Recall") + " " + _("long"), "back_long", ""),
		(_("History"), "archive", ""),
		(_("History long"), "archive_long", ""),
		(_("Aspect"), "mode", ""),
		(_("Aspect long"), "mode_long", ""),
		(_("Home"), "home", ""),
		(_("Home long"), "home_long", ""),
		(_("End"), "end", ""),
		(_("End long"), "end_long", ""),
		(_("Next"), "next", ""),
		(_("Previous"), "previous", ""),
		(_("Audio"), "audio", ""),
		(_("Audio long"), "audio_long", ""),
		(_("Play"), "play", ""),
		(_("Playpause"), "playpause", ""),
		(_("Stop"), "stop", ""),
		(_("Pause"), "pause", ""),
		(_("Rewind"), "rewind", ""),
		(_("Fastforward"), "fastforward", ""),
		(_("Skip back"), "skip_back", ""),
		(_("Skip forward"), "skip_forward", ""),
		(_("activatePiP"), "activatePiP", ""),
		(_("Time"), "time", ""),
		(_("Time long"), "time_long", ""),
		(_("Playlist"), "playlist", ""),
		(_("Playlist long"), "playlist_long", ""),
		(_("Timeshift"), "timeshift", ""),
		(_("Search/WEB"), "search", ""),
		(_("Search/WEB long"), "search_long", ""),
		(_("Slow"), "slow", ""),
		(_("Mark/Portal/Playlist"), "mark", ""),
		(_("Mark/Portal/Playlist long"), "mark_long", ""),
		(_("Sleep"), "sleep", ""),
		(_("Sleep long"), "sleep_long", ""),
		(_("Power"), "power", ""),
		(_("Power long"), "power_long", ""),
		(_("HDMIin"), "HDMIin", "Infobar/HDMIIn"),
		(_("HDMIin") + " " + _("long"), "HDMIin_long", (SystemInfo["LcdLiveTV"] and "Infobar/ToggleLCDLiveTV") or ""),
		(_("Help"), "displayHelp", ""),
		(_("Help long"), "displayHelp_long", ""),
		(_("Context"), "contextMenu", "Infobar/showExtensionSelection"),
		(_("Context long"), "context_long", ""),
		(_("SAT"), "sat", "Infobar/openSatellites"),
		(_("SAT long"), "sat_long", ""),
		(_("F1/LAN"), "f1", "Infobar/showNetworkMounts"),
		(_("F1/LAN long"), "f1_long", ""),
		(_("F1"), "f1", ""),
		(_("F1 long"), "f1_long", ""),
		(_("F2"), "f2", ""),
		(_("F2 long"), "f2_long", ""),
		(_("F3"), "f3", ""),
		(_("F3 long"), "f3_long", ""),
		(_("F4"), "f4", ""),
		(_("F4 long"), "f4_long", ""),
		(_("PIP"), "f6", ""),
		(_("PIP long"), "f6_long", ""),
		(_("MOUSE"), "mouse", ""),
		(_("MOUSE long"), "mouse_long", ""),
		(_("VOD"), "vod", ""),
		(_("VOD long"), "vod_long", ""),
		(_("ZOOM"), "zoom", ""),
		(_("ZOOM long"), "zoom_long", "")]

config.misc.ButtonSetup = ConfigSubsection()
config.misc.ButtonSetup.additional_keys = ConfigYesNo(default=True)
for x in getButtonSetupKeys():
	exec "config.misc.ButtonSetup." + x[1] + " = ConfigText(default='" + x[2] + "')"

def getButtonSetupFunctions():
	ButtonSetupFunctions = []
	twinPlugins = []
	twinPaths = {}
	pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_EVENTINFO)
	pluginlist.sort(key=lambda p: p.name)
	for plugin in pluginlist:
		if plugin.name not in twinPlugins and plugin.path and 'selectedevent' not in plugin.__call__.func_code.co_varnames:
			if twinPaths.has_key(plugin.path[plugin.path.rfind("Plugins"):]):
				twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] += 1
			else:
				twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] = 1
			ButtonSetupFunctions.append((plugin.name, plugin.path[plugin.path.rfind("Plugins"):] + "/" + str(twinPaths[plugin.path[plugin.path.rfind("Plugins"):]]) , "EPG"))
			twinPlugins.append(plugin.name)
	pluginlist = plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_EVENTINFO])
	pluginlist.sort(key=lambda p: p.name)
	for plugin in pluginlist:
		if plugin.name not in twinPlugins and plugin.path:
			if twinPaths.has_key(plugin.path[plugin.path.rfind("Plugins"):]):
				twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] += 1
			else:
				twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] = 1
			ButtonSetupFunctions.append((plugin.name, plugin.path[plugin.path.rfind("Plugins"):] + "/" + str(twinPaths[plugin.path[plugin.path.rfind("Plugins"):]]) , "Plugins"))
			twinPlugins.append(plugin.name)
	ButtonSetupFunctions.append((_("Show vertical Program Guide"), "Infobar/openVerticalEPG", "EPG"))
	ButtonSetupFunctions.append((_("Show graphical multi EPG"), "Infobar/openGraphEPG", "EPG"))
	ButtonSetupFunctions.append((_("Main menu"), "Infobar/mainMenu", "InfoBar"))
	ButtonSetupFunctions.append((_("Show help"), "Infobar/showHelp", "InfoBar"))
	ButtonSetupFunctions.append((_("Show extension selection"), "Infobar/showExtensionSelection", "InfoBar"))
	ButtonSetupFunctions.append((_("Zap down"), "Infobar/zapDown", "InfoBar"))
	ButtonSetupFunctions.append((_("Zap up"), "Infobar/zapUp", "InfoBar"))
	ButtonSetupFunctions.append((_("Volume down"), "Infobar/volumeDown", "InfoBar"))
	ButtonSetupFunctions.append((_("Volume up"), "Infobar/volumeUp", "InfoBar"))
	ButtonSetupFunctions.append((_("Show Infobar"), "Infobar/toggleShow", "InfoBar"))
	ButtonSetupFunctions.append((_("Show service list"), "Infobar/openServiceList", "InfoBar"))
	ButtonSetupFunctions.append((_("Show satellites list"), "Infobar/openSatellites", "InfoBar"))
	ButtonSetupFunctions.append((_("Show service list or movies"), "Infobar/showServiceListOrMovies", "InfoBar"))
	ButtonSetupFunctions.append((_("Show movies"), "Infobar/showMovies", "InfoBar"))
	ButtonSetupFunctions.append((_("Show favourites list"), "Infobar/openFavouritesList", "InfoBar"))
	ButtonSetupFunctions.append((_("Show current bouquet channel list"), "Infobar/switchChannelUp", "InfoBar"))
	ButtonSetupFunctions.append((_("History back"), "Infobar/historyBack", "InfoBar"))
	ButtonSetupFunctions.append((_("History next"), "Infobar/historyNext", "InfoBar"))
	ButtonSetupFunctions.append((_("Show event info plugins"), "Infobar/showEventInfoPlugins", "EPG"))
	ButtonSetupFunctions.append((_("Show event details"), "Infobar/openEventView", "EPG"))
	ButtonSetupFunctions.append((_("Show EPG for current service"), "Infobar/openSingleServiceEPG", "EPG"))
	ButtonSetupFunctions.append((_("Show multi EPG"), "Infobar/openMultiServiceEPG", "EPG"))
	ButtonSetupFunctions.append((_("Show subtitle selection"), "Infobar/subtitleSelection", "InfoBar"))
	ButtonSetupFunctions.append((_("Show Audioselection"), "Infobar/audioSelection", "InfoBar"))
	ButtonSetupFunctions.append((_("Switch to radio mode"), "Infobar/showRadio", "InfoBar"))
	ButtonSetupFunctions.append((_("Switch to TV mode"), "Infobar/showTv", "InfoBar"))
	ButtonSetupFunctions.append((_("Instant record"), "Infobar/instantRecord", "InfoBar"))
	ButtonSetupFunctions.append((_("Start instant recording"), "Infobar/startInstantRecording", "InfoBar"))
	ButtonSetupFunctions.append((_("Activate timeshift end"), "Infobar/activateTimeshiftEnd", "InfoBar"))
	ButtonSetupFunctions.append((_("Activate timeshift end and pause"), "Infobar/activateTimeshiftEndAndPause", "InfoBar"))
	ButtonSetupFunctions.append((_("Start timeshift"), "Infobar/startTimeshift", "InfoBar"))
	ButtonSetupFunctions.append((_("Stop timeshift"), "Infobar/stopTimeshift", "InfoBar"))
	ButtonSetupFunctions.append((_("Start teletext"), "Infobar/startTeletext", "InfoBar"))
	ButtonSetupFunctions.append((_("Show subservice selection"), "Infobar/subserviceSelection", "InfoBar"))
	ButtonSetupFunctions.append((_("Letterbox zoom"), "Infobar/vmodeSelection", "InfoBar"))
	ButtonSetupFunctions.append((_("Aspect selection"), "Infobar/aspectSelection", "InfoBar"))
	if SystemInfo["PIPAvailable"]:
		ButtonSetupFunctions.append((_("Show PIP"), "Infobar/showPiP", "InfoBar"))
		ButtonSetupFunctions.append((_("Swap PIP"), "Infobar/swapPiP", "InfoBar"))
		ButtonSetupFunctions.append((_("Move PIP"), "Infobar/movePiP", "InfoBar"))
		ButtonSetupFunctions.append((_("Toggle PIP-ZAP"), "Infobar/togglePipzap", "InfoBar"))
	ButtonSetupFunctions.append((_("Activate HbbTV (RedButton)"), "Infobar/activateRedButton", "InfoBar"))
	if getHaveHDMIinHD() in ('True') or getHaveHDMIinFHD() in ('True'):
		ButtonSetupFunctions.append((_("Toggle HDMI-In full screen"), "Infobar/HDMIInFull", "InfoBar"))
		ButtonSetupFunctions.append((_("Toggle HDMI-In PiP"), "Infobar/HDMIInPiP", "InfoBar"))
	if SystemInfo["LcdLiveTV"]:
		ButtonSetupFunctions.append((_("Toggle LCD LiveTV"), "Infobar/ToggleLCDLiveTV", "InfoBar"))
	if SystemInfo["canMultiBoot"]:
		ButtonSetupFunctions.append((_("MultiBootSelector"), "Module/Screens.MultiBootSelector/MultiBootSelector", "InfoBar"))
	ButtonSetupFunctions.append((_("Do nothing"), "Void", "InfoBar"))
	ButtonSetupFunctions.append((_("Button setup"), "Module/Screens.ButtonSetup/ButtonSetup", "Setup"))
	ButtonSetupFunctions.append((_("Software update"), "Module/Screens.SoftwareUpdate/UpdatePlugin", "Setup"))
	if getHaveCI() in ('True'):
		ButtonSetupFunctions.append((_("CI (Common Interface) Setup"), "Module/Screens.Ci/CiSelection", "Setup"))
	ButtonSetupFunctions.append((_("Videosetup"), "Module/Screens.VideoMode/VideoSetup", "Setup"))
	ButtonSetupFunctions.append((_("Tuner Configuration"), "Module/Screens.Satconfig/NimSelection", "Scanning"))
	ButtonSetupFunctions.append((_("Manual Scan"), "Module/Screens.ScanSetup/ScanSetup", "Scanning"))
	ButtonSetupFunctions.append((_("Automatic Scan"), "Module/Screens.ScanSetup/ScanSimple", "Scanning"))
	for plugin in plugins.getPluginsForMenu("scan"):
		ButtonSetupFunctions.append((plugin[0], "MenuPlugin/scan/" + plugin[2], "Scanning"))
	ButtonSetupFunctions.append((_("Network setup"), "Module/Screens.NetworkSetup/NetworkAdapterSelection", "Setup"))
	ButtonSetupFunctions.append((_("Network menu"), "Infobar/showNetworkMounts", "Setup"))
	ButtonSetupFunctions.append((_("VPN"), "Module/Screens.NetworkSetup/NetworkOpenvpn", "Setup"))
	ButtonSetupFunctions.append((_("Plugin Browser"), "Module/Screens.PluginBrowser/PluginBrowser", "Setup"))
	ButtonSetupFunctions.append((_("Channel info"), "Module/Screens.ServiceInfo/ServiceInfo", "Setup"))
	ButtonSetupFunctions.append((_("Timers"), "Module/Screens.TimerEdit/TimerEditList", "Setup"))
	ButtonSetupFunctions.append((_("AutoTimer overview"), "Infobar/showAutoTimerList", "Setup"))
	if SystemInfo["LCDSKINSetup"]:
		ButtonSetupFunctions.append((_("LCD SkinSelector"), "Module/Screens.SkinSelector/LcdSkinSelector", "Setup"))
	ButtonSetupFunctions.append((_("Timer"), "Module/Screens.TimerEdit/TimerEditList", "Setup"))
	ButtonSetupFunctions.append((_("Open AutoTimer"), "Infobar/showAutoTimerList", "Setup"))
	for plugin in plugins.getPluginsForMenu("system"):
		if plugin[2]:
			ButtonSetupFunctions.append((plugin[0], "MenuPlugin/system/" + plugin[2], "Setup"))
	ButtonSetupFunctions.append((_("Standby"), "Module/Screens.Standby/Standby", "Power"))
	ButtonSetupFunctions.append((_("Restart"), "Module/Screens.Standby/TryQuitMainloop/2", "Power"))
	ButtonSetupFunctions.append((_("Restart GUI"), "Module/Screens.Standby/TryQuitMainloop/3", "Power"))
	ButtonSetupFunctions.append((_("Deep standby"), "Module/Screens.Standby/TryQuitMainloop/1", "Power"))
	ButtonSetupFunctions.append((_("SleepTimer"), "Module/Screens.SleepTimerEdit/SleepTimerEdit", "Power"))
	ButtonSetupFunctions.append((_("PowerTimer"), "Module/Screens.PowerTimerEdit/PowerTimerEditList", "Power"))
	ButtonSetupFunctions.append((_("Usage setup"), "Setup/usage", "Setup"))
	ButtonSetupFunctions.append((_("User interface settings"), "Setup/userinterface", "Setup"))
	ButtonSetupFunctions.append((_("Recording Setup"), "Setup/recording", "Setup"))
	ButtonSetupFunctions.append((_("SkinSelector"), "Module/Screens.SkinSelector/SkinSelector", "Setup"))
	ButtonSetupFunctions.append((_("Harddisk Setup"), "Setup/harddisk", "Setup"))
	ButtonSetupFunctions.append((_("Subtitles settings"), "Setup/subtitlesetup", "Setup"))
	ButtonSetupFunctions.append((_("Language"), "Module/Screens.LanguageSelection/LanguageSelection", "Setup"))
	ButtonSetupFunctions.append((_("OscamInfo Mainmenu"), "Module/Screens.OScamInfo/OscamInfoMenu", "Plugins"))
	ButtonSetupFunctions.append((_("CCcamInfo Mainmenu"), "Module/Screens.CCcamInfo/CCcamInfoMain", "Plugins"))
	ButtonSetupFunctions.append((_("Movieplayer"), "Infobar/showMoviePlayer", "Plugins"))
	if os.path.isdir("/etc/ppanels"):
		for x in [x for x in os.listdir("/etc/ppanels") if x.endswith(".xml")]:
			x = x[:-4]
			ButtonSetupFunctions.append((_("PPanel") + " " + x, "PPanel/" + x, "PPanels"))
	if os.path.isdir("/usr/script"):
		for x in [x for x in os.listdir("/usr/script") if x.endswith(".sh")]:
			x = x[:-3]
	if os.path.isfile("/usr/lib/enigma2/python/Plugins/Extensions/EnhancedMovieCenter/plugin.pyo"):
		ButtonSetupFunctions.append((_("EnhancedMovieCenter"), "EMC/", "Plugins"))
	if os.path.isfile("/usr/lib/enigma2/python/Plugins/Extensions/Kodi/plugin.pyo"):
		ButtonSetupFunctions.append((_("Kodi MediaCenter"), "Kodi/", "Plugins"))
	ButtonSetupFunctions.append((_("OPD BluePanel"), "Module/OPENDROID.BluePanel/BluePanel", "OPD"))
	ButtonSetupFunctions.append((_("OPD Green Panel"), "Module/OPENDROID.GreenPanel/GreenPanel", "OPD"))
	ButtonSetupFunctions.append((_("OPD Download Panel"), "Module/OPENDROID.AddonsPanel/AddonsUtility", "OPD"))
	ButtonSetupFunctions.append((_("OPD OPD_panel"), "Module/OPENDROID.OPD_panel/OPD_panel", "OPD"))
	ButtonSetupFunctions.append((_("OPD ScriptRunner"), "Module/OPENDROID.ScriptRunner/ScriptRunner", "OPD"))
	ButtonSetupFunctions.append((_("OPD SwapManager"), "Module/OPENDROID.SwapManager/Swap", "OPD"))
	ButtonSetupFunctions.append((_("OPD SoftwarePanel"), "Module/OPENDROID.SoftwarePanel/SoftwarePanel", "OPD"))
	ButtonSetupFunctions.append((_("OPD MountManager"), "Module/OPENDROID.MountManager/HddMount", "OPD"))
	ButtonSetupFunctions.append((_("OPD CronManager"), "Module/OPENDROID.CronManager/CronManager", "OPD"))
	ButtonSetupFunctions.append((_("Disable this button"), "Infobar/fakeButton", "Disable Button"))
	return ButtonSetupFunctions

class ButtonSetup(Screen):
	skin = '<screen name="ButtonSetup" position="center,center" size="860,600" title="Quick button setup">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t<widget name="list" position="0,45" size="430,550" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="choosen" position="430,45" size="430,550" scrollbarMode="showOnDemand" />\n\t\t</screen>'

	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self['description'] = Label(_('Click on your remote on the button you want to change'))
		self.session = session
		self.setTitle(_("Button setup"))
		self["key_red"] = Label(_("Exit"))
                self["key_green"] = Label(_("Mode"))
		self.list = []
		self.ButtonSetupKeys = getButtonSetupKeys()
		self.ButtonSetupFunctions = getButtonSetupFunctions()
		for x in self.ButtonSetupKeys:
			self.list.append(ChoiceEntryComponent('',(_(x[0]), x[1])))
		self["list"] = ChoiceList(list=self.list[:config.misc.ButtonSetup.additional_keys.value and len(self.ButtonSetupKeys) or 10], selection = 0)
		self["choosen"] = ChoiceList(list=[])
		self.getFunctions()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"],
		{
		        "ok": self.keyOk,
		        "cancel": self.close,
		        "red": self.close,
		        "up": self.keyUp,
		        "down": self.keyDown,
		        "left": self.keyLeft,
		        "right": self.keyRight,
		        "green": self.greenPressed,
		}, -1)
		self["ButtonSetupButtonActions"] = ButtonSetupActionMap(["ButtonSetupActions"], dict((x[1], self.ButtonSetupGlobal) for x in self.ButtonSetupKeys))
		self.longkeyPressed = False
		self.onLayoutFinish.append(self.__layoutFinished)
		self.onExecBegin.append(self.getFunctions)

	def __layoutFinished(self):
		self["choosen"].selectionEnabled(0)
		text = "Style: Enigma2"
		if config.usage.keymap.value == "/usr/share/enigma2/keymap.ntr":
			text = "Style: Neutrino"
		elif config.usage.keymap.value == "/usr/share/enigma2/keymap.u80":
			text = "Style: User"
		self["key_green"].setText(_(text))

	def disableKeyMap(self):
		globalActionMap.setEnabled(False)
		eActionMap.getInstance().unbindNativeKey("ListboxActions", 0)
		eActionMap.getInstance().unbindNativeKey("ListboxActions", 1)
		eActionMap.getInstance().unbindNativeKey("ListboxActions", 4)
		eActionMap.getInstance().unbindNativeKey("ListboxActions", 5)

	def enableKeyMap(self):
		globalActionMap.setEnabled(True)
		eActionMap.getInstance().bindKey("keymap.xml", "generic", 103, 5, "ListboxActions", "moveUp")
		eActionMap.getInstance().bindKey("keymap.xml", "generic", 108, 5, "ListboxActions", "moveDown")
		eActionMap.getInstance().bindKey("keymap.xml", "generic", 105, 5, "ListboxActions", "pageUp")
		eActionMap.getInstance().bindKey("keymap.xml", "generic", 106, 5, "ListboxActions", "pageDown")

	def ButtonSetupGlobal(self, key):
		if self.longkeyPressed:
			self.longkeyPressed = False
		index = 0
		for x in self.list[:config.misc.ButtonSetup.additional_keys.value and len(self.ButtonSetupKeys) or 10]:
			if key == x[0][1]:
				self["list"].moveToIndex(index)
				if key.endswith("_long"):
					self.longkeyPressed = True
				break
			index += 1
		self.getFunctions()

	def keyOk(self):
		self.session.open(ButtonSetupSelect, self["list"].l.getCurrentSelection())

	def keyLeft(self):
		self['list'].instance.moveSelection(self["list"].instance.pageUp)
		self.getFunctions()

	def keyRight(self):
		self['list'].instance.moveSelection(self["list"].instance.pageDown)
		self.getFunctions()

	def keyUp(self):
		self['list'].instance.moveSelection(self["list"].instance.moveUp)
		self.getFunctions()

	def keyDown(self):
		self['list'].instance.moveSelection(self["list"].instance.moveDown)
		self.getFunctions()

	def getFunctions(self):
		key = self["list"].l.getCurrentSelection()[0][1]
		if key:
			selected = []
			for x in eval("config.misc.ButtonSetup." + key + ".value.split(',')"):
				function = list(function for function in self.ButtonSetupFunctions if function[1] == x )
				if function:
					selected.append(ChoiceEntryComponent('',((function[0][0]), function[0][1])))
			self["choosen"].setList(selected)

	def redPressed(self):
		from InfoBar import InfoBar
		InfoBarInstance = InfoBar.instance
		if not InfoBarInstance.LongButtonPressed:
			self.close()

	def greenPressed(self):
		self.session.open(KeymapSel)

class ButtonSetupSelect(Screen):
	skin = '<screen name="ButtonSetupSelect" position="center,center" size="860,600" title="Quick button setup">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t<widget name="list" position="0,45" size="430,550" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="choosen" position="430,45" size="430,550" scrollbarMode="showOnDemand" />\n\t\t</screen>'

	def __init__(self, session, key, args=None):
		Screen.__init__(self, session)
		self.skinName="ButtonSetupSelect"
		self['description'] = Label(_('Select the desired function and click on "OK" to assign it. Use "CH+/-" to toggle between the lists. Select an assigned function and click on "OK" to de-assign it. Use "Next/Previous" to change the order of the assigned functions.'))
		self.session = session
		self.key = key
		self.setTitle(_("button setup for") + ": " + key[0][0])
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		self.mode = "list"
		self.ButtonSetupFunctions = getButtonSetupFunctions()
		self.config = eval("config.misc.ButtonSetup." + key[0][1])
		self.expanded = []
		self.selected = []
		for x in self.config.value.split(','):
                        if x.startswith("ZapPanic"):
                                self.selected.append(ChoiceEntryComponent("", (_("Panic to") + " " + ServiceReference(eServiceReference(x.split("/", 1)[1]).toString()).getServiceName(), x)))
                        elif x.startswith("Zap"):
                                self.selected.append(ChoiceEntryComponent('', (_("Zap to") + ' ' + ServiceReference(eServiceReference(x.split("/", 1)[1]).toString()).getServiceName(), x)))
                        else:
                                function = list((function for function in self.ButtonSetupFunctions if function[1] == x))
                                if function:
                                        self.selected.append(ChoiceEntryComponent('', (function[0][0], function[0][1])))

		self.prevselected = self.selected[:]
		self["choosen"] = ChoiceList(list=self.selected, selection=0)
		self["list"] = ChoiceList(list=self.getFunctionList(), selection=0)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "KeyboardInputActions"], 
		{
			"ok": self.keyOk,
			"cancel": self.cancel,
			"red": self.cancel,
			"green": self.save,
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"pageUp": self.toggleMode,
			"pageDown": self.toggleMode,
			"moveUp": self.moveUp,
			"moveDown": self.moveDown,
		}, -1)
		self.onLayoutFinish.append(self.__layoutFinished)

	def __layoutFinished(self):
		self["choosen"].selectionEnabled(0)

	def getFunctionList(self):
		functionslist = []
		catagories = {}
		for function in self.ButtonSetupFunctions:
			if not catagories.has_key(function[2]):
				catagories[function[2]] = []
			catagories[function[2]].append(function)

		for catagorie in sorted(list(catagories)):
			if catagorie in self.expanded:
				functionslist.append(ChoiceEntryComponent('expanded',((catagorie), "Expander")))
				for function in catagories[catagorie]:
					functionslist.append(ChoiceEntryComponent('verticalline',((function[0]), function[1])))

			else:
				functionslist.append(ChoiceEntryComponent('expandable',((catagorie), "Expander")))

		return functionslist

	def toggleMode(self):
		if self.mode == "list" and self.selected:
			self.mode = "choosen"
			self["choosen"].selectionEnabled(1)
			self["list"].selectionEnabled(0)
		elif self.mode == "choosen":
			self.mode = "list"
			self["choosen"].selectionEnabled(0)
			self["list"].selectionEnabled(1)

	def keyOk(self):
		if self.mode == "list":
			currentSelected = self["list"].l.getCurrentSelection()
			if currentSelected[0][1] == "Expander":
				if currentSelected[0][0] in self.expanded:
					self.expanded.remove(currentSelected[0][0])
				else:
					self.expanded.append(currentSelected[0][0])
				self["list"].setList(self.getFunctionList())
			else:
				if currentSelected[:2] in self.selected:
					self.selected.remove(currentSelected[:2])
				else:
					self.selected.append(currentSelected[:2])
		elif self.selected:
			self.selected.remove(self["choosen"].l.getCurrentSelection())
			if not self.selected:
				self.toggleMode()
		self["choosen"].setList(self.selected)

	def zaptoCallback(self, *args):
		if args:
			currentSelected = self['list'].l.getCurrentSelection()[:]
			currentSelected[1] = currentSelected[1][:-1] + (currentSelected[0][0] + ' ' + ServiceReference(args[0]).getServiceName(),)
			self.selected.append([(currentSelected[0][0], currentSelected[0][1] + '/' + args[0].toString()), currentSelected[1]])

	def keyLeft(self):
		self[self.mode].instance.moveSelection(self[self.mode].instance.pageUp)

	def keyRight(self):
		self[self.mode].instance.moveSelection(self[self.mode].instance.pageDown)

	def keyUp(self):
		self[self.mode].instance.moveSelection(self[self.mode].instance.moveUp)

	def keyDown(self):
		self[self.mode].instance.moveSelection(self[self.mode].instance.moveDown)

	def moveUp(self):
		self.moveChoosen(self.keyUp)

	def moveDown(self):
		self.moveChoosen(self.keyDown)

	def moveChoosen(self, direction):
		if self.mode == "choosen":
			currentIndex = self["choosen"].getSelectionIndex()
			swapIndex = (currentIndex + (direction == self.keyDown and 1 or -1)) % len(self["choosen"].list)
			self["choosen"].list[currentIndex], self["choosen"].list[swapIndex] = self["choosen"].list[swapIndex], self["choosen"].list[currentIndex]
			self["choosen"].setList(self["choosen"].list)
			direction()
		else:
			return 0

	def save(self):
		configValue = []
		for x in self.selected:
			configValue.append(x[0][1])
		self.config.value = ",".join(configValue)
		self.config.save()
		self.close()

	def cancel(self):
		if self.selected != self.prevselected:
			self.session.openWithCallback(self.cancelCallback, MessageBox, _("Are you sure to cancel all changes"), default=False)
		else:
			self.close()

	def cancelCallback(self, answer):
		answer and self.close()

class ButtonSetupActionMap(ActionMap):
	def action(self, contexts, action):
		if (action in tuple(x[1] for x in getButtonSetupKeys()) and self.actions.has_key(action)):
			res = self.actions[action](action)
			if res is not None:
				return res
			return 1
		else:
			return ActionMap.action(self, contexts, action)

class helpableButtonSetupActionMap(HelpableActionMap):
	def action(self, contexts, action):
		if (action in tuple(x[1] for x in getButtonSetupKeys()) and self.actions.has_key(action)):
			res = self.actions[action](action)
			if res is not None:
				return res
			return 1
		else:
			return ActionMap.action(self, contexts, action)

class InfoBarButtonSetup():
	def __init__(self):
		self.ButtonSetupKeys = getButtonSetupKeys()
		self["ButtonSetupButtonActions"] = helpableButtonSetupActionMap(self, "ButtonSetupActions",
			dict((x[1],(self.ButtonSetupGlobal, boundFunction(self.getHelpText, x[1]))) for x in self.ButtonSetupKeys), -10)
		self.longkeyPressed = False
		self.onExecEnd.append(self.clearLongkeyPressed)

	def clearLongkeyPressed(self):
		self.longkeyPressed = False

	def getKeyFunctions(self, key):
		if key in ("play", "playpause", "Stop", "stop", "pause", "rewind", "next", "previous", "fastforward", "skip_back", "skip_forward") and (self.__class__.__name__ == "MoviePlayer" or hasattr(self, "timeshiftActivated") and self.timeshiftActivated()):
			return False
		selection = eval("config.misc.ButtonSetup." + key + ".value.split(',')")
		selected = []
		for x in selection:
			if x.startswith("ZapPanic"):
				selected.append(((_("Panic to") + " " + ServiceReference(eServiceReference(x.split("/", 1)[1]).toString()).getServiceName()), x))
			elif x.startswith("Zap"):
				selected.append(((_("Zap to") + " " + ServiceReference(eServiceReference(x.split("/", 1)[1]).toString()).getServiceName()), x))
			else:
				function = list(function for function in getButtonSetupFunctions() if function[1] == x )
				if function:
					selected.append(function[0])
		return selected

	def getHelpText(self, key):
		selected = self.getKeyFunctions(key)
		if not selected:
			return
		if len(selected) == 1:
			return selected[0][0]
		else:
			return _("ButtonSetup") + " " + tuple(x[0] for x in self.ButtonSetupKeys if x[1] == key)[0]

	def ButtonSetupGlobal(self, key):
		if self.longkeyPressed:
			self.longkeyPressed = False
		else:
			selected = self.getKeyFunctions(key)
			if not selected:
				return 0
			elif len(selected) == 1:
				if key.endswith("_long"):
					self.longkeyPressed = True
				return self.execButtonSetup(selected[0])
			else:
				key = tuple(x[0] for x in self.ButtonSetupKeys if x[1] == key)[0]
				self.session.openWithCallback(self.execButtonSetup, ChoiceBox, (_("ButtonSetup")) + ": " + key, selected)

	def execButtonSetup(self, selected):
		if selected:
			selected = selected[1].split("/")
			if selected[0] == "Plugins":
				twinPlugins = []
				twinPaths = {}
				pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_EVENTINFO)
				pluginlist.sort(key=lambda p: p.name)
				for plugin in pluginlist:
					if plugin.name not in twinPlugins and plugin.path and 'selectedevent' not in plugin.__call__.func_code.co_varnames:
						if twinPaths.has_key(plugin.path[plugin.path.rfind("Plugins"):]):
							twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] += 1
						else:
							twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] = 1
						if plugin.path[plugin.path.rfind("Plugins"):] + "/" + str(twinPaths[plugin.path[plugin.path.rfind("Plugins"):]]) == "/".join(selected):
							self.runPlugin(plugin)
							return
						twinPlugins.append(plugin.name)
				pluginlist = plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU])
				pluginlist.sort(key=lambda p: p.name)
				for plugin in pluginlist:
					if plugin.name not in twinPlugins and plugin.path:
						if twinPaths.has_key(plugin.path[plugin.path.rfind("Plugins"):]):
							twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] += 1
						else:
							twinPaths[plugin.path[plugin.path.rfind("Plugins"):]] = 1
						if plugin.path[plugin.path.rfind("Plugins"):] + "/" + str(twinPaths[plugin.path[plugin.path.rfind("Plugins"):]]) == "/".join(selected):
							self.runPlugin(plugin)
							return
						twinPlugins.append(plugin.name)
			elif selected[0] == "MenuPlugin":
				for plugin in plugins.getPluginsForMenu(selected[1]):
					if plugin[2] == selected[2]:
						self.runPlugin(plugin[1])
						return
			elif selected[0] == "Infobar":
				if hasattr(self, selected[1]):
					exec "self." + ".".join(selected[1:]) + "()"
				else:
					return 0
			elif selected[0] == "Module":
				try:
					exec "from %s import %s" % (selected[1], selected[2])
					exec "self.session.open(%s)" %  ",".join(selected[2:])
				except:
					print "[ButtonSetup] error during executing module %s, screen %s" % (selected[1], selected[2])
			elif selected[0] == "Setup":
				from Screens.Setup import Setup
				exec "self.session.open(Setup, \"%s\")" % selected[1]
			elif selected[0].startswith("Zap"):
				if selected[0] == "ZapPanic":
					self.servicelist.history = []
					self.pipShown() and self.showPiP()
				self.servicelist.servicelist.setCurrent(eServiceReference("/".join(selected[1:])))
				self.servicelist.zap(enable_pipzap = True)
				if hasattr(self, "lastservice"):
					self.lastservice = eServiceReference("/".join(selected[1:]))
					self.close()
				else:
					self.show()
				from Screens.MovieSelection import defaultMoviePath
				moviepath = defaultMoviePath()
				if moviepath:
					config.movielist.last_videodir.value = moviepath
			elif selected[0] == "PPanel":
				ppanelFileName = '/etc/ppanels/' + selected[1] + ".xml"
				if os.path.isfile(ppanelFileName) and os.path.isdir('/usr/lib/enigma2/python/Plugins/Extensions/PPanel'):
					from Plugins.Extensions.PPanel.ppanel import PPanel
					self.session.open(PPanel, name=selected[1] + ' PPanel', node=None, filename=ppanelFileName, deletenode=None)
			elif selected[0] == "Shellscript":
				command = '/usr/script/' + selected[1] + ".sh"
				if os.path.isfile(command) and os.path.isdir('/usr/lib/enigma2/python/Plugins/Extensions/PPanel'):
					from Plugins.Extensions.PPanel.ppanel import Execute
					self.session.open(Execute, selected[1] + " shellscript", None, command)
				else:
					from Screens.Console import Console
					exec "self.session.open(Console,_(selected[1]),[command])"
			elif selected[0] == "EMC":
				try:
					from Plugins.Extensions.EnhancedMovieCenter.plugin import showMoviesNew
					from Screens.InfoBar import InfoBar
					open(showMoviesNew(InfoBar.instance))
				except Exception as e:
					print('[EMCPlayer] showMovies exception:\n' + str(e))
			elif selected[0] == "ScriptRunner":
				if os.path.isfile("/usr/lib/enigma2/python/OPENDROID/ScriptRunner.pyo"):
					from OPENDROID.ScriptRunner import ScriptRunner
					self.session.open (ScriptRunner)
			elif selected[0] == "Kodi":
				if os.path.isfile("/usr/lib/enigma2/python/Plugins/Extensions/Kodi/plugin.pyo"):
					from Plugins.Extensions.Kodi.plugin import KodiMainScreen
					self.session.open(KodiMainScreen)
			elif selected[0] == "Bluetooth":
				if os.path.isfile("/usr/lib/enigma2/python/Plugins/SystemPlugins/BluetoothSetup/plugin.pyo"):
					from Plugins.SystemPlugins.BluetoothSetup.plugin import BluetoothSetup
					self.session.open(BluetoothSetup)
			elif selected[0] == "YoutubeTV":
				if os.path.isfile("/usr/lib/enigma2/python/Plugins/Extensions/Chromium/plugin.pyo"):
					from Plugins.Extensions.Chromium.youtube import YoutubeTVWindow
					self.session.open(YoutubeTVWindow)

	def showServiceListOrMovies(self):
		if hasattr(self, "openServiceList"):
			self.openServiceList()
		elif hasattr(self, "showMovies"):
			self.showMovies()

	def ToggleLCDLiveTV(self):
		config.lcd.showTv.value = not config.lcd.showTv.value


from Components.ConfigList import ConfigListScreen
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from enigma import eEnv
from Screens.Standby import quitMainloop, TryQuitMainloop
from Components.config import ConfigSubsection, ConfigInteger, ConfigText, getConfigListEntry, ConfigSelection, ConfigIP, ConfigYesNo, ConfigSequence, ConfigNumber, NoSave, ConfigEnableDisable, configfile
from os import path

class KeymapSel(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = ['SetupInfo', 'Setup']
		Screen.setTitle(self, _('Keymap Selection') + '...')
		self.setup_title = _('Keymap Selection') + '...'
		self['HelpWindow'] = Pixmap()
		self['HelpWindow'].hide()
		self['status'] = StaticText()
		self['footnote'] = Label('')
		self['description'] = Label('Copy your keymap to\n/usr/share/enigma2/keymap.usr')
		self['labelInfo'] = Label(_('Copy your keymap to\n/usr/share/enigma2/keymap.usr'))
		usrkey = eEnv.resolve('${datadir}/enigma2/keymap.usr')
		ntrkey = eEnv.resolve('${datadir}/enigma2/keymap.ntr')
		u80key = eEnv.resolve('${datadir}/enigma2/keymap.u80')
		self.actkeymap = self.getKeymap(config.usage.keymap.value)
		keySel = [('keymap.xml', _('Default  (keymap.xml)'))]
		if path.isfile(usrkey):
			keySel.append(('keymap.usr', _('User  (keymap.usr)')))
		if path.isfile(ntrkey):
			keySel.append(('keymap.ntr', _('Neutrino  (keymap.ntr)')))
		if path.isfile(u80key):
			keySel.append(('keymap.u80', _('UP80  (keymap.u80)')))
		if self.actkeymap == usrkey and not path.isfile(usrkey):
			setDefaultKeymap()
		if self.actkeymap == ntrkey and not path.isfile(ntrkey):
			setDefaultKeymap()
		if self.actkeymap == u80key and not path.isfile(u80key):
			setDefaultKeymap()
		self.keyshow = ConfigSelection(keySel)
		self.keyshow.value = self.actkeymap
		self.onChangedEntry = []
		self.list = []
		ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
		self.createSetup()
		self['actions'] = ActionMap(['SetupActions', 'ColorActions'],
		{
			'ok': self.keySave,
			'cancel': self.keyCancel,
			'red': self.keyCancel,
			'green': self.keySave,
			'menu': self.keyCancel,
		}, -2)
		self['key_red'] = StaticText(_('Cancel'))
		self['key_green'] = StaticText(_('OK'))
		if self.selectionChanged not in self['config'].onSelectionChanged:
			self['config'].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_('Use Keymap'), self.keyshow))
		self['config'].list = self.list
		self['config'].setList(self.list)
		if config.usage.sort_settings.value:
			self['config'].list.sort()
		return

	def selectionChanged(self):
		self['status'].setText(self['config'].getCurrent()[0])

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

		self.selectionChanged()

	def getCurrentEntry(self):
		return self['config'].getCurrent()[0]

	def getCurrentValue(self):
		return str(self['config'].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self['config'].getCurrent() and len(self['config'].getCurrent()) > 2 and self['config'].getCurrent()[2] or ''

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def saveAll(self):
		config.usage.keymap.value = eEnv.resolve('${datadir}/enigma2/' + self.keyshow.value)
		config.usage.keymap.save()
		configfile.save()
		if self.actkeymap != self.keyshow.value:
			self.changedFinished()

	def keySave(self):
		self.saveAll()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			return
		for x in self['config'].list:
			x[1].cancel()

		self.close()

	def keyCancel(self):
		if self['config'].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving settings?'))
		else:
			self.close()

	def getKeymap(self, file):
		return file[file.rfind('/') + 1:]

	def changedFinished(self):
		self.session.openWithCallback(self.ExecuteRestart, MessageBox, _('Keymap changed, you need to restart the GUI') + '\n' + _('Do you want to restart now?'), MessageBox.TYPE_YESNO)
		self.close()

	def ExecuteRestart(self, result):
		if result:
			quitMainloop(3)
		else:
			self.close()
