#!/usr/bin/python
import image
#import solver
import objects

image_path = "/home/joseph/scratch/CV/app_vm/data/screenshot.png"
image_path = "/home/joseph/Pictures/kfmIkJC.png"
template_path = "/home/joseph/scratch/CV/app_vm/data/templates/"

storage = objects.Data_storage()
image.image_find(image_path, template_path, storage)

