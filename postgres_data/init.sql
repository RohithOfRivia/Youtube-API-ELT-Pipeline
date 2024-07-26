CREATE TABLE IF NOT EXISTS videos(
    id SERIAL PRIMARY KEY,
    req_date DATE,
    daily_rank SMALLINT,
    title VARCHAR(200),
    video_id VARCHAR(100),
    publish_date TIMESTAMP,
    channel_id VARCHAR (100),
    descr TEXT,
    thumbnail_link VARCHAR (100),
    dimension VARCHAR (5),
    views VARCHAR (50),
    likes INTEGER,
    comments INTEGER,
    favourite_count INTEGER,
    category SMALLINT,
    PRIMARY KEY (req_date, video_id)
);

insert into videos (req_date, daily_rank, title, video_id, publish_date, channel_id, descr, thumbnail_link, dimension, views, likes, comments, favourite_count, category) values
-- ('2024-07-21T06:41:10', 3, 'test', 'sjnnfjns', '2024-07-11T06:55:16', 'UCWJ2lWNubArHWmf3FIHbfcQ', 'test_descr', 'thumbnail', '2d', 50000, 50000, 5000, 0, 5);

CREATE TABLE channels(
    channel_id VARCHAR(100) PRIMARY KEY,
    channel_name VARCHAR (100),
    channel_username VARCHAR(70),
    descr TEXT,
    channel_start_date DATE,
    subs INTEGER,
    views BIGINT,
    video_count INTEGER,
    kids_channel BOOLEAN,
    profile_picture_url VARCHAR(200)
);

CREATE TABLE stop_words (
    word VARCHAR(30)
);

COPY stop_words(word)
FROM '/stopwords.txt'
WITH (FORMAT text);

