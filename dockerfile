FROM python:3.12.10-slim

WORKDIR /app

# System dependencies for Orange, numpy, pandas, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libsm6 \
    libxext6 \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]
