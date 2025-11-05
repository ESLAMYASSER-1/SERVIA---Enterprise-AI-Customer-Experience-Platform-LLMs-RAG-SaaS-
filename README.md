# Customer Service App Builder APP

### This app focuses on making the automation of building customer service support system available in fast, easy and robust way using the SOTA in AI, automation, and DevOps techniques

## installation 
1. environment Preparation 
```bash
    # Linux
    python -m venv <envName>
    source <envName>/bin/activate

    # Windows
    python -m venv <envName>
    cd <envName>/Scripts && activate && cd ../../
```

```bash 
    pip install -r requirements.txt
```


2. set environment variables 
```bash
    cd src && cp .env.example .env && cd ..
```
- then set your environment variables in <b><i> /src/.env </i></b>

3. Start Docker servers
- install docker 
```bash 
# Uninstall old versions if present
sudo apt-get remove docker docker-engine docker.io containerd runc

# Update package index and install dependencies
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker’s official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker’s stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the package index again
sudo apt-get update

# Install Docker Engine, CLI, containerd, Docker Compose plugin
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group (enables running docker without sudo)
sudo usermod -aG docker $USER

# Print installed versions to verify
docker --version
docker compose version

echo "Done! Log out and log in again if you want to use 'docker' without sudo."
```

- build and run servers
```bash 
cd docker
docker compose up --build -d
cd ..
```

3. Run your Server
```bash 
    cd src
    uvicorn --port=8000 main:app
    cd ..
```





















## step by step 
### Technical 
1) start of the project
0) - initiate main.py as entry point for FastAPI
0) - add pydantic BaseSettings for env vars handling 
0) base route and base configurations
0) - add routes/base.py to handle landing endpoint 
0) - add lifespan for FastAPI app to handle startup and shtdown
0) data route
0) - created ResponseEnums 
0) - created routes/data.py to handle data processes 
0) database connection and models 
0) - add database connection to app that connect when server run
0) - create AdminModel to handle admin operations
0) - created BaseDataModel and BaseController to be the root of data models and controllers
0) - check authentication for admins in dataUpload Endpoint
0) - implement dataController to get data from google form // and process data by company name and convert it to json then json to chunks 
0) adding chunks to database
0) - Company model to handle company names and id with indexing 
0) - chunks schema for mongoDB
0) - chunk Model to handle chunks 
0) embedding and LLM services 
0) - create LLM_Interface to be absract interface for embedding and generation models interfaces
0) - add Weaviate client connection to the app
0) - create weaviate schema
0) - create weaviate provider
0) - create vectorDB service  
0) LLM router and LLM generation 
0) - create routes/nlp route
0) - set the geneartion model provider
0) - make VDB hypred search based on query and vector 
0) - edit nlpRouter for query endpoint
0) - cont .... voice get and then query 
0) - cont .... llm router 
0) - cont .... llm generation 
0) - cont .... Prompt template 
0) - cont .... Prompt factory 


### NonTechnical
1) creating file structure and environment using MVC pattern 
2) Prep Git and remote Repo
3) Write down README file 
4) write down requirements.txt
5) add .gitignore and .env and .env.example
6) create assets folder and it's .gitignore 
7) admin should be added using shell to DB
8) create domain forlder which is for main interfaces(abstract classes) and providers(API providers) and services(factories and services handlers)
9) .cont
