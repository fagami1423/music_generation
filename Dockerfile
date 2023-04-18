FROM python:3.8



# RUN pip install magenta==2.1.3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --default-timeout=60 fastapi uvicorn python-multipart
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y fluidsynth

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]