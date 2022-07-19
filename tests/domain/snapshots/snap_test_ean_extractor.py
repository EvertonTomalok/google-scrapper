# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_extracting_ean_multiple_stores 1'] = {
    'product_link': '',
    'search_ean': '889894929969',
    'single_store': False,
    'status': 'M'
}

snapshots['test_extracting_ean_not_found 1'] = {
    'status': 'N'
}

snapshots['test_extracting_ean_ok 1'] = {
    'product_link': 'https://www.google.com/shopping/product/16797439570901513171?biw=1324&bih=576&sxsrf=ALeKk03T97qKezPlInGA0wm235_ZU1VjKA:1611085291344&q=7891114090307&oq=7891114090307&gs_lcp=Cgtwcm9kdWN0cy1jYxAMOgcIIxCwAxAnOgcIIxDqAhAnOgsIrgEQygMQ6gIQJ1DvueYJWO-55glg0cHmCWgCcAB4AIAB_AGIAfwBkgEDMi0xmAEAoAEBoAECqgEPcHJvZHVjdHMtY2Mtd2l6sAEQyAEBwAEB&sclient=products-cc&prds=epd:4027024290362439363,prmr:1&sa=X&ved=0ahUKEwi__YueranuAhXsguAKHboOB_gQ3q4ECGI#online',
    'search_ean': '7891114090307',
    'status': 'S'
}

snapshots['test_extracting_ean_single 1'] = {
    'product_link': 'https://www.google.com/aclk?sa=L&ai=DChcSEwi00N-54ajuAhULEpEKHVoaDUoYABABGgJjZQ&sig=AOD64_0gHq8SjeonSXjMKDeD3dqGaEoZag&ctype=5&q=&ved=0ahUKEwjAxNu54ajuAhVzIbkGHUy9C_IQgeUECFE&adurl=',
    'search_ean': '7898617108027',
    'single_store': True,
    'status': 'U'
}
