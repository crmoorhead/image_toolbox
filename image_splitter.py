# IMAGE TOOLBOX

from PIL import Image
import os, sys

sonardir="C:\\Users\\the_n\\Documents\\PhD Stuff\\Projects\\OBJECT RECOGNITION\\sonar_originals"

# THIS CODE IS A MESS! GET A PROPER WORKFLOW GOING!

''''# CREATE DICTIONARY OF ALL FILES IN SONAR DIRECTORY

# Assigns the images a number for key in the dictionary and the entry being a tuple of the original file name and the image object imported.
# Any files that are not images are ignored.

directory = os.fsencode(sonardir)
images={}
index=1
for file in os.listdir(directory):
    try:
        images[index]=[os.fsdecode(file),Image.open(sonardir+"\\" +os.fsdecode(file))]
        index+=1
    except IOError:
        pass


# SHOW IMAGE

# NOTE: We need the first index to reference the key and the second index to reference the Image object

# images[0][1].show()



# FUNCTION TO GENERATE COORDINATES OF DIVISIONS OF ORIGINAL IMAGE

# This function supports 2 modes, "number" and "size".

# For "number", the grid argument, (m,n), returns the lattice points that will split the orignal image into m*n non-overlapping boxes.
# FOr "size", the grid argument returns the lattice points that will split the image into non-overlapping boxes each of dimension (m,n).

# If the original image is not evenly split, we have several modes - "centre", "stop" and "overlap".

# "centre" discards pixels on the outer margin of the original image.
# "stop" takes as many steps as it can and then discards the remainder.
# "overlap" creates the number/size of box specified by the grid argument, but adjusts so as to allow the boxes to overlap.

# The function for the overlapping windows option runs as follows

def overlap(length,split_size):
    extra=length%split_size                                     # Number of pixels that must be shared among intervals
    if extra==0:                                                # If no pixels need to be shared, then we can return a list of non-overlapping intervals
        n=length//split_size                                    # Number of intervals needed to span length
        chunk=lambda i : (i*split_size,(i+1)*split_size-1)      # Formula for ith interval
        chunks=list(map(chunk,range(n)))                        # List of all intervals
    else:
        n=length//split_size+1                                  # Number of intervals that will span the length
        n_share=(n*split_size-length)//(n-1)                    # The overlap constant i.e pixels shared between an interval and its neighbour
        if (n*split_size-length)%(n-1)==0:
            chunk= lambda i : (i*(split_size-n_share),i*(split_size-n_share)+split_size-1)  # Formula for ith interval
            chunks=list(map(chunk,range(n)))
        else:
            chunks=overlap(n*(split_size-n_share)+n_share,split_size)
            remainder=n*(split_size-n_share)+n_share-length   # Number of leftover pixels after each interval is allocated overlap constant
            for r in range(remainder):
                chunks[-r-1]=(chunks[-r-1][0]-remainder+r,chunks[-r-1][1]-remainder+r) # Shift overlap of final remainder to one pixel shared among the final chunks

    return chunks

def divis(im,grid,mode,image_mode):
    divisions=[]
    boxes=[]
    if mode=="number":                                      # We split the image into m x n subimages
        for axis in range(len(grid)):
            step=im[axis]//grid[axis]                       # Calculate dimensions of each subimage on each axis
            if im[axis]%step==0:
                divisions.append(overlap(im[axis],step))    # If image splits evenly, generate intevals
            else:
                if image_mode=="stop":                      # If image does not split evenly, either truncate it or create overlaps depending on image_mode
                    divisions.append(overlap(grid[axis]*step,step))
                else:
                    divisions.append(overlap(im[axis],step+1))
    elif mode=="size":                                      # Splits image up into subimages of fixed size (x x y)
        if image_mode=="stop":
            for axis in range(len(grid)):
                step=im[axis]//grid[axis]
                divisions.append(overlap(grid[axis]*step,grid[axis]))
        else:
            for axis in range(len(grid)):
                divisions.append(overlap(im[axis],grid[axis]))

    else:
        print("Mode is not correct")
    for i in range(len(divisions[0])):
        for j in range(len(divisions[1])):
            boxes.append((divisions[0][i][0],divisions[1][j][0],divisions[0][i][1],divisions[1][j][1]))
    #print(len(boxes))
    return boxes

# EXAMPLES

#print(divis((200,200),(4,6),mode="number",image_mode="stop"))
#print(divis((200,200),(7,3),mode="number",image_mode="overlap"))
#print(divis((190,200),(25,25),mode="size",image_mode="stop"))
#print(divis((190,200),(25,25),mode="size",image_mode="overlap"))

# FUNCTION TO PRODUCE A LIST OF IMAGES CUT FROM A LARGER IMAGE

def cuttings(im,cuts):
    cutlist=[]
    for box in cuts:
        cutlist.append(im.crop(box))
    return cutlist

# FUNCTION TO SAVE A LIST OF IMAGES TO A GIVEN FILENAME, FORMAT AND DIRECTORY

# ims = list of Image objects
# names = tuple of the form (root_directory,new_directory,filename_stem)
# img_type = file format of image


import os,time

now=list(time.localtime())
datestamp=" ("+str(now[2])+"-"+str(now[1])+"-"+str(now[0])+"-"+str(now[3])+"-"+str(now[4])+"-"+str(now[5])+")"
window=(72,72)
run_directory="image_windows "+str(window)+datestamp

def save_splits(ims, names, img_type):
    try:
        os.mkdir(names[0]+"\\"+names[1])
    except IOError:
        pass
    img_num=1
    for im in ims:
        name=names[0]+"\\"+names[1]+"\\"+names[2]+str(img_num)+"."+img_type
        im.save(name)
        img_num+=1

# ITERATE THROUGH FOLDER OF SONAR IMAGES

total_images=0
for i in range(1,len(images)+1):
    im=images[i][1] #.convert("L")
    lattice_points=divis(im.size,window,"size","overlap")
    im_slices=cuttings(im,lattice_points)
    total_images+=len(im_slices)
    save_splits(im_slices,(sonardir,run_directory,"im"+str(i)+"_slice"),"jpg")
    try:
        os.mkdir(sonardir+"\\"+run_directory+"\\relabelled_images")
    except IOError:
        pass
    im.save(sonardir+"\\"+run_directory+"\\relabelled_images"+"\\im"+str(i)+".jpg")
print(total_images)'''


