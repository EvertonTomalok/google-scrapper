# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_data_quality_ok 1'] = {
    'brand': 'CADENCE',
    'ean': 1,
    'product_name': 'Cafeteira',
    'provider': ''
}
