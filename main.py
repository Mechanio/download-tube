import os
import sys

import requests
from pytubefix import YouTube, Playlist
from PyQt5 import QtWidgets, QtGui

from tempdesign import Ui_MainWindow
# from mydesign import Ui_MainWindow
from messagewindows import Ui_Dialog, Ui_Form


def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    application.ui.downloadProgressBar.setValue(round(percentage_of_completion))
    if round(percentage_of_completion) == 100 and application.ui.ItemsProgressBar.isVisible() is False:
        application.ui.Button.setEnabled(True)
        application.ui.Button.setText("Download")
        application.ui.UrlLine.setEnabled(True)


class ErrorMessageWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.setFixedSize(410, 216)
        self.ui.setupUi(self)

class MessageWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setFixedSize(514, 450)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.error_videos = []
        self.only_in_playlist = set()

        self.ui.TypeComboBox.addItem("Video")
        self.ui.TypeComboBox.addItem("Playlist")
        self.ui.downloadProgressBar.setVisible(False)
        self.ui.ItemsProgressBar.setVisible(False)
        self.ui.Button.clicked.connect(self.btn_clicked)
        self.ui.UrlLine.textChanged.connect(self.video_info)
        self.ui.TypeComboBox.currentTextChanged.connect(self.video_info)

        self.ui.FolderPathButton_2.clicked.connect(self.browse_folder)
        self.ui.FolderPathLine_2.textChanged.connect(self.check_to_analyze_playlist)
        self.ui.UrlLine_2.textChanged.connect(self.check_to_analyze_playlist)
        self.ui.AnalyzeButton.clicked.connect(self.analyze_playlist)
        self.ui.UpdateButton.clicked.connect(self.update_playlist)

    def show_error_message_window(self, videos):
        self.error_m_window = ErrorMessageWindow()
        self.error_m_window.ui.scrollArea.setText(videos)
        self.error_m_window.show()

    def show_message_window(self):
        self.m_window = MessageWindow()
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

    def browse_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', directory=os.getcwd())
        self.ui.FolderPathLine_2.setText(folder_path)

    def check_to_analyze_playlist(self):
        if self.ui.FolderPathLine_2.text() and self.ui.UrlLine_2.text():
            self.ui.AnalyzeButton.setEnabled(True)
        else:
            self.ui.AnalyzeButton.setEnabled(False)

    def analyze_playlist(self):
        try:
            names_from_folder = set(os.path.splitext(filename)[0] for filename in os.listdir(self.ui.FolderPathLine_2.text()))
            names_from_playlist = set()
            playlist = Playlist(self.ui.UrlLine_2.text())
            for video in playlist.video_urls:
                yt = YouTube(video)
                names_from_playlist.add(yt.title.replace(f"{os.sep}", ""))
            only_in_folder = names_from_folder - names_from_playlist
            self.only_in_playlist = names_from_playlist - names_from_folder
            self.ui.InFolderScrollArea.setText(only_in_folder)
            self.ui.InPlaylistScrollArea.setText(self.only_in_playlist)
            self.ui.UpdateButton.setEnabled(True)
        except Exception:
            self.ui.InFolderScrollArea.setText("error")

    def update_playlist(self):
        playlist = Playlist(self.ui.UrlLine_2.text())
        for video in playlist.video_urls:
            yt = YouTube(video)
            if yt.title.replace(f"{os.sep}", "") in self.only_in_playlist:
                self.downloading(video, self.ui.FolderPathLine_2.text())
        else:
            if self.error_videos:
                self.show_error_message_window(self.error_videos)
                self.error_videos = []
            self.show_message_window()


    def btn_clicked(self):
        url = self.ui.UrlLine.text()
        yt_type = self.ui.TypeComboBox.currentText()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', directory=os.getcwd())
        if folder_path != '':
            if yt_type == "Video":
                self.downloading(url, folder_path)
            elif yt_type == "Playlist":
                self.ui.ItemsProgressBar.setVisible(True)
                playlist = Playlist(url)
                self.ui.ItemsProgressBar.setMaximum(playlist.length)
                self.ui.ItemsLabel.setText(f"0/{playlist.length}")
                downloaded_videos = -1
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
                        self.show_error_message_window(self.error_videos)
                        self.error_videos = []
            self.show_message_window()

    def downloading(self, url, folder_path):
        self.ui.Button.setEnabled(False)
        self.ui.Button.setText("Downloading...")
        self.ui.UrlLine.setEnabled(False)
        self.ui.downloadProgressBar.setVisible(True)
        yt = YouTube(url, on_progress_callback=on_progress)
        try:
            if self.ui.FormatComboBox.currentText() == "Audio (.mp3)":
                video = yt.streams.filter(only_audio=True, abr="160kbps").first()
                if isinstance(video, type(None)):
                    video = yt.streams.get_audio_only()
                video = video.download(output_path=folder_path)
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
