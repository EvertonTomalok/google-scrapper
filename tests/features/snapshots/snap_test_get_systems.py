# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_available_systems 1'] = {
    'CASAS BAHIA': {
        'store_id': 2,
        'store_name': 'CASAS BAHIA',
        'store_ref': 'Casas Bahia',
        'system': 'casasbahia'
    },
    'MAGAZINE LUIZA': {
        'store_id': 1,
        'store_name': 'MAGAZINE LUIZA',
        'store_ref': 'Magazine Luiza',
        'system': 'magazineluiza'
    }
}
