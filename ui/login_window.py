from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt
import database.connection as db


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Manager - Conectar")
        self.setMinimumWidth(500)
        self.main_window = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Conexiones guardadas:"))
        self.connections_list = QListWidget()
        self.connections_list.itemClicked.connect(self.load_saved_connection)
        left_layout.addWidget(self.connections_list)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Nueva conexión"))

        form = QFormLayout()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nombre de la conexión")
        form.addRow("Nombre:", self.input_name)

        self.input_host = QLineEdit()
        self.input_host.setText("localhost")
        form.addRow("Host:", self.input_host)

        self.input_port = QLineEdit()
        self.input_port.setText("3050")
        form.addRow("Puerto:", self.input_port)

        self.input_database = QLineEdit()
        self.input_database.setPlaceholderText("C:/ruta/base.fdb")
        form.addRow("Base de datos:", self.input_database)

        self.input_user = QLineEdit()
        self.input_user.setText("SYSDBA")
        form.addRow("Usuario:", self.input_user)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        form.addRow("Contraseña:", self.input_password)

        right_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Guardar conexión")
        btn_save.clicked.connect(self.save_connection)
        btn_connect = QPushButton("Conectar")
        btn_connect.clicked.connect(self.connect)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_connect)

        right_layout.addLayout(btn_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def save_connection(self):
        name = self.input_name.text().strip()
        host = self.input_host.text().strip()
        port = self.input_port.text().strip()
        database = self.input_database.text().strip()
        user = self.input_user.text().strip()
        password = self.input_password.text()

        if not name or not host or not database or not user:
            QMessageBox.warning(self, "Error", "Completa todos los campos obligatorios.")
            return

        saved = db.save_connection(name, host, port, database, user, password)
        if saved:
            self.connections_list.addItem(name)
            QMessageBox.information(self, "OK", "Conexión guardada.")
        else:
            QMessageBox.warning(self, "Error", "Ya existe una conexión con ese nombre.")

    def load_saved_connection(self, item):
        name = item.text()
        for c in db.get_saved_connections():
            if c["name"] == name:
                self.input_name.setText(c["name"])
                self.input_host.setText(c["host"])
                self.input_port.setText(c["port"])
                self.input_database.setText(c["database"])
                self.input_user.setText(c["user"])
                self.input_password.setText(c["password"])
                break

    def connect(self):
        host = self.input_host.text().strip()
        port = self.input_port.text().strip()
        database = self.input_database.text().strip()
        user = self.input_user.text().strip()
        password = self.input_password.text()

        if not host or not database or not user:
            QMessageBox.warning(self, "Error", "Host, base de datos y usuario son obligatorios.")
            return

        try:
            db.connect(host, port, database, user, password)
            from ui.main_window import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
