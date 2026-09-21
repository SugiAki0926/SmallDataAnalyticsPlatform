select
    air_pollution_id,
    city_id::integer,
    (to_timestamp(dt) at time zone 'Asia/Tokyo') as air_pollution_at,
    created_at,
    updated_at,
    aqi as air_quality_index,
    co as carbon_monoxide,
    no as nitrogen_monoxide,
    no2 as nitrogen_dioxide,
    o3 as ozone,
    so2 as sulphur_dioxide,
    pm2_5 as fine_particulate_matter,
    pm10 as coarse_particulate_matter,
    nh3 as ammonia
from {{source('raw', 'air_pollution')}}
