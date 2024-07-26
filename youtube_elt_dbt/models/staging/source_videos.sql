

{{ config(materialized='view') }}

WITH source_videos AS (

    SELECT * FROM videos

)

SELECT *
FROM source_videos

