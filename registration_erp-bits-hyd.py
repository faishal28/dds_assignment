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

def PerformanceRecord(token):
	#connecting to db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()

	#getting grades and courses completed
	command1 = "SELECT Course_id, Course_grade FROM Enroll where Course_status='Completed' and Student_id = %s"
	mycursor.execute(command1, (token[0],))
	result = mycursor.fetchall()

    #getting courses details of each course
	finalList = []
	total_credits = 0
	total_score = 0
	gradetoScore = {'A' : 10, 'A-' : 9, 'B' : 8, 'B-': 7, 'C' : 6, 'C-' : 5, 'E' : 2, 'NC' : 0}
	command2 = "SELECT Course_name, Course_credits FROM Course where Course_id = %s"
	for x in result:
		mycursor.execute(command2, (x[0],))
		result2 = mycursor.fetchall()
		total_credits += result2[0][1]
		total_score += gradetoScore[x[1]]*result2[0][1]
		l = [x[0], result2[0][0], result2[0][1], x[1]]
		finalList.append(l)

	#printing result
	table = BeautifulTable()
	table.columns.header = ["Course_id", "Course_name", "Course_credits", "Grade"]
	for x in finalList:
		table.rows.append(x)
	print(table)
	if(total_credits > 0):
		print("CGPA : ", "{:.2f}".format(total_score/total_credits))
	else:
		print("CGPA : NA")

def ViewCurrent(token):
	#connecting to db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()

	#getting all the courses enrolled by student which are currently running
	command1 = "SELECT Course_id FROM Enroll where Course_status='Running' and Student_id = %s"
	mycursor.execute(command1, (token[0],))
	result = mycursor.fetchall()

	#getting names of the courses
	finalList = []
	command2 = "SELECT Course_name, Course_credits FROM Course where Course_id = %s"
	for x in result:
		mycursor.execute(command2, (x[0],))
		result2 = mycursor.fetchall()
		l = [x[0], result2[0][0], result2[0][1]]
		finalList.append(l)

	#printing result
	table = BeautifulTable()
	table.columns.header = ["Course_id", "Course_name", "Course_credits"]
	for x in finalList:
		table.rows.append(x)
	print(table)

def ViewSchedule(token):
	#connecting to db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()

	#getting all the courses enrolled by student which are currently running
	command1 = "SELECT Course_id FROM Enroll where Course_status='Running' and Student_id = %s"
	mycursor.execute(command1, (token[0],))
	result = mycursor.fetchall()

	#making calendar object
	calendar = {}
	weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
	hours = {}
	for i in range(1,11):
		hours[i] = 'X'
	for day in weekdays:
		calendar[day] = hours





def displayMenu(token):
	welcome = "Hi, " + token[1] + " welcome to your new Semester"
	#print(chr(27) + "[2J")
	print(welcome, flush=True)	
	options = ["View Courses Offered in Current Semester", "View Academic History", "View Registered Courses", "Register For Course", "View Schedule"]
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
		elif(selection == 2):
			PerformanceRecord(token)
		elif(selection == 3):
			ViewCurrent(token)
		elif(selection == 5):
			ViewSchedule(token)
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