# jumia-shoe-etl
 ETL pipeline that scrapes men's shoes from Jumia's fragment API, cleans prices &amp; discounts, deduplicates products, and loads into PostgreSQL.
# Scalable Web Scraping & Data Pipeline (Jumia Price Tracker)

## 📌 Overview

This project builds a scalable data pipeline that scrapes product data from an e-commerce platform, processes it, and stores it in a structured database for analysis.

The pipeline is designed to run repeatedly, allowing tracking of product price changes over time.

---

## 🎯 Objectives

* Scrape semi-dynamic web pages reliably
* Handle pagination and extract structured data
* Clean and transform raw scraped data
* Store data in a relational database
* Track historical changes (price trends)
* Containerize the entire system for reproducibility

---

## 🧱 Architecture

**Pipeline Flow:**

Scraping → Transformation → Database Load → Analysis

* **Extract**: Scrapes product data (name, price, link)
* **Transform**: Cleans data, generates unique product IDs
* **Load**: Inserts into PostgreSQL with proper schema
* **Storage**:

  * `products` table → product metadata
  * `price_logs` table → historical price tracking

---

## ⚙️ Tech Stack

* Python (requests, BeautifulSoup, pandas)
* PostgreSQL
* SQLAlchemy
* Docker & Docker Compose

---

## 🗄️ Database Schema

### Products Table

| Column       | Type | Description               |
| ------------ | ---- | ------------------------- |
| id           | TEXT | Unique product identifier |
| name | TEXT | Name of product           |

---

### Price Logs Table

| Column     | Type  | Description             |
| ---------- | ----- | ----------------------- |
| id         | TEXT  | Unique entry identifier |
| product_id | TEXT  | Foreign key to products |
| price      | FLOAT | Product price           |
| discount   | FLOAT | Discount value (if any) |
| timestamp  | DATE  | Date of scraping        |

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone <https://github.com/Ayoisegun/jumia-shoe-etl.git>
cd de_scraping_project
```

---
### 2. Environment Variables Setup

This project uses environment variables to configure the database connection.

1. Create a .env file in the root directory
touch .env
2. Add the following variables
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=jumia

DB_HOST=db
DB_NAME=jumia
DB_USER=postgres
DB_PASSWORD=password
---

### 3. Run with Docker

```bash
docker-compose up --build
```

This will:

* Start PostgreSQL
* Run the scraping pipeline
* Load data into the database

---

## 🔄 Pipeline Behavior

* Scrapes multiple pages of product listings
* Handles pagination automatically
* Cleans inconsistent price formats
* Generates stable product IDs:

  * Extracted from URL where possible
  * Falls back to hashed values when needed
* Avoids duplicate entries using constraints

---

## 📊 Example Insights

With the stored data, you can run queries such as:

* Track price changes over time
* Identify cheapest products in a category
* Analyze discount patterns
* Monitor pricing trends

---

## ⚠️ Challenges & Solutions

### 1. Dynamic Content

* Some data loaded via backend fragments
* Solution: reverse-engineered request endpoints

### 2. Missing Product IDs

* No explicit ID from source
* Solution: extract from URL + fallback hashing

### 3. Data Quality Issues

* Inconsistent price formats
* Solution: cleaning and validation in transformation stage

### 4. Database Constraints

* Type mismatches and overflows
* Solution: proper casting and schema design

---

## 🧠 Key Learnings

* Web scraping in real-world scenarios requires investigation, not assumptions
* Data cleaning is as important as data collection
* Schema design directly impacts pipeline stability
* Containerization makes projects reproducible and portable

---

## 🔮 Future Improvements

* Schedule pipeline to run daily (cron or Airflow)
* Switch to the standard category URL (/mens-shoes/?page=1) for real pagination
* Add logging and monitoring
* Expand to multiple product categories
* Build a dashboard for visualization
* Implement API-based scraping where available

---

## 📌 Notes

* This project is for educational purposes
* Scraping respects reasonable request limits and delays

---
