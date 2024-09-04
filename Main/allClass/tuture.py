#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

import RPi.GPIO as GPIO
import time

from allClass.motors.motorDC import DC
from allClass.motors.servoMotor import PAPA
from allClass.sensors.Color import Color
from allClass.sensors.Infrared import Infrared
from allClass.sensors.UltraSonic import UltraSonic

class Car:
	def __init__(self):
		# Défini le mode des GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		# Initialise le servo-moteur
		self.direction = PAPA()
		# Initialise le moteur gauche
		self.mL = DC(24, 23, 5)
		# Initialise le moteur droit
		self.mR = DC(27, 22, 4)

		# Initialise le capteur d'ultrason gauche
		self.sL = UltraSonic(11, 9)
		# Initialise le capteur d'ultrason devant
		self.sF = UltraSonic(6, 5)
		# Initialise le capteur d'ultrason droit
		self.sR = UltraSonic(26, 19)

		# Initialise le capteur d'infrarouge
		self.sI = Infrared(20)
		
		# Initialise le capteur de couleur
		self.sC = Color()
	
	def move(self, speed):
		# Fait tourner les moteurs (vers l'avant si "speed" est positif vers l'arrière si négatif)
		if(100 >= speed >= 10):
			self.mL.forward()
			self.mL.setSpeed(speed)
			self.mR.forward()
			self.mR.setSpeed(speed)
		elif(-100 <= speed <= -10):
			self.mL.backward()
			self.mL.setSpeed(abs(speed))
			self.mR.backward()
			self.mR.setSpeed(abs(speed))
		else:
			self.mL.setSpeed(0)
			self.mR.setSpeed(0)

	def turn(self, deg):
		# Fait tourner les roues
		if(self.direction.minPulse <= deg <= self.direction.maxPulse):
			self.direction.setPosition(deg)
	
	def start(self):
		# Lance tous le thread de chaque capteur
		self.sL.start()
		self.sF.start()
		self.sR.start()
		self.sI.start()
		self.sC.start()
		self.direction.start()
		# Réinitialise l'angle des roues et la vitesse des moteurs
		self.direction.reset()
		self.move(0)
	
	def stop(self):
		# Arrête les moteurs
		self.mL.stop()
		self.mR.stop()
		# Mets les roues droites
		self.direction.reset()
		self.direction.stop()
		# Arrête le thread de chaque capteur
		self.sL.stop()
		self.sF.stop()
		self.sR.stop()
		
		self.sI.stop()
		self.sC.stop()
		# Nettoye l'état des GPIO
		GPIO.cleanup()