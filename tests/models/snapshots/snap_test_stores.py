# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_stores_ok 1'] = {
    'platform': 'magazineluiza',
    'seller_default': 'Magazine Luiza',
    'status': 'S',
    'store_id': 1,
    'store_name': 'MAGAZINE LUIZA',
    'store_ref': 'Magazine Luiza',
    'store_table': 'magazine_luiza',
    'url': 'https://www.magazineluiza.com.br'
}
