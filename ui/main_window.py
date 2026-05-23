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

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Objetos")
        self.tree.itemClicked.connect(self.on_tree_item_clicked)

        self.categories = {}
        for name in ["Tablas", "Vistas", "Procedimientos", "Funciones",
                     "Triggers", "Indices", "Secuencias", "Usuarios", "Paquetes"]:
            item = QTreeWidgetItem([name])
            self.tree.addTopLevelItem(item)
            self.categories[name] = item

        left_layout.addWidget(self.tree)

        btn_new_table = QPushButton("+ Nueva Tabla")
        btn_new_table.clicked.connect(self.open_create_table)
        btn_new_view = QPushButton("+ Nueva Vista")
        btn_new_view.clicked.connect(self.open_create_view)
        btn_refresh = QPushButton("Actualizar")
        btn_refresh.clicked.connect(self.refresh_objects)

        left_layout.addWidget(btn_new_table)
        left_layout.addWidget(btn_new_view)
        left_layout.addWidget(btn_refresh)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.tabs = QTabWidget()

        self.ddl_tab = QWidget()
        ddl_layout = QVBoxLayout(self.ddl_tab)
        self.ddl_text = QTextEdit()
        self.ddl_text.setReadOnly(True)
        self.ddl_text.setPlaceholderText("Selecciona un objeto para ver su DDL")
        btn_modify = QPushButton("Modificar (Exportar DDL al editor SQL)")
        btn_modify.clicked.connect(self.export_ddl_to_editor)
        ddl_layout.addWidget(self.ddl_text)
        ddl_layout.addWidget(btn_modify)
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

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([240, 860])

        main_layout.addWidget(splitter)

    def load_objects(self):
        for category in self.categories.values():
            category.takeChildren()

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

    def refresh_objects(self):
        self.load_objects()

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

    def export_ddl_to_editor(self):
        ddl = self.ddl_text.toPlainText().strip()
        if not ddl:
            QMessageBox.warning(self, "Aviso", "Primero selecciona un objeto del árbol.")
            return
        self.sql_editor.setText(ddl)
        self.tabs.setCurrentIndex(1)

    def open_create_table(self):
        from ui.create_table_dialog import CreateTableDialog
        dialog = CreateTableDialog(self)
        if dialog.exec_():
            self.load_objects()

    def open_create_view(self):
        from ui.create_view_dialog import CreateViewDialog
        dialog = CreateViewDialog(self)
        if dialog.exec_():
            self.load_objects()

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
                self.load_objects()
                return

            columns, rows = result
            self.results_table.setColumnCount(len(columns))
            self.results_table.setHorizontalHeaderLabels(columns)
            self.results_table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.results_table.setItem(
                        row_idx, col_idx,
                        QTableWidgetItem(str(value) if value is not None else "")
                    )

        except Exception as e:
            QMessageBox.critical(self, "Error SQL", str(e))
