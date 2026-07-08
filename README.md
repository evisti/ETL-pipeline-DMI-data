# ETL pipeline for weather data

This project creates an ETL pipeline to build a database that can be used to analyze weather data. The data is retrived from the Danish Meteorological Institute’s (DMI) Open Data API.

The project uses Python to assemble data into a Pandas dataframe and store into a PostgreSQL database.

The DMI observation data are time-resolved raw data collected at DMI's observation stations in Denmark and Greenland. It contains a number of parameters including temperature, humidity, wind, precipitation, radiation etc.

The API documentation can be found here: https://www.dmi.dk/friedata/dokumentation-paa-engelsk


Focus on:
- Object oriented design
- Code quality & best practices
