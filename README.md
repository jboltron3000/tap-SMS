# tap-SMS

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [Lightspeed Retail](https://www.lightspeedhq.com/) and [SMS Software](https://storetraffic.com/)
- Extracts the following resources:
  - [Traffic](http://help.storetraffic.com/tmas-manage-locations-web-api?from_search=22892211)
  - [Inventory](https://developers.lightspeedhq.com/retail/tutorials/inventory/)
  - [Order](https://developers.lightspeedhq.com/retail/endpoints/Order/)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

Copyright &copy; 2018 Stitch
