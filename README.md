# web-scraping

I made this project to teach myself the concepts of web scraping in Python, database manipulation, using git with command line and markdown language as well.

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

![Database Relational Model](https://imgsafe.org/image/282fcc9e33)




At first the program access the campi pages, then parse all the entries.

![Campi](campi_pages)

