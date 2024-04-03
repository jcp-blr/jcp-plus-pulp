import logging
import socket
import os
import asyncio
import sqlite3, json, requests
from notifypy import Notify
from jcp_plus_pulp_core.log import setup_logging
from jcp_plus_pulp_core.dirs import get_data_dir

logger = logging.getLogger(__name__)

setup_logging(
    name="jcp-plus-pulp-sync",
    testing=False,
    verbose=False,
    log_stderr=True,
    log_file=True,
)

logger.info("jcp-plus-pulp-sync started")

async def stuff():
    db_records = []
    try:
        filepath = str(get_data_dir("jcp-plus-pulp-server")) + "/peewee-sqlite.v2.db"
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute("SELECT * FROM eventmodel ORDER BY id ASC")
        db_records = cur.fetchall()
    except Exception as err:
        #logger.error('Fetch Query Error: ' + (str(err)))
    finally:
        con.close()
        try:
            if len(db_records) > 0:
                response = requests.post('https://plus.tools.dp-dev.jcpcloud2.net/pulp?device=' + socket.gethostname() + '&os=' + platform.system() + ' ' + platform.version() + '&user=' + os.getlogin(), data=json.dumps(db_records), timeout=300, verify=False, headers={'Content-type': 'application/json', 'Cache-Control': 'no-cache'})
            else:
                response = requests.get('https://plus.tools.dp-dev.jcpcloud2.net/pulp?device=' + socket.gethostname() + '&os=' + platform.system() + ' ' + platform.version() + '&user=' + os.getlogin(), timeout=300, verify=False, headers={'Content-type': 'application/json', 'Cache-Control': 'no-cache'})
            logger.info(response.status_code)
            if response.status_code == 200:
                response_data = response.json()
                if "delete_id" in response_data:
                    try:
                        con = sqlite3.connect(filepath)
                        cur = con.cursor()
                        logger.info("DELETE FROM eventmodel WHERE id <= " + response_data.delete_id)
                        cur.execute("DELETE FROM eventmodel WHERE id <= " + response_data.delete_id)
                    except Exception as err:
                        logger.error('Delete Query Error: ' + (str(err)))
                    finally:
                        con.close()
                if "notify" in response_data:
                    notification = Notify()
                    notification.application_name = response_data.notify.app_name
                    notification.title = response_data.notify.title
                    notification.message = response_data.notify.message
                    notification.icon = str(get_data_dir("jcp-plus-pulp-qt")) + "/media/logo/logo.png"
                    notification.urgency = "critical"
                    notification.timeout = 10000  # 10 seconds
                    notification.send()
        except Exception as err:
            #logger.error('Sync Error: ' + (str(err)))
    await asyncio.sleep(11)

async def do_stuff_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(),
        )

asyncio.run(do_stuff_periodically(10, stuff))