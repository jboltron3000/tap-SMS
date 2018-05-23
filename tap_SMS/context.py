from datetime import datetime, date, timedelta
import time
import strict_rfc3339
import pdb
import pendulum
import pytz
import singer
from singer import bookmarks as bks_
from .http import Client
from singer import metrics
import json

class Context(object):
    """Represents a collection of global objects necessary for performing
    discovery or for running syncs. Notably, it contains

    - config  - The JSON structure from the config.json argument
    - state   - The mutable state dict that is shared among streams
    - client  - An HTTP client object for interacting with the API
    - catalog - A singer.catalog.Catalog. Note this will be None during
                discovery.
    """
    def __init__(self, config, state):
        self.config = config
        self.state = state
        self.client = Client(config)
        self._catalog = None
        self.selected_stream_ids = None

    @property
    def catalog(self):
        return self._catalog

    @catalog.setter
    def catalog(self, catalog):
        self._catalog = catalog
        self.selected_stream_ids = set(
            [s.tap_stream_id for s in catalog.streams
             if s.is_selected()]
        )

    def bookmarks(self):
        if "bookmarks" not in self.state:
            self.state["bookmarks"] = self.state
        return self.state["bookmarks"]

    def bookmark(self, path):
        bookmark = self.bookmarks()
        for p in path:
            if p not in bookmark:
                bookmark.clear()
                bookmark['type'] = "STATE"
                bookmark['traffic'] = p  
        return bookmark

    def set_bookmark(self, path, val):
        if isinstance(val, datetime):
            val = val.isoformat()
        self.bookmark(path[:-1])[path[-1]] = val

    def update_start_date_bookmark(self, path):
        val = self.bookmark(path)
        if not val:
            val = self.config["start_date"]
            self.set_bookmark(path, val)
        return val

    def write_state(self):
        singer.write_state(self.state)
        f = open("state.json", 'w')
        message = json.dumps(self.state)
        f.write(str(message))
        f.close()
        
        
    def write_page(self, stream_ids, page):
        title = page['TRAFFIC']
        data = title['data']
        ext_time = singer.utils.now()
        path = []
        for item in data:
            ext_time = item['@trafficDate']
            #pdb.set_trace()
            singer.write_record(stream_ids, item)
            counter = metrics.record_counter(stream_ids)
            counter.increment(len(item))
        #ext_time = ext_time.timestamp()
        #ext_time = strict_rfc3339.timestamp_to_rfc3339_utcoffset(ext_time)
        path.append(ext_time)
        self.update_start_date_bookmark(path)
            
