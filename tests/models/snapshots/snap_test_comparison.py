# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_comparison_valid_complete 1'] = {
    'date': '2021-01-27',
    'ean': 121341,
    'hour': '10',
    'price_to': 2.0,
    'store_id': 1
}
