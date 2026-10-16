# Step 1
from lesson_setup import *
phase = np.linspace(0, 1, 100, endpoint=False)
shape = np.sin(2*np.pi*phase) + 0.5*np.cos(4*np.pi*phase)
shape /= np.sqrt(np.mean(shape**2))
residuals = candidate[:, None] * shape
residual_movie(baseline, candidate)

# Step 2
replicated = np.repeat(residuals, 10, axis=1)
assert replicated.shape == (5, 1000)
assert np.allclose(np.sqrt(np.mean(replicated**2, axis=1)), candidate)
print("Independent specimens:", replicated.shape[0])
residual_movie(baseline, candidate)
print("Complete: inspect assets/lesson and animations in the file browser.")
