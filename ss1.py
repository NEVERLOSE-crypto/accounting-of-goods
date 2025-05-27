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
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 6:
                            self.items[idx] = ExportItem(*parts)
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(None, "Ошибка", 
                                         f"Файл {self.file_name} не найден!\n"
                                         f"Создайте файл в папке: {os.getcwd()}")
    
    def get_all_operations(self):
        return list(self.items.values())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Загрузка UI файла
        ui_path = os.path.join(os.path.dirname(__file__), 'export_analyser.ui')
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(None, "Ошибка", 
                                         f"Файл интерфейса не найден!\n"
                                         f"Ожидаемый путь: {ui_path}")
            sys.exit(1)
        
        # Инициализация анализатора
        self.analyser = ExportAnalyser()
        self.analyser.read_data_from_file()
        
        # Настройка таблицы
        self.tableOperations.setHorizontalHeaderLabels([
            "Товар", "Страна", "Импортер", 
            "Производитель", "Цена (руб)", "Объем (шт)"
        ])
        self.tableOperations.setSortingEnabled(True)
        
        # Подключение кнопок
        self.btnLoad.clicked.connect(self.load_table)
        self.btnClear.clicked.connect(self.clear_table)
    
    def load_table(self):
        try:
            # Перечитываем файл при каждой загрузке
            self.analyser.read_data_from_file()
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
                
                # Форматирование цены
                price_item = QTableWidgetItem(f"{item.price:,.2f}".replace(',', ' '))
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.tableOperations.setItem(row, 4, price_item)
                
                # Форматирование объема
                volume_item = QTableWidgetItem(f"{item.volume:,}".replace(',', ' '))
                volume_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.tableOperations.setItem(row, 5, volume_item)
            
            self.tableOperations.resizeColumnsToContents()
            self.tableOperations.sortByColumn(5, QtCore.Qt.AscendingOrder)  # Сортировка по объему
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{str(e)}")
    
    def clear_table(self):
        self.tableOperations.setRowCount(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Настройка стиля
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
