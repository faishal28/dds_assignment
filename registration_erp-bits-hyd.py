import mysql.connector
from beautifultable import BeautifulTable

def ViewCourses(token):
	#connecting to db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()

	#getting student's stream_id
	command1 = "SELECT Stream_id, Current_sem, Current_year FROM Student where Student_id = %s"
	mycursor.execute(command1, (token[0],))
	result = mycursor.fetchall()
	stream_id = result[0][0]
	student_sem = result[0][1]
	student_year = result[0][2]

	#getting department offering above stream
	command2 = "SELECT Dept_name from Stream where Stream_id = %s"
	mycursor.execute(command2, (stream_id,))
	result = mycursor.fetchall()
	dept_name = result[0][0]

	#getting all the courses offered by the above dept
	command3 = "SELECT Course_id, Course_name, Course_credits, Course_type, Lec, Tut, Lab, Total_seats from Course where Dept_name = %s and Course_year = %s and Course_sem = %s"
	mycursor.execute(command3, (dept_name, student_year, student_sem))
	result = mycursor.fetchall()
	
	#printing result
	table = BeautifulTable()
	table.columns.header = ["Course_id", "Course_name", "Course_credits", "Course_type", "Lec", "Tut", "Lab", "Total_seats"]
	for x in result:
		table.rows.append(x)
	print(table)

def displayMenu(token):
	welcome = "Hi, " + token[1] + " welcome to your new Semester"
	#print(chr(27) + "[2J")
	print(welcome, flush=True)	
	options = ["View Courses Offered in Current Semester", "View Academic History", "Register For Course", "View Schedule"]
	count = 0
	for x in options:
		count += 1
		print(count, x)

def menu(token):
	while(True):
		displayMenu(token)
		selection = int(input("Enter operation you want to perform: "))
		if(selection == 1):
			ViewCourses(token)
		else:
			print("Invalid Selection")



def loginWindow():
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()
	id_ = input("Enter your id: ")
	password_ = input("Enter your password: ")
	command = "SELECT password, Student_name FROM Student where Student_id = %s"
	mycursor.execute(command, (id_,))
	myresult = mycursor.fetchall()
	if(myresult[0][0] == password_):
		print("Success!")
		token = (id_, myresult[0][1])
		menu(token)
	else:
		print("Invalid Password or ID")
	''' If login successfule load the menu, with student id and Name'''

if __name__ == '__main__':
	loginWindow()