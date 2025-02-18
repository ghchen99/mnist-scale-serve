import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

def create_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model():
    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    # Normalize and reshape
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)
    
    # Create and train model
    model = create_model()
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))
    return model

def get_model():
    model_path = '/app/models/mnist_model.keras'
    try:
        # Try to load existing model
        if os.path.exists(model_path):
            print("Loading existing model...")
            model = tf.keras.models.load_model(model_path)
        else:
            print("Training new model...")
            model = train_model()
            model.save(model_path)
            print("Model saved successfully")
    except Exception as e:
        print(f"Error loading/training model: {str(e)}")
        raise
    return model