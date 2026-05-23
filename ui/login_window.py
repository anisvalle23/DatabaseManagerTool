from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox, QFormLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import database.connection as db


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Manager")
        self.setMinimumSize(650, 420)
        self.main_window = None
        self.setup_ui()

    def setup_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Database Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #722F37; margin-bottom: 6px;")
        outer_layout.addWidget(title)

        subtitle = QLabel("Firebird Database Administration Tool")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #C9A84C; font-size: 11px; font-weight: normal; margin-bottom: 16px;")
        outer_layout.addWidget(subtitle)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #C9A84C;")
        outer_layout.addWidget(line)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        left_layout = QVBoxLayout()
        saved_label = QLabel("Conexiones guardadas")
        saved_label.setStyleSheet("color: #722F37; font-size: 12px;")
        left_layout.addWidget(saved_label)
        self.connections_list = QListWidget()
        self.connections_list.setMinimumWidth(180)
        self.connections_list.itemClicked.connect(self.load_saved_connection)
        left_layout.addWidget(self.connections_list)

        right_layout = QVBoxLayout()
        new_conn_label = QLabel("Nueva conexión")
        new_conn_label.setStyleSheet("color: #722F37; font-size: 12px;")
        right_layout.addWidget(new_conn_label)

        form = QFormLayout()
        form.setSpacing(8)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Mi conexión")
        form.addRow("Nombre:", self.input_name)

        self.input_host = QLineEdit()
        self.input_host.setText("localhost")
        form.addRow("Host:", self.input_host)

        self.input_port = QLineEdit()
        self.input_port.setText("3050")
        form.addRow("Puerto:", self.input_port)

        self.input_database = QLineEdit()
        self.input_database.setPlaceholderText("/ruta/base.fdb")
        form.addRow("Base de datos:", self.input_database)

        self.input_user = QLineEdit()
        self.input_user.setText("SYSDBA")
        form.addRow("Usuario:", self.input_user)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        form.addRow("Contraseña:", self.input_password)

        right_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_save = QPushButton("Guardar conexión")
        btn_save.setStyleSheet("background-color: #C9A84C;")
        btn_save.clicked.connect(self.save_connection)
        btn_connect = QPushButton("Conectar")
        btn_connect.clicked.connect(self.connect)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_connect)
        right_layout.addLayout(btn_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        outer_layout.addSpacing(10)
        outer_layout.addLayout(main_layout)
        self.setLayout(outer_layout)

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
