# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_product_ok 1'] = {
    'attribute_name': 'voltagem',
    'attribute_value': '110V',
    'ean': 123456769,
    'product_reference': 'tw-1000',
    'seller_name': 'Magalu',
    'sku': 'wv12345',
    'status': 'S',
    'store_id': 1,
    'url': 'https://example.com'
}

snapshots['test_product_ok_with_fields_not_required 1'] = {
    'ean': 123456769,
    'sku': 'wv12345',
    'status': 'N',
    'store_id': 1,
    'url': 'https://example.com'
}
