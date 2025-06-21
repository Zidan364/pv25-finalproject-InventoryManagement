import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QMessageBox, QTableWidgetItem, QFileDialog
)
from PyQt6.QtCore import QDate
from ui_inventory import Ui_MainWindow
from database import init_db, tambah_data, ambil_semua_data, hapus_data, edit_data

STUDENT_NAME = "Zidan Shoni Ikram"
STUDENT_ID = "F1D022165"

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set status bar
        student_label = QLabel(f"{STUDENT_NAME} - {STUDENT_ID}")
        self.statusBar().addPermanentWidget(student_label)

        # Set default pilihan dan tanggal
        self.ui.comboKategori.addItems(["Makanan", "Minuman", "Alat Tulis", "Elektronik", "Lainnya"])
        self.ui.dateTanggalMasuk.setDate(QDate.currentDate())

        # Koneksi aksi tombol
        self.ui.actionKeluar.triggered.connect(self.close)
        self.ui.actionTentang.triggered.connect(self.show_about)
        self.ui.btnTambah.clicked.connect(self.tambah_data_inventory)
        self.ui.btnHapus.clicked.connect(self.hapus_data_inventory)
        self.ui.btnEdit.clicked.connect(self.edit_data_inventory)
        self.ui.btnCari.clicked.connect(self.cari_data)
        self.ui.btnExportCSV.clicked.connect(self.ekspor_ke_csv)
        self.ui.tableInventory.cellClicked.connect(self.pilih_data)

        self.load_data_to_table()

        self.setStyleSheet("""
            
            QWidget {
                background-color: white;
                color: black;
            }               
            QPushButton {
                padding: 6px 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton#btnTambah {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnEdit {
                background-color: #2196F3;
                color: white;
            }
            QPushButton#btnHapus {
                background-color: #f44336;
                color: white;
            }
            QPushButton#btnExportCSV {
                background-color: #ff9800;
                color: white;
            }
            QPushButton#btnCari {
                background-color: #9c27b0;
                color: white;
            }
            QLineEdit, QPlainTextEdit, QComboBox, QDateEdit {
                padding: 4px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
            QTableWidget {
                font-size: 12px;
            }
            QHeaderView::section {
                font-weight: bold;
                background-color: #f0f0f0;
                padding: 4px;
                color: black;
            }
        """)

    def load_data_to_table(self):
        self.ui.tableInventory.setRowCount(0)
        data = ambil_semua_data()
        self.ui.tableInventory.setColumnCount(6)
        self.ui.tableInventory.setHorizontalHeaderLabels(
            ["ID", "Nama", "Kategori", "Tanggal", "Status", "Catatan"]
        )

        for row_index, row_data in enumerate(data):
            self.ui.tableInventory.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                self.ui.tableInventory.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        self.ui.tableInventory.resizeColumnsToContents()
        self.ui.tableInventory.horizontalHeader().setStretchLastSection(True)

    def tambah_data_inventory(self):
        nama = self.ui.lineNamaBarang.text()
        kategori = self.ui.comboKategori.currentText()
        tanggal = self.ui.dateTanggalMasuk.date().toString("yyyy-MM-dd")
        status = self.ui.comboStatus.currentText()
        catatan = self.ui.plainCatatan.toPlainText()

        if nama.strip() == "":
            QMessageBox.warning(self, "Peringatan", "Nama Barang tidak boleh kosong!")
            return

        tambah_data(nama, kategori, tanggal, status, catatan)
        QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")
        self.load_data_to_table()

    def hapus_data_inventory(self):
        selected = self.ui.tableInventory.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang ingin dihapus!")
            return

        id_barang = self.ui.tableInventory.item(selected, 0).text()
        hapus_data(id_barang)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
        self.load_data_to_table()

    def edit_data_inventory(self):
        selected = self.ui.tableInventory.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang ingin diedit!")
            return

        id_barang = int(self.ui.tableInventory.item(selected, 0).text())
        nama = self.ui.lineNamaBarang.text()
        kategori = self.ui.comboKategori.currentText()
        tanggal = self.ui.dateTanggalMasuk.date().toString("yyyy-MM-dd")
        status = self.ui.comboStatus.currentText()
        catatan = self.ui.plainCatatan.toPlainText()

        edit_data(id_barang, nama, kategori, tanggal, status, catatan)
        QMessageBox.information(self, "Sukses", "Data berhasil diperbarui!")
        self.load_data_to_table()

    def cari_data(self):
        keyword = self.ui.lineSearch.text().lower()
        semua_data = ambil_semua_data()
        hasil_filter = [
            row for row in semua_data
            if keyword in row[1].lower() or keyword in row[2].lower()
        ]

        self.ui.tableInventory.setRowCount(0)
        for row_index, row_data in enumerate(hasil_filter):
            self.ui.tableInventory.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                self.ui.tableInventory.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        self.ui.tableInventory.resizeColumnsToContents()
        self.ui.tableInventory.horizontalHeader().setStretchLastSection(True)

    def pilih_data(self, row, col):
        self.ui.lineNamaBarang.setText(self.ui.tableInventory.item(row, 1).text())
        index_kat = self.ui.comboKategori.findText(self.ui.tableInventory.item(row, 2).text())
        self.ui.comboKategori.setCurrentIndex(index_kat)
        self.ui.dateTanggalMasuk.setDate(
            QDate.fromString(self.ui.tableInventory.item(row, 3).text(), "yyyy-MM-dd")
        )
        index_status = self.ui.comboStatus.findText(self.ui.tableInventory.item(row, 4).text())
        self.ui.comboStatus.setCurrentIndex(index_status)
        self.ui.plainCatatan.setPlainText(self.ui.tableInventory.item(row, 5).text())

    def ekspor_ke_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if path:
            data = ambil_semua_data()
            with open(path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nama", "Kategori", "Tanggal", "Status", "Catatan"])
                for row in data:
                    writer.writerow(row)
            QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke CSV!")

    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang Aplikasi",
            "Inventory Management Mini App\nDibuat dengan PyQt6.\n\n© 2025 Zidan Shoni Ikram"
        )


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
