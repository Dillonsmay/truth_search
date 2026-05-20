# TRUTH\_SEARCH

A privacy-respecting, AI-augmented metasearch engine that delivers verified information through a local Retrieval-Augmented Generation (RAG) pipeline.

## Overview

TRUTH\_SEARCH is a sophisticated search platform designed to provide users with accurate, locally-processed information while maintaining strict privacy standards. Built upon a robust architecture that integrates SearXNG for powerful metasearching capabilities and local LLM integration via LM Studio, this system strips out SEO spam and synthesizes data using Retrieval-Augmented Generation (RAG) techniques.

The platform operates entirely within a Dockerized environment, ensuring reproducibility and ease of deployment. All processing occurs locally on the user's machine, eliminating concerns about data privacy or third-party analytics.

## Key Features

* **Privacy-Focused**: No external data transmission; all processing happens locally
* **AI-Augmented Search**: Leverages local LLMs for intelligent information synthesis
* **Metasearch Integration**: Utilizes SearXNG to aggregate results from multiple sources
* **RAG Pipeline**: Implements Retrieval-Augmented Generation for enhanced accuracy
* **Spam-Free Results**: Actively filters out SEO spam and irrelevant content

## Tech Stack

* **Backend**: Python, FastAPI
* **Containerization**: Docker, docker-compose
* **Search Engine**: SearXNG (metasearch)
* **Frontend**: Vanilla JavaScript
* **Local LLM Integration**: LM Studio
* **Deployment**: Dockerized microservices architecture

## Architecture

```mermaid

graph LR

A\[User UI] --> B\[FastAPI]

B --> C\[SearXNG]

C --> B

B --> D\[Local LLM (LM Studio)]

D --> B

B --> A

