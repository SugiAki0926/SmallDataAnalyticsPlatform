select
    id as city_id,
    year,
    jan,
    feb,
    mar,
    apr,
    may,
    jun,
    jul,
    aug,
    sep,
    oct,
    nov,
    dec
from
    {{ref('kyoto_historical_weather')}}
