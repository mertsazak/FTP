import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from ftplib import FTP

class FTPClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()

#-----------------GUI Tasarım Bölümü------------------------------------------------------------------------------------
        self.setWindowTitle("FTP Client")
        self.setGeometry(100, 100, 400, 300)

        self.host_label = QLabel("Host:")
        self.host_entry = QLineEdit()
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_entry = QLineEdit()
        self.password_label = QLabel("Şifre:")
        self.password_entry = QLineEdit()
        self.connect_btn = QPushButton("Bağlan")
        self.connect_btn.clicked.connect(self.connect_ftp)

        self.upload_btn = QPushButton("Dosya Yükle")
        self.upload_btn.clicked.connect(self.upload_file)
        self.download_btn = QPushButton("Dosya İndir")
        self.download_btn.clicked.connect(self.download_file)
        self.create_dir_btn = QPushButton("Dizin Oluştur")
        self.create_dir_btn.clicked.connect(self.create_directory)
        self.delete_btn = QPushButton("Dosya/Dizin Sil")
        self.delete_btn.clicked.connect(self.delete_file_or_directory)
        self.rename_btn = QPushButton("Dosya Adı Değiştir")
        self.rename_btn.clicked.connect(self.rename_file)
        self.list_btn = QPushButton("Dizin ve Dosyaları Listele")
        self.list_btn.clicked.connect(self.list_directory)

        layout = QVBoxLayout()
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_entry)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.create_dir_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.rename_btn)
        layout.addWidget(self.list_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.ftp = None
#-----------------------------------------------------------------------------------------------------------------------

    # Uygulamanın testlerinin yapılması için https://dlptest.com/ftp-test/ adresi kullanılmıştır.
    # Host:ftp.dlptest.com
    # Kullanıcı Adı:dlpuser
    # Şifre:rNrKYTX9g7z3RgJRmxWuGHbeu

    # FTP sunucusu ile bağlantı kurma fonksiyonu
    def connect_ftp(self):
        host = self.host_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()

        try:
            self.ftp = FTP(host)
            self.ftp.login(username, password)
            QMessageBox.information(self, "Bağlantı", "FTP sunucusuna bağlandı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    # FTP sunucusuna dosya yükleme fonksiyonu
    def upload_file(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        filename, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "All Files (*)")
        if filename:
            with open(filename, 'rb') as file:
                self.ftp.storbinary(f'STOR {filename}', file)
            QMessageBox.information(self, "Başarılı", f"{filename} dosyası yüklendi.")

    # FTP sunucusundan dosya indirme fonksiyonu
    def download_file(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Dosya İndir", "", "All Files (*)")
        if filename:
            with open(filename, 'wb') as file:
                self.ftp.retrbinary(f'RETR {filename}', file.write)
            QMessageBox.information(self, "Başarılı", f"{filename} dosyası indirildi.")

    # FTP sunucusunda dizin oluşturma fonksiyonu
    def create_directory(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        directory_name, ok = QInputDialog.getText(self, "Dizin Oluştur", "Dizin adı girin:")
        if ok:
            self.ftp.mkd(directory_name)
            QMessageBox.information(self, "Başarılı", f"{directory_name} adında bir dizin oluşturuldu.")

    # FTP sunucusunda dizin veya dosya silme fonksiyonu
    def delete_file_or_directory(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        filename, ok = QInputDialog.getText(self, "Dosya/Dizin Sil", "Silinecek dosya/dizin adı girin:")
        if ok:
            try:
                self.ftp.delete(filename)
                QMessageBox.information(self, "Başarılı", f"{filename} başarıyla silindi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))

    # FTP sunucusunda dosya adı değiştirme fonksiyonu
    def rename_file(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        old_name, ok = QInputDialog.getText(self, "Dosya Adı Değiştir", "Eski dosya adı girin:")
        new_name, ok = QInputDialog.getText(self, "Dosya Adı Değiştir", "Yeni dosya adı girin:")
        if ok:
            try:
                self.ftp.rename(old_name, new_name)
                QMessageBox.information(self, "Başarılı", f"{old_name} dosyasının adı {new_name} olarak değiştirildi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))

    # FTP sunucusunda dizinleri listeleme fonksiyonu
    def list_directory(self):
        if self.ftp is None:
            QMessageBox.critical(self, "Hata", "Önce FTP sunucusuna bağlanın.")
            return

        directory_contents = self.ftp.nlst()
        directory_listing = "\n".join(directory_contents)
        QMessageBox.information(self, "Dizin İçeriği", directory_listing)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FTPClientWindow()
    window.show()
    sys.exit(app.exec_())
