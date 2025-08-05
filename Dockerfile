FROM python:3.10.15-slim-bookworm

# Working directory set karo
WORKDIR /workspace

# Requirements copy aur install karo
COPY requirements.txt .
RUN pip install --no-cache-dir pip setuptools wheel --upgrade \
    && pip install --no-cache-dir -r requirements.txt

# Pura project copy karo
COPY . .

# Port expose karo
EXPOSE 3000

# run.py se start karo (jo locally working hai)
CMD ["python", "run.py"]
