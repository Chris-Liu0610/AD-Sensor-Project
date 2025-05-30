import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app'))


def test_headpose_example():

    import cv2
    import numpy as np

    try:
        from app.model.headpose_example import FacePoseDetector
    except ImportError as e:
        print(f"ImportError: {e}")
        return

    detector = FacePoseDetector()
    cap = cv2.VideoCapture(0)
      
    if not cap.isOpened():
        print("無法開啟攝影機")
        return
    
    print("按 'q' 退出")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        frame = cv2.flip(frame, 1)
        rvec, tvec, nose_tip_2d = detector.detect_face_pose(frame)
        
        if rvec is not None:
            frame = detector.annotate_image(frame, rvec, tvec, nose_tip_2d)
            
        cv2.imshow('Face Pose Detection - Triple Arrows', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

   


if __name__ == "__main__":
    test_headpose_example()