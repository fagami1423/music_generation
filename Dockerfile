FROM python:3.8



# RUN pip install magenta==2.1.3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
