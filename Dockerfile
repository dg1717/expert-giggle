# Use the official Python image
FROM python:latest

# Set the working directory in the container
WORKDIR /path/in/container

# Copy the local directory into the container at /path/in/container
COPY . /path/in/container

# Setup virtual environment
RUN python3 -m venv myenv
RUN /bin/bash -c "source myenv/bin/activate"

# Install system dependencies for aiohttp and ChromeDriver
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Install Google Chrome within the Docker container
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install requirements, including WebDriver Manager
RUN pip install -r /path/in/container/requirements.txt

# Run Behave tests
CMD ["behave", "features"]