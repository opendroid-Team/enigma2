#------------------------------------------------------
# Release Mod. 0.1 30/07/2016 by M43C0
# for ALL - Do NOT REMOVE THIS DISCLAIMER
#------------------------------------------------------
#
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference
from ServiceReference import resolveAlternate
from Components.Element import cached

import os,glob,xml.etree.cElementTree

Base=[("","","","")]
BasePlug=[("","","","")]

def CheckName():
    Creator=""
    if os.path.exists('/etc/image-version'):
      try:
        a = open('/etc/image-version', 'r')
        rf = a.readlines()
        a.close()				
        for line in rf:
          LoadConf = line.strip()		  
          elements = LoadConf.split('=')
          if LoadConf.lower().find('creator') != -1 :
            try:		  
              return elements[1].lower().strip()			
            except:
              pass			  						  		
      except:
        pass
    for x in glob.glob("/usr/lib/enigma2/python/Plugins/*"):
      x = x.replace("/usr/lib/enigma2/python/Plugins/","")
      if not x.find("Extensions") != -1 and not x.find("SystemPlugins") != -1 and not x.find("__init__") != -1 and not x.find("Plugin") != -1:
        return x.lower()
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/PKT'):	
      return "pkt"
    return ""
	
def DownloadMyUrlxml():
    MyName = CheckName()
    list = []	
    try:	
      mdom = xml.etree.cElementTree.parse("/usr/share/enigma2/oDreamy-FHD/teamz.xml")
      for x in mdom.getroot():
        if x.tag == "ruleset" and str(x.get("name")) == "ColorKeys":
          root =  x
          break			
      for x in root:
        if x.tag == "rule":                               
          if x.get("type") == "marker":	 
            Name = str(x.get("Name"))	
            if Name.lower().find(MyName) != -1:
              Red = str(x.get("Red"))
              Green = str(x.get("Green"))
              Yellow = str(x.get("Yellow"))
              Blue = str(x.get("Blue"))						
              list.append((Red,Green,Yellow,Blue))
    except:
      return	  
    return list	
	
def DownloadMyUrlxmlPlug():
    MyName = CheckName()
    list = []	
    try:	
      mdom = xml.etree.cElementTree.parse("/usr/share/enigma2/oDreamy-FHD/teamz.xml")
      for x in mdom.getroot():
        if x.tag == "ruleset" and str(x.get("name")) == "Plugins":
          root =  x
          break			
      for x in root:
        if x.tag == "rule":                               
          if x.get("type") == "marker":	 
            Name = str(x.get("Name"))	
            if Name.lower().find(MyName) != -1:
              Red = str(x.get("Red"))
              Green = str(x.get("Green"))
              Yellow = str(x.get("Yellow"))
              Blue = str(x.get("Blue"))						
              list.append((Red,Green,Yellow,Blue))
    except:
      return	  
    return list	
	
try:	
  Button = DownloadMyUrlxml()
  if not Button:
    Button = Base
  Red,Green,Yellow,Blue = Button[0] 
except:
  Red,Green,Yellow,Blue = Base[0]  

try:	
  ButtonPlug = DownloadMyUrlxmlPlug()
  if not ButtonPlug:
    ButtonPlug = BasePlug
  RedPlug,GreenPlug,YellowPlug,BluePlug = ButtonPlug[0] 
except:
  RedPlug,GreenPlug,YellowPlug,BluePlug = BasePlug[0] 
  
class Colorlabel(Converter, object):	
    def __init__(self, type):
        Converter.__init__(self, type)		
        self.type = type

    @cached
    def getText(self):
        if self.type == "labelred":
          return Red
        elif self.type == "labelyellow":
          return Yellow
        elif self.type == "labelgreen":
          return Green
        elif self.type == "labelblue":
          return Blue	
        elif self.type == "pluginred":
          return RedPlug
        elif self.type == "pluginyellow":
          return YellowPlug
        elif self.type == "plugingreen":
          return GreenPlug
        elif self.type == "pluginblue":
          return BluePlug			  		  
        else:
          return
		  
    text = property(getText)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
            Converter.changed(self, what)