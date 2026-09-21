{% snapshot snap_locations %}

{{
    config(
        schema='snapshots',
        unique_key='city_id',
        strategy='check',
        check_cols=[
            'city_name_en',
            'city_name_ja',
        ],
    )
}}

select
    city_id,
    city_name_en,
    city_name_ja,
    country_code,
    created_at,
    updated_at
from {{ ref('stg_locations') }}

{% endsnapshot %}
