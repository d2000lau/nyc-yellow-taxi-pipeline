
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "taxi"."analytics_staging"."stg_yellow_taxi_trips"
where trip_distance <= 0
  
  
      
    ) dbt_internal_test