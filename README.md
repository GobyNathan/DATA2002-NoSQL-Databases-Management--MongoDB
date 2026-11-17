# DATA2002 — NoSQL Databases Management (MongoDB)
**Dublin City Council — Hazardous Waste Management & Illegal Dumping Enforcement System**

## Group 6 Members
- **Gobijan Nathakrishnan** (Team Lead) — Python CLI Application (`MongoDB.py`), Analytical Queries (#13–#15 in `DBScript.txt`), & Repository Coordination
- **Manech Lecerf** — Database Schema Design (`DBSchema.doc`), Database Setup & Data Population (Part 2 + Query #1 in `DBScript.txt`)
- **Enric Mendez Codina** — MongoDB Querying & Aggregations (Queries #2–#12 in `DBScript.txt`) & RBAC Security (`adminRole` / `Admin` user)

---

## Project Structure
- [`MongoDB/`](./MongoDB/) — Modular Python package for Part 4 (20 Marks):
  - [`MongoDB.py`](./MongoDB/MongoDB.py) — Main CLI entry point (`python3 MongoDB/MongoDB.py`).
  - [`cli.py`](./MongoDB/cli.py) — Interactive console menus and main application loop.
  - [`config.py`](./MongoDB/config.py) — Database URI, collection constants, and connection factory.
  - [`crud.py`](./MongoDB/crud.py) — PyMongo Read, Create, Update, Delete, and Keyword Search operations.
  - [`models.py`](./MongoDB/models.py) — Interactive document builders for `hazardousIncidents` and `patrolInspections`.
  - [`utils.py`](./MongoDB/utils.py) — Input validation prompts, JSON formatting, and filter builders.
  - [`requirements.txt`](./MongoDB/requirements.txt) — Python dependencies (`pymongo`).
- [`DBScript.txt`](./DBScript.txt) — Part 2 & Part 3: MongoDB shell (`mongosh`) script containing collection setup, sample data population (10+ docs per collection), 15 queries, and `adminRole` security configuration.
- [`Documentation/`](./Documentation/) — Assignment specification, technical blueprint, and team task division plan.

---

## Quick Start

### 1. Run the MongoDB Script (`DBScript.txt`)
```bash
mongosh < DBScript.txt
```

### 2. Run the Python Console Application (`MongoDB/MongoDB.py`)
Install `pymongo` and launch the interactive menu:
```bash
pip install -r MongoDB/requirements.txt
python3 MongoDB/MongoDB.py
```
*(Optional: set `MONGODB_URI` environment variable if connecting to a non-default MongoDB instance; defaults to `mongodb://localhost:27017/`).*
