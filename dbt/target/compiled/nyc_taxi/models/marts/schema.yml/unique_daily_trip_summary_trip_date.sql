
    
    

select
    trip_date as unique_field,
    count(*) as n_records

from "taxi"."analytics_analytics"."daily_trip_summary"
where trip_date is not null
group by trip_date
having count(*) > 1


