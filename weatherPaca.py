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

        departements = self.fill_cb("paca/paca.txt")
        self.ui.cbDepartements.insertItems(0, departements)
        self.ui.cbDepartements.setCurrentText(departements[1])

        print("Connexion à OpenWheather")
        self.owm = pyowm.OWM('d24df2ad820eeec286b0b612714a6a96')

    def fill_cb_city(self, dept):
        print(dept)
        file = "paca/alpesdehauteprovence.txt"
        self.ui.cbVilles.clear()
        if dept == "Alpes de hautes Provence":
            file = "paca/alpesdehauteprovence.txt"
        elif dept == "Hautes Alpes":
            file = "paca/hautesalpes.txt"
        elif dept == "Alpes Maritimes":
            file = "paca/alpesmaritimes.txt"
        elif dept == "Bouches du Rhône":
            file = "paca/bouchesdurhone.txt"
        elif dept == "Vaucluse":
            file = "paca/vaucluse.txt"

        print(file)

        cities = self.fill_cb(file)
        self.ui.cbVilles.insertItems(0, cities)

    def fill_cb(self, file):
        self.ui.cbVilles.setEnabled(True)
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        lines_stripped = []
        for dep in lines:
            lines_stripped.append(dep.strip("\n"))
        print(lines)
        print(lines_stripped)
        return sorted(lines_stripped)

    def show_city(self):
        self.ville = self.ui.cbVilles.currentText()
        self.ville = self.ville.strip("\n")
        print(f'Ville choisie : {self.ville}')
        self.ui.lbPrevisionsVille.setText("Prévisions pour : "+self.ville)
        if self.ville!="":
            self.previsions()


    def previsions(self):
        observation = self.owm.weather_at_place(self.ville)
        weather = observation.get_weather()
        temperature = weather.get_temperature('celsius')
        print(temperature)
        tc = temperature["temp"]
        humidity = weather.get_humidity()
        print(humidity)
        now = weather.get_reference_time()
        tz = pytz.timezone('Europe/Paris')
        print(f'Timestamp prévisions : {now}')
        la_date = datetime.fromtimestamp(now,tz).strftime('%d/%m/%Y - %H:%M:%S')
        print(f'Date prévisions : {la_date}')
        self.ui.lbDatePrevisions.setText(str(la_date))
        wind = weather.get_wind()
        windS = wind["speed"] * 3.6
        print(f'Vent : {windS} km/h')
        windD = wind["deg"]
        pressure = weather.get_pressure()
        print(f'pression : {pressure["press"]} hPa')
        cloud = weather.get_clouds()
        print(f'Nuages : {cloud}')
        rain = weather.get_rain().get('3h')
        print(f'Pluie : {rain}')
        snow = weather.get_snow().get('3h')
        print(f'Neige : {snow}')

        self.ui.lcdTemperature.display(tc)
        self.ui.lcdHumidity.display(humidity)
        self.ui.lcdPression.display(pressure["press"])
        self.ui.lcdVitesseVent.display(windS)
        self.ui.lcdDirectionVent.display(windD)
        self.ui.lcdNuage.display(cloud)
        self.ui.lcdNeige.display(snow)
        self.ui.lcdPluie.display(rain)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationIHM()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()