from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Tools.LoadPixmap import LoadPixmap
class info(Screen):
        skin = """
		<screen name="info" position="center,60" size="800,635" title="installation info" >
		<widget name="lab1" position="80,100" size="710,350" zPosition="2" scrollbarMode="showOnDemand" transparent="1"/>
		<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="red" backgroundColor="red" transparent="1" />		
		<widget name="key_green" position="400,600" zPosition="1" size="100,45" font="Regular;18" foregroundColor="green" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;18" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />
		</screen>"""

        def __init__(self, session):
                Screen.__init__(self, session)
                self['lab1'] = ScrollLabel('')
#                self.setTitle('OPDBoot %s - Menu' % PLUGINVERSION)
                self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], 
		{
			'back': self.close,
			'ok': self.close,
			'up': self['lab1'].pageUp,
			'left': self['lab1'].pageUp,
			'down': self['lab1'].pageDown,
			'right': self['lab1'].pageDown})
                self['lab1'].hide()
                self.updatetext()

        def updatetext(self):
                message = _('GUIDE FOR CORRECT INSTALLATION OF OPDBOOT.\n\n')
                message += _('Attention! During the entire installation process does not restart the receiver!\n\n')
                message += _('Warning! for the correct functioning of OPDboot, a USB or HDD memory is required, formatted in the Linux ext3 or ext4 system files\n\n')
                message += _('1. If you do not have a media formatted in ext3 or ext4, open menu, general configurations, system, storage device, select the drive and format it.\n\n')
                message += _('2. Go to the mount device manager from the OPD panel, services, device mount management and install hdd and usb correctly.\n\n')
                message += _('3. Now install OPDboot on the device by going to: menu, multiboot OPD.\n\n')
                message += _('4. On OPDboot press: menu to choose the type of start. Attention select: Start without Bootmanager for 64Bit devices.\n\n')
                message += _('5. Press the green button and select the source to install the multiboot image.\n\n')
                message += _('6. Downloaded the image, we have the possibility to choose whether to copy the settings from the flash image! choose YES if we want to import the settings, the password, network configurations etc ...\n\n')
                message += _('7. In case of problems with the installation, cancel and ask OpenDroid-Team for support on:\n\n')
                message += _('https://droidsat.org/forum')
                self['lab1'].show()
                self['lab1'].setText(message)

