import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtGui import QIcon
import socket
import CoAP_encoder
import CoAP_decoder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('CoAPP - A CoAP Client')
        self.setWindowIcon(QIcon('icon5.png'))

        self.setUpMainWindow()
        self.centerOnScreen()
        self.show()

    def setUpMainWindow(self):
        main_layout = QVBoxLayout(self)

        # IP Address
        ip_layout = QHBoxLayout()
        ip_label = QLabel('IP Address:')
        self.ip_edit = QLineEdit()
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_edit)
        main_layout.addLayout(ip_layout)

        # Port
        port_layout = QHBoxLayout()
        port_label = QLabel('Port:')
        self.port_edit = QLineEdit()
        self.port_edit.setText('5683')  # Default value
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_edit)
        main_layout.addLayout(port_layout)

        # CoAP Methods
        coap_layout = QHBoxLayout()
        coap_label = QLabel('CoAP Method:')
        self.get_checkbox = QCheckBox('GET')
        self.put_checkbox = QCheckBox('PUT')
        self.post_checkbox = QCheckBox('POST')
        self.delete_checkbox = QCheckBox('DELETE')
        self.get_checkbox.setChecked(True)  # Default selection
        self.get_checkbox.clicked.connect(lambda: self.handleCheckboxClick(self.get_checkbox))
        self.put_checkbox.clicked.connect(lambda: self.handleCheckboxClick(self.put_checkbox))
        self.post_checkbox.clicked.connect(lambda: self.handleCheckboxClick(self.post_checkbox))
        self.delete_checkbox.clicked.connect(lambda: self.handleCheckboxClick(self.delete_checkbox))
        coap_layout.addWidget(coap_label)
        coap_layout.addWidget(self.get_checkbox)
        coap_layout.addWidget(self.put_checkbox)
        coap_layout.addWidget(self.post_checkbox)
        coap_layout.addWidget(self.delete_checkbox)
        main_layout.addLayout(coap_layout)

        # Path Address
        path_layout = QHBoxLayout()
        path_label = QLabel('Path Address:')
        self.path_edit = QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        main_layout.addLayout(path_layout)

        # Payload
        self.payload_label = QLabel('Payload:')
        self.payload_edit = QLineEdit()
        self.payload_edit.setEnabled(False)  # Initially disabled
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_edit)
        main_layout.addLayout(payload_layout)

        # Send Button
        send_button = QPushButton('Send Request', self)
        send_button.clicked.connect(self.sendRequest)
        main_layout.addWidget(send_button)

        # Response Label
        self.response_label = QLabel('Response:')
        main_layout.addWidget(self.response_label)

        self.setLayout(main_layout)

    def centerOnScreen(self):
        """Function to center the window on the screen based on widget size"""
        main_layout = self.layout()  # Assuming you are using a QVBoxLayout or QHBoxLayout as the main layout

        # Calculate the size of the main layout (including all widgets)
        layout_width = main_layout.sizeHint().width()
        layout_height = main_layout.sizeHint().height()

        # Calculate the center position for the window
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - layout_width) // 2
        y = (screen_geometry.height() - layout_height) // 2

        # Set the geometry of the window to adjust its size and position
        self.setGeometry(x, y, layout_width, layout_height)


    def handleCheckboxClick(self, checkbox):
        # Uncheck other checkboxes when one is clicked
        checkboxes = [self.get_checkbox, self.put_checkbox, self.post_checkbox, self.delete_checkbox]
        for cb in checkboxes:
            if cb != checkbox:
                cb.setChecked(False)
        self.updatePayloadState()

    def updatePayloadState(self):
        # Disable payload for GET and DELETE methods
        self.payload_edit.setEnabled(not (self.get_checkbox.isChecked() or self.delete_checkbox.isChecked()))

    def sendRequest(self):
        ip_address = self.ip_edit.text()
        port = int(self.port_edit.text())

        # Check which HTTP method is selected
        if self.get_checkbox.isChecked():
            method = 'GET'
        elif self.put_checkbox.isChecked():
            method = 'PUT'
        elif self.post_checkbox.isChecked():
            method = 'POST'
        elif self.delete_checkbox.isChecked():
            method = 'DELETE'
        else:
            QMessageBox.critical(self, 'Error', 'Please select a COAP method.')
            return

        path = self.path_edit.text()
        payload = self.payload_edit.text()

        # Connect to the server and send the CoAP request
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(5)
        client_socket.connect((ip_address, port))

        built_packet = CoAP_encoder.build_packet(
            method=method,
            option=11,
            option_value=path,
            payload=payload)

        client_socket.send(built_packet)

        # Receive and process the response packet
        try:
            received_data = client_socket.recv(1024)
        except socket.timeout:
            QMessageBox.warning(self, 'Timeout', 'Receiving packet timed out...')
        else:
            decoded_packet = CoAP_decoder.decode_packet(received_data)
            response_text = f'Response for {method}: {decoded_packet[-1:]}'
            self.response_label.setText(response_text)

        client_socket.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
