# set base image (host OS)
FROM python:3.9

# Environment setup
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

# System deps
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /work

# Install schema-automator + API server
RUN pip install schema-automator fastapi uvicorn

# Copy your API wrapper
COPY main.py .

# Replace this line:
# CMD [ "bash" ]
# With the command to launch FastAPI
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8080"]