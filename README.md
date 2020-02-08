# image_toolbox

A collection of tools useful for image manipulation and creation of data augmentation policies. It is important to note that all transformations treat an image as an array that contains integer values between 0 and 255, although in certain circumstances non-integer values in this range are valid as the functions will output in integer values only. When passing into training, however, these arrays are normalised by dividing through by 255.

## Image interaction

- **image_dict (source_dir,\*args)**: Rather than work with all images in the workspace, this creates a dictionary of all filepaths in a given directory. It will only add files of type .jpg, .bmp or .png to the dictionary. It has two optional arguments, "size" and "type" which will also add information on the dimensions and file type of each file.

- **show_image(source)**: Displays a single image. The input can be a filepath or an array. 

- **animate(images,\*args,\*\*kwargs)**: Take a list of images as input and will animate them. The optional argument "loop" will loop the list until the assigned duration is completed. This is 10s as default. Optional keyword argument "duration" allows this to be set. Optional keyword "speed" allows the time between each frame to be altered. 

- **process(image_src, functions,\*args,\*\*kwargs)**: Takes an image dictionary or image in the form of an array and applies a list of functions (transformations) to that image. If the optional argument "greyscale" or "grayscale" is used, then the resulting image will be so. If the source is a dictionary, a name for a save directory for the resulting images must be provided. The keyword "annotate" provides an additional identifier for each batch of processed images in the save directory so that muliple copies of transformed images can be saved to the same directory.

- **get_stats(image_dict,\args,\*\*kwargs)**: Takes an image dict which has entries for the dimensions of each image and returns some statistical measure of the set of the sizes of all the images. It can be an optional argument among "max","min","median" or "mean" which returns a tuple for (width, height) of the set. Similarly, the keyword "percentile" (0-100) gives the relevant percentile. This function is generally useful for deciding what dimensions to standardise a set of images to for feeding into a CNN.

## Geometric Transformations

- **resize(im,\*args,\*\*kwargs)**: The function takes an image array and changes its size according to the keyword arguments. By default, interpolation is linear, but this can be changed using the "inter" keyword with options being "nearest", "linear", "cubic", "lanczos" and "area" corresponding to nearest neighbour, linear, cubic, Lanczos and area (?) interpolation rules. The modes to be chosen via keywords are "scale_to_width", which will scale the image to a given width of pixels where the height also changes proportionally, "scale_to_height", with similar behaviour, "ratios", where the input is a tuple of the scale factors of (width, height) and "fit_dimensions", which specifies the pixels for (width, height) expicitly. THe first two preserve the aspect ratio of the original image, where the last two need not. 

- **reflect(im,\*args)**: Takes an image and flips horizontally, vertically or both. Accepts arguments "H"/"horizontal" or "V"/"vertical".

- **transpose(im,\*args)**: Takes an image and flips according to the transpose operation.  An optional argument "reverse" implements a "reverse transpose". Standard transpose is equivalent to the matrix operation whereas reverse transpose is a reflection across the other diagonal. Standard transposition is the same as a horizontal reflection followed by a 90 deg anticlockwise rotation or a vertical reflection followed by a 90 deg clockwise rotation. The reverse transosition can be obtained by reversing the order of the above. The reverse transpose is a 180 deg rotation of the regular transpose.

- **pad(im,\*args,\*\*kwargs)**: Takes an image as argument and accepts arguemts and keyword arguments to adjust settings. The "padding" keyword argument determins the type of padding and can take values "constant","copy","reflect" or "wrap". If not given, the default is constant colour black. If "greyscale" argument is given, the function knows to pad only a single layer. For constant padding, the keyword argument "pad_colour" is given, it most be a BGR vector if colour or a single integer value if greyscale. If the kwarg "pad_to_fit" is used, it must have the value of a tuple of the new dimensions. The alignment of the original image with regard to the new image is determined by the "align" kwarg that is a list containing descriptions from "top","bottom", "left" and "right". By default, the original is padded equally in all directions. 

- **square_image(im,\*args,\*\*kwargs)**: This takes all the same optional arguments and keyword arguments as the pad function but will automatically create a square image that will have dimensions of the longest side of the origianl. Useful for creating square images that can be subsequently resxaled for input into a CNN.

- **fit_to_stats(im_dict, mode, \*args, \*\*kwargs)**: This takes an image dictionary as input and fits to a size determined by the statistical properties of the images in that dictionary. Note that the dictionary "size" option must be used. The resize function is held within this function, so the arguments and keyword arguments there can be applied here. This includes the interpolation rules. The "mode" argument can be any of those in the get_stats funtion. 

- **rotate(im,degrees,\*args,\*\*kwargs)**: This takes an image and rotates it by the given number of degrees. The default is clockwise but can be changed by using the "anticlockwise" argument. The default is to not change the dimensions of the image, which leads to clipping of the rotated image. If the "adjust" argument is supplied, the image dimensions change to accomodate. The default and only background is black.

- **shear(im, \*\*kwargs)**: This takes an image and applies a shear transformation to it. It requires either the "shear_horz" or "shear_vert" keywords with corresponding floats. Both cannot be applied siumultaneously. The factor is the tangent of the shear angle with the axis perpendicular to the direction of shear. Thus the final image dimensions are extended in the direction of shear by a number of pixels equal to this factor multiplied by the length of the perpendicular direction in pixels.


## Statistical and Channel Transformations

- **invert(im,\*args,\*\*kwargs)**: This takes an image and inverts it to the negative of that image with all pixel values being mapped according to $ x'=255-x $.

- channel_mix
- random_mix
- jumble
- brightness
- blend
- add_noise
- denoise
- histogram_shift

## Deletion/Insertion Transformations

- **crop(im,\*args,\*\*kwargs)**: This takes an image and returns a rectangular selection of the original image. There are three optional keyword arguments, "crop_centre", "crop_width" and "crop_height". All coordinates are measured from the top left hand corner of the input image with the first coordinate being the vertical direction and the second coordinate being the horizontal direction. If the centre is not specified, then the crop is measured from this corner. The crop dimensions in pixels are set by the values of "crop_width" and "crop_height" which default to the dimensions of the original image if not stated. Note that crops extending beyond the bounds of the original image are automatically clipped.

- **mask(im,\*args,\*\*kwargs)**: This is the opposite of the crop function in that it returns the original image with the specified rectangular section removed. It has simalar keyword arguments ("mask_centre","mask_width" and "mask_height") that are defined as above, plus the optional "mask_colour". The value of "mask_colour" can be an RGB triple or a single value for greyscale with all values being integers in the range 0-255. The default colour is black.

- **translate(im,\*args,\*\*kwargs)**: Performs a translation of the original image while retaining the original image dimensions. Takes two possible keyword arguments, "horizontal_shift" and "vertical_shift" which are the number of pixels moved in the right and down directions respectively (coordinates are measured relative to the top left corner of the original image). By default, the background colour revealed by the image translation is black, but can be set according to the optional "bg_colour" keyword that takes values acceptable to the "mask_colour" argument. ** only the default is currently working
