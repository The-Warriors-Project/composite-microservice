from fastapi import FastAPI, Response, status
from datetime import datetime
import json
from composite_endpoint import composite_router

app = FastAPI()
app.include_router(composite_router)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())

    msg = {
            "name": "Composite-Microservice",
            "health": "Good",
            "at time": t
           }

    result = Response(json.dumps(msg), status_code=status.HTTP_200_OK)

    return result
