dan# 2023CISCN

## RUN IN DOCKER

```bash
docker build -t cicsn .
#build it first
docker-compose up -d
```

## FUNCTION

`--mysql` use mysql
default is sqlite

`--scan` scan the ip which is alive,  default it uses nmap

`--scan scan-fscan`, use fscan which is faster than the default one


`--port` find the open port from an ip, default it uses nmap

`--port port-allscan`, use nmap to scan 1-65535 port, it takes lots of time so be careful when using

`--port port-fscan`, use fscan which is faster than the default one


`--services` find the web service fingerprint, protocol and more information on certain ip

`--SERVICES services-fscan-protocol` Using fscan to identify the protocols used by the corresponding IP addresses, it is worth noting that, due to the characteristics of fscan itself, in order to save resources and improve efficiency, we have saved the web application detection by fscan during port scanning


`--honeypot` Check honeypot use the api

`--scale` if you use scale mode in docker-compose, please make sure you have this options to hava a random delay before running


