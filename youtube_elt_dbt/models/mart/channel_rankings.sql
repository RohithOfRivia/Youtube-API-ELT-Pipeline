{{ config(materialized='view') }}

WITH channel_rankings AS  (
    SELECT 
        channels.channel_name, COUNT(channels.channel_name), rank() 
            OVER 
                (ORDER BY COUNT(*) DESC) as rank, channels.channel_id
            FROM 
                channels INNER JOIN videos ON channels.channel_id = videos.channel_id
            GROUP BY
                channels.channel_name, channels.channel_id
)

SELECT * FROM channel_rankings