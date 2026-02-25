import os
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_onednn_backend"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"

import sys
from PyQt6.QtWidgets import QApplication
from src.gui import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
