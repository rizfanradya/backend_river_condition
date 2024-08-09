from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils import SERVER_PORT, data_that_must_exist_in_the_database, check_and_remove_orphaned_files, run_shell_commands
import os
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler

import routers.user as user
import routers.master as master


# FastAPI instance
app = FastAPI(
    title="App River Ranger",
    description="API River Ranger Documentations"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# self serve static files
absolute_uploads_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'cruds', 'uploads')
origin_dir = os.path.join(absolute_uploads_path, 'origin')
thumbnail_dir = os.path.join(absolute_uploads_path, 'thumbnails')
os.makedirs(origin_dir, exist_ok=True)
os.makedirs(thumbnail_dir, exist_ok=True)
app.mount("/origin", StaticFiles(directory=origin_dir), name="origin")
app.mount("/thumbnails", StaticFiles(directory=thumbnail_dir), name="thumbnails")

# routers
app.include_router(user.router, tags=["User API"], prefix="/api")
app.include_router(master.router, tags=["Master API"], prefix="/api")

# scheduler
scheduler = BackgroundScheduler()
# run every 1 hour
scheduler.add_job(check_and_remove_orphaned_files, 'interval', hours=1)
# run every 1 day
# scheduler.add_job(check_and_remove_orphaned_files, 'interval', days=1)
scheduler.start()


@app.get("/")
def root():
    data_that_must_exist_in_the_database()
    return {"message": "River Condition API"}


# run the server
if __name__ == "__main__":
    data_that_must_exist_in_the_database()
    # run_shell_commands()
    uvicorn.run("app:app", host="0.0.0.0", reload=True,
                port=int(SERVER_PORT))  # type: ignore
