#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

import RPi.GPIO as GPIO
import time
import board
import adafruit_tcs34725

from allClass.sensors.Sensors import Sensor

class Color(Sensor):
	def __init__(self):
		super().__init__()
		# Initialise l'I2C
		self.i2c = board.I2C()
		self.sensor = adafruit_tcs34725.TCS34725(self.i2c)

		# Initialise les variables de la classe
		self.colors = []
		self.valColor = 0
		self.valTemp = 0
		self.valLux = 0
		self.valStart = False

	def run(self):
		# Fonction lancer avec le thread
		while not self.isKilled:
			# Met à jour chaque variable
			self.setColor(self.sensor.color_rgb_bytes)
			self.setTemp(self.sensor.color_temperature)
			self.setLux(self.sensor.lux)

		# Message lors de la fin du thread ( programme )
		print(self, " is killed")

	def getGO(self):
		# Retourne la valeur de départ (si le feu est vert)
		return self.valStart
	
	def setColor(self, _valC):
		# Définit la valeur de la couleur
		# Calcule la moyenne des valeurs reçues par le capteur pour être sur d'avoir du vert
		if(len(self.colors) == 0):
			if(_valC[1] > _valC[0] and _valC[0] > _valC[2]):
				self.valStart = True
			else:
				self.valStart = False
			
			self.valColor = _valC
			self.colors.append(_valC)
		else:
			moyenneG = 0
			for nbr in self.colors:
				moyenneG += nbr[1]
			moyenneG = moyenneG / len(self.colors)

			if((moyenneG - (moyenneG * 0.1)) < _valC[1] < (moyenneG + (moyenneG * 0.1))):
				if(_valC[1] > _valC[0] and _valC[1] > _valC[2]):
					self.valStart = True
				else:
					self.valStart = False
			
			self.valColor = _valC
			self.colors.append(_valC)

			# Si la liste des valeurs est plus grande que 5, retire le premier élément
			if(len(self.colors) > 5):
				self.colors.pop(0)

	def getColor(self):
		# Retourne la valeur de la couleur
		return self.valColor
	
	def setTemp(self, _valT):
		# Définit la valeur de la température de la couleur
		self.valTemp = _valT

	def getTemp(self):
		# Retourne la valeur de la température de la couleur
		return self.valTemp
	
	def setLux(self, _valL):
		# Définit la valeur de la luminosité
		self.valLux = _valL

	def getLux(self):
		# Retourne la valeur de la luminosité
		return self.valLux