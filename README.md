# PropReturns-Task
PropReturns-Task is a project that involves scraping real estate data from a website, cleaning and processing the data, storing it on a PostgreSQL database hosted locally and creating a Flask application to generate endpoints for accessing the information. This README provides an overview of the project's components and how to use them.
## Project Components
1. **scraper.py** : This script is responsible for scraping data from the desired website. It collects real estate data and stores it in a CSV file.
2. **mumbai_realestate.csv** : This file contains the raw data scraped from the website using scraper.py.
3. **data_cleaning.ipynb** : Jupyter Notebook for data cleaning and preprocessing. It takes the raw data from mumbai_realestate.csv, performs cleaning operations, and stores the cleaned data in a new file.
4. **mumbai_realestate_cleaned.csv** : This file contains the cleaned and processed real estate data obtained after running the data_cleaning.ipynb notebook.
5. **realestate_data_postgreSQL** : This component writes the cleaned data from mumbai_realestate_cleaned.csv into a PostgreSQL database. The script defines the schema for the database and hosts it locally.
6. **app.py** : A Flask application that generates desired endpoints for accessing real estate data. It provides an interface to query and retrieve information from the PostgreSQL database.
   
