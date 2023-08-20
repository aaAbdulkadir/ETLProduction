# Seting up RDS

## Creating Postgres db

1. Click Create database
2. Select PostgreSQL
3. Select the free tier template
4. Name the db instance identifier `airflow-db`
5. Create a master usernamea and password
6. Select `db.t3.micro` for instance config as this is part of the free tier
7. Select `General purpose SSD (gp2)` for storage as this is part of the free tier
8. Under additioanl configuration, add a databse username `airflow_db`
9. Create database

## Opening connection

1. Go to RDS databases
2. Click on VPC security groups under Network & Security
3. Edit the inbound rules and include anywhere for postgers type