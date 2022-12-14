from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(514, 413)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UrlLabel = QtWidgets.QLabel(self.centralwidget)
        self.UrlLabel.setGeometry(QtCore.QRect(10, 55, 58, 16))
        self.UrlLabel.setObjectName("UrlLabel")
        self.UrlLine = QtWidgets.QLineEdit(self.centralwidget)
        self.UrlLine.setEnabled(True)
        self.UrlLine.setGeometry(QtCore.QRect(50, 50, 451, 28))
        self.UrlLine.setObjectName("UrlLine")
        self.Button = QtWidgets.QPushButton(self.centralwidget)
        self.Button.setEnabled(False)
        self.Button.setGeometry(QtCore.QRect(290, 100, 111, 31))
        self.Button.setObjectName("Button")
        self.TypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.TypeComboBox.setGeometry(QtCore.QRect(50, 10, 451, 24))
        self.TypeComboBox.setObjectName("TypeComboBox")
        self.TypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TypeLabel.setGeometry(QtCore.QRect(10, 15, 32, 16))
        self.TypeLabel.setObjectName("TypeLabel")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(50, 150, 411, 211))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.VideoAuthor = QtWidgets.QLabel(self.frame)
        self.VideoAuthor.setGeometry(QtCore.QRect(30, 30, 211, 21))
        self.VideoAuthor.setText("")
        self.VideoAuthor.setObjectName("VideoAuthor")
        self.VideoTitle = QtWidgets.QLabel(self.frame)
        self.VideoTitle.setGeometry(QtCore.QRect(30, 70, 211, 61))
        self.VideoTitle.setText("")
        self.VideoTitle.setWordWrap(True)
        self.VideoTitle.setObjectName("VideoTitle")
        self.VideoPhoto = QtWidgets.QLabel(self.frame)
        self.VideoPhoto.setGeometry(QtCore.QRect(250, 30, 141, 101))
        self.VideoPhoto.setText("")
        self.VideoPhoto.setScaledContents(True)
        self.VideoPhoto.setObjectName("VideoPhoto")
        self.downloadProgressBar = QtWidgets.QProgressBar(self.frame)
        self.downloadProgressBar.setEnabled(True)
        self.downloadProgressBar.setGeometry(QtCore.QRect(40, 150, 331, 23))
        self.downloadProgressBar.setProperty("value", 0)
        self.downloadProgressBar.setTextVisible(True)
        self.downloadProgressBar.setObjectName("downloadProgressBar")
        self.ItemsProgressBar = QtWidgets.QProgressBar(self.frame)
        self.ItemsProgressBar.setEnabled(True)
        self.ItemsProgressBar.setGeometry(QtCore.QRect(40, 180, 331, 23))
        self.ItemsProgressBar.setMaximum(100)
        self.ItemsProgressBar.setProperty("value", 0)
        self.ItemsProgressBar.setTextVisible(False)
        self.ItemsProgressBar.setObjectName("ItemsProgressBar")
        self.ItemsLabel = QtWidgets.QLabel(self.frame)
        self.ItemsLabel.setGeometry(QtCore.QRect(40, 180, 331, 20))
        self.ItemsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ItemsLabel.setText("")
        self.ItemsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemsLabel.setObjectName("ItemsLabel")
        self.FormatComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.FormatComboBox.setGeometry(QtCore.QRect(110, 100, 141, 31))
        self.FormatComboBox.setObjectName("FormatComboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 514, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DownloadTube"))
        self.UrlLabel.setText(_translate("MainWindow", "URL:"))
        self.Button.setText(_translate("MainWindow", "Download"))
        self.TypeLabel.setText(_translate("MainWindow", "Type:"))
