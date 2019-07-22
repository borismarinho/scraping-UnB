import requests
from bs4 import BeautifulSoup

class Departments:

    def __init__(self, cnx):
        self.getURLs(cnx)

    def getURLs(self, cnx):
        urls = []
        query = """SELECT id_Campus, URL
                    FROM campi"""
        cursor = cnx.cursor()
        cursor.execute(query)
        for id_Campus, URL in cursor:
            urls.append((id_Campus, URL))
        cursor.close()
        for each in urls:
            self.addIntoDatabase(cnx, each[1], each[0])

    def addIntoDatabase(self, cnx, url, idCampus):
        source = requests.get(url).text
        soup = BeautifulSoup(source, "lxml")
        soup = soup.find("table", id="datatable")
        soup = soup.find("tbody")
        soup = soup.find_all("tr", recursive=False)

        for each in soup:
            link = each.find("a")
            link = link.get("href")

            each = each.find_all("td")
            code = int(each[0].text)
            acronym = each[1].text
            name = each[2].text

            self.code = code
            self.acronym = acronym
            self.name = name
            self.link = "https://matriculaweb.unb.br/graduacao/" + link

            self.insertIntoDatabase(cnx, idCampus)

    def insertIntoDatabase(self, cnx, idCampus):
        insert = """INSERT INTO departments
                  (Code, Acronym, Name, URL, id_Campus)
                  VALUES ({}, '{}', '{}', '{}', {})""".format(self.code, self.acronym, self.name, self.link, idCampus)

        cursor = cnx.cursor()
        cursor.execute(insert)
        cnx.commit()