FROM python:3.8



# RUN pip install magenta==2.1.3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install fastapi uvicorn python-multipart
RUN pip install --no-cache-dir -r requirements.txt

# Add the following lines to copy and run the list_packages.py script
COPY list_packages.py /app/
RUN python list_packages.py

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]