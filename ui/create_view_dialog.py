from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
import database.connection as db


class CreateViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Vista")
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre de la vista:"))
        self.input_name = QLineEdit()
        name_layout.addWidget(self.input_name)
        layout.addLayout(name_layout)

        layout.addWidget(QLabel("Sentencia SELECT:"))
        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("SELECT columna1, columna2 FROM tabla WHERE ...")
        layout.addWidget(self.sql_editor)

        layout.addWidget(QLabel("Vista previa del DDL:"))
        self.ddl_preview = QTextEdit()
        self.ddl_preview.setReadOnly(True)
        self.ddl_preview.setMaximumHeight(100)
        layout.addWidget(self.ddl_preview)

        btn_layout = QHBoxLayout()
        btn_preview = QPushButton("Generar DDL")
        btn_preview.clicked.connect(self.generate_ddl)
        btn_create = QPushButton("Crear Vista")
        btn_create.clicked.connect(self.create_view)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_preview)
        btn_layout.addWidget(btn_create)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def build_ddl(self):
        name = self.input_name.text().strip().upper()
        sql = self.sql_editor.toPlainText().strip()
        if not name:
            return None, "Escribe el nombre de la vista."
        if not sql:
            return None, "Escribe la sentencia SELECT."
        return f"CREATE VIEW {name} AS\n{sql}", None

    def generate_ddl(self):
        ddl, error = self.build_ddl()
        if error:
            QMessageBox.warning(self, "Error", error)
            return
        self.ddl_preview.setText(ddl)

    def create_view(self):
        ddl, error = self.build_ddl()
        if error:
            QMessageBox.warning(self, "Error", error)
            return
        self.ddl_preview.setText(ddl)
        try:
            db.execute_query(ddl)
            QMessageBox.information(self, "OK", "Vista creada exitosamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear la vista:\n{str(e)}")
