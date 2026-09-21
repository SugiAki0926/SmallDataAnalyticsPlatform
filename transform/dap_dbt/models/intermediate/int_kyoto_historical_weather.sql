select
    city_id,
    year,
    month,
    make_date(year, month, 1) as year_month,
    temperature_celsius
from
    {{ ref('stg_kyoto_historical_weather') }}
cross join lateral (
    values
        (1, jan),
        (2, feb),
        (3, mar),
        (4, apr),
        (5, may),
        (6, jun),
        (7, jul),
        (8, aug),
        (9, sep),
        (10, oct),
        (11, nov),
        (12, dec)
) as unpivoted(month, temperature_celsius)
where
    temperature_celsius is not null
