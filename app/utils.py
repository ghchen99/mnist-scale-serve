import numpy as np
from PIL import Image

def preprocess_image(image):
    # Convert to grayscale
    image = image.convert('L')
    
    # Resize to 28x28
    image = image.resize((28, 28))
    
    # Convert to numpy array and normalize
    image_array = np.array(image)
    image_array = image_array.astype('float32') / 255.0
    
    # Add channel dimension
    image_array = np.expand_dims(image_array, axis=-1)
    
    return image_array