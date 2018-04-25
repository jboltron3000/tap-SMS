#!/usr/bin/env python3
import os
import pdb
import json
import singer
from singer import utils
from singer.catalog import Catalog, CatalogEntry, Schema
from . import streams as streams_
from .context import Context
from . import schemas

REQUIRED_CONFIG_KEYS = ["start_date", "access_token", "username", "password"]
LOGGER = singer.get_logger()


def check_credentials_are_authorized(ctx):
    pass


def discover(ctx):
    check_credentials_are_authorized(ctx)
    catalog = Catalog([])
    for tap_stream_id in schemas.stream_ids:
        schema = Schema.from_dict(schemas.load_schema(tap_stream_id),
                                  inclusion="automatic")
        catalog.streams.append(CatalogEntry(
            stream=tap_stream_id,
            tap_stream_id=tap_stream_id,
            key_properties=schemas.pk_fields[tap_stream_id],
            schema=schema,
        ))
    return catalog


def sync(ctx):
    for tap_stream_id in ctx.selected_stream_ids:
        schemas.load_and_write_schema(tap_stream_id)
    streams_.sync_lists(ctx)
    ctx.write_state()


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    ctx = Context(args.config, args.state)
    if args.discover:
        ctx.catalog = discover(ctx)
        discover(ctx).dump()
        print()
    else:
        ctx.catalog = discover(ctx)
        ctx.selected_stream_ids = set(
            [s.tap_stream_id for s in ctx.catalog.streams]
        )
        sync(ctx)

if __name__ == "__main__":
    main()
