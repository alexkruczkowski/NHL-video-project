FROM python:latest

# Install dependencies
COPY requirements-etl.txt .
RUN pip install -r requirements.txt

# Copy files
COPY / .

# Run the application
CMD ["python", "nhl_etl.py"]
