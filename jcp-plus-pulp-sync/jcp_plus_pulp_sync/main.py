import logging
from jcp_plus_pulp_core.log import setup_logging

import socket
import os
import asyncio
from jcp_plus_pulp_core.dirs import get_data_dir
import sqlite3, json, requests
from notifypy import Notify

logger = logging.getLogger(__name__)

setup_logging(
    name="jcp-plus-pulp-sync",
    testing=False,
    verbose=False,
    log_stderr=True,
    log_file=True,
)

logger.info("jcp-plus-pulp-sync started")
print("logged")

async def stuff():
    db_records = []
    try:
        filepath = str(get_data_dir("jcp-plus-pulp-server")) + "/peewee-sqlite.v2.db"
        logger.info("jcp-plus-pulp-sync db filepath is " + str(filepath))
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute("SELECT * FROM eventmodel ORDER BY id ASC")
        db_records = cur.fetchall()
        
    except Exception as err:
        print('Query Error: ' + (str(err)))
    finally:
        con.close()
        try:
            if len(db_records) > 0:
                response = requests.post('https://plus.tools.dp-dev.jcpcloud2.net/pulp?hostname=' + socket.gethostname() + '&username=' + os.getlogin(), data=json.dumps(db_records), timeout=300)
            else:
                response = requests.get('https://plus.tools.dp-dev.jcpcloud2.net/pulp?hostname=' + socket.gethostname() + '&username=' + os.getlogin(), timeout=300)
                if response.status_code == 200:
                    response_data = response.json()
                    print(response_data.status)
                    if "delete_id" in response_data:
                        try:
                            con = sqlite3.connect(filepath)
                            cur = con.cursor()
                            cur.execute("DELETE FROM eventmodel WHERE id <= " + response_data.delete_id)
                        except Exception as err:
                            print('Query Error: ' + (str(err)))
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
            print('Sync Error: ' + (str(err)))
    await asyncio.sleep(10)

async def do_stuff_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(),
        )

asyncio.run(do_stuff_periodically(10, stuff))