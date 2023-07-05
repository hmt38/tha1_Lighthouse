import sys
import logging


def logs(filename='logs.txt', level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    fh = logging.FileHandler(filename)
    fh.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(
        "[%(asctime)s]\t[%(thread)d]\t[%(filename)s]\t[line: %(lineno)d]\t[%(levelname)s]\t#%(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    logger = logs()
    logger.info("Program Start")

    argv = [x.lower() for x in sys.argv]
    if "--mysql" in argv or "-m" in argv:
        logger.debug("Database: Mysql")
        import mysqldb

        db = mysqldb.db(logger)
    else:
        logger.debug("Database: Sqlite")
        import sqlite

        db = sqlite.db(logger)

    import default

    for item in default.ip_src:
        db.add_scan(item)

    if "--scan" in argv or "-s" in argv:
        logger.debug("SCAN Mode")
        import scan

        if "scan-xxxx" in argv:
            app = scan.app(db, logger, method="scan-xxxx")
        else:
            app = scan.app(db, logger)

    if "--port" in argv or "-p" in argv:
        logger.debug("PORT Mode")
        import port

        if "port-xxxx" in argv:
            app = port.app(db, logger, method="port-xxxx")
        else:
            app = port.app(db, logger)

    if "--services" in argv or "-se" in argv:
        logger.debug("SERVICES Mode")
        import services

        if "services-xxxx" in argv:
            app = services.app(db, logger, method="services-xxxx")
        else:
            app = services.app(db, logger)

    app.run()
