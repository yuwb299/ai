from paddleocr import PaddleOCR
from src.config import OCR_LANG


class OCREngine:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=OCR_LANG, show_log=False)
    
    def recognize(self, image):
        result = self.ocr.ocr(image, cls=True)
        texts = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                position = line[0]
                texts.append({
                    "text": text,
                    "confidence": confidence,
                    "position": position
                })
        return texts
    
    def get_full_text(self, image):
        results = self.recognize(image)
        return "\n".join([r["text"] for r in results])
