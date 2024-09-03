FROM --platform=linux/amd64 debian:bookworm AS builder

RUN apt update && apt install -y make gcc git
RUN git clone https://github.com/wolfcw/libfaketime.git && \
    cd libfaketime && \
    git checkout a04750217b8dc890ac584b92229d8c4a3f23c3e0 && \
    make

FROM --platform=linux/amd64 node:21.7.2-bookworm

WORKDIR /app
RUN apt update && apt install -y chromium
COPY --from=builder /libfaketime/src/libfaketime.so.1 /usr/local/lib/libfaketime.so.1
COPY .yarn .yarn
COPY package.json yarn.lock .yarnrc.yml ./
RUN yarn install
COPY . .
RUN yarn build
CMD ["yarn", "start"]
