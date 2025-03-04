"""
This is the main file of the FastAPI application. It is the entry point of the application.
"""

from configs import app
from user.endpoints import router as user_router


app.include_router(user_router, prefix="/user")



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)