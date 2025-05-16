# === Makefile for StudyBuddy RAG Chatbot ===

# Python and virtual environment config
VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# === Commands ===

# 🔧 Setup environment
setup:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# 📚 Build vector DB
build-db:
	$(PYTHON) src/extract_text.py
	$(PYTHON) src/build_vectorstore.py

# 💬 Run chatbot
run:
	$(PYTHON) src/rag_query.py

# 🧹 Clean Chroma DB and JSON
clean:
	rm -rf alexxu_db
	rm -f data/book_pages.json

# 🐳 Docker Compose
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
