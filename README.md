# Trend Engine

## Summary

Trend Engine is a personal data-driven project focused on **collecting and organizing articles from online content feeds** in order to better understand what topics are being discussed across sources.

At its current stage, the project focuses on:

- Ingesting articles from predefined sources(RSS feeds)
- Storing and deduplicating articles in a structured database
- Assigning simple, source-derived topics to articles. Deeper analysis is planned for future iterations.

The broader goal is to **reduce doom-scrolling** by creating a clean, structured view of incoming content, while laying the groundwork for future trend detection, topic modeling, and summarization.

## Motivation

I built this tool to help myself stay informed without constantly scrolling through feeds. Instead of consuming everything in real time, the idea is to collect content in the background and surface
what’s relevant in a more deliberate, digestible way.

## Data Model

https://dbdiagram.io/d/FeedScope-68efcd9d2e68d21b41a3386f

## Installation

1. Clone the repository

```commandline
git clone https://github.com/Wahib13/trend-engine
cd trend-engine
```

2. Install dependencies

```commandline
pip install -r requirements.txt
```

3. Environment setup:
   Make a copy of the example environment files:

```commandline
cp .env.example .env
cp ui/.env.example ui/.env
```

4. Initialize the database:

```commandline
cd src/
python -m scripts.init_db
```

# Running Tests

```commandline
cd src/
python -m pytest
```

# Running Ingestion

```commandline
cd src/
python -m scripts.run_ingestion
```

# Running the Frontend
```commandline
cd ui/
npm install
npm run dev
```

# Running both UI and API with docker-compose 
```commandline
docker compose up
```