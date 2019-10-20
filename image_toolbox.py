# image_toolbox

# All tools for image manipulation and management, including the creation of augmentation policies.

# Prerequisites

import numpy as np
import cv2
from timeit import default_timer as t

# Image interaction

def image_dict(source_dir,*args,**kwargs):
    from os import listdir
    im_types=["jpg","png","bmp"]
    im_dict={name[:-4]:{"path":source_dir+"\\"+name} for name in listdir(source_dir) if name[-3:] in im_types}
    if "size" in args:
        for name in im_dict:
            im_dict[name]["dims"]=cv2.imread(im_dict[name]["path"],cv2.IMREAD_COLOR).shape[:2]
    if "type" in args:
        for name in im_dict:
            im_dict[name]["type"]=im_dict[name]["path"][-3:]
    return im_dict

def show_image(source):
    if source.__class__==str:
        im=cv2.imread(source)
    elif source.__class__==np.ndarray:
        im=source
    else:
        print("Source Not of Correct Type")
        return None
    cv2.imshow(None,im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def animate(images,*args,**kwargs):
    if "speed" in kwargs:
        s=kwargs["speed"]
    else:
        s=100

    if "duration" in kwargs:
        duration=kwargs["duration"]
    else:
        duration=10

    if "loop" in args:
        start=t()
        f=0
        total=len(images)
        while t()-start<duration:
            cv2.imshow(None,images[f])
            cv2.waitKey(s)
            f=(f+1)%total
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        for i in images:
            cv2.imshow(None,i)
            cv2.waitKey(s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process(image_src,functions,*args,**kwargs):
    if "save_dir" in kwargs:
        from os.path import exists
    if exists(kwargs["save_dir"])==False:
        from os import mkdir
        mkdir(kwargs["save_dir"])
    if image_src.__class__==dict:
        if "save_dir" not in kwargs:
            print("You must provide a save directory")
        else:
            if "annotate" not in kwargs:
                kwargs["annotate"]=""
            for name in image_src:
                if "greyscale" in args or "grayscale" in args:
                    im_array=cv2.imread(image_src[name]["path"],cv2.IMREAD_GRAYSCALE)
                else:
                    im_array=cv2.imread(image_src[name]["path"],cv2.IMREAD_COLOR)
                for function in functions:
                    im_array=function(im_array,*args,**kwargs)
                    #show_image(im_array)
                cv2.imwrite(kwargs["save_dir"]+"\\"+name+kwargs["annotate"]+".jpg",im_array)

    elif image_src.__class__==np.ndarray:
        for function in functions:
            image_src=function(image_src,*args,**kwargs)
            #show_image(im_array)
            if "save_dir" in kwargs:
                if "annotate" not in kwargs:
                    kwargs["annotate"]=""
                cv2.imwrite(kwargs["save_dir"]+"\\"+name+kwargs["annotate"]+".jpg",image_src)
        return image_src
    else:
        print("Source Not of Correct Type")
        return None

def get_stats(im_dict,*args,**kwargs):
    if "max" in args:
        max_width=max([im_dict[im]["dims"][1] for im in im_dict])
        max_height=max([im_dict[im]["dims"][0] for im in im_dict])
        return (max_width,max_height)
    elif "min" in args:
        min_width=min([im_dict[im]["dims"][1] for im in im_dict])
        min_height=min([im_dict[im]["dims"][0] for im in im_dict])
        return (min_width,min_height)
    elif "mean" in args:
        mean_width=sum([im_dict[im]["dims"][1] for im in im_dict])//len(im_dict)
        mean_height=sum([im_dict[im]["dims"][0] for im in im_dict])//len(im_dict)
        return (mean_width,mean_height)
    elif "median" in args:
        median_width=sorted([im_dict[im]["dims"][1] for im in im_dict])[len(im_dict)//2]
        median_height=sorted([im_dict[im]["dims"][0] for im in im_dict])[len(im_dict)//2]
        return (median_width,median_height)
    elif "percentile" in kwargs:
        perc_width=sorted([im_dict[im]["dims"][1] for im in im_dict])[len(im_dict)*kwargs["percentile"]//100]
        perc_height=sorted([im_dict[im]["dims"][0] for im in im_dict])[len(im_dict)*kwargs["percentile"]//100]
        return (perc_width,perc_height)
    else:
        return None

# Transformations

