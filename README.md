# tap-SMS

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from[SMS Software WEB API](https://storetraffic.com/)
- Extracts the following resources:
  - [Traffic](http://help.storetraffic.com/tmas-manage-locations-web-api?from_search=22892211)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

# 1. Quick Start

1. Install

	pip install tap-jira

2. Create the config file

	Create a JSON file called config.json. Its contents should look like:

 	{
    	 "start_date": "2010-01-01",
     	 "client_id" : 123456,
         "token" : "12345689790980988976876"
 	}
 	
 	The start_date specifies the date at which the tap will begin pulling data (for those resources that support this).

3. Run the Tap in Discovery Mode

    tap-SMS -c config.json --discover > properties.json

4. Run the Tap in Sync Mode

tap-SMS -c config.json --catalog properties.json
---

Copyright &copy; 2018 Stitch
