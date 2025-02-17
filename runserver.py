import uvicorn
from app import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                host=settings.APP_HOST,
                port=settings.APP_PORT,
                reload=settings.RELOAD)
