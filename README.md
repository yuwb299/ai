# OCR to Word - 摄像头文字识别工具

通过摄像头识别文字，自动整理成Word文档。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 功能

- 启动摄像头实时预览
- 拍照识别文字
- 导入本地图片识别
- 保存识别结果为Word文档

## 目录结构

```
.
├── main.py              # 程序入口
├── requirements.txt     # 依赖
└── src/
    ├── config.py        # 配置
    ├── camera.py        # 摄像头管理
    ├── ocr_engine.py    # OCR引擎
    ├── doc_generator.py # Word生成器
    └── gui.py           # 界面
```
