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

Copyright &copy; 2018 Stitch
