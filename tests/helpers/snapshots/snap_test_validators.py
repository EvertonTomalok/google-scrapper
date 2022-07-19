# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_store_validation_ok 1'] = 'SUCCESS'

snapshots['test_store_validation_ok 2'] = {
    'platform': 'magazineluiza',
    'seller_default': 'Magazine Luiza',
    'status': 'S',
    'store_id': 1,
    'store_name': 'MAGAZINE LUIZA',
    'store_ref': 'Magazine Luiza',
    'store_table': 'magazine_luiza',
    'url': 'https://www.magazineluiza.com.br'
}

snapshots['test_store_validation_status_not_exist 1'] = 'ERROR'

snapshots['test_store_validation_status_not_exist 2'] = {
    'data_received': {
        'platform': 'magazineluiza',
        'seller_default': 'Magazine Luiza',
        'status': 'Sem Correspondencia',
        'store_id': 1,
        'store_name': 'MAGAZINE LUIZA',
        'store_ref': 'Magazine Luiza',
        'store_table': 'magazine_luiza',
        'url': 'https://www.magazineluiza.com.br'
    },
    'fields_with_error': [
        {
            'status': "The value from status must to be 'S' or 'N'."
        }
    ]
}

snapshots['test_validation_not_ok 1'] = 'ERROR'

snapshots['test_validation_not_ok 2'] = {
    'data_received': {
        'price_to': 200,
        'store_id': 1
    },
    'fields_with_error': [
        {
            'ean': 'This field is required.'
        },
        {
            'date': 'This field is required.'
        },
        {
            'hour': 'This field is required.'
        }
    ]
}

snapshots['test_validation_ok 1'] = 'SUCCESS'

snapshots['test_validation_ok 2'] = {
    'date': '2021-01-27',
    'ean': 123415,
    'hour': '11:20:00',
    'price_to': 200.0,
    'store_id': 1
}
