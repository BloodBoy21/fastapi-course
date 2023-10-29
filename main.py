from project import app
import os

if __name__ == "__main__":
    import uvicorn

    environment = os.getenv("ENVIRONMENT", "development")
    config = {"port": os.getenv("PORT", 3000), "app": app}
    if environment != "production":
        config["reload"] = True
        config["app"] = "main:app"
    uvicorn.run(**config)
