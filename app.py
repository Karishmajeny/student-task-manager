from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

CSV_FILE = "tasks.csv"



# -------------------------------
# Read Tasks
# -------------------------------

def read_tasks():

    tasks = []

    with open(
        CSV_FILE,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["id"] and row["title"]:
                tasks.append(row)

    return tasks



# -------------------------------
# Write Tasks
# -------------------------------

def write_tasks(tasks):

    fieldnames = [
        "id",
        "title",
        "description",
        "priority",
        "due_date",
        "status"
    ]


    with open(
        CSV_FILE,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )


        writer.writeheader()

        writer.writerows(tasks)



# -------------------------------
# Dashboard
# -------------------------------

@app.route("/")
def home():

    tasks = read_tasks()


    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"]=="Completed"
    )


    pending = sum(
        1 for task in tasks
        if task["status"]=="Pending"
    )


    high = sum(
        1 for task in tasks
        if task["priority"]=="High"
    )


    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        high=high
    )



# -------------------------------
# Add Task
# -------------------------------

@app.route("/add", methods=["GET","POST"])
def add_task():

    if request.method=="POST":


        tasks = read_tasks()


        new_task = {

            "id":str(len(tasks)+1),

            "title":request.form["title"],

            "description":request.form["description"],

            "priority":request.form["priority"],

            "due_date":request.form["due_date"],

            "status":"Pending"

        }


        tasks.append(new_task)


        write_tasks(tasks)


        return redirect("/")


    return render_template("add_task.html")



# -------------------------------
# Delete Task
# -------------------------------

@app.route("/delete/<int:id>")
def delete_task(id):

    tasks = read_tasks()


    updated_tasks = []


    for task in tasks:

        if int(task["id"]) != id:

            updated_tasks.append(task)



    for index, task in enumerate(updated_tasks, start=1):

        task["id"] = str(index)



    write_tasks(updated_tasks)


    return redirect("/")



# -------------------------------
# Edit Task
# -------------------------------

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_task(id):

    tasks = read_tasks()


    selected_task = None



    # Find task

    for task in tasks:

        if int(task["id"]) == id:

            selected_task = task



    if request.method=="POST":


        selected_task["title"] = request.form["title"]

        selected_task["description"] = request.form["description"]

        selected_task["priority"] = request.form["priority"]

        selected_task["due_date"] = request.form["due_date"]

        selected_task["status"] = request.form["status"]



        write_tasks(tasks)


        return redirect("/")



    return render_template(
        "edit_task.html",
        task=selected_task
    )



if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )