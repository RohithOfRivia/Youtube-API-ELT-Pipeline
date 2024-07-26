{{ config(materialized='view') }}

WITH channel_counts AS (
    SELECT
        COUNT(DISTINCT video_id) AS video_count, source_videos.channel_id, channels.channel_name
    FROM
        source_videos LEFT JOIN channels 
            ON source_videos.channel_id = channels.channel_id 
    GROUP BY source_videos.channel_id, channels.channel_name

),

ranked_channels AS (
    SELECT
        channel_name,
        video_count,
        RANK() OVER (ORDER BY video_count DESC) AS rank
    FROM
        channel_counts
)


SELECT * FROM ranked_channels