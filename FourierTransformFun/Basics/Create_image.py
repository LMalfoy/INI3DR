import numpy as np
import tifffile
import scipy.io.wavfile as wavfile

'''
Functions
'''

def generate_image(px):
    # Generates a random grayscale image
    # Note that values in the numpy array are stored as unsigned 8-bit integers
    return np.random.randint(0, 256, size=(px, px), dtype=np.uint8)

def generate_soundwave(sample_rate=44100, duration=1):
    # Generate a random soundwave
    # Duration is the duration in seconds, sample rate is the sample rate per second
    num_samples = int(sample_rate * duration)
    return np.random.uniform(-1, 1, num_samples)

def save_image(image_array, filename):
    # Save the image array to a file
    tifffile.imwrite(filename, image_array)

def save_soundwave(soundwave_array, filename, sample_rate=44100):
    # Save the soundwave array to a file
    wavfile.write(filename, sample_rate, soundwave_array)

# Example usage
if __name__ == "__main__":
    # Generate and save image
    image = generate_image(1024)
    save_image(image, "random_image.tif")

    # Generate and save a soundwave
    sound = generate_soundwave(44100, duration=5)
    save_soundwave(sound, "random_soundwave.wav")
