import cv2
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap
from src.config import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT


class CameraThread(QThread):
    frame_ready = pyqtSignal(QPixmap)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.camera = None
    
    def run(self):
        self.camera = cv2.VideoCapture(CAMERA_INDEX)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        self.running = True
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                image = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.frame_ready.emit(pixmap)
            self.msleep(30)
    
    def stop(self):
        self.running = False
        if self.camera:
            self.camera.release()
        self.wait()
    
    def capture_frame(self):
        if self.camera is None:
            return None
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None
