#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

from ina219 import INA219
from ina219 import DeviceRangeError
from threading import Thread
import time

class INA(Thread):
	def __init__(self, _servo):
		super().__init__()
		# Initialise les variables de la classe
		self.isKilled = False
		self.servo = _servo

		# Initialise l'INA219
		self.SHUNT_OHMS = 0.1
		self.ina = INA219(self.SHUNT_OHMS)
		self.ina.configure()
	
	def run(self):
		# Fonction lancer avec le thread
		while not self.isKilled:
			try:
				self.getVoltage()
				self.getCurrent()
				self.getPower()
				self.getShuntVoltage()
			except DeviceRangeError as e:
				# Courant hors plage de l'appareil avec résistance shunt spécifiée
				if(self.servo.getPosition() < self.servo.midPulse):
					self.servo.setPosition(self.servo.getPosition() + 25)
				elif(self.servo.getPosition() > self.servo.midPulse):
					self.servo.setPosition(self.servo.getPosition() - 25)

		# Message lors de la fin du thread ( programme )
		print(self, " is killed")
	
	def getVoltage(self):
		# Retourne la valeur du voltage
		return self.ina.voltage()
	
	def getCurrent(self):
		# Retourne la valeur de ¯\_(ツ)_/¯
		return self.ina.current()
	
	def getPower(self):
		# Retourne la valeur de 'puissance' ¯\_(ツ)_/¯
		return self.ina.power()
	
	def getShuntVoltage(self):
		# Retourne la valeur de ¯\_(ツ)_/¯
		return self.ina.shunt_voltage()
	
	def stop(self):
		# Arrête le thread en cours
		self.isKilled = True
		self.join()