#!/usr/bin/python

import os
import sys
import opdboot
import shutil
for delusb in os.listdir('/media/opdboot/OPDBootUpload'):
	if delusb.split('.')[-1] != 'zip':
		if os.path.isfile('/media/opdboot/OPDBootUpload/' + delusb) is True:
			os.remove('/media/opdboot/OPDBootUpload/' + delusb)
		else:    
			shutil.rmtree('/media/opdboot/OPDBootUpload/' + delusb)
if len(sys.argv) < 8:
        pass
else:
        opdboot.OPDBootMainEx(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
