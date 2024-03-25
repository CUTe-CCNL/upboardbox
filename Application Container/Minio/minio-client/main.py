import os

from minio import Minio
from minio.error import S3Error

class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        """
        初始化 MinioClient 類的實例。
        :param endpoint: MinIO 服務的地址。
        :param access_key: MinIO 服務的存取金鑰。
        :param secret_key: MinIO 服務的秘密金鑰。
        :param secure: 是否使用 HTTPS (默認為 False，即使用 HTTP)。
        """
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def upload_file(self, bucket_name, source_file_path, destination_file_name):
        """
        上傳文件到指定的 MinIO bucket。
        :param bucket_name: 目標 bucket 的名稱。
        :param source_file_path: 源文件的路徑。
        :param destination_file_name: 在 MinIO 上的文件名稱。
        """
        # 檢查 bucket 是否存在，如果不存在則創建
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"Created bucket {bucket_name}")
        else:
            print(f"Bucket {bucket_name} already exists")

        # 上傳文件
        self.client.fput_object(bucket_name, destination_file_name, source_file_path)
        print(f"{source_file_path} successfully uploaded as object {destination_file_name} to bucket {bucket_name}")

    def list_bucket_contents(self, bucket_name):
        """
        列出指定 bucket 中的所有對象。
        :param bucket_name: 要列出內容的 bucket 的名稱。
        """
        try:
            objects = self.client.list_objects(bucket_name)
            for obj in objects:
                print(obj.object_name)
        except S3Error as exc:
            print("Error occurred while listing bucket contents:", exc)

    def download_file(self, bucket_name, object_name, download_dir):
        """
        從指定的 MinIO bucket 下載文件。
        :param bucket_name: 目標 bucket 的名稱。
        :param object_name: MinIO 上的文件名稱。
        :param file_path: 文件下載到本地的路徑。
        """
        file_path = os.path.join(download_dir, object_name)

        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"Successfully downloaded {object_name} to {file_path}")
        except S3Error as exc:
            print(f"Error occurred while downloading {object_name}:", exc)

# 使用示例
if __name__ == "__main__":
    # 初始化 MinioClient 實例
    minio_client = MinioClient("m1:9000", "username", "passwd")

    # 上傳文件示例
    minio_client.upload_file("python-test-bucket", "hello.txt", "hello.txt")

    # 列出 bucket 內容示例
    minio_client.list_bucket_contents("python-test-bucket")

    minio_client.download_file("python-test-bucket", "my-test-file.txt", "/app/")
