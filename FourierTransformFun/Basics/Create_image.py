import numpy as np
import tifffile
import scipy.io.wavfile as wavfile

'''
Generation functions
'''
# IMAGE STUFF
def generate_image(px=1024):
    # Generates a random grayscale image
    # Note that values in the numpy array are stored as unsigned 8-bit integers
    return np.random.randint(0, 256, size=(px, px), dtype=np.uint8)

def generate_image_with_sine_waves(px=1024, x_freq=1, y_freq=2):
    # Generate time vectors
    x = np.linspace(0, 1, px)
    y = np.linspace(0, 1, px)

    # Generate time vector grids
    xx, yy = np.meshgrid(x, y)

    # Calculate pixel values using sine waves
    x_phase = 0 # in radians
    y_phase = 0 # in radians
    sine_wave_x = np.sin(2 * np.pi * x_freq * xx + x_phase)
    sine_wave_y = np.sin(2 * np.pi * y_freq * yy + y_phase)

    # Combine sine waves along the x and y directions
    image_array = (sine_wave_x + sine_wave_y) * 127.5 + 127.5 # Scaling to 0-255 grayscale

    # Clip pixel values to ensure they are within valid range [0, 255]
    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    return image_array


# SOUND STUFF
def generate_soundwave(sample_rate=44100, duration=1):
    # Generate a random soundwave
    # Duration is the duration in seconds, sample rate is the sample rate per second
    num_samples = int(sample_rate * duration)
    return np.random.uniform(-1, 1, num_samples)


'''
Saving functions
'''

def save_image(image_array, filename):
    # Save the image array to a file
    tifffile.imwrite(filename, image_array)

def save_soundwave(soundwave_array, filename, sample_rate=44100):
    # Save the soundwave array to a file
    wavfile.write(filename, sample_rate, soundwave_array)

'''
Example usage
'''


if __name__ == "__main__":
    # Generate and save image
    image = generate_image(1024)
    save_image(image, "random_image.tif")

    # Generate and save a soundwave
    sound = generate_soundwave(44100, duration=5)
    save_soundwave(sound, "random_soundwave.wav")

    # Testing
    sine_image = generate_image_with_sine_waves(px=1024)
    save_image(sine_image, "sine_image.tif")
