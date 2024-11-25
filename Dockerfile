# python runtime. I have using 3.11 because on this environment only I have built this app 
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# application code copying in this
COPY . /app

# using port 8000 to run the app
EXPOSE 8000

# as the fatsapi I am using, hence using uvicorn command for running the app
CMD ["uvicorn", "app5:app", "--host", "0.0.0.0", "--port", "8000"]
