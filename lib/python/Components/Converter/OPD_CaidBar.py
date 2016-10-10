# CaidBar Converter
# Copyright (c) 2boom 2014
# v.0.3-r6
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Poll import Poll
import os

class OPD_CaidBar(Poll, Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type.split(',')
		self.maincolor = self.convert_color(self.type[0].strip())
		self.emmcolor = self.convert_color(self.type[1].strip())
		self.ecmcolor = self.convert_color(self.type[2].strip())
		self.poll_interval = 1000
		self.poll_enabled = True
		self.caid_default = ['B', 'D', 'I', 'S', 'V', 'N', 'EX', 'CW', 'ND', 'CO', 'BI']
		self.txt_caids = {'26':'BI', '01':'S', '06':'I', '17':'B', '05':'V', '18':'N', '09':'ND', '0B':'CO', '0D':'CW', '4A':'D', '27':'EX',\
			'7B':'D',  '0E':'PV', '22':'CC', '07':'DC', '56':'VM', 'A1':'RC', 'FF':'FF'}
	
	def convert_color(self, color_in):
		hex_color = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',\
			'a':':', 'b':';', 'c':'<', 'd':'=', 'e':'>', 'f':'?', 'A':':', 'B':';', 'C':'<', 'D':'=', 'E':'>', 'F':'?'}
		color_out = '\c'
		for i in range(1, len(color_in)):
			color_out += hex_color.get(color_in[i])
		return color_out

	def getCaidInEcmFile(self):
		caidvalue = return_line = ''
		zero_line = '0000'
		ecm_files = ['/tmp/ecm.info', '/tmp/ecm1.info'] # Tuner A,B
		for ecm_file in ecm_files:
			if os.path.isfile(ecm_file):
				try:
					filedata = open(ecm_file)
				except:
					filedata = False
				if filedata:
					for line in filedata.readlines():
						if "caid:" in line:
							caidvalue = line.strip("\n").split()[-1][2:]
							if len(caidvalue) < 4:
								caidvalue = zero_line[len(caidvalue):] + caidvalue
						elif "CaID" in line or "CAID" in line:
							caidvalue = line.split(',')[0].split()[-1][2:]
					return_line += ' %s ' % self.txt_caids.get(caidvalue[:2].upper(), ' ')
				filedata.close()
		return return_line

	def getServiceInfoString(self, info, what):
		value = info.getInfo(what)
		if value == -3:
			line_caids = info.getInfoObject(what)
			if line_caids and len(line_caids) > 0:
				return_value = ''
				for caid in line_caids:
					return_value += '%.4X ' % caid
				return return_value[:-1]
			else:
				return ''
		return '%d' % value
		
	def addspaces(self, what):
		return ' %s ' % what

	@cached
	def getText(self):
		string = ecmcaid = line_caids = ''
		service = self.source.service
		info = service and service.info()
		if not info:
			for i in range(len(self.caid_default)):
				string += self.maincolor + self.caid_default[i] + '  '
			return string
		caidinfo = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
		if caidinfo:
			ecmcaid = self.getCaidInEcmFile()
		for caid in caidinfo.split():
			line_caids += self.addspaces(self.txt_caids.get(caid[:2]))
		for i in range(len(self.caid_default)):
			if self.addspaces(self.caid_default[i]) in ecmcaid:
				string += self.ecmcolor
			elif self.addspaces(self.caid_default[i]) in line_caids:
				string += self.emmcolor
			else:
				string += self.maincolor
			string += self.caid_default[i] + '  '
		return string.strip()

	text = property(getText)

	def changed(self, what):
		if what[0] is self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] is self.CHANGED_POLL:
			self.downstream_elements.changed(what)
