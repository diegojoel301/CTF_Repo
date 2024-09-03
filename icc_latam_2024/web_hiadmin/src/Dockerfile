FROM node:17.6

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY ./ ./

EXPOSE 3000

USER appuser

CMD node index.js