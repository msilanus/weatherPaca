from PyQt5 import QtWidgets
from weatherPacaGUI import Ui_MainWindow
import sys
import pyowm
from _datetime import datetime
import pytz

class ApplicationIHM(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationIHM, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        f = open("paca/paca.txt", 'r')
        lines = f.readlines()
        f.close()
        lines_stripped = []
        for dep in lines:
            lines_stripped.append(dep.strip("\n"))
        print(lines)
        print(lines_stripped)
        self.ui.cbDepartements.insertItems(0, lines_stripped)
        self.ui.cbDepartements.setCurrentText(lines_stripped[0])


    def fill_cb_city(self, dept):
        print("fill_cb_city")


    def show_city(self):
        print("show_city")


    def previsions(self):
        print("previsions")

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationIHM()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()