FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install pip and build tools
RUN pip install --upgrade pip setuptools wheel

# Copy project files
COPY . .

# Install dependencies from pyproject.toml
RUN pip install .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]