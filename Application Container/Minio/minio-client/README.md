# 操作手冊

## 技術文件概覽

本文件旨在提供對於使用 Python 和 MinIO 構建的文件儲存系統的詳細說明。系統支援文件的上傳、下載、列出以及刪除功能。

## 系統需求
- Python 3.6+
- MinIO Server
- MinIO Python SDK (minio)

## 安裝與設定
1.確保已安裝 MinIO Server 並且正在運行。
2.使用 pip 安裝 MinIO Python SDK:

```bash
pip install minio
```
3.配置您的 MinIO 存取和秘密金鑰。

## 組件說明

系統主要由以下組件構成：

 模型（Models）:

- File: 代表一個文件，含有文件的路徑屬性。

儲存庫接口（Storage Repository Interface）:

- StorageRepository: 定義與儲存系統互動所需的方法。

儲存庫實現（Storage Repository Implementation）:

- MinIOStorage: StorageRepository 的一個實現，使用 MinIO 作為底層儲存解決方案。

操作類別（Operation Classes）:

- DeleteFile: 負責文件的刪除。
- DownloadFile: 負責文件的下載。
- ListFile: 負責列出所有文件。
- UploadFile: 負責文件的上傳。

## 使用範例

1.初始化 MinIO 儲存:

```python
from domain.repositories.storage_repository import MinIOStorage

storage = MinIOStorage(endpoint='localhost:9000', access_key='yourAccessKey', secret_key='yourSecretKey', bucket_name='yourBucketName')
```

2.上傳文件:

```python
from domain.models.file import File
from domain.use_cases.upload_file import UploadFile

upload_file_use_case = UploadFile(storage)
upload_file_use_case.execute(File('destination/path.jpg'), File('source/path.jpg'))
```

3.下載文件:

```python
from domain.use_cases.download_file import DownloadFile

download_file_use_case = DownloadFile(storage)
download_file = download_file_use_case.execute('file_name.jpg', 'destination/path')
```

4.列出所有文件:
```python
from domain.use_cases.list_file import ListFile

list_file_use_case = ListFile(storage)
list_file_use_case.execute()
```

5.刪除文件:
```python
from domain.use_cases.delete_file import DeleteFile

delete_file_use_case = DeleteFile(storage)
delete_file_use_case.execute('file_name.jpg')
```