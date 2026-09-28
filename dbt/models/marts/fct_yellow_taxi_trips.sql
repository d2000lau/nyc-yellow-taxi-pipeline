select
    vendor_id,
    pickup_datetime,
    dropoff_datetime,

    date(pickup_datetime) as pickup_date,
    extract(hour from pickup_datetime) as pickup_hour,

    passenger_count,
    trip_distance,
    trip_duration_minutes,

    ratecode_id,
    store_and_fwd_flag,

    pickup_location_id,
    dropoff_location_id,

    payment_type,

    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge

from {{ ref('stg_yellow_taxi_trips') }}