#python image from dockerhub
FROM python:3.9-alpine3.13
#name of the DOCKER IMAGE maintainer, optional
LABEL maintainer = "naman arora"

#do not buffer the output, print directly on screen, prevents delays from python to screen
ENV PYTHONUNBUFFERED 1

# copy files from local machine to docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
#def dir from where our commands will be running -> from base django proj folder in this case
WORKDIR /app
#expose the port needed for uk what
EXPOSE 8000 
#defines build arguement DEV defaulting to false, docker-compose can overwrite it to true
ARG DEV=false
#run command runs commands on python image, multiple commands can be seperated by "&& \" and its beneficial to run multiple commands inn a single command
# Multiple rum commands keeps on adding image layers so we avoid doing that
#create virtual environment in /py
#(virtual env is optional inside a dockerfile, but it might have some benefirs in the edge cases, so its better to include it)
RUN python -m venv /py && \
    #upgrade pip installer, install all requirements from .txt and then delete the .txt file to keep docker image as lightweight as possible
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # /py/bin/pip install flake8 && \
    #shell scripting if statement, ends with fi, only install dev req(flake8) if we are in development environment
    if [$DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    #we add user to ensure that,WE DONT USE THE ROOT USER with full priveledges,full access
    #DO NOT RUN YOUR APPLICATION USING ROOT USER, SO THAT INCASE OF A BREACH, ATTACKER DOESNT HAVE FULL ACCESS
    adduser \
        #we donot need password for this user,DO IT BY DEFAULT WHEN WE RUN IT
        --disabled-password \
        #do not create home dir for this user,to keep iage lightweight
        --no-create-home \
        #name
        django-user 
        
#updates env variable, PATH
#ass this to system path
ENV PATH = "/py/bin:$PATH"


#using this line, we switch user from root user to django-user
#before this point, root user was needed to setup the docker image, but now we can shift to the django-uuser with less permissions
USER django-user