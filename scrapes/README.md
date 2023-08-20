## Terraform

- Deploy Airflow on EC2
- Postgres db to store datasets
- S3 to store dags


## CI/CD Pipeline

- Developer pushes dags from local GitHub, webhook triggers and pushes file to S3 bucket.  Configure EC2 to copy files from s3.

## Revised

Run Airflow on an EC2 instance

configure rds inbound rules, configure inbound rules of ec2 to go on airflow webiste, configure load code to find profile name from cli and aws config