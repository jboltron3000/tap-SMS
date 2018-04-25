import singer
import pdb
from .schemas import IDS


LOGGER = singer.get_logger()


def metrics(tap_stream_id, records):
    with singer.metrics.record_counter(tap_stream_id) as counter:
        counter.increment(len(records))

def write_records(tap_stream_id, records):
    singer.write_records(tap_stream_id, records)
    metrics(tap_stream_id, records)
            
def sync_lists(ctx):
	for tap_stream_id in ctx.selected_stream_ids:
		page = ctx.client.request(tap_stream_id, "GET", "https://www.smssoftware.net/tms/manTrafExp?fromDate=01/01/2018&toDate=01/21/2018&interval=60&hours=0&reqType=td&apiKey=75WAJ5WJLP44MAZC58B37T6N5BT8KD4J&locationId=TLS000")
		#pdb.set_trace()
		ctx.write_page(tap_stream_id, page)
