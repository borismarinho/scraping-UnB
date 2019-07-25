import mysql.connector
import departments
import disciplines
import classes
cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='unb-2-2019')

# departments.Departments(cnx)
# disciplines.Disciplines(cnx)
classes.Classes(cnx)
