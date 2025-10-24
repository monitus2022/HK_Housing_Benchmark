from config import housing_benchmark_config, cloud_storage_secrets
import boto3
from logger import housing_logger
from pathlib import Path


class StorageManager:
    def __init__(self):
        self.s3_client = None
        self.service_type = housing_benchmark_config.cloud_storage.service_type

        # Get configuration based on service type
        if self.service_type == "aws":
            self.bucket_name = housing_benchmark_config.aws.bucket_name
            self.region = housing_benchmark_config.aws.region
            self.account_id = None
        elif self.service_type == "cloudflare":
            self.bucket_name = housing_benchmark_config.cloudflare.bucket_name
            self.region = housing_benchmark_config.cloudflare.region
            self.account_id = cloud_storage_secrets.account_id
        else:
            raise ValueError(f"Unsupported service type: {self.service_type}")

        self.access_key_id = cloud_storage_secrets.access_key_id
        self.secret_access_key = cloud_storage_secrets.secret_access_key

        self._initialize_s3_client()

    def _initialize_s3_client(self):
        """Initialize the S3 client for the configured service."""
        try:
            # Determine endpoint URL and region based on service type
            if self.service_type == "aws":
                endpoint_url = f"https://s3.{self.region}.amazonaws.com"
                region_name = self.region
                service_name = "AWS S3"
            elif self.service_type == "cloudflare":
                endpoint_url = housing_benchmark_config.cloudflare.endpoint_url.format(
                    account_id=self.account_id
                )
                region_name = self.region
                service_name = "Cloudflare R2"
            else:
                raise ValueError(f"Unsupported service type: {self.service_type}")

            self.s3_client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=region_name,
            )
            housing_logger.info(f"{service_name} S3 client initialized successfully")
        except Exception as e:
            housing_logger.error(
                f"Failed to initialize {self.service_type} S3 client: {e}"
            )
            raise

    def upload_files_from_data_folder(self):
        """
        Upload all files from the data folder to the configured S3-compatible bucket.
        """
        try:
            service_name = "AWS S3" if self.service_type == "aws" else "Cloudflare R2"
            housing_logger.info(
                f"Starting upload of files from data folder to {service_name}"
            )

            data_path = Path(housing_benchmark_config.storage.root_path)

            if not data_path.exists():
                housing_logger.warning(f"Data folder {data_path} does not exist")
                return

            # Walk through all files in the data directory
            for file_path in data_path.rglob("*"):
                if file_path.is_file() and file_path.name != ".DS_Store":
                    # Get relative path for S3 key
                    relative_path = file_path.relative_to(data_path.parent)
                    s3_key = str(relative_path)

                    self._upload_file(str(file_path), s3_key)

            service_name = "AWS S3" if self.service_type == "aws" else "Cloudflare R2"
            housing_logger.info(
                f"Upload of files from data folder to {service_name} completed successfully"
            )

        except Exception as e:
            housing_logger.error(f"Upload failed: {e}")
            raise

    def _upload_file(self, local_file_path: str, s3_key: str):
        """
        Upload a single file to the configured S3-compatible service.

        Args:
            local_file_path: Path to the local file
            s3_key: Key for the file in S3 bucket
        """
        try:
            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_key)
            housing_logger.info(
                f"Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_key}"
            )
        except Exception as e:
            housing_logger.error(f"Failed to upload {local_file_path}: {e}")
            raise

    def _download_folder(self, folder_path: str):
        """
        Download all files from a specific folder in the configured S3-compatible bucket to the data folder.

        Args:
            folder_path: The folder path (prefix) in the S3 bucket to download from
        """
        try:
            service_name = "AWS S3" if self.service_type == "aws" else "Cloudflare R2"
            housing_logger.info(
                f"Starting download of files from {service_name} folder '{folder_path}' to data folder"
            )

            data_path = Path(housing_benchmark_config.storage.root_path)

            # Ensure folder_path ends with '/'
            if not folder_path.endswith('/'):
                folder_path += '/'

            # List all objects in the bucket with the specified prefix
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=folder_path):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        s3_key = obj['Key']
                        # Compute local path relative to the folder_path
                        relative_path = s3_key[len(folder_path):]
                        local_path = data_path / relative_path
                        local_path.parent.mkdir(parents=True, exist_ok=True)
                        self._download_file(s3_key, str(local_path))

            housing_logger.info(
                f"Download of files from {service_name} folder '{folder_path}' to data folder completed successfully"
            )

        except Exception as e:
            housing_logger.error(f"Download failed: {e}")
            raise

    def _download_file(self, s3_key: str, local_file_path: str):
        """
        Download a single file from the configured S3-compatible service.

        Args:
            s3_key: Key for the file in S3 bucket
            local_file_path: Path to the local file
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_file_path)
            housing_logger.info(
                f"Downloaded s3://{self.bucket_name}/{s3_key} to {local_file_path}"
            )
        except Exception as e:
            housing_logger.error(f"Failed to download {s3_key}: {e}")
            raise

    def download_all_from_datahub(self):
        """
        Download all files from the datahub folder in the configured S3-compatible bucket to the local data folder.
        """
        try:
            datahub_folder = housing_benchmark_config.cloudflare.datahub_folder_name
            self._download_folder(datahub_folder)
        except Exception as e:
            housing_logger.error(f"Download from datahub failed: {e}")
            raise
