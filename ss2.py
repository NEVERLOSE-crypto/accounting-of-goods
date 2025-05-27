import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore

class ExportItem:
    def __init__(self, product, country, importer, manufacturer, price, volume):
        self.product = product.strip()
        self.country = country.strip()
        self.importer = importer.strip()
        self.manufacturer = manufacturer.strip()
        self.price = float(price)
        self.volume = int(volume)

class ExportAnalyser:
    def __init__(self):
        self.items = {}
        self.file_name = 'exports.txt'
    
    def read_data_from_file(self):
        self.items = {}
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                for idx, line in enumerate(file):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 6:
                            self.items[idx] = ExportItem(*parts)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(None, "Ошибка", f"Файл {self.file_name} не найден")
    
    def get_all_operations(self):
        return list(self.items.values())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка UI файла
        ui_path = os.path.join(os.path.dirname(__file__), 'export_analyser.ui')
        uic.loadUi(ui_path, self)
        
        self.analyser = ExportAnalyser()
        self.analyser.read_data_from_file()
        
        # Подключение кнопок
        self.btnLoad.clicked.connect(self.load_table)
        self.btnClear.clicked.connect(self.clear_table)
        
        # Настройка таблицы
        self.tableOperations.setHorizontalHeaderLabels([
            "Товар", "Страна", "Импортер", 
            "Производитель", "Цена", "Объем"
        ])
        self.tableOperations.setSortingEnabled(True)
    
    def load_table(self):
        operations = sorted(
            self.analyser.get_all_operations(),
            key=lambda x: x.volume
        )
        
        self.tableOperations.setRowCount(len(operations))
        
        for row, item in enumerate(operations):
            self.tableOperations.setItem(row, 0, QTableWidgetItem(item.product))
            self.tableOperations.setItem(row, 1, QTableWidgetItem(item.country))
            self.tableOperations.setItem(row, 2, QTableWidgetItem(item.importer))
            self.tableOperations.setItem(row, 3, QTableWidgetItem(item.manufacturer))
            
            price_item = QTableWidgetItem(f"{item.price:.2f}")
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableOperations.setItem(row, 4, price_item)
            
            volume_item = QTableWidgetItem(str(item.volume))
            volume_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableOperations.setItem(row, 5, volume_item)
        
        self.tableOperations.resizeColumnsToContents()
    
    def clear_table(self):
        self.tableOperations.setRowCount(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())