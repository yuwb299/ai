import cv2
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from src.camera import CameraThread
from src.ocr_engine import OCREngine
from src.doc_generator import DocGenerator
from src.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.camera_thread = CameraThread()
        self.ocr_engine = OCREngine()
        self.doc_generator = DocGenerator()
        self.captured_image = None
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = QVBoxLayout()
        
        self.video_label = QLabel()
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(self.video_label)
        
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("启动摄像头")
        self.btn_capture = QPushButton("拍照识别")
        self.btn_capture.setEnabled(False)
        self.btn_import = QPushButton("导入图片")
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_capture)
        btn_layout.addWidget(self.btn_import)
        left_panel.addLayout(btn_layout)
        
        main_layout.addLayout(left_panel)
        
        right_panel = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText("OCR识别结果将显示在这里...")
        right_panel.addWidget(QLabel("识别结果:"))
        right_panel.addWidget(self.result_text)
        
        btn_right_layout = QHBoxLayout()
        self.btn_save = QPushButton("保存为Word")
        self.btn_clear = QPushButton("清空")
        btn_right_layout.addWidget(self.btn_save)
        btn_right_layout.addWidget(self.btn_clear)
        right_panel.addLayout(btn_right_layout)
        
        main_layout.addLayout(right_panel)
    
    def _connect_signals(self):
        self.btn_start.clicked.connect(self._toggle_camera)
        self.btn_capture.clicked.connect(self._capture_and_recognize)
        self.btn_import.clicked.connect(self._import_image)
        self.btn_save.clicked.connect(self._save_to_word)
        self.btn_clear.clicked.connect(self._clear_result)
        self.camera_thread.frame_ready.connect(self._update_frame)
    
    def _toggle_camera(self):
        if self.camera_thread.running:
            self.camera_thread.stop()
            self.btn_start.setText("启动摄像头")
            self.btn_capture.setEnabled(False)
        else:
            self.camera_thread.start()
            self.btn_start.setText("停止摄像头")
            self.btn_capture.setEnabled(True)
    
    def _update_frame(self, pixmap):
        scaled = pixmap.scaled(
            self.video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_label.setPixmap(scaled)
    
    def _capture_and_recognize(self):
        self.captured_image = self.camera_thread.capture_frame()
        if self.captured_image is not None:
            self._process_image(self.captured_image)
    
    def _import_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                self.captured_image = image
                self._process_image(image)
    
    def _process_image(self, image):
        text = self.ocr_engine.get_full_text(image)
        self.result_text.setPlainText(text)
    
    def _save_to_word(self):
        text = self.result_text.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "警告", "没有可保存的内容！")
            return
        
        filepath = self.doc_generator.create_document(text)
        QMessageBox.information(self, "成功", f"文档已保存至:\n{filepath}")
    
    def _clear_result(self):
        self.result_text.clear()
        self.captured_image = None
    
    def closeEvent(self, event):
        if self.camera_thread.running:
            self.camera_thread.stop()
        event.accept()
