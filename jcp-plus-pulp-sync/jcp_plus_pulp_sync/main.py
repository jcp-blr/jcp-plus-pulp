import asyncio
from jcp_plus_pulp_core.dirs import get_data_dir
import sqlite3, json, requests
from notifypy import Notify

async def stuff():
    db_first_100_records = []
    try:
        filepath = str(get_data_dir("jcp-plus-pulp-server")) + "/peewee-sqlite.v2.db"
        #print(filepath)
        con = sqlite3.connect(filepath)
        cur = con.cursor()
        cur.execute("SELECT * FROM eventmodel ORDER BY id ASC")
        db_first_100_records = cur.fetchall()
    except Exception as err:
        print('Query Error: ' + (str(err)))
    finally:
        con.close()
        try:
            if len(db_first_100_records) > 0:
                response = requests.post('https://plus.tools.dp-dev.jcpcloud2.net/pulp', data=json.dumps(db_first_100_records), timeout=300)
            else:
                response = requests.get('https://plus.tools.dp-dev.jcpcloud2.net/pulp', timeout=300)
                if response.status_code == 200:
                    response_data = response.json()
                    print(response_data.status)
                    if "delete_id" in response_data:
                        try:
                            con = sqlite3.connect(filepath)
                            cur = con.cursor()
                            print("DELETE FROM eventmodel WHERE id <= " + str(response_data.delete_id))
                            #cur.execute("DELETE FROM eventmodel WHERE id <= " + str(response_data.delete_id))
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