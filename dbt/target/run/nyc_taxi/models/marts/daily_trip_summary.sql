
  
    

  create  table "taxi"."analytics_analytics"."daily_trip_summary__dbt_tmp"
  
  
    as
  
  (
    select
    date(pickup_datetime) as trip_date,
    count(*) as trip_count,
    sum(total_amount) as total_revenue,
    avg(trip_distance) as avg_trip_distance,
    avg(trip_duration_minutes) as avg_trip_duration_minutes

from "taxi"."analytics_staging"."stg_yellow_taxi_trips"

group by date(pickup_datetime)
order by trip_date
  );
  