from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from Backend.WebAPI.Controllers.UserController import UserController
from Backend.WebAPI.Controllers.TaskController import TaskController
from Backend.WebAPI.Controllers.CommentController import CommentController
from Backend.WebAPI.Controllers.ActivityController import ActivityController
from Backend.WebAPI.Controllers.AttachmentController import AttachmentController
from Backend.WebAPI.Controllers.MemberController import MemberController
from Backend.Service.Services.Users.UserService import UserService
from Backend.Service.Services.Tasks.TaskService import TaskService
from Backend.Service.Services.Comments.CommentService import CommentService
from Backend.Service.Services.Activities.ActivityService import ActivityService
from Backend.Service.Services.Attachments.AttachmentService import AttachmentService
from Backend.Service.Services.Members.MemberService import MemberService
from Backend.Data.Repositories.UserRepository import UserRepository
from Backend.Data.Repositories.TaskRepository import TaskRepository
from Backend.Data.Repositories.CommentRepository import CommentRepository
from Backend.Data.Repositories.ActivityRepository import ActivityRepository
from Backend.Data.Repositories.AttachmentRepository import AttachmentRepository
from Backend.Data.Repositories.MemberRepository import MemberRepository
from Backend.Data.UnitOfWork import UnitOfWork
import webbrowser
import threading
import time

app = FastAPI(
    title="MoonTrip API",
    description="API for MoonTrip project management application",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create repositories
user_repository = UserRepository()
task_repository = TaskRepository()
comment_repository = CommentRepository()
activity_repository = ActivityRepository()
attachment_repository = AttachmentRepository()
member_repository = MemberRepository()

# Create unit of work
unit_of_work = UnitOfWork()

# Create services
user_service = UserService(unit_of_work)
task_service = TaskService(unit_of_work)
comment_service = CommentService(unit_of_work)
activity_service = ActivityService(unit_of_work)
attachment_service = AttachmentService(unit_of_work)
member_service = MemberService(unit_of_work)

# Create API router
api_router = APIRouter()

# Create and register controllers
user_controller = UserController(api_router, user_service)
task_controller = TaskController(api_router, task_service)
comment_controller = CommentController(api_router, comment_service)
activity_controller = ActivityController(api_router, activity_service)
attachment_controller = AttachmentController(api_router, attachment_service)
member_controller = MemberController(api_router, member_service)

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to MoonTrip API",
        "documentation": "/swagger",
        "version": "1.0.0"
    }

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(1.5)  # Wait for the server to start
    webbrowser.open('http://localhost:8000/swagger')

if __name__ == "__main__":
    import uvicorn
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)