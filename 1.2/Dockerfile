# dockerfile, image(linux image), container

# First let's build our dockerfile
## specify base imgae
FROM python:3.8

##Select work directory
WORKDIR /noonPyMe/1.2

## Adding our package into our container
COPY  . /noonPyMe/1.2

## configure the logger file
RUN mkdir __logger
# ----------------------------------------------------
#Before installing selenium to the image, i need to install chrome at the top of the image, since i will use selenium.
# Here, we're using google chrome since it doesn't display user interface which is providing more performace
## Adding trusting keys apt for the repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

## Adding google chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

## Updating apt to see, and install chrome
RUN apt-get -y update

## Install google chrome
RUN apt-get install -y google-chrome-stable
# ----------------------------------------------------
# Install Chrome Driver
## Download the chrome driver
RUN wget -O  /tmp/chromedriver.zip  http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

## Unzip the chrome driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip  chromedriver -d /usr/local/bin/

## set the display port as environment variable (set the display port (99) as Selenium is using this. It will avoid some crushes.)
ENV DISPLAY=99
# ----------------------------------------------------
## installing our libraries
RUN pip install --upgrade pip
RUN pip3 install selenium  

## specify our entry interaction language
 CMD [ "python",  "./deploy.py"]

# Second, let's build our docker image (if you modified your module after building your image, you've to re-build it again)
 ## docker build -t @NameOfImage @location

 # ----------------------------------------------------
 ## Run the image
 ## docker run @NameOfImage

 ## Run interactive mode
 ## docker run -ti  @NameOfImage
 
 ## Run I/O dockor to download written file
#  docker run -it --rm -v $(pwd)/directory:/directory @NameOfImage
