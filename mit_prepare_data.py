import tensorflow as tf

import os
import json
import numpy as np

def load_test_set(data_dir='data', test_file='TestImages.txt'):
    full_path = os.path.join(data_dir, 'mit67')

    try:
        print("Trying to load previously generated data and labels")
        x_test = np.load(os.path.join(full_path, 'x_test.npy'))
        y_test = np.load(os.path.join(full_path, 'y_test.npy'))
        
    except IOError:
        print("Not found, generating...")
        with open(os.path.join(full_path, test_file), 'r') as f:
            test_images = [os.path.join(full_path, l.strip()) for l in f.readlines()]

        with open(os.path.join(full_path, "class_labels.json"), 'r') as f:
            labels = json.load(f)

        test_labels = [labels[s.split('/')[-2]] for s in test_images]
        processed_images = np.empty((len(test_images), 224, 224, 3))
        for i, image in enumerate(test_images):
            image = tf.io.read_file(image)
            image = tf.image.decode_jpeg(image, channels=3)
            image = tf.cast(image, tf.float32)
            image = (image/127.5) - 1
            image = tf.image.resize(image, (224, 224))
            processed_images[i] = image

        x_test = processed_images
        y_test = np.array(test_labels)

        print("Saving numpy arrays")
        np.save(os.path.join(full_path, 'x_test.npy'), x_test)
        np.save(os.path.join(full_path, 'y_test.npy'), y_test)

    return x_test, y_test