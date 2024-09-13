# PDF Data Collection

This project is built using [Scrapy](https://scrapy.org/), a fast high-level web crawling and web scraping framework for Python. Follow the steps below to set up and run the project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Common Commands](#common-commands)


## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer, which comes with Python
- **Scrapy**: The web scraping framework

You can verify the installations by running:

```bash
python --version
pip --version
```

# Installation
1. Clone repository

```bash
git clone https://github.com/Kimhuoy/ocr_collect_data/tree/main
cd ocr_collect_data
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```
Alternatively, you can install Scrapy directly:

```bash
pip install scrapy
```


# How to Run
To run a spider and start scraping data:

Navigate to the Scrapy project directory:
```bash
cd pdf_collect_data/pdf_collect_data
```

Run a spider using the following command:
```bash
scrapy crawl <spider_name>
```

Example:

```bash
scrapy crawl example_spider
```

Optionally, you can output the scraped data to a file:

```bash
scrapy crawl <spider_name> -o output/data.json
```
Supported output formats include JSON, CSV, and XML.


# Common Commands

Create a new spider:
```bash
scrapy genspider <spider_name> <domain>
```

List all available spiders:
```bash
scrapy list
```

Run a spider in interactive mode:
```bash
scrapy shell <url>
```

View available options for a spider:
```bash
scrapy crawl <spider_name> --help
```

Clear the cache (if using caching):
```bash
rm -rf .scrapy/httpcache
```
