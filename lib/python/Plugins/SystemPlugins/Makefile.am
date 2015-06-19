installdir = $(pkglibdir)/python/Plugins/SystemPlugins

SUBDIRS = SoftwareManager PositionerSetup Satfinder \
	VideoTune Hotplug \
	DefaultServicesScanner CommonInterfaceAssignment \
	HdmiCEC VideoClippingSetup NetDrive \
	VideoEnhancement WirelessLan NetworkWizard \
	SABnzbdSetup OSD3DSetup DeviceManager SwapManager

if HAVE_LIBVUGLES2
SUBDIRS += AnimationSetup
endif

if DREAMBOX
SUBDIRS += FrontprocessorUpgrade NFIFlash SatelliteEquipmentControl DiseqcTester CableScan
endif

install_PYTHON = __init__.py
