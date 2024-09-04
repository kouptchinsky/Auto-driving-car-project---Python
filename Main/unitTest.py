import time
import unittest
import RPi.GPIO as GPIO

from allClass.motors.motorDC import DC
from allClass.motors.servoMotor import PAPA
from allClass.sensors.Color import Color
from allClass.sensors.Infrared import Infrared
from allClass.sensors.Sensors import Sensor
from allClass.sensors.UltraSonic import UltraSonic
from allClass.tuture import Car

class testMotorDC(unittest.TestCase):

	def setUp(self):
		print("--- Test MotorDC ---")
		# Initialise le moteur
		self.m = DC(24, 23, 5)

	def test_simple(self):
		# avant
		self.m.motor('True')
		self.m.setSpeed(30)
		self.assertEqual(self.m.getSpeed(), 1200)
		print(self.m.getSpeed())

		# arriere
		self.m.motor('False')
		self.m.setSpeed(50)
		self.assertEqual(self.m.getSpeed(), 2000)

	def tearDown(self):
		print("--- Fin du Test ---")


class testServoMotor(unittest.TestCase):

	def setUp(self):
		print("--- Test ServoMotor ---")
		# Initialise le servo-moteur
		self.direction = PAPA()

	def test_simple(self):
		self.direction.setPosition(100)
		self.direction.update()
		time.sleep(1)

		# test si la valeur est bien entre 100 et 400 ( valeur min des roues et max) 
		self.assertGreaterEqual(self.direction.getPosition(), 150)
		self.assertLessEqual(self.direction.getPosition(), 400)
		print(self.direction.getPosition())
		
	def tearDown(self):
		print("--- Fin du Test ---")


class testSensors(unittest.TestCase):

	def setUp(self):
		print("--- Test Sensors ---")
		# Initialise la class "Sensor"
		self.sS = Sensor()

	def tearDown(self):
		print("--- Fin du Test ---")


class testColor(unittest.TestCase):

	def setUp(self):
		print("--- Test Color ---")
		# Initialise un capteur de couleur
		self.sC = Color()

	def tearDown(self):
		print("--- Fin du Test ---")


class testUlraSonic(unittest.TestCase):

		def setUp(self):
			print("--- Test UltraSonic ---")
			# Initialise un capteur ultrason
			self.sU = UltraSonic(6, 5)
			# Demarre le thread du capteur
			self.sU.start()

		def test_simple(self):
			time.sleep(1)
			#test si le capteur ne depasse pas la distance max
			self.assertLessEqual(self.sU.getDistance() , 400)
			print(self.sU.getDistance())

		def tearDown(self):
			print("--- Fin du Test ---")


class testInfrared(unittest.TestCase):

	def setUp(self):
		print("--- Test Infrared ---")
		# Initialisation d'un capteur infrarouge
		self.sI = Infrared(20)

	def test_simple(self):
		time.sleep(1)
		#test si valeur de sortie ressort un 0 lorsque qu'il detetcte quelque chose, peut aussi etre essayer lorsque qu'il ne detecte rien et qu'il est a 1
		self.assertEqual(self.sI.getValue(), 0)
		print(self.sI.getValue())
		
	def tearDown(self):
		print("--- Fin du Test ---")

		
if __name__ == '__main__':
	# Number GPIOs by its physical location
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	unittest.main()
