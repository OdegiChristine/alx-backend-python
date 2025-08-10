# Python base image
FROM python:3.10

# Prevent python form writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files into container
COPY . /app/
COPY wait-for-db.sh /wait-for-db.sh

# Expose the port django will run on
EXPOSE 8000

ENTRYPOINT ["/wait-for-db.sh"]

# -p flag used when running the container
# docker run -p 8000:8000 messaging-app

# Command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
