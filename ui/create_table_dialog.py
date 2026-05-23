from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QCheckBox, QMessageBox, QHeaderView, QTextEdit
)
from PyQt5.QtCore import Qt
import database.connection as db

FIREBIRD_TYPES = [
    "INTEGER", "BIGINT", "SMALLINT", "FLOAT", "DOUBLE PRECISION",
    "NUMERIC", "DECIMAL", "CHAR", "VARCHAR", "DATE", "TIME",
    "TIMESTAMP", "BOOLEAN", "BLOB"
]

TYPES_WITH_LENGTH = ["CHAR", "VARCHAR", "NUMERIC", "DECIMAL"]


class CreateTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Tabla")
        self.setMinimumSize(750, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre de la tabla:"))
        self.input_name = QLineEdit()
        name_layout.addWidget(self.input_name)
        layout.addLayout(name_layout)

        layout.addWidget(QLabel("Columnas:"))

        self.columns_table = QTableWidget(0, 5)
        self.columns_table.setHorizontalHeaderLabels(
            ["Nombre", "Tipo", "Longitud/Precisión", "Escala", "NOT NULL"]
        )
        self.columns_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.columns_table)

        btn_cols_layout = QHBoxLayout()
        btn_add_col = QPushButton("+ Agregar columna")
        btn_add_col.clicked.connect(self.add_column)
        btn_remove_col = QPushButton("- Eliminar columna")
        btn_remove_col.clicked.connect(self.remove_column)
        btn_cols_layout.addWidget(btn_add_col)
        btn_cols_layout.addWidget(btn_remove_col)
        layout.addLayout(btn_cols_layout)

        layout.addWidget(QLabel("Vista previa del DDL:"))
        self.ddl_preview = QTextEdit()
        self.ddl_preview.setReadOnly(True)
        self.ddl_preview.setMaximumHeight(120)
        layout.addWidget(self.ddl_preview)

        btn_layout = QHBoxLayout()
        btn_preview = QPushButton("Generar DDL")
        btn_preview.clicked.connect(self.generate_ddl)
        btn_create = QPushButton("Crear Tabla")
        btn_create.clicked.connect(self.create_table)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_preview)
        btn_layout.addWidget(btn_create)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def add_column(self):
        row = self.columns_table.rowCount()
        self.columns_table.insertRow(row)

        name_item = QTableWidgetItem("")
        self.columns_table.setItem(row, 0, name_item)

        type_combo = QComboBox()
        for t in FIREBIRD_TYPES:
            type_combo.addItem(t)
        self.columns_table.setCellWidget(row, 1, type_combo)

        length_item = QTableWidgetItem("")
        self.columns_table.setItem(row, 2, length_item)

        scale_item = QTableWidgetItem("")
        self.columns_table.setItem(row, 3, scale_item)

        not_null_check = QCheckBox()
        not_null_check.setChecked(False)
        container = QWidget()
        cb_layout = QHBoxLayout(container)
        cb_layout.addWidget(not_null_check)
        cb_layout.setAlignment(Qt.AlignCenter)
        cb_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_table.setCellWidget(row, 4, container)

    def remove_column(self):
        row = self.columns_table.currentRow()
        if row >= 0:
            self.columns_table.removeRow(row)

    def build_ddl(self):
        table_name = self.input_name.text().strip().upper()
        if not table_name:
            return None, "Escribe el nombre de la tabla."

        if self.columns_table.rowCount() == 0:
            return None, "Agrega al menos una columna."

        columns = []
        for row in range(self.columns_table.rowCount()):
            name_item = self.columns_table.item(row, 0)
            if not name_item or not name_item.text().strip():
                return None, f"La columna {row + 1} no tiene nombre."

            col_name = name_item.text().strip().upper()
            type_combo = self.columns_table.cellWidget(row, 1)
            col_type = type_combo.currentText()

            length_item = self.columns_table.item(row, 2)
            length = length_item.text().strip() if length_item else ""

            scale_item = self.columns_table.item(row, 3)
            scale = scale_item.text().strip() if scale_item else ""

            container = self.columns_table.cellWidget(row, 4)
            not_null = False
            if container:
                cb = container.findChild(QCheckBox)
                if cb:
                    not_null = cb.isChecked()

            if col_type in ("NUMERIC", "DECIMAL"):
                if length and scale:
                    type_str = f"{col_type}({length},{scale})"
                elif length:
                    type_str = f"{col_type}({length})"
                else:
                    type_str = col_type
            elif col_type in ("CHAR", "VARCHAR"):
                if length:
                    type_str = f"{col_type}({length})"
                else:
                    type_str = f"{col_type}(100)"
            else:
                type_str = col_type

            null_str = " NOT NULL" if not_null else ""
            columns.append(f"    {col_name} {type_str}{null_str}")

        ddl = f"CREATE TABLE {table_name} (\n"
        ddl += ",\n".join(columns)
        ddl += "\n);"
        return ddl, None

    def generate_ddl(self):
        ddl, error = self.build_ddl()
        if error:
            QMessageBox.warning(self, "Error", error)
            return
        self.ddl_preview.setText(ddl)

    def create_table(self):
        ddl, error = self.build_ddl()
        if error:
            QMessageBox.warning(self, "Error", error)
            return

        self.ddl_preview.setText(ddl)

        try:
            db.execute_query(ddl)
            QMessageBox.information(self, "OK", f"Tabla creada exitosamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear la tabla:\n{str(e)}")
