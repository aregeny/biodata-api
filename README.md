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

## Running locally
git clone https://github.com/aregeny/biodata-api \n
cd biodata-api \n
docker compose up --build

## Running Test Suite
source venv/bin/activate \n
pytest tests/ -v

## API Endpoints
- GET /genes/  -> List all genes in database
- POST /genes/ -> create a gene & add to database
- GET /genes/{id} -> retrieve a gene by ID
- PUT /genes/{id} -> update a specific gene
- DELETE /genes/{id} -> delete a gene
- GET /genes/search/ -> return genes by filtering for organism name or chromosome number

## Future Improvements

- Expand test suite for more rigourous testing of endpoints
- Implement an application load balancer with a fixed DNS to achieve a static public IP
- Implement an application load balancer and a domain name for HTTPS implementation
