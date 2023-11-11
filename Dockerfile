FROM python:3.10.12

# Set the working directory in the container
WORKDIR /home/nonroot

# Create a group and user to run the app
# Note: The -S option does not exist in the addgroup and adduser for Ubuntu, it's used in Alpine
RUN groupadd -r nonroot && \
    useradd --no-log-init -r -g nonroot nonroot

# Copy the current directory contents into the container at /home/nonroot
COPY ./requirements.txt ./requirements.txt
COPY ./app.py ./app.py
COPY ./templates/ ./templates/
COPY ./list.txt ./list.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Change to non-root user
USER nonroot

# Run app.py when the container launches
CMD ["python", "app.py"]


