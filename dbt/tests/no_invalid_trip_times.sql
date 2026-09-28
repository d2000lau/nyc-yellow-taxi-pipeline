select *
from {{ ref('stg_yellow_taxi_trips') }}
where dropoff_datetime <= pickup_datetime