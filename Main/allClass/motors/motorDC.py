#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

import RPi.GPIO as GPIO
import time

import allClass.motors.PCA9685 as PCA

class DC:
	def __init__(self, _pinA, _pinB, _en):
		# Initialise les variables des pins
		self.pinA = _pinA
		self.pinB = _pinB
		self.en = _en
		self.speed = 0
		# Initialise le contrôleur du servo
		self.pwm = PCA.PWM()
		self.pwm.frequency = 60

		self.forwardB = 'True'
		try:
			for line in open("config"):
				if line[0:8] == "forward0":
					self.forwardB = line[11:-1]
		except:
			pass
		if self.forwardB == 'True':
			self.backwardB = 'False'
		elif self.forwardB == 'False':
			self.backwardB = 'True'
		
		# Configure les broches GPIO
		GPIO.setup(self.pinA, GPIO.OUT)
		GPIO.setup(self.pinB, GPIO.OUT)

	def motor(self,x):
		# Définit l'état des pins pour avancer ou reculer
		if x == 'True':
			GPIO.output(self.pinA, GPIO.LOW)
			GPIO.output(self.pinB, GPIO.HIGH)
		elif x == 'False':
			GPIO.output(self.pinA, GPIO.HIGH)
			GPIO.output(self.pinB, GPIO.LOW)
		else:
			raise Exception('Config Error')

	def update(self):
		# Met à jour la vitesse du moteur
		self.pwm.write(self.en, 0, self.speed)

	def setSpeed(self, speed):
		# Définit la valeur de la variable de vitesse du moteur
		speed *= 40
		self.speed = speed
		self.update()

	def getSpeed(self):
		# Retourne la valeur de la variable de vitesse du moteur
		return self.speed
	
	def backward(self):
		# Définit le moteur en marche arrière
		self.motor(self.forwardB)

	def forward(self):
		# Définit le moteur en marche avant
		self.motor(self.backwardB)

	def stop(self):
		# Arrête le moteur
		GPIO.output(self.pinA, GPIO.LOW)
		GPIO.output(self.pinB, GPIO.LOW)