import math
import numpy as np
import matplotlib.pyplot as plt

# Set the parameters of the sine wave
amplitude = 1 # Amplitude of the wave
frequency = 1 # Frequency of the wave in Hertz
phase = 0 # Phase shift of the wave in radians
sampling_rate = 100 # Number of samples per second
duration = 1 # Duration of the wave in seconds

# Create a numpy array of time values from 0 to duration
time = np.linspace(0, 1, 1024, endpoint=False)

# Calculate the sine wave values for each time value
sine_wave = amplitude * np.sin(2 * np.pi * frequency * time + phase)

# Plot the sine wave
plt.plot(time, sine_wave)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Sine Wave Generator')
plt.show()