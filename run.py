import os
os.environ["HF_HOME"] = "/tmp/huggingface"  # Or any writeable path
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/transformers"
os.environ["HF_DATASETS_CACHE"] = "/tmp/huggingface/datasets"
os.environ["HF_METRICS_CACHE"] = "/tmp/huggingface/metrics"

from dotenv import load_dotenv
load_dotenv()
# from app.settings import settings
# port = settings.port
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
import os
import uvicorn

if __name__ == "__main__":
    # Render always sets PORT environment variable

  port = int(os.environ.get("PORT", 3000))  # set default port as 3000
print(f"PORT from env: {port}")
uvicorn.run("app.main:app", host="0.0.0.0", port=port)         