
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "taxi"."analytics_staging"."stg_yellow_taxi_trips"
where dropoff_datetime <= pickup_datetime
  
  
      
    ) dbt_internal_test