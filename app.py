from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils import SERVER_PORT, data_that_must_exist_in_the_database

import routers.user as user
import routers.data as data
import routers.choice as choice
import routers.role as role


app = FastAPI(
    title="App River Condition",
    description="API River Condition Documentations"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router, tags=["User API"], prefix="/api")
app.include_router(role.router, tags=["Role API"], prefix="/api")
app.include_router(data.router, tags=["Data API"], prefix="/api")
app.include_router(choice.router, tags=["Choice API"], prefix="/api")


@app.get("/")
def root():
    data_that_must_exist_in_the_database()
    return {"message": "River Condition API"}


if __name__ == "__main__":
    data_that_must_exist_in_the_database()
    uvicorn.run("app:app", host="0.0.0.0", reload=True,
                port=int(SERVER_PORT))  # type: ignore
