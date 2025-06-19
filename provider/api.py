from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id == 1:
        return {"id": 1, "name": "John Doe"}
    return {"error": "User not found"}, 404