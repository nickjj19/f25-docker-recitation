# specifies the Parent Image from which you are building.
FROM python:3.9

# specify the working directory for the image
WORKDIR /code

# TODO
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install deps (use requirements.txt if you have one)
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# If you don't have requirements.txt, comment the two lines above and use:
# RUN pip install --no-cache-dir fastapi uvicorn requests

# Copy app code
COPY ./app /code/app

# Expose port
EXPOSE 8080

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]