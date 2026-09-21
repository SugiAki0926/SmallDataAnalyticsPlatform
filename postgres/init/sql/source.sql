CREATE SCHEMA IF NOT EXISTS weather;


CREATE TABLE weather.locations (
    city_id         INTEGER PRIMARY KEY,

    name            VARCHAR(200) NOT NULL,
    local_name      VARCHAR(200),
    country         CHAR(2) NOT NULL,
    lat             DOUBLE PRECISION NOT NULL,
    lon             DOUBLE PRECISION NOT NULL,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_latitude
        CHECK (lat BETWEEN -90 AND 90),

    CONSTRAINT chk_longitude
        CHECK (lon BETWEEN -180 AND 180),

    CONSTRAINT uq_location
        UNIQUE (lat, lon, country)
);


CREATE TABLE weather.current_weather (
    current_weather_id  BIGSERIAL PRIMARY KEY,

    city_id             INTEGER NOT NULL
        REFERENCES weather.locations (city_id),

    dt                  BIGINT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    weather_id          INTEGER,
    main                VARCHAR(50),
    description         VARCHAR(200),
    icon                VARCHAR(10),

    temp                DOUBLE PRECISION,
    feels_like          DOUBLE PRECISION,
    temp_min            DOUBLE PRECISION,
    temp_max            DOUBLE PRECISION,
    pressure            INTEGER,
    humidity            SMALLINT,
    sea_level           INTEGER,
    grnd_level          INTEGER,

    visibility          INTEGER,
    speed               DOUBLE PRECISION,
    deg                 SMALLINT,
    gust                DOUBLE PRECISION,
    clouds_all          SMALLINT,

    sunrise             BIGINT,
    sunset              BIGINT,
    timezone            INTEGER,

    CONSTRAINT chk_current_humidity
        CHECK (humidity BETWEEN 0 AND 100),

    CONSTRAINT chk_current_cloudiness
        CHECK (clouds_all BETWEEN 0 AND 100),

    CONSTRAINT chk_current_wind_direction
        CHECK (deg IS NULL OR deg BETWEEN 0 AND 360),

    CONSTRAINT uq_current_weather
        UNIQUE (city_id, dt)
);

CREATE TABLE weather.weather_forecasts (
    weather_forecast_id BIGSERIAL PRIMARY KEY,

    city_id             INTEGER NOT NULL
        REFERENCES weather.locations (city_id),

    dt                  BIGINT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    temp                DOUBLE PRECISION,
    feels_like          DOUBLE PRECISION,
    temp_min            DOUBLE PRECISION,
    temp_max            DOUBLE PRECISION,
    pressure            INTEGER,
    sea_level           INTEGER,
    grnd_level          INTEGER,
    humidity            SMALLINT,

    weather_id          INTEGER,
    main                VARCHAR(50),
    description         VARCHAR(200),
    icon                VARCHAR(10),

    clouds_all          SMALLINT,
    speed               DOUBLE PRECISION,
    deg                 SMALLINT,
    gust                DOUBLE PRECISION,
    visibility          INTEGER,
    pop                 DOUBLE PRECISION,
    pod                 CHAR(1),

    CONSTRAINT chk_forecast_humidity
        CHECK (humidity BETWEEN 0 AND 100),

    CONSTRAINT chk_forecast_cloudiness
        CHECK (clouds_all BETWEEN 0 AND 100),

    CONSTRAINT chk_forecast_pop
        CHECK (pop IS NULL OR pop BETWEEN 0 AND 1),

    CONSTRAINT chk_forecast_wind_direction
        CHECK (deg IS NULL OR deg BETWEEN 0 AND 360),

    CONSTRAINT chk_part_of_day
        CHECK (pod IS NULL OR pod IN ('d', 'n'))
);

CREATE TABLE weather.air_pollution (
    air_pollution_id BIGSERIAL PRIMARY KEY,

    city_id          INTEGER NOT NULL
        REFERENCES weather.locations (city_id),

    dt               BIGINT NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    aqi              SMALLINT NOT NULL,
    co               DOUBLE PRECISION,
    "no"             DOUBLE PRECISION,
    no2              DOUBLE PRECISION,
    o3               DOUBLE PRECISION,
    so2              DOUBLE PRECISION,
    pm2_5            DOUBLE PRECISION,
    pm10             DOUBLE PRECISION,
    nh3              DOUBLE PRECISION,

    CONSTRAINT chk_aqi
        CHECK (aqi BETWEEN 1 AND 5),

    CONSTRAINT uq_air_pollution
        UNIQUE (city_id, dt)
);
