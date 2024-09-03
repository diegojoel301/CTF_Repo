#!/bin/bash

# 启动 PostgreSQL 服务
/etc/init.d/postgresql start
chmod +s /readflag
sed -i "s/uuid/`uuid`/g" init.sql


sudo -u postgres psql -U postgres -f /init.sql
rm -f /init.sql

sleep 2
useradd java
# 运行 Spring Boot 应用
nohup sudo -u java /usr/local/openjdk-17/bin/java -jar /ChatterBox-0.0.1-SNAPSHOT.jar &

tail -f /etc/passwd