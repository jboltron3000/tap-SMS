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
    start_date = datetime.datetime.now() 
    end_date = (start_date + datetime.timedelta(-30))
    start_date = start_date.strftime('%m/%d/%Y')
    end_date = end_date.strftime('%m/%d/%Y')
    url = "https://www.smssoftware.net/tms/manTrafExp?fromDate=" + str(end_date) + "&toDate=" + str(start_date) + "&interval=0&hours=0&reqType=tdd&apiKey=75WAJ5WJLP44MAZC58B37T6N5BT8KD4J&locationId=TLS000"
    for tap_stream_id in ctx.selected_stream_ids:
	    page = ctx.client.request(tap_stream_id, "GET", url)
		#pdb.set_trace()
	    ctx.write_page(tap_stream_id, page)
