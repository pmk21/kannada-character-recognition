import os
from shutil import copyfile

#Source path
PATH = 'Kannada/Hnd/Img/'

#Labels of images
sample_folders = os.listdir(PATH)

if 'static' not in os.listdir('webapp/templates'):
    os.mkdir('webapp/templates/static')

if 'classes' not in os.listdir('webapp/templates/static'):
    os.mkdir('webapp/templates/static/classes')

dest_path = 'webapp/templates/static/classes/'
img_class = 1

#Copies one image from each class
for i in sample_folders:
    temp_path = PATH + i +'/'
    src_path = temp_path + os.listdir(temp_path)[0]
    fin_path = dest_path + str(img_class) + '.png'
    copyfile(src_path, fin_path)
    img_class += 1