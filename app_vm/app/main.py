#!/usr/bin/python
from __future__ import print_function
import glob

import image
import solver
import objects

template_path = "/home/joseph/scratch/CV/app_vm/data/templates/"

for image_path in glob.glob("/home/joseph/Pictures/Inf_Loops/*.jpg"):
#    image_path = "/home/joseph/scratch/CV/app_vm/data/screenshot.png"
#    image_path = "/home/joseph/Pictures/kfmIkJC.png"
    print('')
    print("Running Infinity Loop solver on "+image_path.split("/")[-1])
    for i in range(80):
        print("=",end='')
    print('')
    print('')

    storage = objects.Data_storage()
    image.image_find(image_path, template_path, storage)
    solver.solve(storage)
    print("continuing")
    for i,item in enumerate(storage.required_points):
        if i % 2 == 0:
            print(" ",item)
        elif i%2 == 1:
            print(item)
    print(storage.fixed_points)
    solver.check(storage,image_path)
