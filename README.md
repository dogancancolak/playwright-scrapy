# Quotes Scrapy Project

This project uses [Scrapy](https://scrapy.org/) to collect quotes from `http://quotes.toscrape.com`.  
Different spiders demonstrate different output methods:

- **quotes_json** → saves data as a JSON array (`quotes_array.json`)
- **quotes_ndjson** → saves data as line-delimited NDJSON (`quotes_lines.jsonl`)
- **quotes_db** → stores data in a PostgreSQL database

---

## 🚀 Usage

### Installation
Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd quotes_project
pip install -r requirements.txt
```

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

- `scrapy`
- `itemloaders`
- `psycopg2-binary`
- `python-dotenv`

Install them with:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
quotes_project/
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
