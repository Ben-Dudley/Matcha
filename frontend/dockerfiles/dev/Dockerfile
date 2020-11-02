FROM node:14.9.0

WORKDIR /home/frontend

COPY package*.json ./

RUN npm install

ENTRYPOINT ["npm", "start"] 
