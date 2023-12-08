#!/usr/bin/env python3
import cdsapi

c = cdsapi.Client()

# loop through all years
for year in range(1992,2021,1):
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'grib',
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
                'boundary_layer_height', 'cloud_base_height', 'convective_available_potential_energy',
                'convective_rain_rate', 'convective_snowfall', 'leaf_area_index_high_vegetation',
                'leaf_area_index_low_vegetation', 'runoff', 'soil_type',
                'total_precipitation',
            ],
            'year': str(year),
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': '12:00',
            'area': [
                70.34, -178.8, 17.94,
                -65.26,
            ],
        },
        'data/{}_us_data.grib'.format(str(year)))