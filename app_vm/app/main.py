#!/usr/bin/python
from __future__ import print_function
import image
import solver
import objects

#image_path = "/home/joseph/scratch/CV/app_vm/data/screenshot.png"
image_path = "/home/joseph/Pictures/kfmIkJC.png"
template_path = "/home/joseph/scratch/CV/app_vm/data/templates/"

print('')
print("Running Infinity Loop solver on "+image_path.split("/")[-1])
for i in range(80):
    print("=",end='')
print('')
print('')

storage = objects.Data_storage()
image.image_find(image_path, template_path, storage)
solver.solve(storage)
for i,item in enumerate(storage.required_points):
    if i % 2 == 0:
        print(" ",item)
    elif i%2 == 1:
        print(item)
print(storage.fixed_points)
