# startupradar.co Data Challenge

We're the tech analyst of a new Green Tech fund.
It is the first day on the job and our Managing Director wants us to get straight to work.
To become more efficient, our task is to build an AI that will replace all the other associates.
"From now on, we'll just do data-driven sourcing" is the firm's proclaimed future strategy.

To do this, they hand you a list of startups they have recently looked at along with a rating from the Managing Director and further information about the startup.

"Show me what you got" are the lasts words after handing over the data and this repository, 
so you get straight to work.

## The Data
For this challenge, we will be working with a subset of data from [startupradar.co](https://startuprdadar.co).
It can be found inside the `.data/` directory.
In the directory, there's a single dataframe containing the dataset called `full.parquet`.
It contains the following information:
- the startups' domain as index 
- rating of the startup by our Managing Directory on a scale from 1 (irrelevant) to 5 (highly relevant)
- the domains whois/DNS data with the columns `created`, `changed`, `expires` and the days since the domains was created and changed (`days_since_created` and `days_since_changed`)
- the raw text of the website inside `text`
- a textual embedding of the startups website with columns prefixed with `e{0-1535}` that should provide a semantic understanding of the website

## Setup
This repo contains a dockerized python environment.
It also contains pinned and unpinned dependencies.
Use the pinned ones if possible.

Set up and run via Docker:
```shell
touch .env
docker compose build
docker compose up -d
docker compose exec app python cli.py
```

Set up and run via python's venv:
```shell
touch .env
python -m venv venv
source venv/bin/activate
python cli.py
```

## Task 1: Data Analysis
First off, let's try to impress the MD by providing an analysis of the data.

- Task 1.1: install the dependencies and load the parquet file, feel free to use the provided docker setup or a virtual environment
- Task 1.2: find out which of the columns has missing values and how many. Print this information on the console.
- Task 1.3: analyze the texts and try to quickly generate a list of words that are more frequent in highly-rated startups

## Task 2: Prediction
Now that we've made a good first impression, let's see if we can automate our deal sourcing.
For this, we want to find a way to predict the ratings our MD has provided us based on the data we got.

- Task 2.1: implement a way to predict the ratings, i.e. the score between 1 and 5
- Task 2.2 create a dataframe with your predictions alongside the actual values and store it inside `predictions.parquet`
- Task 2.3: measure the quality of your prediction with the mean squared error and print it on the command line

Finally:
- commit your code in the repo, comment where necessary
- make sure it's runnable and all dependencies are updated
- if you're not able to solve something, commit the code you tried and comment what you wanted to do

Hints:
- sklearn and pandas provide a lot of functionality to quickly get something going. Feel free to use it and avoid to implement major functionality yourself.
- no external data or dependencies are required or expected
- there are more columns than rows, so you will need a way to prevent over-fitting. Some of the options are usage of specific models, feature reduction/selection, but manual selection is fine, too
- maybe starting with a baseline prediction and improving step by step could avoid going too deeply
- the code needs to be reviewable but not production-ready
- the model should train within minutes, not hours, sacrificing quality is fine