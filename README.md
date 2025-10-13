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

3. Run your Server
```bash 
    cd src
    uvicorn --reload --port=8000 main:app
    cd ..
```





















## step by step 
### Technical 
1) initiate main.py as entry point for FastAPI
2) add pydantic BaseSettings for env vars handling 
3) add routes/base.py to handle landing endpoint 
4) add lifespan for FastAPI app to handle startup and shtdown
5) created ResponseEnums 
6) created routes/data.py to handle data processes 
7) add data base connection to app that connect when server run
8) create AdminModel to handle admin operations
9) created BaseDataModel and BaseController to be the root of data models and controllers
10) check authentication for admins in dataUpload Endpoint
9) ...cont... (database collection for admins and companies)

### NonTechnical
1) creating file structure and environment using MVC pattern 
2) Prep Git and remote Repo
3) Write down README file 
4) write down requirements.txt
5) add .gitignore and .env and .env.example
6) create assets folder and it's .gitignore 
7) -  admin should be added using shell to api
8) 
