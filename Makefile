.PHONY: help build run stop clean test test-comprehensive logs shell dev install local-run demo health status

help: ## Show this help message
	@echo "Voice-Text Conversion API - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker-compose build

run: ## Run the application with Docker Compose
	docker-compose up -d

dev: ## Run the application in development mode with live reload
	docker-compose up

stop: ## Stop the running containers
	docker-compose down

clean: ## Remove containers, networks, and images
	docker-compose down --volumes --remove-orphans
	docker image prune -f

test: ## Run the basic test client
	docker-compose exec voice2text-api python app/test_client.py

test-comprehensive: ## Run comprehensive tests for both voice-to-text and text-to-voice
	docker-compose exec voice2text-api python app/test_comprehensive.py

test-voice-to-text: ## Test voice-to-text functionality specifically
	@echo "Testing voice-to-text conversion..."
	curl -X POST "http://localhost:8000/voice-to-text/" \
		-H "accept: application/json" \
		-H "Content-Type: multipart/form-data" || echo "Requires audio file"

test-text-to-voice: ## Test text-to-voice functionality
	@echo "Testing text-to-voice conversion..."
	curl -X POST "http://localhost:8000/text-to-voice/" \
		-H "accept: application/octet-stream" \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d "text=Hello world, this is a test&rate=normal&volume=normal&output_format=wav" \
		--output test_speech.wav && echo "Audio saved as test_speech.wav"

test-voices: ## Get available voices
	@echo "Getting available voices..."
	curl -X GET "http://localhost:8000/voices/" -H "accept: application/json" | python -m json.tool

test-formats: ## Get supported formats
	@echo "Getting supported formats..."
	curl -X GET "http://localhost:8000/formats/" -H "accept: application/json" | python -m json.tool

logs: ## Show application logs
	docker-compose logs -f voice2text-api

shell: ## Open a shell inside the running container
	docker-compose exec voice2text-api /bin/bash

install: ## Install dependencies locally (for development)
	pip install -r requirements.txt

local-run: ## Run the application locally (without Docker)
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

local-test: ## Run tests locally
	python app/test_comprehensive.py

demo: ## Open the API documentation
	@echo "API documentation available at:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc:      http://localhost:8000/redoc"
	@echo "Make sure the API is running first with 'make run'"

health: ## Check API health
	curl -f http://localhost:8000/health || echo "API is not responding"

status: ## Show container status
	docker-compose ps

# Development helpers
create-sample-audio: ## Create a sample audio file for testing
	@echo "Creating sample audio file..."
	curl -X POST "http://localhost:8000/text-to-voice/" \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d "text=This is a sample audio file for testing voice to text conversion&rate=normal&volume=normal" \
		--output sample_test_audio.wav && echo "Sample audio created: sample_test_audio.wav"

quick-test: ## Quick test of both functionalities
	@echo "🚀 Running quick test of both functionalities..."
	@make test-text-to-voice
	@echo "\n📊 API Status:"
	@make health
	@echo "\n🎤 Available voices (first few):"
	@curl -s "http://localhost:8000/voices/" | python -c "import sys,json; data=json.load(sys.stdin); [print(f\"  - {v.get('name', 'Unknown')}\") for v in data.get('voices', [])[:3]]" 2>/dev/null || echo "  (Error getting voices)"

setup: ## Setup the project (build and run)
	@echo "🔧 Setting up Voice-Text Conversion API..."
	@make build
	@make run
	@echo "⏳ Waiting for API to start..."
	@sleep 10
	@make health

full-test: ## Build, run, and test everything
	@echo "🎯 Running full test suite..."
	@make setup
	@make test-comprehensive
