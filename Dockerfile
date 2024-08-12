FROM python:alpine3.19

# Set working directory in the container
WORKDIR /cf-api

# Copy local contents to the container
COPY . /cf-api

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable for the download_files.py script
ENV FILES_TO_DOWNLOAD=20

# Run the download_files.py
RUN echo $FILES_TO_DOWNLOAD | python download_files.py

# Add new user and group ids
ARG USER_ID
ARG GROUP_ID
RUN addgroup -g $GROUP_ID myuser && \
    adduser -u $USER_ID -G myuser -h /home/myuser -D myuser

# Change ownership of the working directory to the created user
RUN chown -R myuser:myuser /cf-api

# Create the database directory and set permissions
RUN mkdir -p /cf-api/data && chown -R myuser:myuser /cf-api/data

# Switch to the created user
USER myuser

# Make port 8000 available
EXPOSE 8000

# Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]