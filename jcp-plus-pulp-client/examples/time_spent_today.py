# NOTE: Might not treat timezones correctly.

from datetime import datetime, time, timedelta
import socket

import jcp_plus_pulp_client

if __name__ == "__main__":
    # Set this to your AFK bucket
    bucket_id = f"jcp-plus-pulp-monitor-away_{socket.gethostname()}"

    daystart = datetime.combine(datetime.now().date(), time())
    dayend = daystart + timedelta(days=1)

    awc = jcp_plus_pulp_client.PULPMonitorClient("testclient")
    events = awc.get_events(bucket_id, start=daystart, end=dayend)
    events = [e for e in events if e.data["status"] == "not-afk"]
    total_duration = sum((e.duration for e in events), timedelta())
    print(f"Total time spent on computer today: {total_duration}")
