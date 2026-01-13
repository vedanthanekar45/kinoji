# Kinoji (I got this name from GPT, means something related to cinema.. idk)

### Project Overview

Kinoji is a data engineering and analytics engine designed to aggregate, process, and visualize the history of modern cinema. The project was conceived to move beyond simple movie tracking and instead uncover deeper relationships between films, studios, actors, and audience reception.

While existing platforms like IMDb or TMDB provide raw data, they lack the tools to derive complex insights—such as genre saturation over decades, the correlation between studio output and critical success, or the "stickiness" of specific directors. Kinoji fills this gap by harvesting high-quality data and structuring it for heavy analytical querying.

### Data Collection Strategy

The core value of this project lies in its dataset. The Movie Database (TMDB) contains over 2 million records, but the majority are noise, test data, adult content, or obscure clips with zero cultural relevance.

To build a high-signal dataset, I implemented a targeted harvesting pipeline:

* **Chronological Iteration:** The scraper processes history year by year, from 1920 to 2025.
* **Relevance Filtering:** Instead of a raw dump, the system extracts only the top 1,000 movies per year based on popularity metrics, ensuring coverage of every culturally significant film (blockbusters, award winners, and cult classics) while filtering out the long tail of garbage data.
* **Validation:** A secondary constraint of `vote_count > 10` is applied to ensure every record represents a film that has actually been watched and reviewed.

The result is a clean, normalized library of approximately **60,225 movies** that accurately represents the history of commercial cinema.

### System Architecture

The application is built on a high-performance backend designed to handle complex relational queries that would choke standard document stores.

* **Runtime:** Python 3.12
* **Database:** PostgreSQL 17 (Self-hosted on Docker)
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Infrastructure:** DigitalOcean Droplet

### Database Design

The schema follows strict Third Normal Form (3NF) to prioritize data integrity and query flexibility. Unlike simple JSON dumps, Kinoji splits entities into dedicated tables (`Movies`, `Actors`, `Directors`, `Studios`, `Genres`) connected by association tables.

This normalized structure allows for complex analytical queries, such as:

* *"Which production studios have the highest average rating for Horror movies since 2010?"*
* *"How has the average runtime of Action movies changed compared to Dramas over the last 50 years?"*

### Search Implementation

The search engine addresses the common discrepancy between user input and database records (e.g., users typing "Spiderman" while the database stores "Spider-Man").

Instead of relying on heavy full-text search engines like Elasticsearch, the backend implements a Regex-based normalization layer directly within the SQL query. This strips special characters and punctuation on the fly, allowing for accurate retrieval regardless of input formatting errors.

### Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/kinoji.git
cd kinoji

```

**2. Infrastructure Setup**
Ensure Docker is installed and running.

```bash
docker-compose up -d

```

**3. Configuration**
Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgresql://user:password@localhost:5432/kinoji
TMDB_API_KEY=your_api_key

```

**4. Database Migration**
Apply the schema to your local database instance:

```bash
alembic upgrade head

```

**5. Start the Application**

```bash
uvicorn main:app --reload

```
