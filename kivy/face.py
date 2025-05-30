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

    frameOpencvDnn = age_and_gender(frame,faceBoxes,frameOpencvDnn)



    return frameOpencvDnn, faceBoxes


def age_and_gender(frame,faceBoxes, frameOpencvDnn):
    for faceBox in faceBoxes:
        # получаем изображение лица на основе рамки
        face=frame[max(0,faceBox[1]):
                   min(faceBox[3],frame.shape[0]-1),max(0,faceBox[0])
                   :min(faceBox[2], frame.shape[1]-1)]
        # получаем на этой основе новый бинарный пиксельный объект
        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        # отправляем его в нейросеть для определения пола
        genderNet.setInput(blob)
        # получаем результат работы нейросети
        genderPreds=genderNet.forward()
        # выбираем пол на основе этого результата
        gender=genderList[genderPreds[0].argmax()]
        # отправляем результат в переменную с полом

        # делаем то же самое для возраста
        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]

        # добавляем текст возле каждой рамки в кадре

        cv2.putText(frameOpencvDnn, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 255), 2, cv2.LINE_AA)
        return frameOpencvDnn




video = cv2.VideoCapture(0)

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
faceNet = cv2.dnn.readNet(faceModel, faceProto)

genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"

# настраиваем свет
MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
# итоговые результаты работы нейросетей для пола и возраста
genderList=['Male ','Female']
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

# запускаем нейросети по определению пола и возраста
genderNet=cv2.dnn.readNet(genderModel,genderProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)


def loadFromImg(path):

    frame = cv2.imread(path)
    if type(frame) != type(None):

        resultImg, faceBoxes = highlightFace(faceNet, frame)

        if not faceBoxes:
            print("Лица не распознаны")




        else:
            return cv2.cvtColor(resultImg, cv2.COLOR_BGR2RGB)




def loadFromCam():

    hasFrame, frame = video.read()

    resultImg, faceBoxes = highlightFace(faceNet, frame)

    if not faceBoxes:
        print("Лица не распознаны")

    else:
        return cv2.cvtColor(resultImg, cv2.COLOR_BGR2RGB)






