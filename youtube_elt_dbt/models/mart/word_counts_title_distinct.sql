{{ config(materialized='view') }}


WITH words AS (
    SELECT
        DISTINCT ON (video_id)
            unnest(string_to_array(lower(title), ' ')) AS word
    FROM
        source_videos
),

word_counts AS ( 

    SELECT 
        word, COUNT(*) AS occurences
    FROM
        words
    GROUP BY
        word
),

word_counts_filtered AS (
    SELECT  
        wc.word, wc.occurences
    FROM
        word_counts wc
            LEFT JOIN source_stop_words ssw ON wc.word = ssw.word
    WHERE
        ssw.word IS NULL
    ORDER BY 
        occurences DESC
)

-- psql elt_user -d airflow
SELECT * FROM word_counts_filtered 