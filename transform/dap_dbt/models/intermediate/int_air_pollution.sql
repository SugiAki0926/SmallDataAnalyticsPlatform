select
    sa.city_id,
    sl.city_name_en,
    sa.air_pollution_at,
    sa.carbon_monoxide,
    sa.nitrogen_monoxide,
    sa.nitrogen_dioxide,
    sa.ozone,
    sa.sulphur_dioxide,
    sa.fine_particulate_matter,
    sa.coarse_particulate_matter,
    sa.ammonia
from
    {{ ref('stg_air_pollution') }} as sa
inner join
    {{ ref('stg_locations') }} as sl
on sa.city_id = sl.city_id
