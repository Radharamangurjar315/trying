# from app.settings import settings
# port = settings.port
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
import os
import uvicorn

if __name__ == "__main__":
    # Render always sets PORT environment variable
    port = int(os.environ.get("PORT"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
