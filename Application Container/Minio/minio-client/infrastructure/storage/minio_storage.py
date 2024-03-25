import os

from minio import Minio
# from minio.error import S3Error


from domain.models.file import File
from domain.repositories.storage_repository import StorageRepository

class MinIOStorage(StorageRepository):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"Created bucket {bucket_name}")


    def upload_file(self, destination_file: File, source_file: File) -> None:
        self.client.fput_object(self.bucket_name, destination_file.path, source_file.path)
        print(f"{source_file} successfully uploaded as object {destination_file} to bucket {self.bucket_name}")


    def download_file(self, file_name: str, file_path: str) -> File:
        download_path = os.path.join(file_path, file_name)
        self.client.fget_object(self.bucket_name, file_name, download_path)
        print(f"Successfully downloaded {file_name} to {file_path}")


    def list_files(self) -> list[str]:
        print(f"Files in {self.bucket_name} bucket:")
        objects = self.client.list_objects(self.bucket_name)
        for obj in objects:
            print(obj.object_name)

    def delete_file(self, file_name: str) -> None:
        self.client.remove_object(self.bucket_name, file_name)
        print(f"Successfully deleted {self.bucket_name} from bucket {file_name}")

