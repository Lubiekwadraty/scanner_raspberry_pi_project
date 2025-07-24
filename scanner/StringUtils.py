#!/usr/bin/python3

class StringUtils:
	
	@staticmethod
	def boolValue(v):
		if v==True or v=="true" or v=="on" or v=="enabled" or v=="checked" or v=="tak" or v=="t" or v=="y":
			return True
			
		if isinstance(v, (int, float, complex)) and v>0:
			return True
			
		return False
	
	@staticmethod
	def intValue(v):
		if isinstance(v, (int, float, complex)): 
			return int(v)

		if isinstance(v, (str)):
			try:
				return int(float(v.replace(',', '.')))
			except ValueError:
				return 0
			
		return 0
		
