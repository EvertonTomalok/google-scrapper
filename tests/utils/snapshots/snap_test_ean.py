# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_generate_ean_variations_allowed[1010101010] 1'] = [
    '1010101010',
    '01010101010',
    '001010101010',
    '0001010101010'
]

snapshots['test_generate_ean_variations_allowed[11111111111] 1'] = [
    '11111111111',
    '011111111111',
    '0011111111111'
]

snapshots['test_generate_ean_variations_allowed[121212121212] 1'] = [
    '121212121212',
    '0121212121212'
]

snapshots['test_generate_ean_variations_allowed[1313131313131] 1'] = [
    '1313131313131'
]

snapshots['test_generate_ean_variations_allowed[88888888] 1'] = [
    '88888888',
    '088888888',
    '0088888888',
    '00088888888',
    '000088888888',
    '0000088888888'
]

snapshots['test_generate_ean_variations_allowed[999999999] 1'] = [
    '999999999',
    '0999999999',
    '00999999999',
    '000999999999',
    '0000999999999'
]

snapshots['test_generate_ean_variations_not_allowed[1234567] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[123456] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[12345] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[1234] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[123] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[12] 1'] = [
]

snapshots['test_generate_ean_variations_not_allowed[1] 1'] = [
]
