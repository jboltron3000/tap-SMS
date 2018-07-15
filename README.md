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
     	 "username": "your-jira-username",
     	 "password": "your-jira-password",
     	 "base_url": "https://your-jira-domain"
 	}
 	
 	The start_date specifies the date at which the tap will begin pulling data (for those resources that support this).
---

Copyright &copy; 2018 Stitch
