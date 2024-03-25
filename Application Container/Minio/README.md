# MinIO

## MinIO 介紹

### MinIO Client

MinIO Client 可以提供使用者以類 UNIX 指令，對 MinIO 中的檔案進行操作。如`ls`、`cp`等等

## MinIO 安裝過程：以 SNSD 為例

本範例在 Alpine Linux 虛擬機中，以 Podman 建立 MinIO 的 Pod。另會安裝 MinIO Client 及 s3fs，並嘗試傳入檔案進行測試

### 前置準備

首先須建立金鑰
```
export MINIO_ACCESS_KEY=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
export MINIO_SECRET_KEY=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
```

建立供稍後 MinIO Pod 掛載的目錄 `~/ms`

```
sudo rm -r ~/ms; mkdir ~/ms
```

### 建立 MinIO 的 Pod

建立 Pod 時，預先建立一個 Root 使用者 bigred12345
並將 MinIO 中檔案的儲存位置掛載到剛建立的目錄 `~/ms`

```
sudo podman run --name m1 -d -p 9000:9000 -p 9001:9001 -v ~/ms:/data -e MINIO_SERVER_ACCESS_KEY=$MINIO_ACCESS_KEY -e MINIO_SERVER_SECRET_KEY=$MINIO_SECRET_KEY -e MINIO_ROOT_USER='bigred12345' -e MINIO_ROOT_PASSWORD='bigred12345' quay.io/minio/minio server --console-address ":9001" /data
# 9000 Port 用於連接 MinIO 的 API
# 9001 Port 連接 MinIO 的管理介面
# 同時建立 Root 使用者帳號密碼為 bigred12345
```

Pod 建立成功後，可以嘗試連線到 MinIO 的管理介面：

`http:<虛擬機的IP>:9001`

若建立成功，可以看見管理介面的登入頁

![MinIO_Web_Login Page](https://imgur.com/Rgrpvhf.png)