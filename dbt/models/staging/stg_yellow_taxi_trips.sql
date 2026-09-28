with source as (

    select *
    from raw.yellow_taxi_trips

),

cleaned as (

    select
        vendor_id,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
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
        congestion_surcharge,

        extract(
            epoch from (dropoff_datetime - pickup_datetime)
        ) / 60.0 as trip_duration_minutes

    from source

    where pickup_datetime is not null
      and dropoff_datetime is not null
      and trip_distance > 0
      and total_amount > 0
      and dropoff_datetime > pickup_datetime
      and extract(
            epoch from (dropoff_datetime - pickup_datetime)
          ) / 60.0 < 1440

)

select *
from cleaned