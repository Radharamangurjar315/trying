# Use slim-bookworm for latest security patches
FROM python:3.12-slim-bookworm

WORKDIR /home/user/app

# Upgrade pip/tools
RUN pip install --no-cache-dir pip setuptools wheel --upgrade

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
