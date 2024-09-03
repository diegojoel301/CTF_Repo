FROM node:21-alpine

ENV LANG="C.UTF-8" PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV FLAG_IMAGE="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAAEiAQAAAAB1xeIbAAABg0lEQVR4nO2aQWrDMBBF39SGLBXoAXIU5WY9U29gHyUHKEjLgMvvwpKbJtB248iJNCt7eKDPaDzMDDbxt40v/4CgUY1qVKMatXXKkvUwWg/E7DkW1VUF5SVJAcCdDegkSfpJ3V9XFVRMOW5vAeYns768rmem+htPfBXE9U5s1K+UHe99YpVUznsnrrL9cujaqvrHplLsRwOgW/yfttaJjco2x/4ix8c9lj6DkrrqoewYU38vBdCQXwvrem6KuY8fnARuSr7BSfiQmnwNW1X/2BRphHITGmDO+3nUGlhuZqvqH5vie3y9vAWXR1rfYr8adRF7fIBUeObPoNWcValUVRbL5aYTPrSasyo1tzK5me8mwWfqO8fDlBudrap/CmrZY5rtIRWeuJMdy+qqgorLrj7uhD/15G1yWV3PTN3uMV1A4+Fs+EDb369J3cTevxv4006M+1BOVw3U9R5TxG6y8XA2EfupmK4aqOs9pgEm4k7gPkyldNVAWfs3qlGNalSjqqC+AAcsx/qNFOr4AAAAAElFTkSuQmCC"

RUN apk update
RUN apk add --no-cache zlib-dev udev nss ca-certificates
RUN apk add --no-cache chromium
RUN apk add --no-cache nginx redis python3 py3-pip
RUN yarn cache clean
RUN rm -rf /tmp/* /etc/apk/* /var/cache/apk/* /usr/share/man

COPY nginx.conf /etc/nginx/nginx.conf
COPY certs /etc/nginx/ssl

COPY frontend/deploy.tar /tmp/deploy.tar
RUN mkdir /var/www/rest
RUN tar -xvf /tmp/deploy.tar -C /var/www/rest

WORKDIR /bot
COPY bot .
RUN npm install

WORKDIR /app
COPY backend .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt --break-system-packages

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]