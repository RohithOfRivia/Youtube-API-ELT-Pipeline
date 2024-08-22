{{ config(materialized='view') }}


WITH unique_videos AS ( 
    SELECT 
        DISTINCT title  
    FROM 
        videos
        ), 

words AS (SELECT word, count(*) as occurences
    FROM ( 
        SELECT 
            lower(regexp_split_to_table(title, ' ')) as word
        FROM 
            unique_videos
    ) t
    GROUP BY word),

word_counts_filtered AS (
    SELECT
        wc.word, wc.occurences
    FROM
        words wc
            LEFT JOIN source_stop_words ssw ON wc.word = ssw.word
    WHERE
        ssw.word IS NULL
    ORDER BY
        occurences DESC
)

SELECT * FROM word_counts_filtered
