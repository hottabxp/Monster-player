import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import main_ui  # Это наш конвертированный файл дизайна
from basslib import Bass
from playlist import Playlist


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def  __init__(self, parent=None, test=None, channel=None):
        self.test = test
        self.channel = channel
        QtCore.QThread.__init__(self, parent)
    def run(self):
        self.running = True
        while self.running:
            self.sleep(1)
            x = self.test.ChannelGetTags(self.channel)
            self.mysignal.emit(x)

        print('Stop')



class ExampleApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.playlist_ = Playlist()

        self.mythread = None

        self.horizontalSlider.setValue(20) # % громкости при старте приложения

        self.bass = Bass()
        self.bass.init()
        self.stream = 0

        self.listWidget.itemDoubleClicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.pause)
        self.horizontalSlider.valueChanged.connect(self.changedVolume)

        self.stations = self.playlist_.getStations()
        self.listWidget.addItems([x[1] for x in self.stations])

    def on_change(self, s):

        self.label.setText(s)

    def getVolume(self):
        volume = float(self.horizontalSlider.value()/100) # Значение ползунка
        return volume

    def changedVolume(self):
      volume = float(self.horizontalSlider.value()/100) # Значение ползунка
      self.bass.SetVolume(self.stream, volume)


    def pause(self):
        self.bass.Pause(self.stream)

    def play(self):

        if self.mythread:
            self.mythread.running = False


        current = self.listWidget.currentRow()
        url = self.stations[current][2]

        status = self.bass.Stop(self.stream)
        self.stream = self.bass.StreamCreateURL(url)
        self.bass.SetVolume(self.stream, self.getVolume())
        self.mythread = MyThread(test=self.bass, channel=self.stream)

        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.mythread.start()
        
        print(status)
        self.bass.Play(self.stream, False) 

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()