select
    city_id,
    name as city_name_en,
    local_name as city_name_ja,
    country as country_code,
    lat as city_latitude,
    lon as city_longitude,
    created_at,
    updated_at
from {{source('raw', 'locations')}}
