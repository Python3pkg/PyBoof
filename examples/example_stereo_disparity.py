import numpy as np

import matplotlib.pyplot as plt
import pyboof as pb

# Enable use of memory mapped files for MUCH faster conversion between some python and boofcv data types
pb.init_memmap(5)

# Load two images
image0 = pb.load_single_band("../data/example/stereo/sundial01_left.jpg", np.uint8)
image1 = pb.load_single_band("../data/example/stereo/sundial01_right.jpg", np.uint8)

# Load stereo rectification
stereo_param = pb.StereoParameters()
stereo_param.load("../data/example/calibration/stereo/Bumblebee2_Chess/stereo.xml")

# Rectify and undistort the images
model_rectifier = pb.StereoRectification(stereo_param.left, stereo_param.right, stereo_param.right_to_left)
model_rectifier.full_view_left()

distort_left = model_rectifier.create_distortion(pb.ImageType(image0.getImageType()), True)
distort_right = model_rectifier.create_distortion(pb.ImageType(image0.getImageType()), False)

rect0 = image0.createSameShape()
rect1 = image1.createSameShape()

distort_left.apply(image0, rect0)
distort_right.apply(image1, rect1)

# Configure and compute disparity
config = pb.ConfigStereoDisparity()
config.minDisparity = 0
config.maxDisparity = 40

factory = pb.FactoryStereoDisparity(np.uint8)

disparityAlg = factory.region_wta(config)

disparityAlg.process(rect0, rect1)

disparity_image = pb.boof_to_ndarray(disparityAlg.get_disparity_image())

plt.imshow(disparity_image)
plt.show()

print "Done!"