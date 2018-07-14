from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.PluginComponent import plugins
from Components.Sources.List import List
from Components.Label import Label
from Components.config import config, configfile
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.LoadPixmap import LoadPixmap
from Components.UsageConfig import *
from Components.ConfigList import ConfigListScreen
from AddonsPanel import * 
from Plugin import ManualPanel, InstallFeed
import os
from OPENDROID.OPD_panel import OPD_panel
from Screens.Ipkg import Ipkg
class GreenPanel(Screen):
	skin = """
		<screen name="GreenPanel" position="center,60" size="1225,635" title="Green Panel" >
		<widget source="list" render="Listbox" position="80,100" size="600,400" enableWrapAround="1" zPosition="2" scrollbarMode="showOnDemand"  transparent="1">
		<convert type="TemplatedMultiContent">
		{"template": [MultiContentEntryText(pos = (115, 3), size = (385, 24), font=0, text = 0),MultiContentEntryText(pos = (115, 25), size = (385, 20), font=1, text = 1),MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 2),],"fonts": [gFont("Regular", 22),gFont("Regular", 18)],
"itemHeight": 50}
		</convert>
		</widget>
		<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="red" backgroundColor="red" transparent="1" />		
		<widget name="key_green" position="410,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="green" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />
		<widget name="key_blue" position="945,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="blue" backgroundColor="blue" transparent="1" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Green Panel"))
		self.list = []
		self['list'] = List(self.list)
		self.updateList()
		self['key_red'] = Label(_('Ipk Tools'))
		self['key_green'] = Label(_('OPD_panel'))
		self['key_yellow'] = Label(_('Addons '))
		self['key_blue'] = Label(_('Extension Install'))
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
		{'ok': self.save, 
		 'back': self.close, 
		 'red': self.openManualInstaller, 
		 'green': self.OPD_panel, 
		 'yellow': self.openAddonsManager, 
		 'blue': self.ExtensionInstaller
		}, -1)
	def save(self):
		self.run()
	def run(self):
		mysel = self['list'].getCurrent()
		if mysel:
			mysel
			plugin = mysel[3]
			plugin(session=self.session)
		else:
			mysel
	def updateList(self):
		self.list = []
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, '/usr/lib/enigma2/python/OPENDROID/icons/plugin.png'))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png, plugin)
			self.list.append(res)
		self['list'].list = self.list
		return None
	def openAddonsManager(self):
		self.session.open(AddonsUtility)
	def openManualInstaller(self):
		self.session.open(ManualPanel)
	def OPD_panel(self):
		self.session.open(OPD_panel)	
	def ExtensionInstaller(self):
		self.session.open(InstallFeed)
	def NotYet(self):
		mybox = self.session.open(MessageBox, 'Function Not Yet Available', MessageBox.TYPE_INFO)
		mybox.setTitle(_('Info'))
		
class DecodingSetup(ConfigListScreen, Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Decoding Setup'))
        list = []
        list.append(getConfigListEntry(_('Show No free tuner info'), config.usage.messageNoResources))
        list.append(getConfigListEntry(_('Show Tune failed info'), config.usage.messageTuneFailed))
        list.append(getConfigListEntry(_('Show No data on transponder info'), config.usage.messageNoPAT))
        list.append(getConfigListEntry(_('Show Service not found info'), config.usage.messageNoPATEntry))
        list.append(getConfigListEntry(_('Show Service invalid info'), config.usage.messageNoPMT))
        list.append(getConfigListEntry(_('Hide zap errors'), config.usage.hide_zap_errors))
        list.append(getConfigListEntry(_('Include EIT in http streams'), config.streaming.stream_eit))
        list.append(getConfigListEntry(_('Include AIT in http streams'), config.streaming.stream_ait))
        list.append(getConfigListEntry(_('Include ECM in http streams'), config.streaming.stream_ecm))
        list.append(getConfigListEntry(_('Include AIT in recordings'), config.recording.include_ait))
        list.append(getConfigListEntry(_('Include CI assignment'), config.misc.use_ci_assignment))
        list.append(getConfigListEntry(_('Descramble http streams'), config.streaming.descramble))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        ConfigListScreen.__init__(self, list)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': self.dontSaveAndExit,
         'green': self.saveAndExit,
         'cancel': self.dontSaveAndExit}, -1)

    def saveAndExit(self):
        if config.usage.dsemudmessages.value is not False:
            os.system('rm -rf /var/etc/.no_osd_messages')
        elif config.usage.dsemudmessages.value is not True:
            os.system('touch /var/etc/.no_osd_messages')
        if config.usage.messageYesPmt.value is not False:
            os.system('rm -rf /var/etc/.no_pmt_tmp')
        elif config.usage.messageYesPmt.value is not True:
            os.system('touch /var/etc/.no_pmt_tmp')
        for x in self['config'].list:
            x[1].save()

        config.usage.save()
        self.close()

    def dontSaveAndExit(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


config.infobar = ConfigSubsection()
config.infobar.weatherEnabled = ConfigYesNo(default=True)
config.infobar.permanentClockPosition = ConfigSelection(choices=['<>'], default='<>')
config.infobar.Ecn = ConfigYesNo(default=True)
config.infobar.CamName = ConfigYesNo(default=True)
config.infobar.NetInfo = ConfigYesNo(default=True)
config.infobar.EcmInfo = ConfigYesNo(default=True)
config.infobar.CryptoBar = ConfigYesNo(default=True)		

class InfoBarSetup(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Infobar Setup'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['description'] = Label(_('* = Restart Required'))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.keySave,
         'back': self.keyCancel,
         'red': self.keyCancel}, -2)
        self.list.append(getConfigListEntry(_('1st infobar timeout'), config.usage.infobar_timeout))
        self.list.append(getConfigListEntry(_('Show 2nd infobar'), config.usage.show_second_infobar))
        self.list.append(getConfigListEntry(_('Enable OK for channel selection'), config.usage.okbutton_mode))
        self.list.append(getConfigListEntry(_('Enable volume control with LEFT/RIGHT arrow buttons'), config.usage.volume_instead_of_channelselection))
        self.list.append(getConfigListEntry(_('Enable zapping with UP/DOWN arrow buttons'), config.usage.zap_with_arrow_buttons))
        self.list.append(getConfigListEntry(_('Infobar frontend data source'), config.usage.infobar_frontend_source))
        self.list.append(getConfigListEntry(_('Show PVR status in Movie Player'), config.usage.show_event_progress_in_servicelist))
        self.list.append(getConfigListEntry(_('Show channel number in infobar'), config.usage.show_infobar_channel_number))
        self.list.append(getConfigListEntry(_('Show infobar on channel change'), config.usage.show_infobar_on_zap))
        self.list.append(getConfigListEntry(_('Show infobar on skip forward/backward'), config.usage.show_infobar_on_skip))
        self.list.append(getConfigListEntry(_('Show infobar on event change'), config.usage.movieplayer_pvrstate))
        self.list.append(getConfigListEntry(_('Show infobar picons'), config.usage.showpicon))
        self.list.append(getConfigListEntry(_('Show Source Info'), config.infobar.Ecn))
        self.list.append(getConfigListEntry(_('Show SoftCam name'), config.infobar.CamName))
        self.list.append(getConfigListEntry(_('Show Netcard Info'), config.infobar.NetInfo))
        self.list.append(getConfigListEntry(_('Show ECM-Info'), config.infobar.EcmInfo))
        self.list.append(getConfigListEntry(_('Show Crypto-Bar'), config.infobar.CryptoBar))
        self.list.append(getConfigListEntry(_('Show EIT now/next in infobar'), config.usage.show_eit_nownext))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)

    def keyRight(self):
        ConfigListScreen.keyRight(self)

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        self.close()

    def keyCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()

