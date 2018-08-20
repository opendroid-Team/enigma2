from enigma import ePicLoad
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigSlider, getConfigListEntry
from Components.Pixmap import Pixmap
from Tools.Directories import resolveFilename, fileExists, SCOPE_ACTIVE_SKIN
import os

class opdBootLogoSelector(Screen):
    skin = '\n\t\t<screen name="opdBootLogoSelector" position="center,center" size="560,550">\n\t\t\t<widget name="Preview" position="15,0" size="530,310" alphatest="on" zPosition="0" />\n\t\t\t<widget name="config" position="15,320" size="530,240" itemHeight="30" foregroundColor="window-fg" backgroundColor="window-bg" transparent="0" scrollbarMode="showOnDemand" enableWrapAround="1" />\n\t\t\t<ePixmap pixmap="buttons/red.png" position="0,e-40" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,e-40" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<ePixmap pixmap="buttons/green.png" position="140,e-40" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_green" position="140,e-40" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('OPD BootLogo settings'))
        self.previewPath = ''
        self.bootlogolist = []
        mypath = '/usr/share/bootlogos/'
        if not fileExists(mypath):
            os.system('mkdir /usr/share/bootlogos/')
        myimages = os.listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.bootlogolist.append(fil)

        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        self['Preview'] = Pixmap()
        self['config'] = MenuList(self.bootlogolist)
        self.current_sel = self['config'].getCurrent()
        self['actions'] = ActionMap(['WizardActions', 'SetupActions', 'ColorActions'], {'up': self.keyUp,
         'down': self.keyDown,
         'ok': self.keyGo,
         'save': self.keyGo,
         'cancel': self.keyCancel,
         'green': self.keyGo,
         'red': self.keyCancel}, -2)
        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.showPic)
        self.onLayoutFinish.append(self.layoutFinished)

    def showPic(self, picInfo = ''):
        ptr = self.picload.getData()
        if ptr is not None:
            self['Preview'].instance.setPixmap(ptr.__deref__())
            self['Preview'].show()
        return

    def layoutFinished(self):
        self.picload.setPara((self['Preview'].instance.size().width(),
         self['Preview'].instance.size().height(),
         0,
         0,
         1,
         1,
         '#00000000'))
        self.loadPreview()

    def keyGo(self):
        if self['config'].getCurrent() is not None:
            self.session.openWithCallback(self.confirm, MessageBox, _('Do you want to use this bootlogo as the default?'), MessageBox.TYPE_YESNO, timeout=10, default=False)
        return

    def confirm(self, confirmed):
        if confirmed:
            self.applySettings()

    def keyUp(self):
        self['config'].up()
        self.current_sel = self['config'].getCurrent()
        self.loadPreview()

    def keyDown(self):
        self['config'].down()
        self.current_sel = self['config'].getCurrent()
        self.loadPreview()

    def keyCancel(self):
        self.close()

    def loadPreview(self):
        try:
            pngpath = '/usr/share/enigma2/skin_default/noprev.png'
            if self['config'].getCurrent() is not None:
                root = '/usr/share/bootlogos/'
                pngpath = root + self.current_sel + '/prev.png'
            if self.previewPath != pngpath:
                self.previewPath = pngpath
            self.picload.startDecode(self.previewPath)
        except:
            pass

        return

    def applySettings(self):
        root = '/usr/share/bootlogos/'
        pngpath = root + self.current_sel
        if os.path.exists(pngpath):
            cmd = 'cp -a ' + pngpath + '/*.mvi /usr/share/'
            print cmd
            os.system(cmd)
        self.close()
