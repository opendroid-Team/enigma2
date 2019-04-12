import sys
import os
import struct
import shutil
from boxbranding import getBoxType, getImageDistro, getMachineName, getMachineBrand, getImageVersion, getMachineKernelFile, getMachineRootFile, getMachineBuild, getImageArch, getImageFolder
from os import path
media_nf = '/media/opdboot'
mediahome = media_nf + '/OPDBootI/'

extensions_path = '/usr/lib/enigma2/python/Plugins/Extensions/'
extensions_path_extractpy = extensions_path + 'OPDBoot/ubi_reader/ubi_extract_files.py'
extensions_path_extractpyo = extensions_path_extractpy + 'o'
dev_null = ' > /dev/null 2>&1'

def OPDBootMainEx(source, target, installsettings, bootquest, zipdelete, getimagefolder, getMachineRootFile, getImageArch):
        media_opendroid_target = mediahome + target
        list_one = ['rm -r ' + media_opendroid_target + dev_null,
                    'mkdir ' + media_opendroid_target + dev_null, 
                    'chmod -R 0777 ' + media_opendroid_target]

        for command in list_one:
                os.system(command)

        rc = OPDBootExtract(source, target, zipdelete, getimagefolder, getMachineRootFile, getImageArch)

        list_two = ['mkdir -p ' + media_opendroid_target + '/media' + dev_null,
                    'rm ' + media_opendroid_target + media_nf + dev_null, 
                    'rmdir ' + media_opendroid_target + media_nf + dev_null,
                    'mkdir -p ' + media_opendroid_target + media_nf + dev_null,
                    'cp /etc/network/interfaces ' + media_opendroid_target + '/etc/network/interfaces' + dev_null,
                    'cp /etc/passwd ' + media_opendroid_target + '/etc/passwd' + dev_null,
                    'cp /etc/resolv.conf ' + media_opendroid_target + '/etc/resolv.conf' + dev_null,
                    'cp /etc/wpa_supplicant.conf ' + media_opendroid_target + '/etc/wpa_supplicant.conf' + dev_null,
                    'rm -rf ' + media_opendroid_target + extensions_path + 'HbbTV',
                    'cp -r ' + extensions_path + 'OPDBoot/OPDBoot_client ' + media_opendroid_target + extensions_path + dev_null,
                    'cp -r ' + extensions_path + 'OPDBoot/.opdboot_location ' + media_opendroid_target + extensions_path + 'OPDBoot_client/.opdboot_location' + dev_null]

        for command in list_two:
                os.system(command)

        if installsettings == "True":
                list_three = ['mkdir -p ' + media_opendroid_target + '/etc/enigma2' + dev_null,
                              'cp -f /etc/enigma2/* ' + media_opendroid_target + '/etc/enigma2/',
                              'cp -f /etc/tuxbox/* ' + media_opendroid_target + '/etc/tuxbox/']
                for command in list_three:
                        os.system(command)

        os.system('mkdir -p ' + media_opendroid_target + '/media/usb' + dev_null)

        list_four = ['/etc/fstab', '/usr/lib/enigma2/python/Components/config.py', '/usr/lib/enigma2/python/Tools/HardwareInfoVu.py']
        for entrie in list_four:
                filename = media_opendroid_target + entrie
                tempfile = filename + '.tmp'
                if os.path.exists(filename):
                        out = open(tempfile, 'w')
                        f = open(filename, 'r')
                        for line in f.readlines():
                                if '/etc/fstab' in entrie:
                                        if '/dev/mtdblock2' in line:
                                                line = '#' + line
                                        elif '/dev/root' in line:
                                                line = '#' + line
                                if 'config.py' in entrie:
                                        if 'if file("/proc/stb/info/vumodel")' in line:
                                                line = '#' + line
                                        elif 'rckeyboard_enable = True' in line:
                                                line = '#' + line
                                if 'HardwareInfoVu.py' in entrie:
                                        if 'print "hardware detection failed"' in line:
                                                line = '\t\t    HardwareInfoVu.device_name ="duo"'

                                out.write(line)

                        f.close()
                        out.close()
                        os.rename(tempfile, filename)

        tpmd = media_opendroid_target + '/etc/init.d/tpmd'
        if os.path.exists(tpmd):
                os.remove(tpmd)

        filename = media_opendroid_target + '/etc/bhversion'
        if os.path.exists(filename):
                os.system('echo "BlackHole 2.0.9" > ' + filename)

        mypath = media_opendroid_target + '/usr/lib/opkg/info/'
        if not os.path.exists(mypath):
                mypath = media_opendroid_target + '/var/lib/opkg/info/'

        for file_name in os.listdir(mypath):

                list_five = ['-bootlogo.postinst', '-bootlogo.postrm', '-bootlogo.preinst', '-bootlogo.prerm']

                for entrie in list_five:
                        if entrie in file_name or (('kernel-image' in file_name) and ('postinst' in file_name)):
                                filename = mypath + file_name
                                tempfile = filename + '.tmp'
                                out = open(tempfile, 'w')
                                f = open(filename, 'r')
                                for line in f.readlines():
                                        if '/boot' in line:
                                                line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                                        out.write(line)

                                f.close()
                                out.close()
                                os.rename(tempfile, filename)
                                os.chmod(filename, 0755)

        rc = OPDBootRemoveUnpackDirs(getimagefolder)
        if bootquest == "True":
                out = open(mediahome + '.opdboot', 'w')
                out.write(target)
                out.close()
                os.system('touch /tmp/.opendroidreboot; sync; reboot -p')
        else:
                out = open(mediahome + '.opdboot', 'w')
                out.write(target)
                out.close()
                os.system('echo "[OPDBoot] Image-Install ready, Image starts by next booting, please push exit!"')

def OPDBootRemoveUnpackDirs(getimagefolder):
        os.chdir(media_nf + '/OPDBootUpload')
        if os.path.exists(media_nf + '/OPDBootUpload/%s'% getimagefolder):
                shutil.rmtree('%s'% getimagefolder)

def OPDBootExtract(source, target, zipdelete, getimagefolder, getMachineRootFile, getImageArch):
        OPDBootRemoveUnpackDirs(getimagefolder)
        os.system('rm -rf ' + media_nf + '/ubi')
        if not os.path.exists(media_nf + '/ubi'):
                os.system('mkdir ' + media_nf + '/ubi')
        sourcefile = media_nf + '/OPDBootUpload/%s.zip' % source
        if os.path.exists(sourcefile):
                os.chdir(media_nf + '/OPDBootUpload')
                if os.path.exists(media_nf + '/OPDBootUpload/usb_update.bin'):
                        os.system('rm -rf ' + media_nf + '/OPDBootUpload/usb_update.bin')
                os.system('echo "[OPDBoot] Extracking ZIP image file"')
                os.system('unzip ' + sourcefile)
                if zipdelete == "True":
                        os.system('rm -rf ' + sourcefile)
                else:
                        os.system('echo "[OPDBoot] keep  %s for next time"'% sourcefile)
                if "cortexa15hf-neon-vfpv4" in getImageArch:
                        if os.path.exists(media_nf + '/OPDBootUpload/%s'% getimagefolder):
                                os.chdir('%s'% getimagefolder)
                        print '[OPDBoot] Extracting tar.bz2 image and moving extracted image to our target'
                        if os.path.exists('/usr/bin/bzip2'):
                                sfolder = media_nf + '/OPDBootUpload/%s'% getimagefolder
                                cmd = 'tar -jxf ' + sfolder + '/rootfs.tar.bz2 -C ' + media_nf + '/OPDBootI/' + target + ' > /dev/null 2>&1'
                        os.system(cmd)
                        os.chdir('/home/root')
                else:
                        if os.path.exists(media_nf + '/OPDBootUpload/%s'% getimagefolder):
                                os.chdir('%s'% getimagefolder)
                                os.system('mv %s rootfs.bin'% getMachineRootFile)
                        print '[OPDBoot] Extracting UBIFS image and moving extracted image to our target'
                        if os.path.exists(extensions_path_extractpyo):
                                os.chmod(extensions_path_extractpyo, 0777)
                                cmd = 'python ' + extensions_path_extractpyo + ' rootfs.bin -o ' + media_nf + '/ubi'
                        else:
                                os.chmod(extensions_path_extractpy, 0777)
                                cmd = 'python ' + extensions_path_extractpy + ' rootfs.bin -o ' + media_nf + '/ubi'
                        print cmd
                        os.system(cmd)
                        os.chdir('/home/root')
                        os.system('cp -r -p ' + media_nf + '/ubi/rootfs/* ' + media_nf + '/OPDBootI/' + target)
                        os.system('chmod -R +x ' + media_nf + '/OPDBootI/' + target)
                        os.system('rm -rf ' + media_nf + '/ubi')
        return 1
