FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Install Python's requirements
COPY src/web_service/requirements.txt /src/
RUN pip install -r requirements.txt
