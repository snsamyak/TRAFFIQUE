# # Modern Traffic Signal Simulation
# import random
# import math
# import time
# import threading
# import pygame
# import sys
# import os
# import io
# import base64
#
# # Default values of signal times
# defaultRed = 150
# defaultYellow = 5
# defaultGreen = 20
# defaultMinimum = 10
# defaultMaximum = 40
#
# signals = []
# noOfSignals = 4
# simTime = 300
# timeElapsed = 0
#
# currentGreen = 0
# nextGreen = (currentGreen + 1) % noOfSignals
# currentYellow = 0
#
# # Average times for vehicles to pass the intersection
# carTime = 2
# bikeTime = 1
# rickshawTime = 2.25
# busTime = 2.5
# truckTime = 2.5
#
# # Count of cars at a traffic signal
# noOfCars = 0
# noOfBikes = 0
# noOfBuses = 0
# noOfTrucks = 0
# noOfRickshaws = 0
# noOfLanes = 2
#
# detectionTime = 5
# speeds = {'car': 4, 'bus': 3, 'truck': 3, 'rickshaw': 4, 'bike': 4.5}
#
# # Coordinates of start
# x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
# y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}
#
# vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
#             'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
# vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'rickshaw', 4: 'bike'}
# directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}
#
# # Modern UI coordinates and styling
# signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
# signalTimerCoods = [(530, 190), (810, 190), (810, 530), (530, 530)]
# vehicleCountCoods = [(480, 150), (880, 150), (880, 620), (480, 620)]
# vehicleCountTexts = ["0", "0", "0", "0"]
#
# # Coordinates of stop lines
# stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
# defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {'right': [580, 580, 580], 'down': [320, 320, 320], 'left': [810, 810, 810], 'up': [545, 545, 545]}
#
# mid = {'right': {'x': 705, 'y': 445}, 'down': {'x': 695, 'y': 450}, 'left': {'x': 695, 'y': 425},
#        'up': {'x': 695, 'y': 400}}
# rotationAngle = 3
#
# gap = 15
# gap2 = 15
#
# pygame.init()
# simulation = pygame.sprite.Group()
#
# # Modern color scheme
# COLORS = {
#     'background': (15, 23, 42),  # Slate-900
#     'primary': (59, 130, 246),  # Blue-500
#     'secondary': (139, 92, 246),  # Violet-500
#     'success': (34, 197, 94),  # Green-500
#     'warning': (251, 191, 36),  # Amber-400
#     'danger': (239, 68, 68),  # Red-500
#     'white': (255, 255, 255),
#     'gray': (148, 163, 184),  # Slate-400
#     'dark_gray': (30, 41, 59),  # Slate-800
#     'card_bg': (30, 41, 59),  # Slate-800
#     'border': (51, 65, 85),  # Slate-700
#     'text_light': (241, 245, 249),  # Slate-100
#     'text_dark': (15, 23, 42),  # Slate-900
#     'glass': (255, 255, 255, 40),  # Glass effect
#     'road': (71, 85, 105),  # Slate-600
#     'lane_divider': (203, 213, 225)  # Slate-300
# }
#
#
# class TrafficSignal:
#     def __init__(self, red, yellow, green, minimum, maximum):
#         self.red = red
#         self.yellow = yellow
#         self.green = green
#         self.minimum = minimum
#         self.maximum = maximum
#         self.signalText = "30"
#         self.totalGreenTime = 0
#
#
# class Vehicle(pygame.sprite.Sprite):
#     def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
#         super().__init__()  # correctly initialize pygame Sprite
#         self.lane = lane
#         self.vehicleClass = vehicleClass
#         self.speed = speeds[vehicleClass]
#         self.direction_number = direction_number
#         self.direction = direction
#         self.x = x[direction][lane]
#         self.y = y[direction][lane]
#         self.crossed = 0
#         self.willTurn = will_turn
#         self.turned = 0
#         self.rotateAngle = 0
#         vehicles[direction][lane].append(self)
#         self.index = len(vehicles[direction][lane]) - 1
#
#         # Create vehicle sprite
#         self.create_vehicle_sprite()
#
#         if (direction == 'right'):
#             if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][
#                 self.index - 1].crossed == 0):
#                 self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
#                     self.index - 1].currentImage.get_rect().width - gap
#             else:
#                 self.stop = defaultStop[direction]
#             temp = self.currentImage.get_rect().width + gap
#             x[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif (direction == 'left'):
#             if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
#                 self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
#                     self.index - 1].currentImage.get_rect().width + gap
#             else:
#                 self.stop = defaultStop[direction]
#             temp = self.currentImage.get_rect().width + gap
#             x[direction][lane] += temp
#             stops[direction][lane] += temp
#         elif (direction == 'down'):
#             if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
#                 self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
#                     self.index - 1].currentImage.get_rect().height - gap
#             else:
#                 self.stop = defaultStop[direction]
#             temp = self.currentImage.get_rect().height + gap
#             y[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif (direction == 'up'):
#             if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
#                 self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
#                     self.index - 1].currentImage.get_rect().height + gap
#             else:
#                 self.stop = defaultStop[direction]
#             temp = self.currentImage.get_rect().height + gap
#             y[direction][lane] += temp
#             stops[direction][lane] += temp
#         simulation.add(self)
#
#     def create_vehicle_sprite(self):
#         """Create modern looking vehicle sprites"""
#         vehicle_colors = {
#             'car': COLORS['primary'],
#             'bus': COLORS['warning'],
#             'truck': COLORS['danger'],
#             'rickshaw': COLORS['success'],
#             'bike': COLORS['secondary']
#         }
#
#         if self.direction in ['right', 'left']:
#             if self.vehicleClass == 'bike':
#                 size = (20, 12)
#             elif self.vehicleClass == 'car':
#                 size = (35, 18)
#             elif self.vehicleClass == 'bus':
#                 size = (50, 20)
#             elif self.vehicleClass == 'truck':
#                 size = (45, 20)
#             else:  # rickshaw
#                 size = (25, 15)
#         else:  # up, down
#             if self.vehicleClass == 'bike':
#                 size = (12, 20)
#             elif self.vehicleClass == 'car':
#                 size = (18, 35)
#             elif self.vehicleClass == 'bus':
#                 size = (20, 50)
#             elif self.vehicleClass == 'truck':
#                 size = (20, 45)
#             else:  # rickshaw
#                 size = (15, 25)
#
#         # Create rounded rectangle vehicle
#         self.originalImage = pygame.Surface(size, pygame.SRCALPHA)
#         color = vehicle_colors.get(self.vehicleClass, COLORS['gray'])
#         pygame.draw.rect(self.originalImage, color, (0, 0, size[0], size[1]), border_radius=3)
#         # Add a subtle highlight
#         highlight_color = tuple(min(255, c + 30) for c in color)
#         pygame.draw.rect(self.originalImage, highlight_color, (1, 1, size[0] - 2, 3), border_radius=2)
#
#         self.currentImage = self.originalImage.copy()
#
#     def render(self, screen):
#         screen.blit(self.currentImage, (self.x, self.y))
#
#     def move(self):
#         if (self.direction == 'right'):
#             if (self.crossed == 0 and self.x + self.currentImage.get_rect().width > stopLines[
#                 self.direction]):
#                 self.crossed = 1
#                 vehicles[self.direction]['crossed'] += 1
#             if (self.willTurn == 1):
#                 if (self.crossed == 0 or self.x + self.currentImage.get_rect().width < mid[self.direction]['x']):
#                     if ((self.x + self.currentImage.get_rect().width <= self.stop or (
#                             currentGreen == 0 and currentYellow == 0) or self.crossed == 1) and (
#                             self.index == 0 or self.x + self.currentImage.get_rect().width < (
#                             vehicles[self.direction][self.lane][self.index - 1].x - gap2) or
#                             vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
#                         self.x += self.speed
#                 else:
#                     if (self.turned == 0):
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 2
#                         self.y += 1.8
#                         if (self.rotateAngle == 90):
#                             self.turned = 1
#                     else:
#                         if (self.index == 0 or self.y + self.currentImage.get_rect().height < (
#                                 vehicles[self.direction][self.lane][
#                                     self.index - 1].y - gap2) or self.x + self.currentImage.get_rect().width < (
#                                 vehicles[self.direction][self.lane][self.index - 1].x - gap2)):
#                             self.y += self.speed
#             else:
#                 if ((self.x + self.currentImage.get_rect().width <= self.stop or self.crossed == 1 or (
#                         currentGreen == 0 and currentYellow == 0)) and (
#                         self.index == 0 or self.x + self.currentImage.get_rect().width < (
#                         vehicles[self.direction][self.lane][self.index - 1].x - gap2) or (
#                                 vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
#                     self.x += self.speed
#
#         elif (self.direction == 'down'):
#             if (self.crossed == 0 and self.y + self.currentImage.get_rect().height > stopLines[self.direction]):
#                 self.crossed = 1
#                 vehicles[self.direction]['crossed'] += 1
#             if (self.willTurn == 1):
#                 if (self.crossed == 0 or self.y + self.currentImage.get_rect().height < mid[self.direction]['y']):
#                     if ((self.y + self.currentImage.get_rect().height <= self.stop or (
#                             currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (
#                             self.index == 0 or self.y + self.currentImage.get_rect().height < (
#                             vehicles[self.direction][self.lane][self.index - 1].y - gap2) or
#                             vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
#                         self.y += self.speed
#                 else:
#                     if (self.turned == 0):
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 2.5
#                         self.y += 2
#                         if (self.rotateAngle == 90):
#                             self.turned = 1
#                     else:
#                         if (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index - 1].x +
#                                                          vehicles[self.direction][self.lane][
#                                                              self.index - 1].currentImage.get_rect().width + gap2) or self.y < (
#                                 vehicles[self.direction][self.lane][self.index - 1].y - gap2)):
#                             self.x -= self.speed
#             else:
#                 if ((self.y + self.currentImage.get_rect().height <= self.stop or self.crossed == 1 or (
#                         currentGreen == 1 and currentYellow == 0)) and (
#                         self.index == 0 or self.y + self.currentImage.get_rect().height < (
#                         vehicles[self.direction][self.lane][self.index - 1].y - gap2) or (
#                                 vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
#                     self.y += self.speed
#
#         elif (self.direction == 'left'):
#             if (self.crossed == 0 and self.x < stopLines[self.direction]):
#                 self.crossed = 1
#                 vehicles[self.direction]['crossed'] += 1
#             if (self.willTurn == 1):
#                 if (self.crossed == 0 or self.x > mid[self.direction]['x']):
#                     if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (
#                             self.index == 0 or self.x > (
#                             vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
#                         self.index - 1].currentImage.get_rect().width + gap2) or vehicles[self.direction][self.lane][
#                                 self.index - 1].turned == 1)):
#                         self.x -= self.speed
#                 else:
#                     if (self.turned == 0):
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 1.8
#                         self.y -= 2.5
#                         if (self.rotateAngle == 90):
#                             self.turned = 1
#                     else:
#                         if (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index - 1].y +
#                                                          vehicles[self.direction][self.lane][
#                                                              self.index - 1].currentImage.get_rect().height + gap2) or self.x > (
#                                 vehicles[self.direction][self.lane][self.index - 1].x + gap2)):
#                             self.y -= self.speed
#             else:
#                 if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
#                         self.index == 0 or self.x > (
#                         vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
#                     self.index - 1].currentImage.get_rect().width + gap2) or (
#                                 vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
#                     self.x -= self.speed
#
#         elif (self.direction == 'up'):
#             if (self.crossed == 0 and self.y < stopLines[self.direction]):
#                 self.crossed = 1
#                 vehicles[self.direction]['crossed'] += 1
#             if (self.willTurn == 1):
#                 if (self.crossed == 0 or self.y > mid[self.direction]['y']):
#                     if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (
#                             self.index == 0 or self.y > (
#                             vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
#                         self.index - 1].currentImage.get_rect().height + gap2) or vehicles[self.direction][self.lane][
#                                 self.index - 1].turned == 1)):
#                         self.y -= self.speed
#                 else:
#                     if (self.turned == 0):
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 1
#                         self.y -= 1
#                         if (self.rotateAngle == 90):
#                             self.turned = 1
#                     else:
#                         if (self.index == 0 or self.x < (vehicles[self.direction][self.lane][self.index - 1].x -
#                                                          vehicles[self.direction][self.lane][
#                                                              self.index - 1].currentImage.get_rect().width - gap2) or self.y > (
#                                 vehicles[self.direction][self.lane][self.index - 1].y + gap2)):
#                             self.x += self.speed
#             else:
#                 if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
#                         self.index == 0 or self.y > (
#                         vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
#                     self.index - 1].currentImage.get_rect().height + gap2) or (
#                                 vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
#                     self.y -= self.speed
#
#
# def initialize():
#     ts1 = TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts1)
#     ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts2)
#     ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts3)
#     ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts4)
#     repeat()
#
#
# def setTime():
#     global noOfCars, noOfBikes, noOfBuses, noOfTrucks, noOfRickshaws, noOfLanes
#     global carTime, busTime, truckTime, rickshawTime, bikeTime
#
#     noOfCars, noOfBuses, noOfTrucks, noOfRickshaws, noOfBikes = 0, 0, 0, 0, 0
#     for j in range(len(vehicles[directionNumbers[nextGreen]][0])):
#         vehicle = vehicles[directionNumbers[nextGreen]][0][j]
#         if (vehicle.crossed == 0):
#             noOfBikes += 1
#     for i in range(1, 3):
#         for j in range(len(vehicles[directionNumbers[nextGreen]][i])):
#             vehicle = vehicles[directionNumbers[nextGreen]][i][j]
#             if (vehicle.crossed == 0):
#                 vclass = vehicle.vehicleClass
#                 if (vclass == 'car'):
#                     noOfCars += 1
#                 elif (vclass == 'bus'):
#                     noOfBuses += 1
#                 elif (vclass == 'truck'):
#                     noOfTrucks += 1
#                 elif (vclass == 'rickshaw'):
#                     noOfRickshaws += 1
#
#     greenTime = math.ceil(((noOfCars * carTime) + (noOfRickshaws * rickshawTime) + (noOfBuses * busTime) + (
#             noOfTrucks * truckTime) + (noOfBikes * bikeTime)) / (noOfLanes + 1))
#     print('Green Time: ', greenTime)
#     if (greenTime < defaultMinimum):
#         greenTime = defaultMinimum
#     elif (greenTime > defaultMaximum):
#         greenTime = defaultMaximum
#     signals[(currentGreen + 1) % (noOfSignals)].green = greenTime
#
#
# def repeat():
#     global currentGreen, currentYellow, nextGreen
#     while (signals[currentGreen].green > 0):
#         printStatus()
#         updateValues()
#         if (signals[(currentGreen + 1) % (noOfSignals)].red == detectionTime):
#             thread = threading.Thread(name="detection", target=setTime, args=())
#             thread.daemon = True
#             thread.start()
#         time.sleep(0.84)
#     currentYellow = 1
#     vehicleCountTexts[currentGreen] = "0"
#     for i in range(0, 3):
#         stops[directionNumbers[currentGreen]][i] = defaultStop[directionNumbers[currentGreen]]
#         for vehicle in vehicles[directionNumbers[currentGreen]][i]:
#             vehicle.stop = defaultStop[directionNumbers[currentGreen]]
#     while (signals[currentGreen].yellow > 0):
#         printStatus()
#         updateValues()
#         time.sleep(0.667)
#     currentYellow = 0
#     signals[currentGreen].green = defaultGreen
#     signals[currentGreen].yellow = defaultYellow
#     signals[currentGreen].red = defaultRed
#     currentGreen = nextGreen
#     nextGreen = (currentGreen + 1) % noOfSignals
#     signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green
#     repeat()
#
#
# def printStatus():
#     for i in range(0, noOfSignals):
#         if (i == currentGreen):
#             if (currentYellow == 0):
#                 print(" GREEN TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#             else:
#                 print("YELLOW TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#         else:
#             print("   RED TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#     print()
#
#
# def updateValues():
#     for i in range(0, noOfSignals):
#         if (i == currentGreen):
#             if (currentYellow == 0):
#                 signals[i].green -= 1
#                 signals[i].totalGreenTime += 1
#             else:
#                 signals[i].yellow -= 1
#         else:
#             signals[i].red -= 1
#
#
# def generateVehicles():
#     while (True):
#         vehicle_type = random.randint(0, 4)
#         if (vehicle_type == 4):
#             lane_number = 0
#         else:
#             lane_number = random.randint(0, 1) + 1
#         will_turn = 0
#         if (lane_number == 2):
#             temp = random.randint(0, 4)
#             if (temp <= 2):
#                 will_turn = 1
#             elif (temp > 2):
#                 will_turn = 0
#         temp = random.randint(0, 999)
#         direction_number = 0
#         a = [400, 800, 900, 1000]
#         if (temp < a[0]):
#             direction_number = 0
#         elif (temp < a[1]):
#             direction_number = 1
#         elif (temp < a[2]):
#             direction_number = 2
#         elif (temp < a[3]):
#             direction_number = 3
#         Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number],
#                 will_turn)
#         time.sleep(0.5)
#
#
# def simulationTime():
#     global timeElapsed, simTime
#     while (True):
#         timeElapsed += 1
#         time.sleep(0.6667)
#         if (timeElapsed == simTime):
#             totalVehicles = 0
#             print('Lane-wise Vehicle Counts')
#             for i in range(noOfSignals):
#                 print('Lane', i + 1, ':', vehicles[directionNumbers[i]]['crossed'])
#                 totalVehicles += vehicles[directionNumbers[i]]['crossed']
#             print('Total vehicles passed: ', totalVehicles)
#             print('Total time passed: ', timeElapsed)
#             print('No. of vehicles passed per unit time: ', (float(totalVehicles) / float(timeElapsed)))
#             os._exit(1)
#
#
# def draw_modern_background(screen, screenWidth, screenHeight):
#     """Draw modern road intersection background"""
#     screen.fill(COLORS['background'])
#
#     # Draw main intersection area
#     intersection_rect = pygame.Rect(550, 280, 300, 280)
#     pygame.draw.rect(screen, COLORS['road'], intersection_rect, border_radius=10)
#
#     # Draw roads extending from intersection
#     # Horizontal road
#     pygame.draw.rect(screen, COLORS['road'], (0, 340, screenWidth, 160))
#     # Vertical road
#     pygame.draw.rect(screen, COLORS['road'], (590, 0, 160, screenHeight))
#
#     # Draw lane dividers
#     # Horizontal dividers
#     for x in range(0, screenWidth, 40):
#         pygame.draw.rect(screen, COLORS['lane_divider'], (x, 415, 20, 3))
#         pygame.draw.rect(screen, COLORS['lane_divider'], (x, 445, 20, 3))
#
#     # Vertical dividers
#     for y in range(0, screenHeight, 40):
#         pygame.draw.rect(screen, COLORS['lane_divider'], (665, y, 3, 20))
#         pygame.draw.rect(screen, COLORS['lane_divider'], (695, y, 3, 20))
#
#     # Draw stop lines
#     pygame.draw.rect(screen, COLORS['white'], (590, 340, 3, 160))  # Right
#     pygame.draw.rect(screen, COLORS['white'], (590, 330, 160, 3))  # Down
#     pygame.draw.rect(screen, COLORS['white'], (800, 340, 3, 160))  # Left
#     pygame.draw.rect(screen, COLORS['white'], (590, 535, 160, 3))  # Up
#
#
# def draw_modern_signal(screen, pos, state, timer_text):
#     """Draw modern traffic signal with glass morphism effect"""
#     x, y = pos
#
#     # Background glass panel
#     glass_surface = pygame.Surface((80, 120), pygame.SRCALPHA)
#     pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, 80, 120), border_radius=15)
#     screen.blit(glass_surface, (x - 10, y - 10))
#
#     # Signal housing
#     pygame.draw.rect(screen, COLORS['dark_gray'], (x, y, 60, 100), border_radius=10)
#     pygame.draw.rect(screen, COLORS['border'], (x, y, 60, 100), width=2, border_radius=10)
#
#     # Signal lights
#     red_pos = (x + 15, y + 10)
#     yellow_pos = (x + 15, y + 40)
#     green_pos = (x + 15, y + 70)
#
#     # Draw all lights with dim background
#     pygame.draw.circle(screen, (80, 0, 0), (red_pos[0] + 15, red_pos[1] + 15), 15)
#     pygame.draw.circle(screen, (80, 80, 0), (yellow_pos[0] + 15, yellow_pos[1] + 15), 15)
#     pygame.draw.circle(screen, (0, 80, 0), (green_pos[0] + 15, green_pos[1] + 15), 15)
#
#     # Light up active signal
#     if state == 'red':
#         pygame.draw.circle(screen, COLORS['danger'], (red_pos[0] + 15, red_pos[1] + 15), 15)
#         pygame.draw.circle(screen, COLORS['white'], (red_pos[0] + 15, red_pos[1] + 15), 15, width=3)
#     elif state == 'yellow':
#         pygame.draw.circle(screen, COLORS['warning'], (yellow_pos[0] + 15, yellow_pos[1] + 15), 15)
#         pygame.draw.circle(screen, COLORS['white'], (yellow_pos[0] + 15, yellow_pos[1] + 15), 15, width=3)
#     elif state == 'green':
#         pygame.draw.circle(screen, COLORS['success'], (green_pos[0] + 15, green_pos[1] + 15), 15)
#         pygame.draw.circle(screen, COLORS['white'], (green_pos[0] + 15, green_pos[1] + 15), 15, width=3)
#
#
# def draw_info_panel(screen, font, big_font):
#     """Draw modern information panel"""
#     panel_width = 350
#     panel_height = 200
#     panel_x = 1400 - panel_width - 20
#     panel_y = 20
#
#     # Background panel with glass effect
#     glass_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
#     pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, panel_width, panel_height), border_radius=20)
#     screen.blit(glass_surface, (panel_x, panel_y))
#
#     # Panel border
#     pygame.draw.rect(screen, COLORS['border'], (panel_x, panel_y, panel_width, panel_height),
#                      width=2, border_radius=20)
#
#     # Title
#     title_text = big_font.render("Traffic Control System", True, COLORS['text_light'])
#     screen.blit(title_text, (panel_x + 20, panel_y + 20))
#
#     # Time elapsed
#     time_text = font.render(f"Time Elapsed: {timeElapsed}s", True, COLORS['text_light'])
#     screen.blit(time_text, (panel_x + 20, panel_y + 60))
#
#     # Current signal status
#     status_text = font.render("Current Signal:", True, COLORS['gray'])
#     screen.blit(status_text, (panel_x + 20, panel_y + 90))
#
#     signal_names = ["East →", "South ↓", "West ←", "North ↑"]
#     current_text = font.render(f"{signal_names[currentGreen]}", True, COLORS['success'])
#     screen.blit(current_text, (panel_x + 150, panel_y + 90))
#
#     # Vehicle statistics
#     total_crossed = sum(vehicles[direction]['crossed'] for direction in directionNumbers.values())
#     stats_text = font.render(f"Vehicles Passed: {total_crossed}", True, COLORS['text_light'])
#     screen.blit(stats_text, (panel_x + 20, panel_y + 120))
#
#     if timeElapsed > 0:
#         efficiency = round(total_crossed / timeElapsed, 2)
#         eff_text = font.render(f"Efficiency: {efficiency}/s", True, COLORS['primary'])
#         screen.blit(eff_text, (panel_x + 20, panel_y + 150))
#
#
# def draw_vehicle_count_card(screen, font, pos, direction, count):
#     """Draw modern vehicle count cards"""
#     x, y = pos
#     card_width = 120
#     card_height = 60
#
#     # Card background
#     glass_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
#     pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, card_width, card_height), border_radius=15)
#     screen.blit(glass_surface, (x - card_width // 2, y - card_height // 2))
#
#     # Card border
#     pygame.draw.rect(screen, COLORS['border'],
#                      (x - card_width // 2, y - card_height // 2, card_width, card_height),
#                      width=2, border_radius=15)
#
#     # Direction arrow
#     direction_symbols = {"right": "→", "down": "↓", "left": "←", "up": "↑"}
#     arrow_text = font.render(direction_symbols[direction], True, COLORS['primary'])
#     arrow_rect = arrow_text.get_rect(center=(x, y - 15))
#     screen.blit(arrow_text, arrow_rect)
#
#     # Count
#     count_text = font.render(str(count), True, COLORS['text_light'])
#     count_rect = count_text.get_rect(center=(x, y + 15))
#     screen.blit(count_text, count_rect)
#
#
# def draw_signal_timer_display(screen, font, pos, signal_index):
#     """Draw modern signal timer display"""
#     x, y = pos
#     signal = signals[signal_index]
#
#     # Determine display text and color
#     if signal_index == currentGreen:
#         if currentYellow == 1:
#             if signal.yellow == 0:
#                 text = "STOP"
#                 color = COLORS['danger']
#             else:
#                 text = str(signal.yellow)
#                 color = COLORS['warning']
#         else:
#             if signal.green == 0:
#                 text = "SLOW"
#                 color = COLORS['warning']
#             else:
#                 text = str(signal.green)
#                 color = COLORS['success']
#     else:
#         if signal.red <= 10:
#             if signal.red == 0:
#                 text = "GO"
#                 color = COLORS['success']
#             else:
#                 text = str(signal.red)
#                 color = COLORS['danger']
#         else:
#             text = "---"
#             color = COLORS['gray']
#
#     # Timer background
#     timer_width = 80
#     timer_height = 35
#     glass_surface = pygame.Surface((timer_width, timer_height), pygame.SRCALPHA)
#     pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, timer_width, timer_height), border_radius=10)
#     screen.blit(glass_surface, (x - timer_width // 2, y - timer_height // 2))
#
#     # Timer border
#     pygame.draw.rect(screen, color,
#                      (x - timer_width // 2, y - timer_height // 2, timer_width, timer_height),
#                      width=2, border_radius=10)
#
#     # Timer text
#     timer_text = font.render(text, True, color)
#     timer_rect = timer_text.get_rect(center=(x, y))
#     screen.blit(timer_text, timer_rect)
#
#
# class Main:
#     thread4 = threading.Thread(name="simulationTime", target=simulationTime, args=())
#     thread4.daemon = True
#     thread4.start()
#
#     thread2 = threading.Thread(name="initialization", target=initialize, args=())
#     thread2.daemon = True
#     thread2.start()
#
#     # Modern screen setup
#     screenWidth = 1400
#     screenHeight = 800
#     screenSize = (screenWidth, screenHeight)
#
#     screen = pygame.display.set_mode(screenSize)
#     pygame.display.set_caption("Smart Traffic Control System")
#
#     # Modern fonts
#     font = pygame.font.Font(None, 24)
#     big_font = pygame.font.Font(None, 32)
#     timer_font = pygame.font.Font(None, 28)
#
#     thread3 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())
#     thread3.daemon = True
#     thread3.start()
#
#     clock = pygame.time.Clock()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#         # Draw modern background
#         draw_modern_background(screen, screenWidth, screenHeight)
#
#         # Draw traffic signals
#         for i in range(noOfSignals):
#             if i == currentGreen:
#                 if currentYellow == 1:
#                     state = 'yellow'
#                 else:
#                     state = 'green'
#             else:
#                 state = 'red'
#
#             draw_modern_signal(screen, signalCoods[i], state, str(signals[i].signalText))
#             draw_signal_timer_display(screen, timer_font, signalTimerCoods[i], i)
#
#         # Draw vehicle count cards
#         directions = ["right", "down", "left", "up"]
#         for i, direction in enumerate(directions):
#             count = vehicles[direction]['crossed']
#             draw_vehicle_count_card(screen, font, vehicleCountCoods[i], direction, count)
#
#         # Draw information panel
#         draw_info_panel(screen, font, big_font)
#
#         # Draw vehicles
#         for vehicle in simulation:
#             vehicle.render(screen)
#             vehicle.move()
#
#         # Add subtle animation effect
#         current_time = pygame.time.get_ticks()
#         if current_time % 2000 < 1000:  # Pulse effect every 2 seconds
#             pulse_surface = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
#             alpha = int(20 * (1 + math.sin(current_time * 0.01)))
#             pulse_surface.fill((59, 130, 246, alpha))
#             screen.blit(pulse_surface, (0, 0))
#
#         pygame.display.flip()
#         clock.tick(60)  # 60 FPS for smooth animation



import random
import math
import time
import threading
import pygame
import sys
import os

# Default values of signal times
defaultRed = 150
defaultYellow = 5
defaultGreen = 20
defaultMinimum = 10
defaultMaximum = 40

signals = []
noOfSignals = 4
simTime = 300
timeElapsed = 0

currentGreen = 0
nextGreen = (currentGreen + 1) % noOfSignals
currentYellow = 0

# Average times for vehicles to pass the intersection
carTime = 2
bikeTime = 1
rickshawTime = 2.25
busTime = 2.5
truckTime = 2.5

# Count of various vehicles
noOfCars = 0
noOfBikes = 0
noOfBuses = 0
noOfTrucks = 0
noOfRickshaws = 0
noOfLanes = 2

detectionTime = 5
speeds = {'car': 4, 'bus': 3, 'truck': 3, 'rickshaw': 4, 'bike': 4.5}

# Coordinates of start
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

vehicles = {
    'right': {0: [], 1: [], 2: [], 'crossed': 0},
    'down':  {0: [], 1: [], 2: [], 'crossed': 0},
    'left':  {0: [], 1: [], 2: [], 'crossed': 0},
    'up':    {0: [], 1: [], 2: [], 'crossed': 0}
}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'rickshaw', 4: 'bike'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# UI coordinates (kept as in your original)
signalCoods = [(480, 230), (900, 230), (900, 570), (480, 570)]
signalTimerCoods = [(480, 145), (900, 145), (900, 638), (480, 638)]
vehicleCountCoords = [(410, 230), (970, 230), (970, 570), (410, 570)]
vehicleCountTexts = ["0", "0", "0", "0"]

# Stop lines and defaults
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': [580, 580, 580], 'down': [320, 320, 320], 'left': [810, 810, 810], 'up': [545, 545, 545]}

mid = {'right': {'x': 705, 'y': 445}, 'down': {'x': 695, 'y': 450}, 'left': {'x': 695, 'y': 425},
       'up': {'x': 695, 'y': 400}}
rotationAngle = 3

gap = 15
gap2 = 15

pygame.init()
simulation = pygame.sprite.Group()

# Modern color scheme
COLORS = {
    'background': (15, 23, 42),
    'primary': (59, 130, 246),
    'secondary': (139, 92, 246),
    'success': (34, 197, 94),
    'warning': (251, 191, 36),
    'danger': (239, 68, 68),
    'white': (255, 255, 255),
    'gray': (148, 163, 184),
    'dark_gray': (30, 41, 59),
    'card_bg': (30, 41, 59),
    'border': (51, 65, 85),
    'text_light': (241, 245, 249),
    'text_dark': (15, 23, 42),
    'glass': (255, 255, 255, 40),
    'road': (71, 85, 105),
    'lane_divider': (203, 213, 225)
}


class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = "30"
        self.totalGreenTime = 0


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
        super().__init__()
        self.lane = lane
        self.vehicleClass = vehicleClass  # 'car', 'bus', ...
        self.speed = speeds.get(vehicleClass, 3)
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1

        # Create vehicle sprite
        self.create_vehicle_sprite()

        # compute stop positions and adjust start coordinate for spacing
        if (direction == 'right'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif (direction == 'left'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] += temp
            stops[direction][lane] += temp
        elif (direction == 'down'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].currentImage.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif (direction == 'up'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].currentImage.get_rect().height + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] += temp
            stops[direction][lane] += temp
        simulation.add(self)

    def create_vehicle_sprite(self):
        """Create modern looking vehicle sprites"""
        vehicle_colors = {
            'car': COLORS['primary'],
            'bus': COLORS['warning'],
            'truck': COLORS['danger'],
            'rickshaw': COLORS['success'],
            'bike': COLORS['secondary']
        }

        if self.direction in ['right', 'left']:
            if self.vehicleClass == 'bike':
                size = (20, 12)
            elif self.vehicleClass == 'car':
                size = (35, 18)
            elif self.vehicleClass == 'bus':
                size = (50, 20)
            elif self.vehicleClass == 'truck':
                size = (45, 20)
            else:  # rickshaw
                size = (25, 15)
        else:  # up, down
            if self.vehicleClass == 'bike':
                size = (12, 20)
            elif self.vehicleClass == 'car':
                size = (18, 35)
            elif self.vehicleClass == 'bus':
                size = (20, 50)
            elif self.vehicleClass == 'truck':
                size = (20, 45)
            else:  # rickshaw
                size = (15, 25)

        self.originalImage = pygame.Surface(size, pygame.SRCALPHA)
        color = vehicle_colors.get(self.vehicleClass, COLORS['gray'])
        pygame.draw.rect(self.originalImage, color, (0, 0, size[0], size[1]), border_radius=3)
        highlight_color = tuple(min(255, c + 30) for c in color[:3])
        pygame.draw.rect(self.originalImage, highlight_color, (1, 1, size[0] - 2, 3), border_radius=2)
        self.currentImage = self.originalImage.copy()

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def move(self):
        global vehicles, currentGreen, currentYellow

        # RIGHT
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.currentImage.get_rect().width > stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 1):
                if (self.crossed == 0 or self.x + self.currentImage.get_rect().width < mid[self.direction]['x']):
                    if ((self.x + self.currentImage.get_rect().width <= self.stop or (
                            currentGreen == 0 and currentYellow == 0) or self.crossed == 1) and (
                            self.index == 0 or self.x + self.currentImage.get_rect().width < (
                            vehicles[self.direction][self.lane][self.index - 1].x - gap2) or
                            vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                        self.x += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8
                        if (self.rotateAngle >= 90):
                            self.turned = 1
                    else:
                        if (self.index == 0 or self.y + self.currentImage.get_rect().height < (
                                vehicles[self.direction][self.lane][self.index - 1].y - gap2) or self.x + self.currentImage.get_rect().width < (
                                vehicles[self.direction][self.lane][self.index - 1].x - gap2)):
                            self.y += self.speed
            else:
                if ((self.x + self.currentImage.get_rect().width <= self.stop or self.crossed == 1 or (
                        currentGreen == 0 and currentYellow == 0)) and (
                        self.index == 0 or self.x + self.currentImage.get_rect().width < (
                        vehicles[self.direction][self.lane][self.index - 1].x - gap2) or (
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                    self.x += self.speed

        # DOWN
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.currentImage.get_rect().height > stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 1):
                if (self.crossed == 0 or self.y + self.currentImage.get_rect().height < mid[self.direction]['y']):
                    if ((self.y + self.currentImage.get_rect().height <= self.stop or (
                            currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (
                            self.index == 0 or self.y + self.currentImage.get_rect().height < (
                            vehicles[self.direction][self.lane][self.index - 1].y - gap2) or
                            vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if (self.rotateAngle >= 90):
                            self.turned = 1
                    else:
                        if (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index - 1].x +
                                                         vehicles[self.direction][self.lane][self.index - 1].currentImage.get_rect().width + gap2) or self.y < (
                                vehicles[self.direction][self.lane][self.index - 1].y - gap2)):
                            self.x -= self.speed
            else:
                if ((self.y + self.currentImage.get_rect().height <= self.stop or self.crossed == 1 or (
                        currentGreen == 1 and currentYellow == 0)) and (
                        self.index == 0 or self.y + self.currentImage.get_rect().height < (
                        vehicles[self.direction][self.lane][self.index - 1].y - gap2) or (
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                    self.y += self.speed

        # LEFT
        elif (self.direction == 'left'):
            if (self.crossed == 0 and self.x < stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 1):
                if (self.crossed == 0 or self.x > mid[self.direction]['x']):
                    if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (
                            self.index == 0 or self.x > (
                            vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
                        self.index - 1].currentImage.get_rect().width + gap2) or vehicles[self.direction][self.lane][
                                self.index - 1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if (self.rotateAngle >= 90):
                            self.turned = 1
                    else:
                        if (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index - 1].y +
                                                         vehicles[self.direction][self.lane][
                                                             self.index - 1].currentImage.get_rect().height + gap2) or self.x > (
                                vehicles[self.direction][self.lane][self.index - 1].x + gap2)):
                            self.y -= self.speed
            else:
                if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                        self.index == 0 or self.x > (
                        vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
                    self.index - 1].currentImage.get_rect().width + gap2) or (
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                    self.x -= self.speed

        # UP
        elif (self.direction == 'up'):
            if (self.crossed == 0 and self.y < stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 1):
                if (self.crossed == 0 or self.y > mid[self.direction]['y']):
                    if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (
                            self.index == 0 or self.y > (
                            vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
                        self.index - 1].currentImage.get_rect().height + gap2) or vehicles[self.direction][self.lane][
                                self.index - 1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if (self.rotateAngle >= 90):
                            self.turned = 1
                    else:
                        if (self.index == 0 or self.x < (vehicles[self.direction][self.lane][self.index - 1].x -
                                                         vehicles[self.direction][self.lane][
                                                             self.index - 1].currentImage.get_rect().width - gap2) or self.y > (
                                vehicles[self.direction][self.lane][self.index - 1].y + gap2)):
                            self.x += self.speed
            else:
                if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
                        self.index == 0 or self.y > (
                        vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
                    self.index - 1].currentImage.get_rect().height + gap2) or (
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                    self.y -= self.speed


def initialize():
    # Build initial traffic signals
    signals.clear()
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts4)
    # Ensure globals consistent
    global currentGreen, nextGreen
    currentGreen = 0
    nextGreen = (currentGreen + 1) % noOfSignals


def setTime():
    """Estimate green time for next signal based on queued vehicles (runs in separate thread)."""
    global noOfCars, noOfBikes, noOfBuses, noOfTrucks, noOfRickshaws, noOfLanes
    global carTime, busTime, truckTime, rickshawTime, bikeTime

    # Reset counts
    noOfCars = noOfBuses = noOfTrucks = noOfRickshaws = noOfBikes = 0

    next_dir = directionNumbers[nextGreen]
    # count bikes in lane 0 specially (your original logic)
    for vehicle in vehicles[next_dir][0]:
        if vehicle.crossed == 0:
            noOfBikes += 1
    # count other lanes
    for i in (1, 2):
        for vehicle in vehicles[next_dir][i]:
            if vehicle.crossed == 0:
                vclass = vehicle.vehicleClass
                if vclass == 'car':
                    noOfCars += 1
                elif vclass == 'bus':
                    noOfBuses += 1
                elif vclass == 'truck':
                    noOfTrucks += 1
                elif vclass == 'rickshaw':
                    noOfRickshaws += 1

    greenTime = math.ceil(((noOfCars * carTime) + (noOfRickshaws * rickshawTime) + (noOfBuses * busTime) + (
            noOfTrucks * truckTime) + (noOfBikes * bikeTime)) / (noOfLanes + 1))
    if greenTime < defaultMinimum:
        greenTime = defaultMinimum
    elif greenTime > defaultMaximum:
        greenTime = defaultMaximum

    # Set the green time for the next signal safely
    signals[(currentGreen + 1) % (noOfSignals)].green = greenTime
    print(f"[setTime] next green set to {greenTime}s for signal {(currentGreen + 1) % noOfSignals}")


def signal_controller_loop():
    """Main signal controller loop replacing recursive repeat()."""
    global currentGreen, currentYellow, nextGreen
    while True:
        # GREEN phase for currentGreen
        while signals[currentGreen].green > 0:
            printStatus()
            updateValues()
            # if next signal's red equals detectionTime start setTime thread
            if signals[(currentGreen + 1) % (noOfSignals)].red == detectionTime:
                th = threading.Thread(target=setTime, daemon=True)
                th.start()
            time.sleep(0.84)

        # switch to yellow
        currentYellow = 1
        vehicleCountTexts[currentGreen] = "0"
        for i in range(0, 3):
            stops[directionNumbers[currentGreen]][i] = defaultStop[directionNumbers[currentGreen]]
            for vehicle in vehicles[directionNumbers[currentGreen]][i]:
                vehicle.stop = defaultStop[directionNumbers[currentGreen]]

        while signals[currentGreen].yellow > 0:
            printStatus()
            updateValues()
            time.sleep(0.667)

        # end yellow - reset values for the signal and advance
        currentYellow = 0
        signals[currentGreen].green = defaultGreen
        signals[currentGreen].yellow = defaultYellow
        signals[currentGreen].red = defaultRed

        currentGreen = nextGreen
        nextGreen = (currentGreen + 1) % noOfSignals
        # set red for next
        signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green
        # loop continues


def printStatus():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                print(" GREEN TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
            else:
                print("YELLOW TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
        else:
            print("   RED TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
    print()


def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
                signals[i].totalGreenTime += 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


def generateVehicles():
    """Continuously spawn vehicles (runs in its own thread)."""
    while True:
        vehicle_type = random.randint(0, 4)
        if vehicle_type == 4:
            lane_number = 0
        else:
            lane_number = random.randint(0, 1) + 1

        will_turn = 0
        if lane_number == 2:
            temp = random.randint(0, 4)
            if temp <= 2:
                will_turn = 1
            else:
                will_turn = 0

        temp = random.randint(0, 999)
        direction_number = 0
        a = [400, 800, 900, 1000]
        if temp < a[0]:
            direction_number = 0
        elif temp < a[1]:
            direction_number = 1
        elif temp < a[2]:
            direction_number = 2
        else:
            direction_number = 3

        # create vehicle (directionNumbers maps int -> string)
        try:
            Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
        except Exception as ex:
            print("[generateVehicles] vehicle creation failed:", ex)
        time.sleep(0.5)


def simulationTime():
    """Global simulation time and exit condition (runs in own thread)."""
    global timeElapsed, simTime
    while True:
        timeElapsed += 1
        time.sleep(0.6667)
        if timeElapsed >= simTime:
            totalVehicles = 0
            print('Lane-wise Vehicle Counts')
            for i in range(noOfSignals):
                print('Lane', i + 1, ':', vehicles[directionNumbers[i]]['crossed'])
                totalVehicles += vehicles[directionNumbers[i]]['crossed']
            print('Total vehicles passed: ', totalVehicles)
            print('Total time passed: ', timeElapsed)
            if timeElapsed > 0:
                print('No. of vehicles passed per unit time: ', (float(totalVehicles) / float(timeElapsed)))
            os._exit(0)


def draw_modern_background(screen, screenWidth, screenHeight):
    screen.fill(COLORS['background'])
    intersection_rect = pygame.Rect(550, 280, 300, 280)
    pygame.draw.rect(screen, COLORS['road'], intersection_rect, border_radius=10)
    pygame.draw.rect(screen, COLORS['road'], (0, 340, screenWidth, 160))
    pygame.draw.rect(screen, COLORS['road'], (590, 0, 160, screenHeight))

    for xv in range(0, screenWidth, 40):
        pygame.draw.rect(screen, COLORS['lane_divider'], (xv, 415, 20, 3))
        pygame.draw.rect(screen, COLORS['lane_divIDER'] if False else COLORS['lane_divider'], (xv, 445, 20, 3))

    for yv in range(0, screenHeight, 40):
        pygame.draw.rect(screen, COLORS['lane_divider'], (665, yv, 3, 20))
        pygame.draw.rect(screen, COLORS['lane_divider'], (695, yv, 3, 20))

    pygame.draw.rect(screen, COLORS['white'], (590, 340, 3, 160))
    pygame.draw.rect(screen, COLORS['white'], (590, 330, 160, 3))
    pygame.draw.rect(screen, COLORS['white'], (800, 340, 3, 160))
    pygame.draw.rect(screen, COLORS['white'], (590, 535, 160, 3))


def draw_modern_signal(screen, pos, state, timer_text):
    x_pos, y_pos = pos
    glass_surface = pygame.Surface((60, 90), pygame.SRCALPHA)
    pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, 60, 90), border_radius=10)
    screen.blit(glass_surface, (x_pos - 30, y_pos - 45))

    signal_rect = pygame.Rect(x_pos - 25, y_pos - 40, 50, 80)
    pygame.draw.rect(screen, COLORS['dark_gray'], signal_rect, border_radius=8)
    pygame.draw.rect(screen, COLORS['border'], signal_rect, width=2, border_radius=8)

    light_radius = 10
    red_center = (x_pos, y_pos - 20)
    yellow_center = (x_pos, y_pos)
    green_center = (x_pos, y_pos + 20)

    pygame.draw.circle(screen, (60, 0, 0), red_center, light_radius)
    pygame.draw.circle(screen, (60, 60, 0), yellow_center, light_radius)
    pygame.draw.circle(screen, (0, 60, 0), green_center, light_radius)

    if state == 'red':
        pygame.draw.circle(screen, COLORS['danger'], red_center, light_radius)
        pygame.draw.circle(screen, COLORS['white'], red_center, light_radius, width=2)
    elif state == 'yellow':
        pygame.draw.circle(screen, COLORS['warning'], yellow_center, light_radius)
        pygame.draw.circle(screen, COLORS['white'], yellow_center, light_radius, width=2)
    elif state == 'green':
        pygame.draw.circle(screen, COLORS['success'], green_center, light_radius)
        pygame.draw.circle(screen, COLORS['white'], green_center, light_radius, width=2)


def draw_info_panel(screen, font, big_font):
    panel_width = 350
    panel_height = 200
    panel_x = 1400 - panel_width - 20
    panel_y = 20

    glass_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, panel_width, panel_height), border_radius=20)
    screen.blit(glass_surface, (panel_x, panel_y))
    pygame.draw.rect(screen, COLORS['border'], (panel_x, panel_y, panel_width, panel_height), width=2, border_radius=20)

    title_text = big_font.render("Traffic Control System", True, COLORS['text_light'])
    screen.blit(title_text, (panel_x + 20, panel_y + 20))

    time_text = font.render(f"Time Elapsed: {timeElapsed}s", True, COLORS['text_light'])
    screen.blit(time_text, (panel_x + 20, panel_y + 60))

    status_text = font.render("Current Signal:", True, COLORS['gray'])
    screen.blit(status_text, (panel_x + 20, panel_y + 90))

    signal_names = ["East →", "South ↓", "West ←", "North ↑"]
    current_text = font.render(f"{signal_names[currentGreen]}", True, COLORS['success'])
    screen.blit(current_text, (panel_x + 150, panel_y + 90))

    total_crossed = sum(vehicles[direction]['crossed'] for direction in directionNumbers.values())
    stats_text = font.render(f"Vehicles Passed: {total_crossed}", True, COLORS['text_light'])
    screen.blit(stats_text, (panel_x + 20, panel_y + 120))

    if timeElapsed > 0:
        efficiency = round(total_crossed / timeElapsed, 2)
        eff_text = font.render(f"Efficiency: {efficiency}/s", True, COLORS['primary'])
        screen.blit(eff_text, (panel_x + 20, panel_y + 150))


def draw_vehicle_count_card(screen, font, pos, direction, count):
    x_pos, y_pos = pos
    card_width = 70
    card_height = 50

    glass_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
    pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, card_width, card_height), border_radius=8)
    screen.blit(glass_surface, (x_pos - card_width // 2, y_pos - card_height // 2))

    card_rect = pygame.Rect(x_pos - card_width // 2, y_pos - card_height // 2, card_width, card_height)
    pygame.draw.rect(screen, COLORS['primary'], card_rect, width=2, border_radius=8)

    direction_symbols = {"right": "→", "down": "↓", "left": "←", "up": "↑"}
    arrow_text = direction_symbols.get(direction, "?")
    arrow_font = pygame.font.Font(None, 18)
    arrow_surface = arrow_font.render(arrow_text, True, COLORS['primary'])
    arrow_rect = arrow_surface.get_rect(center=(x_pos, y_pos - 12))
    screen.blit(arrow_surface, arrow_rect)

    count_font = pygame.font.Font(None, 22)
    count_text = count_font.render(str(count), True, COLORS['text_light'])
    count_rect = count_text.get_rect(center=(x_pos, y_pos + 8))
    screen.blit(count_text, count_rect)


def draw_signal_timer_display(screen, font, pos, signal_index):
    x_pos, y_pos = pos
    signal = signals[signal_index]

    if signal_index == currentGreen:
        if currentYellow == 1:
            if signal.yellow == 0:
                text = "STOP"
                color = COLORS['danger']
            else:
                text = str(signal.yellow)
                color = COLORS['warning']
        else:
            if signal.green == 0:
                text = "SLOW"
                color = COLORS['warning']
            else:
                text = str(signal.green)
                color = COLORS['success']
    else:
        if signal.red <= 10:
            if signal.red == 0:
                text = "GO"
                color = COLORS['success']
            else:
                text = str(signal.red)
                color = COLORS['danger']
        else:
            text = "---"
            color = COLORS['gray']

    timer_width = 70
    timer_height = 35
    glass_surface = pygame.Surface((timer_width, timer_height), pygame.SRCALPHA)
    pygame.draw.rect(glass_surface, COLORS['glass'], (0, 0, timer_width, timer_height), border_radius=8)
    screen.blit(glass_surface, (x_pos - timer_width // 2, y_pos - timer_height // 2))

    timer_rect = pygame.Rect(x_pos - timer_width // 2, y_pos - timer_height // 2, timer_width, timer_height)
    pygame.draw.rect(screen, color, timer_rect, width=2, border_radius=8)

    timer_font = pygame.font.Font(None, 24)
    timer_text = timer_font.render(text, True, color)
    timer_rect = timer_text.get_rect(center=(x_pos, y_pos))
    screen.blit(timer_text, timer_rect)


def main():
    global currentGreen, nextGreen

    # initialize signals and globals
    initialize()
    nextGreen = (currentGreen + 1) % noOfSignals

    # start background threads
    t_signal_ctrl = threading.Thread(target=signal_controller_loop, daemon=True)
    t_signal_ctrl.start()

    t_simtime = threading.Thread(target=simulationTime, daemon=True)
    t_simtime.start()

    t_gen = threading.Thread(target=generateVehicles, daemon=True)
    t_gen.start()

    # Pygame setup
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Smart Traffic Control System - Improved UI")

    font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 32)
    timer_font = pygame.font.Font(None, 28)

    clock = pygame.time.Clock()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)

            draw_modern_background(screen, screenWidth, screenHeight)

            # Draw traffic signals
            for i in range(noOfSignals):
                if i == currentGreen:
                    state = 'yellow' if currentYellow == 1 else 'green'
                else:
                    state = 'red'
                draw_modern_signal(screen, signalCoods[i], state, str(signals[i].signalText))
                draw_signal_timer_display(screen, timer_font, signalTimerCoods[i], i)

            directions = ["right", "down", "left", "up"]
            for i, direction in enumerate(directions):
                count = vehicles[direction]['crossed']
                draw_vehicle_count_card(screen, font, vehicleCountCoords[i], direction, count)

            draw_info_panel(screen, font, big_font)

            for vehicle in list(simulation):  # list() to allow safe iteration if group changes
                vehicle.render(screen)
                vehicle.move()

            # subtle pulse
            current_time = pygame.time.get_ticks()
            if current_time % 3000 < 1500:
                pulse_surface = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
                alpha = int(15 * (1 + math.sin(current_time * 0.005)))
                pulse_surface.fill((59, 130, 246, max(0, min(80, alpha))))
                screen.blit(pulse_surface, (0, 0))

            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print("[main] runtime error:", e)
        pygame.quit()
        raise


if __name__ == "__main__":
    main()
