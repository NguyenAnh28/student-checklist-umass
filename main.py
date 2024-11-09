from fastapi import FastAPI, Form
import json
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/submit/")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    data = {
        "name": name,
        "email": email,
        "message": message
    }

    # Save data to submission.json
    with open("submission.json", "w") as json_file:
        json.dump(data, json_file)

    return JSONResponse(content={"message": "Data received and stored successfully", "data": data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
