#0.1 - A basic application using PyQt6

import sys
from PyQt6.QtWidgets    import QApplication, QWidget, QLabel


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Setting up the App's GUI"""
        self.setGeometry(0,0,300,300)
        self.setWindowTitle("QLabel Example")
        self.setUpMainWindow()
        self.centerOnScreen()
        self.show()

    def setUpMainWindow(self):
        """Here is where we create the window components"""
        hello_label = QLabel(self)
        hello_label.setText('Hello Gen-Z!')

    def centerOnScreen(self):
        """Function to center the window on the screen"""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
