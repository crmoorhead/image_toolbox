# image_toolbox

A collection of tools useful for image manipulation and creation of data augmentation policies. 

## Image interaction

- **image_dict (source_dir,\*args)**: Rather than work with all images in the workspace, this creates a dictionary of all filepaths in a given directory. It will only add files of type .jpg, .bmp or .png to the dictionary. It has two optional arguments, "size" and "type" which will also add information on the dimensions and file type of each file.

- **show_image(source)**: Displays a single image. The input can be a filepath or an array. 

- **animate(images,\*args,\**kwargs)**: Take a list of images as input and will animate them. The optional argument "loop" will loop the list until the assigned duration is completed. This is 10s as default. Optional keyword argument "duration" allows this to be set. Optional keyword "speed" allows the time between each frame to be altered. 

- **process(image_src, functions,\*args,\**kwargs)**: Takes an image dictionary or image in the form of an array and applies a list of functions (transformations) to that image. If the optional argument "greyscale" or "grayscale" is used, then the resulting image will be so. If the source is a dictionary, a name for a save directory for the resulting images must be provided. The keyword "annotate" provides an additional identifier for each batch of processed images in the save directory so that muliple copies of transformed images can be saved to the same directory.

- **get_stats(image_dict,\args,\**kwargs)**: Takes an image dict which has entries for the dimensions of each image and returns some statistical measure of the set of the sizes of all the images. It can be an optional argument among "max","min","median" or "mean" which returns a tuple for (width, height) of the set. Similarly, the keyword "percentile" (0-100) gives the relevant percentile. This function is generally useful for deciding what dimensions to standardise a set of images to for feeding into a CNN.

## Geometric Transformations

- Resize
- 


