import uvicorn

def start_users_microservice():
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=5011
    )


if __name__ == "__main__":
    start_users_microservice()
