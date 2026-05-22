from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTabWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import database.connection as db
import database.queries as queries


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Manager - Firebird")
        self.setMinimumSize(1100, 700)
        self.setup_ui()
        self.load_objects()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Objetos")
        self.tree.setMinimumWidth(220)
        self.tree.itemClicked.connect(self.on_tree_item_clicked)

        self.categories = {}
        for name in ["Tablas", "Vistas", "Procedimientos", "Funciones",
                     "Triggers", "Indices", "Secuencias", "Usuarios", "Paquetes"]:
            item = QTreeWidgetItem([name])
            self.tree.addTopLevelItem(item)
            self.categories[name] = item

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.tabs = QTabWidget()

        self.ddl_tab = QWidget()
        ddl_layout = QVBoxLayout(self.ddl_tab)
        self.ddl_text = QTextEdit()
        self.ddl_text.setReadOnly(True)
        self.ddl_text.setPlaceholderText("Selecciona un objeto para ver su DDL")
        ddl_layout.addWidget(self.ddl_text)
        self.tabs.addTab(self.ddl_tab, "DDL")

        self.sql_tab = QWidget()
        sql_layout = QVBoxLayout(self.sql_tab)
        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("Escribe tu sentencia SQL aquí...")
        self.sql_editor.setMaximumHeight(150)
        sql_layout.addWidget(QLabel("Editor SQL:"))
        sql_layout.addWidget(self.sql_editor)

        btn_run = QPushButton("Ejecutar")
        btn_run.clicked.connect(self.run_sql)
        sql_layout.addWidget(btn_run)

        self.results_table = QTableWidget()
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sql_layout.addWidget(QLabel("Resultados:"))
        sql_layout.addWidget(self.results_table)

        self.tabs.addTab(self.sql_tab, "SQL")

        right_layout.addWidget(self.tabs)

        splitter.addWidget(self.tree)
        splitter.addWidget(right_panel)
        splitter.setSizes([220, 880])

        main_layout.addWidget(splitter)

    def load_objects(self):
        try:
            for name in queries.get_tables():
                QTreeWidgetItem(self.categories["Tablas"], [name])

            for name in queries.get_views():
                QTreeWidgetItem(self.categories["Vistas"], [name])

            for name in queries.get_procedures():
                QTreeWidgetItem(self.categories["Procedimientos"], [name])

            for name in queries.get_functions():
                QTreeWidgetItem(self.categories["Funciones"], [name])

            for name in queries.get_triggers():
                QTreeWidgetItem(self.categories["Triggers"], [name])

            for name in queries.get_indexes():
                QTreeWidgetItem(self.categories["Indices"], [name])

            for name in queries.get_sequences():
                QTreeWidgetItem(self.categories["Secuencias"], [name])

            for name in queries.get_users():
                QTreeWidgetItem(self.categories["Usuarios"], [name])

            for name in queries.get_packages():
                QTreeWidgetItem(self.categories["Paquetes"], [name])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los objetos:\n{str(e)}")

    def on_tree_item_clicked(self, item, column):
        parent = item.parent()
        if parent is None:
            return

        category = parent.text(0)
        name = item.text(0).split(" (")[0]
        ddl = ""

        try:
            if category == "Tablas":
                ddl = queries.get_table_ddl(name)
            elif category == "Vistas":
                ddl = queries.get_view_ddl(name)
            elif category == "Procedimientos":
                ddl = queries.get_procedure_ddl(name)
            elif category == "Funciones":
                ddl = queries.get_function_ddl(name)
            elif category == "Triggers":
                ddl = queries.get_trigger_ddl(name)
            else:
                ddl = f"-- DDL no disponible para {category}"
        except Exception as e:
            ddl = f"-- Error al obtener DDL: {str(e)}"

        self.ddl_text.setText(ddl)
        self.tabs.setCurrentIndex(0)

    def run_sql(self):
        sql = self.sql_editor.toPlainText().strip()
        if not sql:
            return

        try:
            result = db.execute_query(sql)
            self.results_table.clear()
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)

            if result is None:
                QMessageBox.information(self, "OK", "Sentencia ejecutada correctamente.")
                return

            columns, rows = result
            self.results_table.setColumnCount(len(columns))
            self.results_table.setHorizontalHeaderLabels(columns)
            self.results_table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value is not None else ""))

        except Exception as e:
            QMessageBox.critical(self, "Error SQL", str(e))
