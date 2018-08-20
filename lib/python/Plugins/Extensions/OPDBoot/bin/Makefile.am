installdir = $(libdir)/enigma2/python/Plugins/Extensions/OPDBoot/bin
dist_install_DATA = \
	opdinitnoboot 
	
if HAVE_MB4K	
	dist_install_DATA += \	
	opdinitboot
else
	dist_install_DATA += \	
	opdbm  \
	opdinitboot \
	fbclear 
endif 


