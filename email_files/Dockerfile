FROM python:latest

# Install dependencies
COPY requirements-email.txt .
RUN pip install -r requirements-email.txt

# Copy files
COPY / .

# Run the application
CMD ["python", "email_send.py"]
