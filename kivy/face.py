import cv2
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()

    frameHight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]

    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300,300), (104, 117, 123), True, False)

    net.setInput(blob)

    detections = net.forward()

    faceBoxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence >= conf_threshold:
            x1 = int(detections[0,0,i,3]* frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHight)

            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHight)

            faceBoxes.append([x1, y1, x2, y2])

            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 225, 0), int(round(frameHight/150)), 8)

    return frameOpencvDnn, faceBoxes


video = cv2.VideoCapture(0)

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
faceNet = cv2.dnn.readNet(faceModel, faceProto)

def loadFromImg(path):

    frame = cv2.imread(path)
    if type(frame) != type(None):

        resultImg, faceBoxes = highlightFace(faceNet, frame)

        if not faceBoxes:
            print("Лица не распознаны")

        cv2.imshow("Face recognition", resultImg)

def loadFromCam():

    hasFrame, frame = video.read()

    resultImg, faceBoxes = highlightFace(faceNet, frame)

    if not faceBoxes:
        print("Лица не распознаны")

    cv2.imshow("Face recognition", resultImg)




