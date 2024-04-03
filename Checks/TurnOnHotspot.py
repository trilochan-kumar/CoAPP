import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Turn on Hotspot")
        self.button.clicked.connect(self.turn_on_hotspot)

        self.setCentralWidget(self.button)

    def turn_on_hotspot(self):
        # Get the current network adapter
        adapter = netsh.wlan.show_interfaces()[0]

        # Set the hotspot name and password
        adapter.set_hotspot_name("My Hotspot")
        adapter.set_hotspot_password("password")

        # Start the hotspot
        adapter.start_hotspot()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
