# image_toolbox

# All tools for image manipulation and management, including the creation of augmentation policies.

# Prerequisites

import numpy as np
import cv2
from timeit import default_timer as t
from imutils import rotate as rot,rotate_bound as rot_bound # Aim to replace this with the getRotationMatrix from openCV

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

def resize(im,*args,**kwargs):
    if "inter" not in kwargs:
        kwargs["inter"]=cv2.INTER_LINEAR
    else:
        if kwargs["inter"]=="nearest":
            kwargs["inter"]=cv2.INTER_NEAREST
        elif kwargs["inter"]=="linear":
            kwargs["inter"]=cv2.INTER_LINEAR
        elif kwargs["inter"]=="cubic":
            kwargs["inter"]=cv2.INTER_CUBIC
        elif kwargs["inter"]=="lanczos":
            kwargs["inter"]=cv2.INTER_LANCZOS4
        elif kwargs["inter"]=="area":
            kwargs["inter"]=cv2.INTER_AREA
        else:
            kwargs["inter"]=cv2.INTER_LINEAR
    if "scale_to_width" in kwargs:
        return cv2.resize(im,(kwargs["scale_to_width"],round(im.shape[0]*kwargs["scale_to_width"]/im.shape[1])),
                          interpolation=kwargs["inter"])
    elif "scale_to_height" in kwargs:
        return cv2.resize(im,(round(im.shape[1]*kwargs["scale_to_height"]/im.shape[0]),kwargs["scale_to_height"]),
                          interpolation=kwargs["inter"])
    elif "ratios" in kwargs:
        return cv2.resize(im,(round(im.shape[1]*kwargs["ratios"][0]),round(im.shape[0]*kwargs["ratios"][1])),
                             interpolation=kwargs["inter"])
    elif "fit_dimensions" in kwargs:
        return cv2.resize(im,(kwargs["fit_dimensions"][0],kwargs["fit_dimensions"][1]),
                          interpolation=kwargs["inter"])
    else:
        return im


def reflect(im,*args,**kwargs):
    if "H" in args or "horizontal" in args:
        return cv2.flip(im,1)
    elif "V" in args or "vertical" in args:
        return cv2.flip(im,0)

def transpose(im,*args,**kwargs):
    if "reverse" in args:
        return cv2.transpose(cv2.flip(im,-1))
    else:
        return cv2.transpose(im)

def random_mix(*args,**kwargs):
    if "bounds" in kwargs:
        lower=kwargs["bounds"][0]
        upper=kwargs["bounds"][1]
    else:
        lower=0
        upper=10
    factors=[randint(lower,upper) for i in range(3)]
    while sum(factors)==0:
        factors=[randint(lower,upper) for i in range(3)]
    factors=[i/sum(factors) for i in factors]
    return factors

def channel_mix(im,*args,**kwargs):
    if im.shape[2]==1: # if greyscale, return the original image
        return im
    else:
        b,g,r=cv2.split(im) # Split into colour channels
    if "random" in args:
        kwargs["R"]="random"
        kwargs["B"]="random"
        kwargs["G"]="random"
    if "R"in kwargs:
        if kwargs["R"].__class__!=list:
            if kwargs["R"]=="random":
                r_factors=random_mix()
            else:
                r_factors=[1,0,0]
        elif len(kwargs["R"])!=3:
            r_factors=[1,0,0]
        else:
            r_factors=[i/sum(kwargs["R"]) for i in kwargs["R"]]
    if "G"in kwargs:
        if kwargs["G"].__class__!=list:
            if kwargs["G"]=="random":
                g_factors=random_mix()
            else:
                g_factors=[0,1,0]
        elif len(kwargs["G"])!=3:
            g_factors=[0,1,0]
        else:
            g_factors=[i/sum(kwargs["G"]) for i in kwargs["G"]]
    if "B"in kwargs:
        if kwargs["B"].__class__!=list:
            if kwargs["B"]=="random":
                b_factors=random_mix()
            else:
                b_factors=[0,0,1]
        elif len(kwargs["B"])!=3:
            b_factors=[0,0,1]
        else:
            b_factors=[i/sum(kwargs["B"]) for i in kwargs["B"]]
    if "LI" in args:
        mat=np.array[b_factors,g_factors,r_factors]
        while np.linalg.det(mat)==0:
            mat=mat+np.random.random((3,3))/5
            mat=np.transpose(np.transpose(mat)/np.sum(mat,axis=1))
        b_factors,g_factors,r_factors=mat[0],mat[1],mat[2]
    b_new=b*b_factors[0]+g*b_factors[1]+r*b_factors[2]
    g_new=b*g_factors[0]+g*g_factors[1]+r*g_factors[2]
    r_new=b*r_factors[0]+g*r_factors[1]+r*r_factors[2]
    im_new=np.array(cv2.merge((b_new,g_new,r_new)),int)
    return im_new

def pad(im,*args,**kwargs):
    pad_vector=[0,0,0,0]      # Instructions for number of pixels to pad top, bottom, left and right.
    if "padding" in kwargs:   # Take type of padding from kwargs and fill with black as default
        pad_rule=kwargs["padding"]
        if kwargs["padding"] not in ["constant","reflect","copy","wrap"]:
            pad_rule=cv2.BORDER_CONSTANT
            if "greyscale" in args:
                color=[0]
            else:
                color=[0,0,0]
        elif kwargs["padding"]=="constant":
            pad_rule=cv2.BORDER_CONSTANT
            if "pad_color" in kwargs:
                color=kwargs["pad_color"]
            else:
                if "greyscale" in args:
                    color=[0]
                else:
                    color=[0,0,0]
        elif kwargs["padding"]=="reflect":
            pad_rule=cv2.BORDER_REFLECT_101
        elif kwargs["padding"]=="copy":
            pad_rule=cv2.BORDER_REPLICATE
        elif kwargs["padding"]=="wrap":
            pad_rule=cv2.BORDER_WRAP
    else:
        pad_rule=cv2.BORDER_CONSTANT
        if "greyscale" in args:
            color=[0]
        else:
            color=[0,0,0]
    if "pad_to_fit" in kwargs:
        image_dims=im.shape[:2]
        new_dims=kwargs["pad_to_fit"]
        extra=[0,0]
        if image_dims[0]>=new_dims[0] and image_dims[1]>=new_dims[1]:
            return im
        if image_dims[0]<new_dims[0]:
            extra[0]=new_dims[0]-image_dims[0]
        if image_dims[1]<new_dims[1]:
            extra[1]=new_dims[1]-image_dims[1]
        if "align" in kwargs:
            if "left" in kwargs["align"] and "right" in kwargs["align"]:
                pad_vector[2]=extra[1]//2
                pad_vector[3]=extra[1]-pad_vector[2]
            elif "left" in kwargs["align"]:
                pad_vector[3]=extra[1]
            elif "right" in kwargs["align"]:
                pad_vector[2]=extra[1]
            else:
                pad_vector[2]=extra[1]//2
                pad_vector[3]=extra[1]-pad_vector[2]
            if "top" in kwargs["align"] and "bottom" in kwargs["align"]:
                pad_vector[1]=extra[0]//2
                pad_vector[0]=extra[0]-pad_vector[2]
            elif "top" in kwargs["align"]:
                pad_vector[1]=extra[0]
            elif "right" in kwargs["align"]:
                pad_vector[0]=extra[0]
            else:
                pad_vector[1]=extra[0]//2
                pad_vector[0]=extra[0]-pad_vector[2]
        else:
            pad_vector[1]=extra[0]//2
            pad_vector[0]=extra[0]-pad_vector[1]
            pad_vector[2]=extra[1]//2
            pad_vector[3]=extra[1]-pad_vector[2]
        if pad_rule==cv2.BORDER_CONSTANT:
            return cv2.copyMakeBorder(im,pad_vector[0],pad_vector[1],pad_vector[2],pad_vector[3],
                                     pad_rule,value=color)
        else:
            return cv2.copyMakeBorder(im,pad_vector[0],pad_vector[1],pad_vector[2],pad_vector[3],pad_rule)

# WE MIGHT WANT TO PAD TO SQUARE FOR PREPROCESSING

def square_image(im,*args,**kwargs):
    dims=im.shape[:2]
    if dims[0]==dims[1]:
        pass
    elif dims[0]<dims[1]:
        im=pad(im,pad_to_fit=(dims[1],dims[1]),*args,**kwargs)
    else:
        im=pad(im,pad_to_fit=(dims[0],dims[0]),*args,**kwargs)
    return im

def fit_to_stats(im_dict,mode,inter,*args,**kwargs):
    target_stats=get_stats(im_dict,mode)
    kwargs["inter"]=inter
    if "width" in args:
        kwargs["scale_to_width"]=target_stats[0]
        process(im_dict,[resize],*args,**kwargs)
    elif "height" in args:
        kwargs["scale_to_height"]=target_stats[1]
        process(im_dict,[resize],*args,**kwargs)
    else:
        kwargs["fit_dimensions"]=target_stats
        process(im_dict,[resize],*args,**kwargs)

def rotate(im, degrees,*args,**kwargs):
    if "anticlockwise" not in args:
        if "adjust_size" in args:
            im=rot_bound(im, degrees)
        else:
            im=rot(im, degrees)
    else:
        if "adjust_size" in args:
            im=rot_bound(im, -degrees)
        else:
            im=rot(im, -degrees)
    return im

def shear(im,*args,**kwargs):
    dims=im.shape[:2]
    if "shear_horz" in kwargs:
        affine=np.array([[1,kwargs["shear_horz"],0],[0,1,0]])
        new_dims=(round(dims[1]*(kwargs["shear_horz"]+1)),dims[0])
        im=cv2.warpAffine(im,affine,new_dims)
    elif "shear_vert" in kwargs:
        affine=np.array([[1,0,0],[kwargs["shear_vert"],1,0]])
        new_dims=(dims[1],round(dims[0]*(kwargs["shear_vert"]+1)))
        im=cv2.warpAffine(im,affine,new_dims)
    else:
        print("Neither horizontal not vertical shear factor given")
    return im

def blend(im1,im2,*args,**kwargs):
    pass

def jumble(im,*args,**kwargs):
    pass

def brightness(im,*args,**kwargs):
    if "fixed_increase" in kwargs:
        im=np.array(im,int)+kwargs["fixed_increase"]
        im=np.array(np.clip(im,0,255),dtype="uint8")
    elif "mult_factor" in kwargs:
        im=np.array(im,int)*kwargs["mult_factor"]
        im=np.array(np.clip(im,0,255),dtype="uint8")
    else:
        pass
    return im

def add_noise(im, *args,**kwargs):
    noise_dims=im.shape
    im=np.array(im,int) # Need to convert to int type to prevent modulo 255 behaviour
    if "gaussian" in kwargs:
        im+=np.array(np.random.normal(0,kwargs["gaussian"],size=noise_dims),dtype=int)
    elif "rayleigh" in kwargs:
        im+=np.array(np.random.rayleigh(kwargs["rayleigh"],size=noise_dims),dtype=int)
    elif "white" in kwargs:
        im+=np.array(np.random.randint(kwargs["white"][0],kwargs["white"][1],size=noise_dims),dtype=int)
    elif "brownian" in kwargs:
        im+=np.array(np.random.exponential(kwargs["brownian"],size=noise_dims),dtype=int)
    elif "s_and_p" in kwargs:
        if kwargs["s_and_p"].__class__==list:
            im+=np.array(np.random.choice([255,0,-255],size=noise_dims,
                                          p=[kwargs["s_and_p"][0],1-kwargs["s_and_p"][0]-kwargs["s_and_p"][1],kwargs["s_and_p"][1]]),dtype=int)
        else:
            im+=np.array(np.random.choice([255,0,-255],size=noise_dims,
                                          p=[kwargs["s_and_p"],1-2*kwargs["s_and_p"],kwargs["s_and_p"]]),dtype=int)
    elif "periodic" in kwargs:
        pass
    elif "speckle" in kwargs:
        pass
    elif "pg" in kwargs:
        pass
    elif "struct" in kwargs:
        pass
    elif "gamma" in kwargs:
        pass
    elif "random" in kwargs:
        pass
    else:
        pass
    return np.array(np.clip(im,0,255),dtype="uint8")

def denoise(im,*args,**kwargs):
    pass

# Check if output array is empty!

def crop(im,*args,**kwargs):
    dims=im.shape[:2]
    if "crop_centre" in kwargs:
        centre=kwargs["crop_centre"]
    else:
        centre=(dims[1]//2,dims[0]//2)
    if "crop_width" in kwargs:
        width_bounds=(centre[1]-kwargs["crop_width"]//2,centre[1]+kwargs["crop_width"]//2)
    else:
        width_bounds=(0,dims[0])
    if "crop_height" in kwargs:
        height_bounds=(centre[0]-kwargs["crop_height"]//2,centre[0]+kwargs["crop_height"]//2)
    else:
        height_bounds=(0,dims[1])
    height_bounds=np.clip(height_bounds,0,dims[1])
    width_bounds=np.clip(width_bounds,0,dims[0])
    im=im[height_bounds[0]:height_bounds[1],width_bounds[0]:width_bounds[1]]
    return im

def mask(im,mask,*args,**kwargs):
    pass

def histogram_shift(im,hist,*args,**kwargs):
    pass

def translate(im,*args,**kwargs):
    im_dims=im.shape[:2]
    if "horizontal_shift" in kwargs:
        if "vertical_shift" in kwargs:
            affine=np.array([[1,0,kwargs["horizontal_shift"]],[0,1,kwargs["vertical_shift"]]],dtype="float32")
            im=cv2.warpAffine(im,affine,(im_dims[1],im_dims[0]))
            return im
        else:
            affine=np.array([[1,0,kwargs["horizontal_shift"]],[0,1,0]])
            im=cv2.warpAffine(im,affine)
            return im
    else:
        if "vertical_shift" in kwargs:
            affine=np.array([[1,0,0],[0,1,kwargs["vertical_shift"]]])
            im=cv2.warpAffine(im,affine)
            return im
        else:
            return im

