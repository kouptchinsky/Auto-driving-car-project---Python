#!/usr/bin/env python3
#coding:utf−8
__author__ = "KOUATCHE TCHADIO Anila Keren , KOUPTCHINSKY Nicolas , LASSOIS Patrick , Mahieu Alexandre , VINETOT Nathan "
__copyright__ = " Copyright 2023 , HEH - Project Voiture "

import keyboard
import os
import random
import time

from allClass.tuture import Car
from manette import PS4Controller

# Fait avancer la voiture avec différentes vitesses
def showSpeed(car):
	car.turn(car.direction.midPulse)
	time.sleep(1)

	for i in range(4):
		car.move(25 * i)
		time.sleep(1)
	
	for i in range(4):
		car.move(100 - (25 * i))
		time.sleep(1)
	
	car.move(0)

# Fait tourner les roues des deux côtés
def showDirection(car):
	car.turn(car.direction.maxPulse)
	time.sleep(0.5)
	car.turn(car.direction.midPulse)
	time.sleep(0.5)
	car.turn(car.direction.minPulse)
	time.sleep(0.5)
	car.turn(car.direction.midPulse)
	time.sleep(0.5)

# Fait faire un cercle avec la voiture puis le reproduit dans l'autre sens
def showCircle(car):
	speed = 60
	mtime = 5

	car.turn(car.direction.maxPulse)
	time.sleep(0.5)
	car.move(speed)
	time.sleep(mtime)
	car.move(0)
	time.sleep(0.5)
	car.turn(car.direction.midPulse)
	time.sleep(0.5)
	car.turn(car.direction.minPulse)
	time.sleep(0.5)
	car.move(speed)
	time.sleep(mtime)
	car.move(0)
	time.sleep(0.5)

# Fait suivre le mur droit à la voiture
def suivimur(car):
	car.move(30)
	while True:
		if(car.sR.getDistance()<22):
			car.turn(180)
		elif(car.sR.getDistance()>23):
			car.turn(350)
		else:
			car.turn(250)

# Éviter l'obstacle devant la voiture
def eviteObj(car):
	car.move(30)
	while True:
			if(car.sF.getDistance()<30):
					car.turn(375)
					time.sleep(1.5)
					car.turn(250)
					time.sleep(1.5)
					car.turn(300)
					time.sleep(1)
					car.turn(250)
					time.sleep(1.5)
					car.turn(400)
					time.sleep(1.5)
					car.turn(300)

# Fait faire le circuit à la voiture
def circuitTour(car):
	car.move(35)
	while not car.sI.valueStop:
		if(car.sF.getDistance() > 35):
			if(car.sR.getDistance() < 30):
				car.turn(230)
			elif(car.sL.getDistance() < 30):
				car.turn(370)
			else:
				car.turn(300)
		elif(car.sR.getDistance() > car.sL.getDistance()):
			car.turn(450)
			time.sleep(0.5)
		else:
			car.turn(150)
			time.sleep(0.5)

# Fait faire un certain nombre de tour(s) à la voiture
def circuitNbrTour(car):
	nbtour=int(input("Combien de tours ? "))
	car.sI.reset(nbtour+1)
	circuitTour(car)

# Fait faire un nombre aléatoire de tour à la voiture
def circuitNbrRandomTour(car):
	nbtour = random.randint(1, 5)
	car.sI.reset(nbtour+1)
	circuitTour(car)

# Fait faire le circuit à la voiture quand le feu passe au vert
def circuitTourColor(car):
	while not car.sC.getGO():
		pass

	circuitTour(car)

# Permets de tester différentes vitesses aux moteurs
def testSpeed(car):
	while True:
		clear()
		print("Vitesse moteur gauche actuelle : ", car.mL.getSpeed())
		print("Vitesse moteur droit actuelle : ", car.mR.getSpeed())
		car.move(int(input("Valeur : ")))

# Permets de tester différents angle au servo-moteur ( roues )
def testDirection(car):
	while True:
		clear()
		printINA(car)
		print("Position actuelle : ", car.direction.getPosition())
		car.turn(int(input("Valeur : ")))

# Permets de faire tourner sur elle-même (faire Burn) la voiture
def testChar(car, left=False, right=False, time=0.0):
	if(left):
		car.mL.backward()
		car.mL.setSpeed(100)
		car.mR.forward()
		car.mR.setSpeed(100)
		time.sleep(time)
		car.move(0)
	
	if(right):
		car.mL.forward()
		car.mL.setSpeed(100)
		car.mR.backward()
		car.mR.setSpeed(100)
		time.sleep(time)
		car.move(0)

# Donne les informations de la voiture + les informations du capteur de couleur
def testColor(car):
	while True:
		printInfo(car)
		print()
		print(car.sC.valColor)
		print(car.sC.valLux)
		print(car.sC.getGO())
		if(car.sC.getGO()):
			car.move(30)
			
# Permets de contrôler la voiture à distance (un peu compliquer)
def testControle(car):
	speed = 0
	while True:
		nbr = input("z | q | s | d >>> ")

		if(nbr == "z"):
			if(speed < 0):
				car.move(0)
				speed = 0
			else:
				car.move(60)
				speed = 60
		elif(nbr == "s"):
			if(speed > 0):
				car.move(0)
				speed = 0
			else:
				car.move(-60)
				speed = -60
		elif(nbr == "q"):
			if(car.direction.getPosition() > 250):
				car.turn(245)
			else:
				car.turn(150)
		elif(nbr == "d"):
			if(car.direction.getPosition() < 250):
				car.turn(255)
			else:
				car.turn(400)

def testControleManette(car):
	ps4 = PS4Controller()
	ps4.init()
	try:
		"""
		{	0: False, A
			1: False, B
			2: False,
			3: False, X
			4: False, Y
			5: False,
			6: False, LU
			7: False, RU
			8: False,
			9: False,
			10: False,
			11: False,
			12: False,
			13: False, START
			14: False,
			15: False, SELECT
			16: False	}

		{	0: 0.07, JG
			1: 0.08, JG
			2: 0.02, JD
			3: 0.06, JD
			4: -1.0, RB
			5: -1.0  LB	}

		{	0: (0, 0) Direction	}
		"""
		ps4.start()
		car.sI.reset(3+1)
		while not car.sI.valueStop:
			if(ps4.axis_data[4] == -1):
				car.move(0 - int(100 * (ps4.axis_data[5] + 1) / 2))
			elif(ps4.axis_data[5] == -1):
				car.move(0 + int(100 * (ps4.axis_data[4] + 1) / 2))
			else:
				car.move(0)
			car.turn(300 + int(150 * ps4.axis_data[0]))

	finally:
		ps4.stop()

# Efface la console
def clear():
	os.system("clear")

# Affiche les informations des différents capteurs (Ultrason, Infrarouge, Couleur, Vitesse des moteurs, Position des servo-moteurs)
def printInfo(car):
	clear()
	print(car.sL.getDistance(), "cm | ", car.sF.getDistance(), "cm | ", car.sR.getDistance(), "cm")
	print("Valeur Infrarouge: ", car.sI.getValue())
	print("O: " , car.sI.opposer, " | C: ", car.sI.compteur, " | Vs: ", car.sI.valueStop)
	print('Valeur Couleur: ', car.sC.getColor())
	print('Valeur Temperature:', car.sC.getTemp(), 'K')
	print('Valeur Lux:', car.sC.getLux())
	print("Vitesse moteur Gauche:", car.mL.getSpeed())
	print("Vitesse moteur Droit:", car.mR.getSpeed())
	print("Position servomoteur:", car.direction.getPosition())
	printINA(car)

# Affiche les informations du limiteur de courant
def printINA(car):
	print("Bus Voltage: %.3f V" % car.direction.ina.getVoltage())
	print("Bus Current: %.3f mA" % car.direction.ina.getCurrent())
	print("Power: %.3f mW" % car.direction.ina.getPower())
	print("Shunt voltage: %.3f mV" % car.direction.ina.getShuntVoltage())

# Affiche un menu
def menu(car):
	try:
		clear()
		print("> ",  ('-'*12), " Menu ", ('-'*12))
		print(" Info General - 		 1")
		print(" Presentation Vitesse - 	 2")
		print(" Presentation Direction - 	 3")
		print(" Presentation Cercle - 		 4")
		print(" Longer mur - 			 5")
		print(" Eviter obstacle - 		 6")
		print(" Circuit - 			 7")
		print(" Circuit n° tour - 		 8")
		print(" Circuit n°? tour - 		 9")
		print(" Circuit feux - 		10")
		print("> ", ('-'*32))
		print(" Test Vitesse - 		11")
		print(" Test Direction - 		12")
		print(" Test Char - 			13")
		print(" Test Capteur Couleur - 	14")
		print(" Test Controle Distance - 	15")
		print(" Test Controle Manette - 	16")
		print("> ", ('-'*32))
		print(" Exit - 			 0")
		print("< ", ('-'*32))
		
		choix = int(input(">>> "))
		if(choix == 0):
			exit()
		elif(choix == 1):
			while True:
				printInfo(car)
				time.sleep(0.5)
		elif(choix == 2):
			showSpeed(car)
		elif(choix == 3):
			showDirection(car)
		elif(choix == 4):
			showCircle(car)
		elif(choix == 5):
			suivimur(car)
		elif(choix == 6):
			eviteObj(car)
		elif(choix == 7):
			car.sI.reset(2)
			circuitTour(car)
		elif(choix == 8):
			circuitNbrTour(car)
		elif(choix == 9):
			circuitNbrRandomTour(car)
		elif(choix == 10):
			circuitTourColor(car)
		elif(choix == 11):
			testSpeed(car)
		elif(choix == 12):
			testDirection(car)
		elif(choix == 13):
			car.turn(150)
			testChar(car, left=True, time=0.5)
			car.turn(350)
			testChar(car, right=True, time=0.5)
		elif(choix == 14):
			testColor(car)
		elif(choix == 15):
			testControle(car)
		elif(choix == 16):
			testControleManette(car)
					
	except Exception as e:
		print(e)
		input("Presse <<ENTER>> pour passer l'erreur")
		menu(car)
	
	finally:
		# Stop les différents composants de la voiture
		car.stop()

if __name__ == "__main__":
	try:
		# Initialise une voiture
		tuture = Car()
		tuture.start()
		while True:
			menu(tuture)

	except Exception as e:
		print(e)