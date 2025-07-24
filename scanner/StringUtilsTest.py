import unittest
from StringUtils import StringUtils

class MyTests(unittest.TestCase):

	def test_boolValue_true(self):
		self.assertEqual(StringUtils.boolValue(True), True)
		self.assertEqual(StringUtils.boolValue(1), True)
		self.assertEqual(StringUtils.boolValue(2), True)
		self.assertEqual(StringUtils.boolValue(1.5), True)

		self.assertEqual(StringUtils.boolValue("on"), True)
		self.assertEqual(StringUtils.boolValue("true"), True)


	def test_boolValue_false(self):
		self.assertEqual(StringUtils.boolValue(False), False)
		self.assertEqual(StringUtils.boolValue(0), False)
		self.assertEqual(StringUtils.boolValue(-1), False)
		self.assertEqual(StringUtils.boolValue(-2), False)
		self.assertEqual(StringUtils.boolValue(-1.5), False)

	def test_boolValue_3(self):

		self.assertEqual(StringUtils.boolValue("enabled"), True)
		self.assertEqual(StringUtils.boolValue("disabled"), False)

		self.assertEqual(StringUtils.boolValue("chcecked"), True)
		self.assertEqual(StringUtils.boolValue("unchcecked"), False)

	# polskie tak/nie    	
		self.assertEqual(StringUtils.boolValue("tak"), True)
		self.assertEqual(StringUtils.boolValue("nie"), False)
		self.assertEqual(StringUtils.boolValue("t"), True)
		self.assertEqual(StringUtils.boolValue("n"), False)

	# angielskie tak/nie    	
		self.assertEqual(StringUtils.boolValue("y"), True)
		self.assertEqual(StringUtils.boolValue("n"), False)

	def test_boolValue_4(self):

		self.assertEqual(StringUtils.boolValue("piesek"), False)
		self.assertEqual(StringUtils.boolValue("foo"), False)

	def test_intValue(self):

		self.assertEqual(StringUtils.intValue(1), 1)
		self.assertEqual(StringUtils.intValue(1.3), 1)
		self.assertEqual(StringUtils.intValue(1.9), 1)
		self.assertEqual(StringUtils.intValue("1.9"), 1)
		self.assertEqual(StringUtils.intValue("1,9"), 1)
		self.assertEqual(StringUtils.intValue(2), 2)
		self.assertEqual(StringUtils.intValue("1"), 1)
		self.assertEqual(StringUtils.intValue("foo"), 0)
		self.assertEqual(StringUtils.intValue("1 foo"), 0)


if __name__ == '__main__':
	unittest.main()
		