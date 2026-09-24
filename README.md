# SERVIA - Enterprise AI Customer Experience Platform

SERVIA is a comprehensive, AI-powered platform designed to automate and enhance customer service support systems. It leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and a multi-tenant SaaS architecture to provide a fast, robust, and scalable customer experience solution. The platform can ingest company-specific data, handle user queries via text or voice, and deliver context-aware responses in multiple languages.

## Architecture Overview

The platform is built using a modern Python stack and follows a clean, modular architecture to separate concerns.

-   **FastAPI Backend**: The core of the application is a high-performance FastAPI server that manages API endpoints, WebSocket connections, and application lifecycle.
-   **Docker & Docker Compose**: All external services (Weaviate, MongoDB, vLLM) are containerized and managed with Docker Compose for easy setup and consistent deployment.
-   **RAG Pipeline**:
    -   **Data Ingestion**: A controller ingests data from Google Sheets, processes it into structured JSON, and splits it into text chunks.
    -   **Vector Database**: [Weaviate](https://weaviate.io/) is used to store vector embeddings of the data chunks for efficient similarity search.
    -   **Embedding**: [Sentence Transformers](https://www.sbert.net/) are used to generate dense vector representations of the text data.
    -   **Retrieval**: Hybrid search is performed on Weaviate to retrieve the most relevant documents based on a user's query.
-   **LLM Services**:
    -   **Generation**: An OpenAI-compatible API, served via [vLLM](https://github.com/vllm-project/vllm), generates conversational responses based on the user's query and the retrieved context.
    -   **Speech-to-Text**: [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) provides efficient and accurate audio transcription for voice-based interactions.
    -   **Prompt Engineering**: A flexible template system allows for dynamic, multi-lingual prompt construction for both routing and generation tasks.
-   **Multi-Tenant Database**: [MongoDB](https://www.mongodb.com/) stores company and chunk metadata, with data logically separated by company.

## Key Features

-   **Multi-Tenant RAG**: Ingest, process, and query data on a per-company basis.
-   **Multi-Modal Input**: Interact with the system via text or real-time audio through a WebSocket interface.
-   **Automated Data Ingestion**: Pulls and processes knowledge base data directly from a specified Google Sheet.
-   **Multi-Language Support**: The prompt templating system is designed to support multiple languages for both system prompts and user responses.
-   **Containerized Dependencies**: All required services (Vector DB, Document DB, LLM Server) are managed by Docker for simplified setup.
-   **Scalable LLM Serving**: Leverages vLLM for high-throughput and efficient LLM inference.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.10+
-   Docker and Docker Compose
-   An NVIDIA GPU is required for running the vLLM and Whisper services efficiently.

### 1. Clone the Repository

```bash
git clone https://github.com/eslamyasser-1/servia---enterprise-ai-customer-experience-platform-llms-rag-saas-.git
cd servia---enterprise-ai-customer-experience-platform-llms-rag-saas-
```

### 2. Configure Environment Variables

First, copy the example environment files for the main application and Docker services.

```bash
# For the main application
cp .env.example .env

# For Docker services
cd docker
cp .env.example .env
cd ..
```

Next, edit the two new `.env` files to set your configuration.

**In `./docker/.env`:**
-   `HF_TOKEN`: Your Hugging Face access token, required to download gated models for vLLM.
-   `MODEL_NAME`: The Hugging Face model to be served by vLLM (e.g., `Qwen/Qwen2-1.5B-Instruct`).

**In `./.env`:**
-   `MONGO_URL`: The connection string for MongoDB. The default (`mongodb://admin:admin123@localhost:27017`) matches the `docker-compose.yaml` setup.
-   `WEAVIATE_URL`: The URL for the Weaviate instance. The default (`http://localhost:8080`) matches the `docker-compose.yaml` setup.
-   `GOOGLE_SHEET_URL`: The public URL of the Google Sheet containing the company data.
-   `EMBEDDING_MODEL`: The Sentence Transformer model for embeddings.
-   `GENERATION_MODEL_NAME`: The model name that matches the one being served by vLLM.
-   `VLLM_PORT`: The port on which the vLLM server is running.

### 3. Set Up Python Environment

Create and activate a virtual environment, then install the required dependencies.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment (Linux/macOS)
source .venv/bin/activate

# Or on Windows
# .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Dependent Services

Use Docker Compose to build and run the Weaviate, MongoDB, and vLLM containers in the background.

```bash
cd docker
docker compose up --build -d
cd ..
```

### 5. Run the Application

You can use the provided shell script to automate the final setup steps and launch the application. This script also handles a known compatibility issue with the `cryptography` library and initializes the database with a default admin user.

```bash
chmod +x run_csab.sh
./run_csab.sh
```

The script performs the following actions:
1.  Ensures Docker services are running.
2.  Installs Python dependencies.
3.  Applies a fix for the `cryptography` library.
4.  Initializes MongoDB with a default admin: `(Name: [Name], Password: [Password])`.
5.  Starts the FastAPI application on `http://0.0.0.0:5000`.

Your SERVIA instance is now running!

## Usage

### 1. Ingest Company Data

To ingest data for a new company, make a GET request to the `/data/start/{company_name}` endpoint. This will pull data from the configured `GOOGLE_SHEET_URL`, process it, generate embeddings, and store them in Weaviate.

You must provide the admin credentials (initialized by `run_csab.sh`) as query parameters.

**Example using `curl`:**
```bash
curl -X GET "http://localhost:5000/data/start/Talabat?Admin_name=[Name]&Admin_password=[Password]"
```
Replace `Talabat` with the name of the company as it appears in your Google Sheet.

### 2. Chat with the Assistant

Connect to the WebSocket endpoint at `/chat/query/{company_name}` to start a conversation.

You can send messages in two formats:
-   **Text Message**:
    ```json
    {
      "type": "text",
      "content": "What are your delivery options?"
    }
    ```
-   **Audio Message**:
    ```json
    {
      "type": "audio",
      "content": "<base64_encoded_audio_string>"
    }
    ```
The server will transcribe the audio, retrieve relevant context, generate a response, and send it back through the WebSocket.
