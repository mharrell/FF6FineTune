# FF6 Fine-Tune — Final Fantasy VI AI Game Guide

A custom AI game guide for Final Fantasy VI, built by fine-tuning a large language model on scraped wiki data. The project covers all versions of the game (SNES, PlayStation, GBA, iOS/Android, Steam, and Pixel Remaster) and is designed to be served through a web interface.

---

## Project Overview

This project builds a domain-specific AI assistant that can answer detailed questions about Final Fantasy VI — covering characters, abilities, espers, items, locations, enemy data, and version differences. Rather than relying on retrieval-augmented generation (RAG), the model is fine-tuned directly using LoRA, allowing it to answer questions natively without needing to look anything up at runtime.

---

## Pipeline

### 1. Data Collection
A custom web scraper built with Python, `requests`, and `BeautifulSoup4` pulls structured content from the Final Fantasy Wiki (Fandom) using the MediaWiki API. The scraper collects 90+ pages covering characters, abilities, espers, locations, items, and battle mechanics.

### 2. Data Cleaning
A regex-based cleaning pipeline strips wiki markup, infobox templates, HTML tags, image references, table syntax, and other artifacts from the raw scraped content, producing clean readable text organized by page and section.

### 3. Training Pair Generation
Cleaned content is converted into question/answer pairs in Alpaca format (the standard format for instruction fine-tuning). Section headings are used to generate contextually appropriate question templates — for example, "obtained" sections generate "How do I find X?" style questions, while "mechanics" sections generate "How does X work?" questions.

### 4. Dataset Expansion
The Anthropic API (Claude Haiku) is used to generate additional question variations for each section, expanding the dataset from ~1,100 base pairs to ~2,800 total training pairs. This improves model generalization by exposing it to more diverse phrasings of the same underlying knowledge.

### 5. Quality Review
A custom interactive CLI review tool samples 200 random pairs and allows manual accept/reject/edit decisions, ensuring training data quality before fine-tuning begins.

### 6. LoRA Fine-Tuning
The cleaned dataset is used to fine-tune a Llama 3.1 8B base model using Low-Rank Adaptation (LoRA) via Hugging Face's PEFT library. Training is performed locally on consumer hardware (NVIDIA RTX 3060 Ti, 8GB VRAM).

### 7. Web Interface
The fine-tuned model is served locally via Ollama and exposed through a FastAPI backend with a React frontend, featuring a dark fantasy aesthetic with FF6-inspired imagery.

---

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python 3.12 |
| Data Collection | requests, BeautifulSoup4, MediaWiki API |
| Data Processing | regex, json |
| AI / ML | Anthropic API (Claude Haiku), Hugging Face Transformers, PEFT (LoRA) |
| Model Serving | Ollama, Llama 3.1 8B |
| Backend | FastAPI |
| Frontend | React |
| Environment | python-dotenv, venv |
| Version Control | Git, GitHub |

---

## Key Concepts Demonstrated

- **Web scraping at scale** — navigating API pagination, handling redirects, and normalizing inconsistent page structures across 90+ wiki pages
- **NLP data preparation** — cleaning and structuring unstructured text for use as machine learning training data
- **Instruction fine-tuning** — converting raw knowledge into Alpaca-format Q&A pairs suitable for LLM fine-tuning
- **LoRA / Parameter-Efficient Fine-Tuning** — adapting a large language model to a specific domain without full retraining
- **LLM API integration** — using Claude Haiku to augment a dataset programmatically while managing token costs
- **Local LLM deployment** — running and querying a fine-tuned model locally via Ollama
- **Full-stack AI application** — connecting a fine-tuned model to a web interface end-to-end

---

## Project Structure

```
FF6FineTune/
├── wiki_scraper.py              # Scrapes FF6 wiki via MediaWiki API
├── data_cleaner.py              # Cleans raw wiki markup
├── training_pair_generator.py  # Converts cleaned data to Q&A pairs
├── expansion_script.py         # Expands pairs using Claude API
├── pair_review.py               # Interactive CLI quality review tool
├── data/
│   ├── raw/                     # Raw scraped wiki data
│   ├── cleaned/                 # Cleaned text data
│   └── training/                # Final training pairs (JSONL)
├── .env.example                 # Environment variable template
└── .gitignore
```

---

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:
```bash
pip install requests beautifulsoup4 lxml anthropic python-dotenv
```
3. Copy `.env.example` to `.env` and add your Anthropic API key
4. Install [Ollama](https://ollama.com) and pull the base model:
```bash
ollama pull llama3.1:8b
```
5. Run the pipeline in order:
```bash
python wiki_scraper.py
python data_cleaner.py
python training_pair_generator.py
python expansion_script.py
python pair_review.py
```

---

## Status

- [x] Data collection
- [x] Data cleaning  
- [x] Training pair generation (2,779 pairs)
- [x] Dataset expansion via Claude API
- [x] Quality review tooling
- [ ] LoRA fine-tuning
- [ ] Web interface
- [ ] Deployment

---

## Author

Built by [mharrell](https://github.com/mharrell)
