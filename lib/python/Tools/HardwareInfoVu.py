class HardwareInfoVu:
	device_name = None

	def __init__(self):
		if HardwareInfoVu.device_name is not None:
#			print "using cached result"
			return

		HardwareInfoVu.device_name = "unknown"
		HardwareInfoVu.vendor_name = "unknown"
		try:
			file = open("/proc/stb/info/vumodel", "r")
			HardwareInfoVu.vendor_name = "vuplus"
			HardwareInfoVu.device_name = file.readline().strip()
			file.close()
		except:
			print "hardware detection failed"

	def get_device_name(self):
		return HardwareInfoVu.device_name

	def get_vendor_name(self):
		return HardwareInfoVu.device_name

