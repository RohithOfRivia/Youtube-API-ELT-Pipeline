{{ config(materialized='view') }}

WITH view_ranks AS  (
    SELECT 
        channel_name, views, channel_start_date, subs, video_count, rank() 
            OVER 
                (ORDER BY views DESC) as rank  
            FROM 
                channels
)

SELECT * FROM view_ranks