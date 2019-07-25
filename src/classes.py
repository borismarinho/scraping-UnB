import requests
from bs4 import BeautifulSoup
import time

class Classes:

    def __init__(self, cnx):
        self.getURLs(cnx)

    def getURLs(self, cnx):
        urls = []
        query = """SELECT id_Discipline, URL
                    FROM disciplines
                    ORDER BY id_Discipline ASC"""
        cursor = cnx.cursor()
        cursor.execute(query)
        for id_Department, URL in cursor:
            urls.append((id_Department, URL))
        cursor.close()
        for each in urls:
            self.addIntoDatabase(cnx, each[1], each[0])
            time.sleep(3)

    def addIntoDatabase(self, cnx, url, idCampus):
        source = open("Matrícula Web _ Dados da Oferta.html", "r", encoding="utf-8")
        # source = requests.get("https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=113034&dep=113").text
        soup = BeautifulSoup(source, "lxml")
        soup = soup.find_all("table", id="datatable")
        for each in soup[1:]:
            self.findClassOffer(each)
            self.findOpenings(each)
            self.findShift(each)
            self.whereWhen(each)
            self.professor(each)
            self.restriction(each)
            self.otherStuff(each)

        input()

    def findClassOffer(self, cls):
        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find("td")
        cls = cls.find_all("td")

        if len(cls) == 1:
            self.cls = cls[0].text
            self.offer = None
        elif len(cls) == 2:
            self.cls = cls[0].text
            self.offer = cls[1].text
        else:
            print("Input error!")

        # print(self.cls, self.offer)

    def findOpenings(self, cls):
        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find_all("td", recursive=False)
        cls = cls[1].find_all("tr")

        if len(cls) == 3:
            for i in range(len(cls)):
                each = cls[i].find_all("td")
                if i == 0:
                    self.totalOp = each[2].text

                elif i == 1:
                    self.occupiedOp = each[2].text

                elif i == 2:
                    self.vacantOp = each[2].text

                else:
                    print("Input error!")

            self.freshmenOp = None
            self.freshmenOcOp = None
            self.freshmenVcOp = None


        elif len(cls) == 6:
            for i in range(len(cls)):
                each = cls[i].find_all("td")
                if i == 0:
                    self.totalOp = each[2].text

                elif i == 1:
                    self.occupiedOp = each[2].text

                elif i == 2:
                    self.vacantOp = each[2].text

                elif i == 3:
                    self.freshmenOp = each[2].text

                elif i == 4:
                    self.freshmenOcOp = each[2].text

                elif i == 5:
                    self.freshmenVcOp = each[2].text

                else:
                    print("Input error!")

        else:
            print("Input error!")

        # print(self.totalOp, self.occupiedOp, self.vacantOp, self.freshmenOp, self.freshmenOcOp, self.freshmenOcOp)

    def findShift(self, cls):
        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find_all("td", recursive=False)
        cls = cls[2].find("tr")

        self.shift = cls.text

        # print(self.shift)

    def whereWhen(self, cls):
        self.timeLocation = []

        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find_all("td", recursive=False)
        cls = cls[3].find_all("table", recursive=False)

        for each in cls:
            tmp = each.find("tbody")
            tmp = tmp.find_all("tr", recursive=False)

            when = tmp[0].find_all("td")
            starts = when[0].text
            ends = when[1].text
            weekday = when[2].text

            where = tmp[1].find_all("td")
            where = where[1].text

            buffer = (starts, ends, weekday, where)
            self.timeLocation.append(buffer)

        # print(self.timeLocation)

    def professor(self, cls):
        self.professors = []

        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find_all("td", recursive=False)
        cls = cls[4].find_all("td")

        for each in cls:
            self.professors.append(each.text)

        # print(self.professors)

    def restriction(self, cls):
        cls = cls.find("tbody")
        cls = cls.find("tr")
        cls = cls.find_all("td", recursive=False)
        cls = cls[5].find("img")

        if cls is None:
            self.restr = None

        elif "1.gif" in cls.get("src"):
            self.restr = 1

        elif "2.gif" in cls.get("src"):
            self.restr = 2

        elif "3.gif" in cls.get("src"):
            self.restr = 3

        else:
            print("Input error!")

        # print(self.restr)

    def otherStuff(self, cls):
        self.clsAndGender = (None, None)
        self.reservation = []
        cls = cls.find("tbody")
        cls = cls.find_all("tr", recursive=False)
        if len(cls) == 1:
            pass
        else:
            for each in cls[1:]:
                if "Reserva para curso" in each.text:
                    pass
                elif "Turma" in each.text and "Sexo" in each.text:
                    tmp = each.find_all("td")
                    self.clsAndGender = (tmp[0].text, tmp[1].text)
                else:
                    tmp = each.find_all("td")
                    self.reservation.append((tmp[0].text, tmp[1].text, tmp[2].text))

        # print(self.clsAndGender, self.reservation)
