from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
import sys, cv2, threading, random
from Camera_GUI import CameraWindow

class MyWidget:
    def __init__(self):
        super().__init__()
        self.window_camera = CameraWindow()
        # self.setUpdatesEnabled(True)
        self.ocv = True
        self.window_w, self.window_h = 640, 480   # 設定視窗長寬
        self.scale = 1                   # 影片高度的比例
        self.photo= False    # 按下拍照紐時的參考變數，預設 False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')    # 設定存檔影片格式
        self.recorderType = False                        # 設定是否處於錄影狀態，預設 False
        # self.ui()
        self.window_camera.record_button.clicked.connect(self.takePhoto)
        self.window_camera.stop_button.clicked.connect(self.recordVideo)




    def closeEvent(self, event):
        self.ocv = False            # 關閉視窗後，設定成 False
        try:
            self.output.release()   # 關閉視窗後，釋放儲存影片的資源
        except:
            pass                    # 如果沒有按下錄製影片按鈕，就略過



    # 按下拍照扭的動作
    def takePhoto(self):
        self.photo = True           # 變數設定為 True

    # 按下錄影按鈕的動作
    def recordVideo(self):
        if self.recorderType == False:
            # 如果按下按鈕時沒有在錄影
            # 設定錄影的檔案
            self.output = cv2.VideoWriter('difficult.mp4', self.fourcc, 30.0, (self.window_w,int(self.window_h*self.scale)))
            self.recorderType = True                   # 改為 True 表示正在錄影
            
        else:
            # 如果按下按鈕時正在錄影
            self.output.release()                    # 釋放檔案資源
            self.recorderType = False                # 改為 False 表示停止錄影

    def opencv(self):
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        while self.ocv:
            ret, frame = self.cap.read()             # 讀取影格
            if not ret:
                print("Cannot receive frame")
                break
            frame = cv2.resize(frame, (self.window_w, int(self.window_h*self.scale)))  # 改變尺寸符合視窗
            if self.photo == True:
                self.photo = False                   # 按下拍照鈕時，會先設定 True，觸發後再設回 False
                cv2.imwrite('1.jpg', frame) # 儲存圖片
            if self.recorderType == True:
                self.output.write(frame)             # 按下錄影時，將檔案儲存到 output
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 改為 RGB
            height, width, channel = frame.shape
            # 278, 480, 3
            bytesPerline = channel * width
            img = QImage(frame, width, height, bytesPerline, QImage.Format.Format_RGB888) # 產生圖片
            # print(img.size())  # 印出圖片大小
            self.window_camera.camera_label.setPixmap(QPixmap.fromImage(img))   # 顯示圖片

    def show(self):
        self.window_camera.closeEvent = self.closeEvent
        self.window_camera.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    video = threading.Thread(target=Form.opencv)
    video.start()
    Form.show()
    sys.exit(app.exec())