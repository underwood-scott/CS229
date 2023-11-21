import cdsapi

c = cdsapi.Client()

# loop through all years
for year in range(1994,2020,1):
    # retrieve grib file for year of interest
    c.retrieve(
        'cems-fire-seasonal',
        {
            'format': 'grib',
            'variable': [
                'burning_index', 'energy_release_component', 'ignition_component',
                'spread_component',
            ],
            'year': str(year),
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': '01',
            'leadtime_hour': [
                '12', '36', '60',
                '84', '108', '132',
                '156', '180', '204',
                '228', '252', '276',
                '300', '324', '348',
                '372', '396', '420',
                '444', '468', '492',
                '516', '540', '564',
                '588', '612', '636',
                '660', '684', '708',
                '732',
            ],
            'area': [
                67.1, -165.8, 17.9,
                -65.4,
            ],
            'release_version': '5',
        },
        'data/{}_us_data.grib'.format(str(year)))
