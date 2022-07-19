from src.features.get_systems import available_systems


def test_available_systems(snapshot):
    mocked_value = [
        {
            'store_id': 1,
            'store_name': 'MAGAZINE LUIZA',
            'store_ref': 'Magazine Luiza',
            'system': 'magazineluiza'
        },
        {
            'store_id': 2,
            'store_name': 'CASAS BAHIA',
            'store_ref': 'Casas Bahia',
            'system': 'casasbahia'
        },
    ]

    available = available_systems(mocked_value)

    snapshot.assert_match(available)
