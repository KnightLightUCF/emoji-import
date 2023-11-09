import cv2
import numpy as np
import skimage.morphology
from PIL import ImageTk, Image, ImageDraw, ImageFont
from stl import mesh
import numpy

img = cv2.imread("/Users/stevenholmes/OneDrive/Knight_Light 11.1.2023/emoji-import/emoji_image.png")
ht, wd = img.shape[:2]

# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# create a binary thresholded image
thresh = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# invert so lines are white
thresh = 1 - thresh

# apply skeletonization
skeleton = skimage.morphology.skeletonize(thresh)
skeleton = (255*skeleton).clip(0,255).astype(np.uint8)

# save result
cv2.imwrite("lines_test.png", skeleton)


img=Image.open('lines_test.png')
img = img.convert('L')
image_array = np.array(img)

edges = cv2.Canny(image_array, threshold1=10, threshold2=10)

vertices = []
height = 0.0
# Calculates vertices and creates a mesh from the x,y values.
for y in range(skeleton.shape[0]):
    for x in range(skeleton.shape[1]):
        if skeleton[y,x]>0:
            vertices.append((x,y,height))
emoji_mesh = mesh.Mesh(np.zeros(len(vertices), dtype=mesh.Mesh.dtype))

for i, vertex in enumerate(vertices):
    emoji_mesh.vectors[i] = [vertex]

# Save the STL file
emoji_mesh.save('emoji_test.stl')