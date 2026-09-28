
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select trip_date
from "taxi"."analytics_analytics"."daily_trip_summary"
where trip_date is null



  
  
      
    ) dbt_internal_test