{{ config(materialized='view') }}

WITH source_stop_words AS (

    SELECT * FROM stop_words

)

SELECT *
FROM source_stop_words