import singer
import pdb
from .schemas import IDS
from datetime import datetime, date, timedelta

LOGGER = singer.get_logger()

def metrics(tap_stream_id, records):
    with singer.metrics.record_counter(tap_stream_id) as counter:
        counter.increment(len(records))

def write_records(tap_stream_id, records):
    singer.write_records(tap_stream_id, records)
    metrics(tap_stream_id, records)
            
def sync_lists(ctx):
    end_date = singer.utils.strptime_with_tz(ctx.config['start_date'])
    while singer.utils.now() >= (end_date + timedelta(+2)):
        if len(ctx.state) < 2 and ctx.first_time == True:
            start_date = singer.utils.strptime_with_tz(ctx.config['start_date'])
        elif len(ctx.state) < 2 and ctx.first_time == False:
            start_date = end_date
        else:
            ctx.first_time = False
            start_date =  singer.utils.strptime_with_tz(ctx.state["traffic"])
        end_date = (start_date + timedelta(+30))
        if singer.utils.now() < end_date:
            end_date = singer.utils.now() + timedelta(-1)
        start_date = start_date.strftime('%m/%d/%Y-%H|%M')
        end_date = end_date.strftime('%m/%d/%Y')
        apiKey = ctx.config['access_token']
        url = "https://www.smssoftware.net/tms/manTrafExp?fromDate=" + str(start_date) + "&toDate=" + str(end_date) + "&interval=0&hours=0&reqType=tdd&apiKey=" + str(apiKey) + "&locationId=TLS000"
        for tap_stream_id in ctx.selected_stream_ids:
            page = ctx.client.request(tap_stream_id, "GET", url)
            page = page['TRAFFIC']
            #pdb.set_trace()
            if len(page) == 1:
                end_date = singer.utils.strptime_with_tz(end_date)
                ctx.first_time = False
            else:
                ctx.write_page(tap_stream_id, page)
                end_date = singer.utils.strptime_with_tz(end_date)
        