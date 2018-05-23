import singer
import pdb
from .schemas import IDS
import datetime 

LOGGER = singer.get_logger()

def metrics(tap_stream_id, records):
    with singer.metrics.record_counter(tap_stream_id) as counter:
        counter.increment(len(records))

def write_records(tap_stream_id, records):
    singer.write_records(tap_stream_id, records)
    metrics(tap_stream_id, records)
            
def sync_lists(ctx):
    start_date =  singer.utils.strptime_with_tz(ctx.state["traffic"])
    end_date = singer.utils.now()
    start_date = start_date.strftime('%m/%d/%Y-%H|%M')
    pdb.set_trace()
    end_date = end_date.strftime('%m/%d/%Y')
    apiKey = ctx.config['access_token']
    url = "https://www.smssoftware.net/tms/manTrafExp?fromDate=" + str(start_date) + "&toDate=" + str(end_date) + "&interval=0&hours=0&reqType=tdd&apiKey=" + str(apiKey) + "&locationId=TLS000"
    for tap_stream_id in ctx.selected_stream_ids:
	    page = ctx.client.request(tap_stream_id, "GET", url)
	    ctx.write_page(tap_stream_id, page)
