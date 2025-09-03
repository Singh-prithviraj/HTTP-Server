# private/AddStudent.py

from data_store import submitted_data

def processRequest(request, response):
    rollNumber = request.get("rollNumber")
    name = request.get("name")

    print("Data Received")
    print(f"Roll number: {rollNumber}, Name: {name}")

    response.write("<!DOCTYPE html>")
    response.write("<html lang='en'>")
    response.write("<head>")
    response.write("<meta charset='utf-8'>")
    response.write("<title>My Web Application</title>")
    response.write("</head>")
    response.write("<body>")
    response.write("<center>")
    response.write("<h1>Student Management</h1>")

    # Case 1: Missing input
    if not rollNumber or not name:
        response.write("<p style='color:red;'>Both fields are required.</p>")
        showForm(response)
    
    # Case 2: Duplicate roll number
    elif rollNumber in submitted_data:
        response.write(f"<p style='color:red;'>Roll number <b>{rollNumber}</b> already exists!</p>")
        showForm(response)
    
    # Case 3: New student added
    else:
        submitted_data[rollNumber] = name
        response.write("<h2>Student Added Successfully</h2>")
        response.write(f"<p>Roll Number: {rollNumber}</p>")
        response.write(f"<p>Name: {name}</p>")

        # Ask if want to add another
        response.write("""
        <p>Do you want to add another student?</p>
        <form method='POST' action='AddStudent'>
            <input type='hidden' name='rollNumber' value=''>
            <input type='hidden' name='name' value=''>
            <button type='submit'>Yes</button>
        </form>
        <form action='index.html'>
            <button type='submit'>No</button>
        </form>
        """)

    response.write("</center></body></html>")

def showForm(response):
    response.write("""
    <form method='POST' action='AddStudent'>
        Roll number <input type='text' name='rollNumber'><br>
        Name <input type='text' name='name'><br>
        <button type='submit'>Add Student</button>
    </form>
    <br>
    <a href='index.html'>Home</a><br>
    """)
