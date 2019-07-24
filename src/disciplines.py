import requests
from bs4 import BeautifulSoup
import time

class Disciplines:

    def __init__(self, cnx):
        self.getURLs(cnx)

    def getURLs(self, cnx):
        urls = []
        query = """SELECT id_Department, URL
                    FROM departments
                    ORDER BY id_Department ASC"""
        cursor = cnx.cursor()
        cursor.execute(query)
        for id_Department, URL in cursor:
            urls.append((id_Department, URL))
        cursor.close()
        for each in urls:
            time.sleep(3)
            self.addIntoDatabase(cnx, each[1], each[0])

    def addIntoDatabase(self, cnx, url, idDepartment):
        try:
            source = requests.get(url).text
            soup = BeautifulSoup(source, "lxml")
            soup = soup.find("table", id="datatable")
            soup = soup.find_all("tr", recursive=False)

            for each in soup[1:]:
                buffer = each.find_all("td")
                code = buffer[0].text
                name = buffer[1].find("a")
                name = name.text
                link = buffer[1].find("a")
                link = link.get("href")
                summary = buffer[2].find("a")
                summary = summary.get("href")

                self.code = code
                self.name = name
                self.link = "https://matriculaweb.unb.br/graduacao/" + link
                self.summary = "https://matriculaweb.unb.br" + summary

                self.insertIntoDatabase(cnx, idDepartment)

        except:
            print("No entries to be evaluated: " + str(idDepartment), url)

    def insertIntoDatabase(self, cnx, idDepartment):
        insert = """INSERT INTO disciplines
                  (Code, Name, URL, Summary, id_Department)
                  VALUES ({}, '{}', '{}', '{}', {})""".format(self.code, self.name, self.link, self.summary, idDepartment)

        cursor = cnx.cursor()
        cursor.execute(insert)
        cnx.commit()
        cursor.close()
