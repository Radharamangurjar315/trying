# Use a secure slim–bookworm Python base
FROM python:3.10.15-slim-bookworm

# 1. Set the container’s working dir to root
WORKDIR /

# 2. Upgrade pip and install Python deps
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir pip setuptools wheel --upgrade \
    && pip install --no-cache-dir -r /requirements.txt

# 3. Copy all your code so that `app/` lives at `/app`
COPY . /

# 4. Expose your FastAPI port
EXPOSE 3000

# 5. Launch Uvicorn pointing at app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
