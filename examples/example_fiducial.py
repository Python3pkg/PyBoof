import pyboof as pb

import numpy as np

data_path = "../data/example/fiducial/image/examples/"

# Load the camera parameters
intrinsic = pb.Intrinsic()
intrinsic.load_xml(data_path+"intrinsic.xml")

configFiducial = pb.ConfigFiducialImage()
configThreshold = pb.ConfigThreshold.create_local(pb.ThresholdType.LOCAL_SQUARE,10)

print("Configuring detector")
detector = pb.FactoryFiducial( np.uint8 ).squareImage(configFiducial,configThreshold)
detector.setIntrinsic(intrinsic)
detector.addPattern(pb.load_single_band(data_path+"../patterns/pentarose.png",np.uint8),4.0)
detector.addPattern(pb.load_single_band(data_path+"../patterns/yu.png",np.uint8),4.0)

print("Detecting image")
detector.detect(pb.load_single_band(data_path+"image00.jpg",np.uint8))

print("Number Found = "+str(detector.totalFound()))

for i in range(detector.totalFound()):
    print("=========== Found #"+str(i))
    fid_to_cam = detector.getFiducialToCamera(i)
    # print fid_to_cam
    print("Pattern ID = "+str(detector.get_id(i)))
    print("Rotation")
    print("  "+str(fid_to_cam.get_rotation()))
    print("Translation")
    print("  "+str(fid_to_cam.get_translation()))

    # TODO Render results