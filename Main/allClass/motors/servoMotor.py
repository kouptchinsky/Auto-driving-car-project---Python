#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

from allClass.motors.PCA9685 import PWM
from allClass.motors.limiteurINA import INA

class PAPA:
	def __init__(self):
		# Initialise les variables de la classe
		self.minPulse = 150
		self.midPulse = 300
		self.maxPulse = 450
		self.position = self.midPulse
		self.frequency = 50

		# Initialise le PWM
		self.pwm = PWM()
		self.pwm.frequency = self.frequency

		# Initialise le INA
		self.ina = INA(self)

	def update(self):
		# Met à jour la position du servo moteur
		if(self.minPulse <= self.position <= self.maxPulse):
			self.pwm.write(0, 0, self.position)
		else:
			self.reset()
	
	def setPosition(self, _pos):
		# Définit la position du servo moteur
		if(self.minPulse <= _pos <= self.maxPulse):
			self.position = _pos
		self.update()
	
	def getPosition(self):
		# Retourne la position du servo moteur
		return self.position

	def reset(self):
		# Met les roues droites
		self.setPosition(self.midPulse)
	
	def start(self):
		# Lance le thread du contrôleur du servo moteur
		self.ina.start()
	
	def stop(self):
		# Arrête le thread du contrôleur du servo moteur
		self.ina.stop()