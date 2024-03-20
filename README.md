# tha1_Lighthouse

## 简介

Lighthouse 灯塔，一个开源资产测绘平台

支持的功能包括：ip的端口/协议/服务探测，基于dom树的网络框架识别，兼容fofa/QUAKE数据，
支持mysql/sqlite，基于云的分布式高并发扫描

## cloud distributed scanning
基于云的分布式扫描

```bash
docker build -t cicsn .
#在运行前先将dockerfile先build了
docker-compose up -d
#你可以更改其中的replicas参数来启用多个容器实现并发扫描
```

## Command
命令

```bash
python main.py <OPTIONS>
#运行指令
python json.py <FILENAME>
#导出文件，FILENAME为导出文件名，默认为output.json
```

第一次记得选定数据库（--mysql/sqlite），第二次运行会追加在之前的结果中

全量扫描顺序（不按照顺序会缺少上游数据无法运行）：1.指定数据库 2.scan 3.port 4.service



OPTIONS有如下：

`--mysql` 使用MYSQL模块（支持分布式），默认使用为SQLITE模块（不支持分布式）

`--scan` 使用默认探活工具NAMP

`--scan scan-fscan`, 使用探活工具FSCAN

`--port` 使用默认端口扫描工具NMAP

`--port port-allscan`, 使用NMAP进行全端口扫描

`--port port-fscan`, 使用FSCAN进行端口扫描

`--port port-fofa`, 使用FOFA进行端口扫描

`--port port-quake`, 使用QUAKE进行端口扫描

`--services` 使用默认工具KSCAN进行端口/协议/服务探测

`--services services-fscan-protocol` 使用FSCAN进行协议探测，前提是以及执行过FSCAN端口探测

`--honeypot` 使用默认的工具QUAKE识别蜜罐

`--honeypot fofa` 使用FOFA识别蜜罐

`--honeypot quake-dump` 使用QUAKE的DUMP数据识别蜜罐

`--scale` 如果你在并发执行，请在命令中加入该选项以随机启动时间

`--webapp` 使用基于Dom树的算法识别网络框架，需要chromedirver

