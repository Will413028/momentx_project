# momentx_project

## curl test command example

### uploadfile api test

```bash
curl -X 'POST' 'http://127.0.0.1:8000/uploadfile' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@path/to/your/file.txt;type=text/plain'

// file example 
// -F 'file=@./article.txt;type=text/plain'
```

### ask question api test

```bash
curl -X 'POST' 'http://127.0.0.1:8000/ask' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "document_name": "已上傳的檔案名稱", "question": "想對文件詢問的問題" }'

// parameter example
// {
//     "document_name": "article.txt",
//     "question": "這篇文章在說什麼？"
// }
```

## API Endpoints

`POST /uploadfile` - upload txt file to azure blob

`POST /ask` - ask a question to txt file

## Database Schema

<https://dbdiagram.io/d/QA-system-6500368802bd1c4a5e693886>

## Database

### SQL Database: using MySQL

### Vector Database: using Qdrant

---

## How to run

### 1. Use Docker Compose

```bash
sudo docker compose up -d
```

### 2. Run local

```bash install dependency
pip install -r requirements.txt
```

```bash run server
uvicorn main:app --reload
```

## Database migration

```bash
alembic upgrade head
```
