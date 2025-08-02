# from app.settings import settings
# port = settings.port
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
import os
from dotenv import load_dotenv
import uvicorn

# Load .env file into environment
load_dotenv()

if __name__ == "__main__":
    port = int(
        os.environ.get("port") or  # Render
        os.environ.get("port", 8000)  # Local .env
    )
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

