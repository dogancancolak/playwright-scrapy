# Quotes Scrapy Project

This project uses [Scrapy](https://scrapy.org/) to collect quotes from `http://quotes.toscrape.com`.  
Different spiders demonstrate different output methods or different work flows:

- **quotes_json** → saves data as a JSON array (`quotes_array.json`)
- **quotes_ndjson** → saves data as line-delimited NDJSON (`quotes_lines.jsonl`)
- **quotes_db** → stores data in a PostgreSQL database
- **quotes_rabbit** → publishes data via RabbitMQ messaging queue
- **quotes_redis** → stores data in redis 
- **quotes_redis_queue** → reads data from redis queue and saves it as line-delimited NDJSON (`quotes_lines.jsonl`)
- **quotes_playwright** → scrapes data from a js first page 
- **quotes_playwright_redis** → scrapes data from a js first page by reading the url from redis queue 

---

## 🧰 Tech Stack

- **Scrapy**  
- **Playwright** (for browser automation / rendering)  
- **PostgreSQL**  
- **Redis**  
- **Docker / Docker Compose**

---

## ⚙️ Key Implementation Details & Highlights

- **Playwright integration:** Uses `scrapy-playwright` or equivalent download handler to let Scrapy handle JavaScript-rendered pages without breaking its pipeline logic.  
- **`playwright_include_page` / `playwright_page_methods`:** Allows spiders to access the actual browser `Page` object, apply waits, scrolls, clicks, etc.  
- **Pagination / Link following:** Spiders detect “next page” links and queue further requests (with `meta={'playwright': True}`) to continue crawling.  
- **Infinite scroll / Load More handling:** Some spiders scroll down programmatically or click “Load More” buttons until new content stops loading.  
- **Database persistence:** Pipeline writes crawled items into PostgreSQL, possibly with deduplication or upsert logic.  
- **Dockerization & orchestration:** All components (crawler, DB, cache) are containerized for easy deployment and reproducibility.

---

---

## 🚀 Setup & Running

### Clone the repository

```bash
git clone https://github.com/dogancancolak/playwright-scrapy.git
cd playwright-scrapy
```

### Option 1: Using Docker

```bash
docker-compose up --build
```

This will spin up containers (PostgreSQL, Redis, and the Scrapy crawler) as configured.

### Option 2: Local / Manual

```bash
pip install -r requirements.txt
playwright install
scrapy crawl quotes_playwright
```

Make sure to configure your `.env` or settings (database URL, Redis URL, etc) before running.

---

### Environment Variables
Create a `.env` file in the project root with your database credentials:

```
DB_HOST=localhost
DB_NAME=scrapydb
DB_USER=postgres
DB_PASS=postgres
```

⚠️ Make sure `.env` is added to `.gitignore` so it’s not committed to your repository.

### Run Spiders
- JSON array output:
```bash
scrapy crawl quotes_json
```

- NDJSON output:
```bash
scrapy crawl quotes_ndjson
```

- Save to PostgreSQL:
```bash
scrapy crawl quotes_db
```

---

## ⚙️ Settings
- Pipelines are defined in `quotes_project/pipelines.py`.
- Database credentials are loaded from `.env` using [python-dotenv](https://pypi.org/project/python-dotenv/).

---

## 📦 Requirements
Main dependencies are listed in `requirements.txt`:

Install them with:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
playwright-scrapy/ #Repository
│   scrapy.cfg
│   README.md
│   .gitignore
│   requirements.txt
│   .env.example
│
└───quotes_project/
    │   items.py
    │   pipelines.py
    │   settings.py
    │
    └───spiders/
        │   quotes_json.py
        │   quotes_ndjson.py
        │   quotes_db.py
        |   ...
```

---

## 📝 Example Outputs

### JSON Array (`quotes_array.json`)
```json
[
  {
    "text": "The world as we have created it is a process of our thinking.",
    "author": "Albert Einstein",
    "tags": ["change", "thinking", "world"]
  },
  {
    "text": "It is our choices, Harry, that show what we truly are.",
    "author": "J.K. Rowling",
    "tags": ["abilities", "choices"]
  }
]
```

### NDJSON (`quotes_lines.jsonl`)
```
{"text": "The world as we have created it is a process of our thinking.", "author": "Albert Einstein", "tags": ["change", "thinking", "world"]}
{"text": "It is our choices, Harry, that show what we truly are.", "author": "J.K. Rowling", "tags": ["abilities", "choices"]}
```

### PostgreSQL Table (`quotes`)
| id | text                                                   | author          | tags                          |
|----|--------------------------------------------------------|-----------------|-------------------------------|
| 1  | The world as we have created it is a process...        | Albert Einstein | {change,thinking,world}       |
| 2  | It is our choices, Harry, that show what we truly are. | J.K. Rowling    | {abilities,choices}           |

---

## 📝 Notes
- Use **JSON Array** output for small datasets.  
- Use **NDJSON** (newline-delimited JSON) for large crawls or when working with big data tools.  
- Use the **PostgreSQL pipeline** when you need structured storage and querying.  
