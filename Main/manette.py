import os
import sys
import pprint
import pygame
import pygame.display
from threading import Thread

class PS4Controller(Thread):
	"""Class representing the PS4 controller. Pretty straightforward functionality."""

	controller = None
	axis_data = None
	button_data = None
	hat_data = None

	def init(self):
		"""Initialize the joystick components"""
		super().__init__()
		# Initialise les variables de la classe
		self.isKilled = False
		self.axis_data = {	0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: -1.0, 5: -1.0}

		os.environ["SDL_VIDEODRIVER"] = "dummy"

		pygame.init()
		pygame.display.init()
		pygame.joystick.init()
		self.controller = pygame.joystick.Joystick(0)
		self.controller.init()

		print(self.controller.get_name())

	def run(self):
		# Fonction lancer avec le thread
		"""Listen for events to happen"""

		if not self.axis_data:
			self.axis_data = {}

		if not self.button_data:
			self.button_data = {}
			for i in range(self.controller.get_numbuttons()):
				self.button_data[i] = False

		if not self.hat_data:
			self.hat_data = {}
			for i in range(self.controller.get_numhats()):
				self.hat_data[i] = (0, 0)

		while not self.isKilled:
			for event in pygame.event.get():
				#os.system('clear')
				if event.type == pygame.JOYAXISMOTION:
					self.axis_data[event.axis] = round(event.value,2)
				elif event.type == pygame.JOYBUTTONDOWN:
					self.button_data[event.button] = True
				elif event.type == pygame.JOYBUTTONUP:
					self.button_data[event.button] = False
				elif event.type == pygame.JOYHATMOTION:
					self.hat_data[event.hat] = event.value

				# Insert your code on what you would like to happen for each event here!
				# In the current setup, I have the state simply printing out to the screen.
				#pprint.pprint(self.axis_data)
				#pprint.pprint(self.button_data)
				#pprint.pprint(self.hat_data)
		
		# Message lors de la fin du thread ( programme )
		print(self, " is killed")
	
	def stop(self):
		# Arrête le thread en cours
		self.isKilled = True
		self.join()
		pygame.quit()
