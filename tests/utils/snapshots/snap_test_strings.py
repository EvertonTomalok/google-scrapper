# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_sanitize_attribute[110V] 1'] = '110'

snapshots['test_sanitize_attribute[127V] 1'] = '110'

snapshots['test_sanitize_attribute[200V] 1'] = '220'

snapshots['test_sanitize_attribute[220V] 1'] = '220'

snapshots['test_sanitize_attribute[BIVOLT] 1'] = 'BIVOLT'
