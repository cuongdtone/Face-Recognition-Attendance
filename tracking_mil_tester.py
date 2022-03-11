import cv2
import sys
from insightface.model_zoo import RetinaFace

Face = RetinaFace(model_file='det_10g.onnx')

tracker = cv2.TrackerMIL_create()
video = cv2.VideoCapture("/home/cuong/Desktop/Speaking/GreenGlobal/Thuong_Chinh_Dien.mp4")

ok, frame = video.read()
# bbox = cv2.selectROI(frame)
# print(bbox) #box is tl_wh
#
bbox, _ = Face.detect(frame, max_num=0, metric='default', input_size=(640, 640))
bbox = bbox[0, :4]
bbox = [int(i) for i in bbox]
bbox[2] = bbox[2] - bbox[0]
bbox[3] = bbox[3] - bbox[1]

print(bbox)

ok = tracker.init(frame, bbox)

cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Tracking', (1280, 720))
count = 0
while True:
    # Read a new frame
    ok, frame = video.read()
    count +=1
    if not ok:
        break
    timer = cv2.getTickCount()
    print(timer)
    if count<10:
        ok, bbox = tracker.update(frame)
    else:
        bbox, _ = Face.detect(frame, max_num=0, metric='default', input_size=(640, 640))
        bbox = bbox[0, :4]
        bbox = [int(i) for i in bbox]
        bbox[2] = bbox[2] - bbox[0]
        bbox[3] = bbox[3] - bbox[1]
        tracker.init(frame, bbox)
        ok = True
        count = 0

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    #visualize
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.putText(frame,"MIL Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27: break