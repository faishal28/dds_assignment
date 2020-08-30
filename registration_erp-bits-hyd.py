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
	mycursor.close()	
	mydb.close()

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
	mycursor.close()	
	mydb.close()

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
	mycursor.close()	
	mydb.close()

def ViewSchedule(token):
	#connecting to db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
	mycursor = mydb.cursor()

	#making calendar object
	calendar = {}
	weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
	hours = {}
	for i in range(1,11):
		hours[i] = 'X'
	for day in weekdays:
		calendar[day] = hours

	#getting all the courses enrolled by student which are currently running
	command1 = "SELECT Course_id FROM Enroll where Course_status='Running' and Student_id = %s"
	mycursor.execute(command1, (token[0],))
	result = mycursor.fetchall()

	#getting all the sections of the courses enrolled
	sections = []
	command2 = "SELECT * FROM Section where Course_id = %s"
	for x in result:
		mycursor.execute(command2, (x[0],))
		sections.append(mycursor.fetchall())

	#placing sections in calendar
	for section in sections:
		for x in section:
			entry = x[1] + ', ' + x[0] + ', ' + x[2]
			hour = x[3]
			for i in range(5,11):
				if(x[i] == 1):
					calendar[weekdays[5 - i]][hour] = entry

	#print calendar
	table = BeautifulTable()
	table.columns.header = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
	for day in calendar:
		l = []
		for hours in calendar[day]:
			l.append(calendar[day][hours])
		table.rows.append(l)
	table.rows.header = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
	print(table)
	mycursor.close()	
	mydb.close()

#convert course schedule to string
def getScheduleString(course):
	res=""
	for i in range(3,len(course)):
		res+=str(course[i])	
 
	return res	
 
 
#check clash
def checkClash(enroll,course_details):
	schedule_course=[]
	schedule_enroll=getScheduleString(enroll)
 
	for section in course_details:
		schedule_course.append(getScheduleString(section))
 
	for	i in range(len(course_details)):
 
		if course_details[i][1]=="Lab" and enroll[1]=="Lab":
			if abs(course_details[i][2]-enroll[2])<2 and (int(schedule_course[i],2) & int(schedule_enroll,2)):
				return True 
 
		elif course_details[i][1]=="Lab" or enroll[1]=="Lab":
			lec=0
			lab=0
			if course_details[i][1]=="Lab":
				lec=enroll[2]
				lab=course_details[i][2]
			else:
				lec=course_details[i][2]
				lab=enroll[2]
			if((int(schedule_course[i],2) & int(schedule_enroll,2)) and (lec==lab or (lab<lec and (lec-lab)<2))):
				return True	 	
 
		elif (course_details[i][2]==enroll[2]) and (int(schedule_course[i],2) & int(schedule_enroll,2)):		
				return True
 
 
	return False
 
 
#register to course
def registerCourse(token):
 
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="ryan",
	  password="password",
	  database="Course_registration"
	)
 
	course_id=input("Enter the Course ID to register for: ")
	student_id=token[0]
 
	command = "SELECT Course_id FROM Enroll where Student_id = %s and Course_status = 'Running'"
	mycursor=mydb.cursor()
 
	mycursor.execute(command,(student_id,))
 
	result=mycursor.fetchall()
 
	temp=[]
	for res in result:
		temp.append(res[0])
 
 
	format_strings = ','.join(['%s'] * len(temp))
	command="SELECT Course_id,Section_type,Section_hour,Mon,Tue,Wed,Thu,Fri,Sat from Section where Course_id in (%s)"%format_strings	
 
	clash_list=[]

	if(len(temp) != 0):
		mycursor.execute(command,tuple(temp))
 
		result=mycursor.fetchall()
	 
		command="SELECT Course_id,Section_type,Section_hour,Mon,Tue,Wed,Thu,Fri,Sat from Section where Course_id = %s"
		mycursor.execute(command,(course_id,))
	 
		course_details=mycursor.fetchall()
	 
		for enroll in result:
			if checkClash(enroll,course_details):
				clash_list.append((enroll[0],enroll[1]))
 
 
	#no clash		
	if len(clash_list)==0:

		command="INSERT INTO Enroll VALUES(%s,%s,%s,%s,%s)"
		mycursor.execute(command,(student_id,course_id,'NA','2020-07-17','Running',))
 
		mydb.commit();
 
		print("Registered for course")
 
	#clash	
	else:
		print(f"You cannot register to this Course due to clashes with courses: {clash_list}")			
 
	mycursor.close()	
	mydb.close()

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
		elif(selection == 4):
			registerCourse(token)
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
	mycursor.close()	
	mydb.close()
	if(myresult[0][0] == password_):
		print("Success!")
		token = (id_, myresult[0][1])
		menu(token)
	else:
		print("Invalid Password or ID")
	''' If login successfule load the menu, with student id and Name'''

if __name__ == '__main__':
	loginWindow()