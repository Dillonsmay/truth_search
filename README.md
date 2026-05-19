# Search API with SearXNG Integration

This project provides a FastAPI application that integrates with SearXNG to provide search functionality.

## Features

- RESTful API endpoints for searching
- Integration with SearXNG for powerful search capabilities
- Dockerized setup for easy deployment

## Getting Started

### Prerequisites

- Docker and docker-compose installed

### Running the Application

1. Clone this repository
2. Run `docker-compose up` to start both FastAPI app and SearXNG
3. Access the API at `http://localhost:8000`

### Available Endpoints

- `GET /` - Welcome message
- `GET /search/{query}` - Search with full results
- `GET /search/simple/{query}` - Search with simplified results (title and URL only)

## API Usage Examples

