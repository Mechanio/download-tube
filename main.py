import os
import sys

import requests
from pytube import YouTube, Playlist
from PyQt5 import QtWidgets, QtGui

from mydesign import Ui_MainWindow
from messagewindow import Ui_Dialog


def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    application.ui.downloadProgressBar.setValue(round(percentage_of_completion))
    if round(percentage_of_completion) == 100 and application.ui.ItemsProgressBar.isVisible() is False:
        application.ui.Button.setEnabled(True)
        application.ui.Button.setText("Download")
        application.ui.UrlLine.setEnabled(True)


class MessageWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.setFixedSize(410, 216)
        self.ui.setupUi(self)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setFixedSize(514, 413)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.error_videos = []

        self.ui.TypeComboBox.addItem("Video")
        self.ui.TypeComboBox.addItem("Playlist")
        self.ui.downloadProgressBar.setVisible(False)
        self.ui.ItemsProgressBar.setVisible(False)
        self.ui.Button.clicked.connect(self.btn_clicked)
        self.ui.UrlLine.textChanged.connect(self.video_info)
        self.ui.TypeComboBox.currentTextChanged.connect(self.video_info)

    def show_message_window(self, videos):
        self.m_window = MessageWindow()
        self.m_window.ui.scrollArea.setText(videos)
        self.m_window.show()

    def video_info(self):
        self.ui.downloadProgressBar.setVisible(False)
        self.ui.ItemsProgressBar.setVisible(False)
        self.ui.ItemsLabel.setText("")
        url = self.ui.UrlLine.text()
        yt_type = self.ui.TypeComboBox.currentText()
        try:
            if yt_type == "Video":
                self.ui.FormatComboBox.clear()
                video = YouTube(url)

                self.ui.FormatComboBox.addItem("Audio (.mp3)")
                self.ui.FormatComboBox.addItem("Low Quality (360p)")
                if video.streams.filter(progressive=True, res="720p").first() is not None:
                    self.ui.FormatComboBox.addItem("High Quality (720p)")

                self.ui.VideoAuthor.setText(video.author)
                self.ui.VideoTitle.setText(video.title)

                photo = QtGui.QImage()
                photo.loadFromData(requests.get(video.thumbnail_url).content)
                self.ui.VideoPhoto.setPixmap(QtGui.QPixmap(photo))
                self.ui.Button.setEnabled(True)
            elif yt_type == "Playlist":
                self.ui.FormatComboBox.clear()
                playlist = Playlist(url)

                self.ui.FormatComboBox.addItem("Audio (.mp3)")
                self.ui.FormatComboBox.addItem("Low Quality (360p)")
                self.ui.FormatComboBox.addItem("High Quality (Mainly)")

                self.ui.VideoAuthor.setText(playlist.owner)
                self.ui.VideoTitle.setText(playlist.title)

                self.ui.VideoPhoto.setText(f"Number of videos - {str(playlist.length)}")
                self.ui.Button.setEnabled(True)
        except Exception:
            self.ui.Button.setEnabled(False)
            self.ui.FormatComboBox.clear()
            self.ui.VideoAuthor.setText("=ERROR=")
            self.ui.VideoTitle.setText("WRONG URL")
            self.ui.VideoPhoto.setPixmap(QtGui.QPixmap(f"static{os.sep}alert.png"))

    def btn_clicked(self):
        url = self.ui.UrlLine.text()
        yt_type = self.ui.TypeComboBox.currentText()
        if yt_type == "Video":
            self.downloading(url)
        elif yt_type == "Playlist":
            self.ui.ItemsProgressBar.setVisible(True)
            playlist = Playlist(url)
            self.ui.ItemsProgressBar.setMaximum(playlist.length)
            self.ui.ItemsLabel.setText(f"0/{playlist.length}")
            downloaded_videos = -1
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', directory=os.getcwd())
            for video in playlist.video_urls:
                downloaded_videos += 1
                self.ui.ItemsLabel.setText(f"{downloaded_videos}/{playlist.length}")
                self.ui.ItemsProgressBar.setValue(downloaded_videos)
                self.downloading(video, folder_path)
            else:
                downloaded_videos += 1
                self.ui.ItemsLabel.setText(f"{downloaded_videos}/{playlist.length}")
                self.ui.ItemsProgressBar.setValue(downloaded_videos)
                application.ui.Button.setEnabled(True)
                application.ui.Button.setText("Download")
                application.ui.UrlLine.setEnabled(True)
                if self.error_videos:
                    self.show_message_window(self.error_videos)
                    self.error_videos = []

    def downloading(self, url, folder_path=None):
        if isinstance(folder_path, type(None)):
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', directory=os.getcwd())
        if folder_path != '':
            self.ui.Button.setEnabled(False)
            self.ui.Button.setText("Downloading...")
            self.ui.UrlLine.setEnabled(False)
            self.ui.downloadProgressBar.setVisible(True)
            yt = YouTube(url, on_progress_callback=on_progress)
            try:
                if self.ui.FormatComboBox.currentText() == "Audio (.mp3)":
                    video = yt.streams.filter(only_audio=True, abr="160kbps").first().download(output_path=folder_path)
                    base, ext = os.path.splitext(video)
                    new_file = base + '.mp3'
                    os.rename(video, new_file)
                elif self.ui.FormatComboBox.currentText() == "Low Quality (360p)":
                    yt.streams.filter(progressive=True, res="360p").first().download(output_path=folder_path)
                elif self.ui.FormatComboBox.currentText() == "High Quality (720p)":
                    yt.streams.filter(progressive=True, res="720p").first().download(output_path=folder_path)
                elif self.ui.FormatComboBox.currentText() == "High Quality (Mainly)":
                    yt.streams.get_highest_resolution().download(output_path=folder_path)
            except Exception:
                self.error_videos.append(f"<b>{yt.author}</b>: {yt.title}")


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())
