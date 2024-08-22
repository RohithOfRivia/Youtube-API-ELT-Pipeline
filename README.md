# Youtube-API-ELT-Pipeline

Welcome to the **Youtube-API-ELT-Pipeline** repository. This project integrates Airflow, Python and PostgreSQL with DBT (Data Build Tool) to manage data pipelines for processing and analyzing YouTube data that is obtained through the [YouTube Data API v3](https://developers.google.com/youtube/v3). Created to run with Docker Desktop for easy execution and setup in a containerized environment.  
## Table of Contents
- [Features](#features)
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Acknowledgments](#acknowledgments)

## Features
- **Airflow Integration**: Seamlessly orchestrates and automates ETL processes(pulling, updating and transforming data) using Python.
- **DBT Models**: Transform raw YouTube data from the database into meaningful insights.

## Overview
###  Airflow Dag:
- Performs a get request using the YouTube API to fetch the top 200 trending videos and some relevant information(title, views, channel name, etc.) in YouTube (Location is set to Canada).
- Parses the API response and uploads the data into the videos table in a PostgreSQL database. Any items conflicting with the database constraints are ignored.
- Performs another get request to fetch details of all channels associated with the videos that were inserted prior to the request. The response is parsed and uploaded to another table called channels.
- Runs DBT to create/update additional models for data analysis
### DBT:
Creates some views that provide meaningful insights from the videos and channels data. This includes:
1. word_counts_title_distinct: Overall count of words that appear in the channel titles, ranked according to number of occurrences. Stopwords are not counted.

2. trending_video_counts_per_channel: Calculates the total number of videos that appear in the top 200 by ever channel. This shows how effective a channel is at producing trending videos.

3. channel_rankings: Calculates the number of videos by each channel appearing in the videos table. Unlike trending_video_counts_per_channel, this adds up all multiple occurrences of a video on a different day. That is, if a video appears in the top 200 on one day, and it shows up again on another day, that counts towards the total video count. This shows how consistent a channel is at publishing trending videos, and also how long it tends to stay in the trending list. 

5. view_ranks: All channels ranked by views, also includes statistics like subscribers, total video count, etc.

### Project Workflow Diagram
<br> ![Dagster project diagram drawio](https://github.com/user-attachments/assets/47545153-c00c-4e6c-b6b0-78ecfd0d19da)
  <br>


###  ER Diagram
<br>

![SQL ER](https://github.com/user-attachments/assets/2045d578-b872-498e-aa81-f6e2e3a82855)

<br>

### DBT models

**word_counts_title_distinct**
<br>
<br>
![Screenshot 2024-08-21 115459](https://github.com/user-attachments/assets/cc6614c6-27f7-4188-8f6e-f6bd178f2fa4)
<br>
<br>
**view_ranks**
<br>
<br>
<img width="450" alt="Screenshot 2024-08-22 115558" src="https://github.com/user-attachments/assets/a7a43778-4523-45d5-830e-76d9ad9f1584">
<br>
<br>

**trending _video_counts**
<br>
<br>
![Screenshot 2024-08-22 115459](https://github.com/user-attachments/assets/e376ee4e-b0f2-4c75-8ebc-d532cfcd1992)
<br>
<br>
**channel_rankings**
<br>
<br>
![Screenshot 2024-08-22 115401](https://github.com/user-attachments/assets/6fd3294d-b8b8-45da-b62d-9354c1664cdd)
<br>

<br>

## Getting Started
### Prerequisites
Ensure you have the following installed on your system:
- [Python 3.8+](https://www.python.org/downloads/)
- [Airflow](https://airflow.apache.org/)
- [DBT](https://docs.getdbt.com/docs/installation)
- [YouTube Data API](https://developers.google.com/youtube/v3) (for fetching YouTube data)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Configuration
- **.env file**: Modify the .env file to add your API key within the double quotes.
- **DBT Configuration**: Modify `dbt_project.yml` and `profiles.yml` according to your setup. Can run without any modifications.
- **Asset execution schedule**: The assets are programmed to run hourly, the schedule object in \_\_init\__.py can be modified to make changes to the schedule.
### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RohithOfRivia/Youtube-API-ELT-Pipeline.git
   cd Youtube-API-ELT-Pipeline
2. **Use docker compose to build and run the containers:**
	  ```bash
	   docker compose up --build
3. **Access webserver for monitoring the assets**::
	- Open your browser and go to this address: *localhost:8080*

	
4. **Access postgres container to monitor the database**: 
	Run these commands to access the database. *(The container name can be obtained from the docker desktop app. Go to the containers and select the postgres container that is not docker_postgresq. You will be able to see a heading on the top of this page, which is the container name.)*  
	```bash
   docker exec -it <container_name> bash
	psql elt_user -d airflow
## Acknowledgments
- [Python](https://www.python.org/)
- [Airflow](https://airflow.apache.org/)
- [DBT](https://getdbt.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
