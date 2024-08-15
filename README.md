# Project_Cryptocurrency_Data_Pipeline

This project is a data pipeline for fetching cryptocurrency OHLCV data from Binance, processing it, and loading it into a PostgreSQL database using Apache Airflow. The pipeline runs within a Docker container for easy deployment and consistency.

## Architecture

![shiba](https://github.com/user-attachments/assets/4bc73ac7-6e18-43db-bd5f-023b3b418516)

## Technologies
- Python
- Docker
- Apache Airflow
- PostgreSQL
- Minio
- Mailhog

## Starting Airflow
Use Docker Compose to start Airflow and its dependencies:
```yaml
docker-compose up -d --build
```

To stop the Docker containers, use:
```yaml
docker-compose down
```
## Running the Pipeline
Once Docker Compose is running, you can access the Airflow web interface at **http://localhost:8080**.

Log in with the default credentials:

**Username**: airflow

**Password**: airflow


## Airflow Connection to MinIO
Since MinIO offers S3 compatible object storage, we can set the connection type to "Amazon Web Services". However, we'll need to set an extra option, so that Airflow connects to MinIO instead of S3.
- **Connection Name:** or any name you likeminio
- **Connection Type:** Amazon Web Services
- **AWS Access Key ID:** <replace_here_with_your_minio_access_key>
- **AWS Secret Access Key:** <replace_here_with_your_minio_secret_key>
- **Extra: a JSON object with the following properties:**

```yam
{
  "host": "http://minio:9000"
}
```

See the example below:

![project_cryp](https://github.com/user-attachments/assets/1bac8b1d-0124-4870-91a9-90faf95e2e02)


**Note**: If you were using AWS S3 already, you don't need to specify the host in the extra.

## Airflow Connection to PostgreSQL

![Screenshot 2024-08-15 143800](https://github.com/user-attachments/assets/7257b442-5de0-444b-b75e-7850d97c4d64)

## Data Pipeline
Completed Data Pipeline

![Screenshot 2024-08-15 122208](https://github.com/user-attachments/assets/da3cd360-ce6d-48cd-b3dd-29cdbdea86ce)


## References
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [MinIO Docker Quickstart Guide](https://docs.min.io/docs/minio-docker-quickstart-guide.html)
- [Deploy MinIO on Docker Compose](https://docs.min.io/docs/deploy-minio-on-docker-compose)
