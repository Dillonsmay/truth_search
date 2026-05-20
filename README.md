# TRUTH\_SEARCH

A privacy-respecting, AI-augmented metasearch engine that delivers verified information through a local Retrieval-Augmented Generation (RAG) pipeline.

## Overview

TRUTH_SEARCH functions as a locally-hosted, Perplexity-style Answer Engine. Built on a robust architecture that integrates SearXNG for metasearch capabilities and a local LLM via LM Studio, the platform prioritizes direct AI synthesis. The UI prominently displays a Markdown-formatted AI response at the top to provide a clear, structured answer, while raw search results are cleanly relegated to a 'SOURCES' section at the bottom.

## Key Features

* **Privacy-Focused**: No external data transmission; all processing happens locally
* **AI-Augmented Search**: Leverages local LLMs for intelligent information synthesis
* **Metasearch Integration**: Utilizes SearXNG to aggregate results from multiple sources
* **RAG Pipeline**: Implements Retrieval-Augmented Generation for enhanced accuracy
* **Spam-Free Results**: Actively filters out SEO spam and irrelevant content

## Privacy & The Filter Bubble

Unlike traditional search engines that track user history to deliver algorithmically personalized (and often ideologically skewed) results, TRUTH_SEARCH acts as an anonymous proxy. By utilizing SearXNG to strip away identifying metadata, cookies, and search history, the platform bypasses the 'Filter Bubble.' This ensures users receive a baseline, unmanipulated index of the web, protecting both their data privacy and the objectivity of their search results.

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
A[User UI] --> B[FastAPI]
B --> C[SearXNG]
C --> B
B --> D[Local LLM - LM Studio]
D --> B
B --> A

