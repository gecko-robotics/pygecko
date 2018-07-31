# Notes

Misc notes and code snippets for things

```python
import numpy as np

# Create a dummy matrix
img = np.ones((50, 50, 3), dtype=np.uint8) * 255
# Save the shape of original matrix.
img_shape = img.shape

message_image = np.ndarray.tobytes(img)

re_img = np.frombuffer(message_image, dtype=np.uint8)

# Convert back the data to original image shape.
re_img = np.reshape(re_img, img_shape)
```

# log viewer

https://www.npmjs.com/package/frontail

    frontail /var/log/system.log /var/log/wifi.log
