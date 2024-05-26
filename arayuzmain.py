import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QFileDialog, QLineEdit, QMessageBox, QTabWidget, QGroupBox, QFormLayout, QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF
from difflib import SequenceMatcher
from collections import Counter

def metin_oku(dosya_yolu):
    try:
        doc = fitz.open(dosya_yolu)
        metin = ""
        for page in doc:
            metin += page.get_text()
        return metin
    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

def kelime_ara(metin, kelime):
    return [i for i in range(len(metin)) if metin.startswith(kelime, i)]

def onemli_kelimeleri_cikar(metin, n=10):
    kelimeler = metin.split()
    return [kelime for kelime, _ in Counter(kelimeler).most_common(n)]

def metin_benzerligi(metin1, metin2):
    return SequenceMatcher(None, metin1, metin2).ratio()

def metin_istatistikleri(metin):
    kelime_sayisi = len(metin.split())
    karakter_sayisi = len(metin)
    cumle_sayisi = metin.count('.')
    return {
        "Kelime Sayısı": kelime_sayisi,
        "Karakter Sayısı": karakter_sayisi,
        "Cümle Sayısı": cumle_sayisi
    }

class Database:
    def __init__(self, db_name="texts.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS texts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)

    def insert_text(self, name, content):
        with self.conn:
            self.conn.execute("INSERT INTO texts (name, content) VALUES (?, ?)", (name, content))

    def get_texts(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, name FROM texts")
            return cursor.fetchall()

    def get_text_by_id(self, text_id):
        with self.conn:
            cursor = self.conn.execute("SELECT content FROM texts WHERE id = ?", (text_id,))
            return cursor.fetchone()[0]

    def delete_text(self, text_id):
        with self.conn:
            self.conn.execute("DELETE FROM texts WHERE id = ?", (text_id,))

class MetinAnalizArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Metin Analiz Arayüzü")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))

        main_layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_file_tab(), "Dosya Yükleme")
        self.tabs.addTab(self.create_analysis_tab(), "Analiz")
        
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def create_file_tab(self):
        file_tab = QWidget()
        layout = QVBoxLayout()

        self.dosya_label = QLabel("Dosya: Henüz Yüklenmedi")
        self.dosya_label.setFont(QFont('Arial', 12))
        self.dosya_label.setStyleSheet("color: gray;")
        layout.addWidget(self.dosya_label)

        self.yukle_btn = QPushButton("Dosya Seç")
        self.yukle_btn.setFont(QFont('Arial', 10))
        self.yukle_btn.setStyleSheet("background-color: #3f91cf; color: white;")
        self.yukle_btn.clicked.connect(self.dosya_yukle)
        layout.addWidget(self.yukle_btn)

        self.sil_btn = QPushButton("Seçili Metni Sil")
        self.sil_btn.setFont(QFont('Arial', 10))
        self.sil_btn.setStyleSheet("background-color: #3f91cf; color: white;")
        self.sil_btn.clicked.connect(self.metni_sil)
        layout.addWidget(self.sil_btn)

        file_tab.setLayout(layout)
        return file_tab

    def create_analysis_tab(self):
        analysis_tab = QWidget()
        layout = QVBoxLayout()

        self.arama_input = QLineEdit(self)
        self.arama_input.setPlaceholderText("Aranacak Kelimeyi Giriniz")
        self.arama_input.setFont(QFont('Arial', 12        ))
        layout.addWidget(self.arama_input)
        
        self.ara_btn = QPushButton("Kelime Ara")
        self.ara_btn.setFont(QFont('Arial', 10))
        self.ara_btn.setStyleSheet("background-color: #3f91cf; color: white;")
        self.ara_btn.clicked.connect(self.kelime_ara)
        layout.addWidget(self.ara_btn)

        self.analiz_btn = QPushButton("Analiz Yap")
        self.analiz_btn.setFont(QFont('Arial', 10))
        self.analiz_btn.setStyleSheet("background-color: #3f91cf; color: white;")
        self.analiz_btn.clicked.connect(self.analiz_yap)
        layout.addWidget(self.analiz_btn)
        
        self.sonuc_groupbox = QGroupBox("Sonuçlar")
        self.sonuc_groupbox.setFont(QFont('Arial', 12))
        self.sonuc_layout = QVBoxLayout()
        self.sonuc_groupbox.setLayout(self.sonuc_layout)
        layout.addWidget(self.sonuc_groupbox)
        
        self.sonuc_text = QTextEdit(self)
        self.sonuc_text.setReadOnly(True)
        self.sonuc_text.setFont(QFont('Arial', 12))
        self.sonuc_layout.addWidget(self.sonuc_text)

        self.benzerlik_btn = QPushButton("Metin Benzerliğini Kontrol Et")
        self.benzerlik_btn.setFont(QFont('Arial', 10))
        self.benzerlik_btn.setStyleSheet("background-color: #3f91cf; color: white;")
        self.benzerlik_btn.clicked.connect(self.benzerlik_kontrol)
        layout.addWidget(self.benzerlik_btn)

        self.create_similarity_selection(layout)

        analysis_tab.setLayout(layout)
        return analysis_tab

    def create_similarity_selection(self, layout):
        self.similarity_groupbox = QGroupBox("Metin Benzerliği Kontrolü")
        self.similarity_groupbox.setFont(QFont('Arial', 12))
        self.similarity_layout = QFormLayout()
        self.similarity_groupbox.setLayout(self.similarity_layout)
        layout.addWidget(self.similarity_groupbox)

        self.text1_combobox = QComboBox(self)
        self.text2_combobox = QComboBox(self)
        self.update_comboboxes()

        self.similarity_layout.addRow("Metin Seçimi", self.text1_combobox)
        self.similarity_layout.addRow("Metin Seçimi", self.text2_combobox)

    def update_comboboxes(self):
        texts = self.db.get_texts()
        self.text1_combobox.clear()
        self.text2_combobox.clear()
        for text_id, name in texts:
            self.text1_combobox.addItem(name, text_id)
            self.text2_combobox.addItem(name, text_id)

    def dosya_yukle(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "PDF Files (*.pdf);;Text Files (*.txt)")
        if dosya_yolu:
            self.dosya_yolu = dosya_yolu
            self.dosya_label.setText(f"Dosya: {dosya_yolu}")
            self.dosya_label.setStyleSheet("color: black;")
            metin = metin_oku(dosya_yolu)
            self.db.insert_text(dosya_yolu.split('/')[-1], metin)
            self.update_comboboxes()

    def kelime_ara(self):
        aranacak_kelime = self.arama_input.text()
        if hasattr(self, 'dosya_yolu') and aranacak_kelime:
            metin = metin_oku(self.dosya_yolu)
            pozisyonlar = kelime_ara(metin, aranacak_kelime)
            if pozisyonlar:
                self.sonuc_text.append(f'"{aranacak_kelime}" kelimesi metin içinde şu pozisyonlarda bulundu: {pozisyonlar}')
            else:
                self.sonuc_text.append(f'"{aranacak_kelime}" kelimesi metin içinde bulunamadı.')
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir dosya seçin ve aranacak kelimeyi girin.")

    def analiz_yap(self):
        if hasattr(self, 'dosya_yolu'):
            metin = metin_oku(self.dosya_yolu)
            if "Bir hata oluştu" not in metin:
                onemli_kelimeler = onemli_kelimeleri_cikar(metin, n=10)
                self.sonuc_text.append(f'Dosyadaki önemli kelimeler: {onemli_kelimeler}')
                istatistikler = metin_istatistikleri(metin)
                self.sonuc_text.append(f'Dosya istatistikleri: {istatistikler}')
            else:
                self.sonuc_text.append(f'Bir hata oluştu: {metin}')
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir dosya seçin.")

    def benzerlik_kontrol(self):
        text1_id = self.text1_combobox.currentData()
        text2_id = self.text2_combobox.currentData()
        
        if text1_id and text2_id:
            metin1 = self.db.get_text_by_id(text1_id)
            metin2 = self.db.get_text_by_id(text2_id)

            benzerlik_derecesi = metin_benzerligi(metin1, metin2)
            self.sonuc_text.append(f'Seçilen metinler arasındaki benzerlik derecesi: {benzerlik_derecesi:.2f}')
        else:
            QMessageBox.warning(self, "Hata", "Lütfen her iki metni de seçin.")



    def metni_sil(self):
        text_id = self.text1_combobox.currentData()
        if text_id:
            self.db.delete_text(text_id)
            QMessageBox.information(self, "Başarılı", "Metin başarıyla silindi.")
            self.update_comboboxes()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek istediğiniz metni seçin.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = MetinAnalizArayuzu()
    pencere.show()
    sys.exit(app.exec_())

