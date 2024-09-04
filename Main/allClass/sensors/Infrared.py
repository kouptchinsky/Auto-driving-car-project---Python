#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

import RPi.GPIO as GPIO
import time

from allClass.sensors.Sensors import Sensor

class Infrared(Sensor):
	def __init__(self, _pin, _nbtour=3):
		super().__init__()
		# Initialise les variables de la classe
		self.pin = _pin
		self.value = 0
		self.opposer = 0
		self.compteur = 0
		self.valueStop = False
		self.temps = 0
		self.nbtour = _nbtour
		
		# Configure les broches GPIO
		GPIO.setup(self.pin, GPIO.IN)
	
	def run(self):
		# Fonction lancer avec le thread
		while not self.isKilled:
			# Met à jour chaque variable
			self.setValue(GPIO.input(self.pin))
			self.check()

		# Message lors de la fin du thread ( programme )
		print(self, " is killed")

	def check(self):
		# Vérifie le temps pour être sur d'avoir passer la ligne
		if(self.getValue() == self.opposer):
			if(self.getValue() == 1):
				self.opposer = 0
				self.temps = time.time()
			else:
				self.opposer = 1
				tempsFin = time.time()
				if(tempsFin - self.temps >= 0.25):
					self.compteur += 1
					if(self.compteur == self.nbtour):
						self.valueStop = True

	def setValue(self, _val):
		# Définit la valeur
		self.value = _val

	def getValue(self):
		# Retourne la valeur
		return self.value

	def reset(self,nbtour):
		# Remets les valeurs des variables pour refaire des tours
		self.opposer=0
		self.compteur=0
		self.valueStop=False
		self.temps=0
		self.nbtour=nbtour