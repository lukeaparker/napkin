# Base image
FROM alpine:3.14

# Copy the code into a folder named app
ADD . /app

# switch the working directory to app
WORKDIR /app

# Install python and node
RUN apk add py3-pip
RUN apk add --update nodejs npm

RUN pip install Flask

# Install python dependencies
RUN pip3 install -r requirements.txt

# Install node dependencies  
RUN npm install 


EXPOSE 5000
CMD [ "npm", "start" ]

