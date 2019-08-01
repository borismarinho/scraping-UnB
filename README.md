# scraping-UnB

I made this project to teach myself the concepts of web scraping in Python, database manipulation, using git with command line and markdown language as well besides gathering information that could be useful to students of the university.

The idea is to parse the entire site of the University where I study (Universidade de Brasília) and gather data of the classes that are being offered this semester: campi, departments, disciplines, classes, teachers, classrooms; store this data in a database and make some statistics with this data.

To set up the environment to this project we will need to install the following modules, so follow the instructions.

* requests (module to make HTTP requests in a simple way, avoiding to deal with HTTP protocol)
```bash
pip install requests
```
* beautifulsoup4 (module to navigate in the HTML tree)
```bash
pip install beautifulsoup4
```
* lxml (parser to the HTML code)
```bash
pip install lxml
```
* mysql-connector-python (module to store and retrieve data from the MySQL database)
```bash
pip install mysql-connector-python
```

## The website
___

The website is organized in the structure of a tree:

![Diagram]()

So we must access the root, so we can get the links to the campi pages, then we access the campi pages to get the departments links and so on. The leaves of the tree are the discipline pages and there we can find the useful info. Because there are only 4 campi, the scrape didn't started at the root, it started directly from campi pages.

This give a hint of how to explore the website and how to design the database. One thing to keep in mind is that the University server is not prepared to scraping, it does not even have a robot.txt file. So it's good manners to scrape it with ease and as a solution to this I also saved the URL's to the pages in the database so I could access them bit by bit without overloading the servers with requests.

## The database
___
At first the database is not normalized because it's more convenient to extract the data according the template of the information, and it looks like that:

![Database Relational Model](https://i.imgsafe.org/28/282fcc9e33.png)

Since it's not an updating database, it will be easier to gather the information in first place and later execute some SQL scripts to normalize and make the database more efficient.

## The software
____
This software is as simple as it could be:
There are 3 classes and a main function, each class parses a different kind of page and the main function construct one of each class.

* Departments: parses the list of departments (as shown in the image) gatherings its attributes and storing all of them in the database
![Departments list](https://i.imgsafe.org/28/28b002cbfc.png)

* Disciplines: parses the list of departments (as shown in the image) gatherings its attributes and storing all of them in the database
![Disciplines list](https://i.imgsafe.org/28/28b058eb28.png)

* Classes: the scraping in this kind of page (as shown in the image) was quite a challenge because the data availabe was not well structured, some of it was in images, and some kind appeared only in some cases, so I've had to consider several edge cases to makes the scraper work well.
![Classes list](https://i.imgsafe.org/28/28b086842e.png)
