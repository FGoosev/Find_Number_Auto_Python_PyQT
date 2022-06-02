import os
import cv2
import numpy as np
import pytesseract
import imutils
from imutils import contours
import easyocr
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()
        self.finalLabel = QLabel()

        self.loadBtn = QPushButton("Загрузить")
        self.read = QPushButton("Считать")
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.finalLabel)
        layout.addWidget(self.loadBtn)
        layout.addWidget(self.read)

        self.loadBtn.clicked.connect(self.load)
        self.read.clicked.connect(self.readingNumber)
        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setFixedSize(QSize(700, 700))
        self.setCentralWidget(container)

    def load(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "./")
        self.src_pixmap = QPixmap(self.fname[0])
        pixmap = QPixmap()
        self.finalLabel.setPixmap(pixmap)
        self.label.setPixmap(self.src_pixmap)


    def readingNumber(self):
        img = cv2.imread(self.fname[0])
        height, weight, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts, _ = contours.sort_contours(cnts[0])

        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            if area > 3000:
                image = img[y:y + h, x:x + w]

                result = pytesseract.image_to_string(image, lang="rus+eng")
                if len(result) > 7:
                    self.finalLabel.setText(result)





app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

'''

'''