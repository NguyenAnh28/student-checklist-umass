from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load data from students.json
def load_data():
    try:
        with open("submission.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"students": []}

# Save data to students.json
def save_data(data):
    with open("submission.json", "w") as file:
        json.dump(data, file, indent=4)

# Route to render onboarding.html
@app.get("/onboarding", response_class=HTMLResponse)
async def get_onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

# Route to render analytics.html
@app.get("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

# Route to handle form submission
@app.post("/submit")
async def submit_student(
    student_name: str = Form(...),
    student_id: str = Form(...),
    student_email: str = Form(...)
):
    #To do: Optimize
    students_data = load_data()  # Load current student data

    # Create a new student record
    new_student = {
        "student_name": student_name,
        "student_id": student_id,
        "student_email": student_email,
        "checklist_status": "not started",  # Default status
        "submission_time": datetime.now().isoformat()  # Current time in ISO format
    }

    # To-do: Optimize
    # Append new student to the list
    students_data['students'].append(new_student)

    # Save updated data back to the JSON file
    save_data(students_data)

    # Optionally, redirect back to the onboarding page
    return templates.TemplateResponse("onboarding.html", {"request": {}, "students": students_data})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
