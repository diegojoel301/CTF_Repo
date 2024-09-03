#!/bin/bash
docker build -t minio/minio:RELEASE.2023-03-13T19-46-17Z.fips-rwctf .
docker run -e MINIO_UPDATE_MINISIGN_PUBKEY= -e MINIO_ROOT_USER=rwctf -e MINIO_ROOT_PASSWORD=rwctf123_for_player -d -p 9000:9000 -p 9090:9090 minio/minio:RELEASE.2023-03-13T19-46-17Z.fips-rwctf server /data --console-address ':9090'