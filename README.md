# ArtBloom: A Hands-On Guide to Creating an Intelligent Art Discovery Backend

## Table of Contents
1. [Project Description](#project-description)
2. [Why Python for Backend Development?](#why-python-for-backend-development)
3. [Learning Objectives](#learning-objectives)
4. [Key Features](#key-features)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Setup and Installation](#setup-and-installation)
8. [Usage](#usage)
9. [Testing and Linting](#testing-and-linting)
10. [Recommendation System](#recommendation-system)
11. [Deployment](#deployment)
12. [Additional Resources](#additional-resources)
13. [Contributing](#contributing)
14. [License](#license)

---

## Project Description

ArtBloom is a backend application designed for art enthusiasts and researchers. It provides robust APIs for browsing, discovering, and analyzing artwork collections. The application integrates seamlessly with the Art Institute of Chicago's open API and offers high-performance endpoints for metadata retrieval and data analysis.

---

## Why Python for Backend Development?

Python is one of the most popular programming languages for backend development due to its simplicity, readability, and vast ecosystem of libraries and frameworks. Here’s why Python is an excellent choice for backend applications:

- **Ease of Use**: Python's clean syntax and readability make it easy to learn and write.
- **Rich Ecosystem**: Frameworks like Sanic, Flask, and Django simplify the development process.
- **Performance**: With asynchronous libraries like Sanic and aiohttp, Python can handle high-concurrency applications efficiently.
- **Integration**: Python offers seamless integration with databases, APIs, and other services.
- **Community Support**: A large, active community ensures quick access to tutorials, documentation, and support.

By using Python, you can focus on solving business problems rather than dealing with the complexities of low-level programming.

---

## Learning Objectives

By following this guide, you will:

- Understand the fundamentals of backend development with Python.
- Learn how to set up and configure a Sanic server.
- Use Tortoise ORM to interact with a PostgreSQL database.
- Write and expose RESTful API endpoints.
- Apply asynchronous programming to handle high-concurrency scenarios.
- Debug, test, and optimize a Python backend application.
- Explore data analysis techniques using Pandas for backend recommendations.

---

## Key Features

### API Endpoints

The application exposes the following endpoints using Sanic:

- **Fallback Endpoint**: Handles non-existent paths and returns a 404 error.
  ```
  GET /
  Response: { "message": "This path does not exist." }
  ```

- **Retrieve All Artworks**: Fetch a list of artworks based on query parameters.
  ```
  GET /artworks
  Query Parameters: filters such as medium, artist, year, etc.
  Response: JSON containing artwork data.
  ```

- **Retrieve Artwork by ID**: Get detailed information about a specific artwork.
  ```
  GET /artworks/<artwork_id>
  Response: JSON containing the artwork's metadata or a 404 error if not found.
  ```

- **Search Artworks**: Search artworks based on specific criteria.
  ```
  GET /artworks/search
  Query Parameters: search keywords.
  Response: JSON containing matching artworks.
  ```

- **Recommendation Route**: Generate artwork recommendations using Pandas to analyze metadata.
  ```
  GET /artworks/recommendations
  Response: JSON containing recommended artworks.
  ```

These endpoints are implemented in the `artworks_router` module and rely on helper functions for data retrieval and processing.

---

## Technology Stack

- **Backend Framework**: Sanic for asynchronous web APIs.
- **Database**: PostgreSQL with Tortoise ORM.
- **Migration Tool**: Aerich for database schema management.
- **API Integration**: HTTPx for fast and reliable integration.
- **Environment Management**: Python-dotenv for configuration.
- **Testing**: PyUnit for unit and integration testing.
- **Linting and Formatting**: Pylint and isort for code quality.
- **Data Analysis**: Pandas for advanced data manipulation.

---

## Project Structure

```
art-bloom/
├── artworks_core/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── artworks_data_helper.py
│   │   ├── artworks_data_reader.py
│   │   ├── artworks_data_writer.py
│   │   └── artworks_router.py
│   ├── artworks_settings/
│   │   ├── __init__.py
│   │   ├── generate_tortoise_config.py
│   │   ├── setup_env_configuration.py
│   │   └── tortoise_config_wrapper.py
│   ├── artworks_utils/
│   │   ├── __init__.py
│   │   ├── app_logger.py
│   │   ├── database_manager.py
│   │   ├── http_request_manager.py
│   │   └── logging.conf
│   └── migrations/
├── tests/
│   ├── __init__.py
│   └── test_format_artworks.py
├── .env
├── .gitignore
├── .pylintrc
├── app.log
├── LICENSE
├── Makefile
├── Pipfile
├── Pipfile.lock
├── pyproject.toml
├── README.md
└── server.py
```

---

## Setup and Installation

### Prerequisites
- Python 3.12+
- PostgreSQL
- Pipenv

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/artbloom.git
   cd art-bloom
   ```

2. **Install Dependencies**:
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   APP_NAME=ArtBloom
   DATABASE_URL=postgres://<username>:<password>@localhost:5432/artbloom
   ARTWORKS_API=https://api.artic.edu/api/v1/artworks
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

4. **Initialize the Database**:
   ```bash
   aerich init -t artworks_settings.tortoise_config_wrapper.TORTOISE_ORM
   aerich init-db
   ```

5. **Run the Application**:
   ```bash
   make run
   ```

---

## Usage

- Access the API at `http://localhost:4000`.
- Use the provided endpoints to interact with artwork data.
- Log outputs are stored in `app.log` for debugging and monitoring.

---

## Testing and Linting

1. **Run Tests**:
   ```bash
   make test
   ```

2. **Lint the Code**:
   ```bash
   make lint
   ```

---

## Recommendation System

### Overview

The recommendation system in ArtBloom dynamically generates artwork suggestions based on user preferences and inferred interests. It combines metadata filtering, temporal diversity, and ranking to provide meaningful recommendations.

### How It Works

1. **User Preferences**:
   - The system starts with explicitly provided preferences, such as:
     - `style_title`: Artistic style (e.g., "Post-Impressionism").
     - `medium_display`: Medium used (e.g., "Oil on canvas").
     - `category_titles`: Categories (e.g., "Painting and Sculpture of Europe").

2. **Filter Artworks**:
   - Artworks are filtered based on the user’s preferences, and a scoring mechanism is applied to prioritize matches.
     ```python
     filtered_artworks["score"] = (
         (filtered_artworks["style_title"] == user_preferences["style_title"]).astype(int) * 3 +
         (filtered_artworks["medium_display"] == user_preferences["medium_display"]).astype(int) * 2 +
         (filtered_artworks["category_titles"].apply(lambda x: any(cat in x for cat in user_preferences["category_titles"]))).astype(int)
     )
     ```

3. **Temporal Inference**:
   - Infer the user’s preferred time period by averaging the creation dates (`avg_date`) of filtered artworks.
     ```python
     user_date_preference = filtered_artworks["avg_date"].mean()
     ```

4. **Rank Artworks by Score and Temporal Similarity**:
   - Rank artworks based on their score and proximity to the inferred time period.
     ```python
     filtered_artworks["date_similarity"] = np.abs(filtered_artworks["avg_date"] - user_date_preference)
     filtered_artworks = filtered_artworks.sort_values(by=["score", "date_similarity"], ascending=[False, True]).head(5)
     ```

5. **Select Top Recommendations**:
   - The top artworks are selected and formatted for the response.

### Example Workflow

#### **Artworks Data**
| ID  | Title                       | Style Title         | Medium Display   | Date Start | Date End | Avg Date | Score |
|-----|-----------------------------|---------------------|------------------|------------|----------|----------|-------|
| 1   | Starry Night                | Post-Impressionism  | Oil on canvas    | 1889       | 1889     | 1889.0   | 6     |
| 2   | Wheatfield with Crows       | Post-Impressionism  | Oil on canvas    | 1890       | 1890     | 1890.0   | 6     |
| 3   | Water Lilies                | Impressionism       | Oil on canvas    | 1875       | 1876     | 1875.5   | 3     |
| 4   | Red Eiffel Tower            | Modernism           | Oil on canvas    | 1911       | 1911     | 1911.0   | 2     |

#### **User Preferences**
```json
{
  "style_title": "Post-Impressionism",
  "medium_display": "Oil on canvas",
  "category_titles": ["Painting and Sculpture of Europe"]
}
```

#### **Steps and Results**
1. **Filter Artworks**: Match artworks based on style, medium, and category preferences, and calculate scores.
2. **Infer Temporal Preference**: Calculate the user’s preferred date range.
   ```
   user_date_preference = mean([1889.0, 1890.0]) = 1889.5
   ```
3. **Rank by Temporal Similarity**: Compute temporal similarity and rank by score and similarity.
   | ID  | Avg Date | Score | Date Similarity |
   |-----|----------|-------|-----------------|
   | 1   | 1889.0   | 6     | 0.5             |
   | 2   | 1890.0   | 6     | 0.5             |
   | 3   | 1875.5   | 3     | 14.0            |
   | 4   | 1911.0   | 2     | 21.5            |
4. **Select Top Recommendations**: Return the top-ranked artworks.

### Key Features

- **Prioritized Matching**: Ensures that artworks with the highest alignment to preferences are ranked first.
- **Temporal Diversity**: Balances relevance and diversity by including artworks near the inferred time period.
- **Scalable Logic**: Easily extendable to incorporate additional metadata or preferences.

---

## Deployment

### Local Deployment
- Run the server using the Makefile target `make run`.
- Ensure PostgreSQL is running locally with the configured database.

### Free Hosting Platforms
- **Render**: Free tier for hosting backend apps.
- **Railway**: Offers $5/month free credits.
- **Fly.io**: Docker-based deployment with global regions.

---

## Additional Resources

- [Sanic Documentation](https://sanic.dev/en/)
- [Tortoise ORM Documentation](https://tortoise-orm.readthedocs.io/en/latest/)
- [PostgreSQL Official Site](https://www.postgresql.org/)
- [Python-dotenv Documentation](https://saurabh-kumar.com/python-dotenv/)
- [Pandas Documentation](https://pandas.pydata.org/)
