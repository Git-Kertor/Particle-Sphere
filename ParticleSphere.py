
#Setup
import pygame, random, math, colorsys, sys, os
import numpy as np

#Variables
window_width = 640
window_height = 640
radius = 300.0
particleAmount = 300

#init
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

points = []
#Cartesian Coordinates of a point on a sphere are derived from here:
#wikipedia.org/wiki/Spherical_coordinate_system#Cartesian_coordinates
def CreateSpherePoints():
	for i in range(particleAmount):
		phi = random.random() * 2.0 * math.pi
		theta = random.random() * 2.0 * math.pi
		x = math.cos(phi) * math.sin(theta)
		y = math.sin(phi) * math.sin(theta)
		z = math.cos(theta)
		points.append((x,y,z))

#To rotate a point on a sphere we use Rodrigues' rotation formula found here:
#wikipedia.org/wiki/Rodrigues%27_rotation_formula
def RotateVector(v, k, theta):
	crossProduct = np.cross(v,k)
	dotProduct = np.dot(v,k)
	return v * math.cos(theta) + (crossProduct) * math.sin(theta) + k * dotProduct * (1 - math.cos(theta))

#To change the color of an image, apparently this is required
def SetColor(img, color):
	colorimg = pygame.Surface(img.get_size())
	colorimg.fill(color)
	render = img.copy()
	render.blit(colorimg, (0,0), special_flags = pygame.BLEND_MULT)
	return render

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('SphereASCII')
CreateSpherePoints()

particle = pygame.image.load("particle.png").convert_alpha()
particle = pygame.transform.scale(particle, (10, 10))

on = True
while on:
	pygame.Surface.fill(display, (0,0,0))
	time = float(pygame.time.get_ticks()) * 0.0001
	for (x,y,z) in points:	
		v = np.array([x,y,z])
		k = np.array([0,1,0])
		theta = time
		rotatedPoint = RotateVector(v, k, theta)

		#rotated vectors
		rx = rotatedPoint[0] * radius + window_width / 2
		ry = rotatedPoint[1] * radius + window_height / 2
		rz = rotatedPoint[2] * 3 + 10

		#color properties
		cx = float(rx) / float(window_width)
		cy = float(rz) / 13.0
		cz = float(rz) / 13.0

		render = SetColor(particle, hsv2rgb(cx, cy, cz))
		render = pygame.transform.scale(render, (rz, rz))
		display.blit(render, (rx, ry))
		

	
	pygame.display.update()
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    on = False
		if event.type == pygame.KEYDOWN:
		    if event.key == pygame.K_ESCAPE:
		        on = False