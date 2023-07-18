import mysqldb
import main
import logging
import json

## init db
logger = main.logs()
# logger = main.logs()
logger.info("Program Start")
db = mysqldb.db(logger)

# content_str = db.get_api_from_ip_and_method("16.163.13.11","port-fofa")
# print(content_str)
# content = json.loads(content_str)
# print(content["results"])

iplist = db.get_all_ip()
flag = 0
for ip in iplist:
    print(ip)
    # if ip == '165.22.22.166':
    #     flag = 1
    # if flag == 1:
    content_str = db.get_api_from_ip_and_method(ip, "port-fofa")
    if content_str is not None:
    # print(content_str)
        content = json.loads(content_str)
        # print(content["results"])
        for i in content["results"]:
            ## 换成\t; 进行分割，方便后续json_output

            try:
                serviceapp = i[4].replace(',','\t; ')
            except:
                serviceapp = i[4]
            db.add_services(i[1],i[2])
            db.add_service_app(i[1],i[2],serviceapp)