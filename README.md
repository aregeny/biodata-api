# Biodata API

A RESTful backend service for storing and querying biological gene data.

Built with FastAPI, PostgreSQL, Docker and AWS.

Project development was AI-assisted.

## Live API

This project is deployed on AWS's ECS with Fargate service. The current free-tier setup does not utilize a load balancer, and thus the public IP changes each time the task is restarted. To minimize AWS costs, the service is only active during demonstrations and is otherwise inactive.

To check on the status of the API and find the live URL see "Live API Status." If you wish to see a demonstration of the Live API and the status is "stopped", please contact me and I will activate the service.

To run the full stack locally, please see "Running Locally".

## Live API Status
Currently stopped. Contact me or see "Running Locally" to run the fullstack.

## Tech Stack
- Python 3.12 / FastAPI
- PostgreSQL / SQLAlchemy 2.0
- Docker / Docker Compose
- AWS (ECR, ECS with Fargate, RDS)

## Architecture
- REST API build with FastAPI and Pydantic for request validation
- PostgreSQL database with SQLAlchemy ORM
- Containerized with Docker, orchestrated locally with Docker Compose
- Deployed to AWS ECS Fargate with RDS PostgreSQL
- Separated test and development databases for clean test isolation

## Running Locally 

### Prerequisities
- Docker Desktop
- Python 3.12

### Setup
git clone https://github.com/aregeny/biodata-api  
cd biodata-api  
docker compose up --build  

The API will be available to view locally at http://localhost:8000/docs

## Running Test Suite
source venv/bin/activate  
pytest tests/ -v

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /genes/ | List all genes in database |
| POST | /genes/ | Create a gene, then add to database |
| GET | /genes/{id} | Retrieve a single gene by ID |
| PUT | /genes/{id} | Update a single gene |
| DELETE | /genes/{id} | Delete a single gene by ID |
| GET | /genes/search/ | Filter genes in database by organism or chromosome |

## Example Request

```bash
curl -X POST "http://localhost:8000/genes/" \
    -H "Content-Type: application/json" |
    -d '{
        "gene_symbol" :  "BRCA1",
        "gene_name": "Breast Cancer Type 1 Susceptibility Protein",
        "organism": "Homo sapiens",
        "chromosome": "17",
        "description": "Tumour suppressor gene involved in DNA double-strand break repair."
    }
```

## Security Nodes
- Credentials managed via environmental variables, never hardcoded
- Test database isolated from development database
- RDS accessible only from ECS Security Group

## Future Improvements

- Move credentials to AWS Secrets Manager
- Implement an application load balancer with a fixed DNS to achieve a static public IP
- Implement an application load balancer and a domain name for HTTPS implementation
- Add authentication and authorization for users
- Add pagination to list endpoints for better UI experience
- Expand to additional biological data types.
