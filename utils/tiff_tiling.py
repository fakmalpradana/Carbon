import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from PIL import Image
import PIL

PIL.Image.MAX_IMAGE_PIXELS = 933120000

def get_transform(image_path):
    with rasterio.open(image_path) as src:
        transform = src.transform
        crs = src.crs
        return transform, crs

def remove_alpha_channel(image):
    if image.mode == "RGBA":
        return image.convert("RGB")
    else:
        return image
    
'''
# untuk data RGB
def split_image(image_path, output_folder):
    image = Image.open(image_path)
    image = remove_alpha_channel(image)
    width, height = image.size
    section_size = 512
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    transform, crs = get_transform(image_path)
    x_origin, y_origin = transform[2], transform[5]

    for i in range(0, width, section_size):
        for j in range(0, height, section_size):
            section = image.crop((i, j, i + section_size, j + section_size)).convert("RGB")  # Convert to RGB
            section_width, section_height = section.size
            if section_width == section_height == section_size:
                # Create a new TIFF file for each section
                filename = f"section_{np.int8(i/section_size)}_{np.int8(j/section_size)}.tif"
                with rasterio.open(os.path.join(output_folder, filename), 'w', driver='GTiff', 
                                    width=section_size, height=section_size, count=3, dtype=np.uint8,
                                    crs=crs, transform=from_origin(x_origin + i * transform[0], 
                                    y_origin + (j-320) * transform[4] + section_size * transform[4], 
                                    transform[0], -transform[4])) as dst:
                    # Convert PIL image to NumPy array properly
                    np_section = np.array(section)
                    print(np_section.shape)
                    dst.write(np.moveaxis(np_section, [0,1,2], [1,2,0]))

'''


# untuk data grayscale
def split_image(image_path, output_folder):
    image = Image.open(image_path)
    image = remove_alpha_channel(image)
    width, height = image.size
    section_size = 512
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    transform, crs = get_transform(image_path)
    x_origin, y_origin = transform[2], transform[5]

    for i in range(0, width, section_size):
        for j in range(0, height, section_size):
            section = image.crop((i, j, i + section_size, j + section_size))
            section_width, section_height = section.size
            if section_width == section_height == section_size:
                # Create a new TIFF file for each section
                filename = f"section_{np.int8(i/section_size)}_{np.int8(j/section_size)}.tif"
                with rasterio.open(os.path.join(output_folder, filename), 'w', driver='GTiff', 
                                    width=section_size, height=section_size, count=1, dtype=np.uint8,
                                    crs=crs, transform=from_origin(x_origin + i * transform[0], 
                                    y_origin + (j-320) * transform[4] + section_size * transform[4], 
                                    transform[0], -transform[4])) as dst:
                    # Convert PIL image to NumPy array properly
                    np_section = np.array(section)
                    np_section = np.expand_dims(np_section, axis=-1)
                    print(np_section.shape)
                    dst.write(np.moveaxis(np_section, [0,1,2], [1,2,0]))


if __name__ == "__main__":
    image_path = "data/jambi/jambi_mask.tif"  # Replace with your TIFF image path
    output_folder = "data/jambi/mask"  # Folder to save the sections
    
    split_image(image_path, output_folder)
    print("Image sections saved successfully.")
