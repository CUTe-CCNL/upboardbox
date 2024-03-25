# MinIO

## MinIO 介紹

MinIO 是一個開源的物件儲存系統（Object Storage System），對 Amazon S3 的 API 完全相容。MinIO 面向於上至 TB 的大容量資料儲存，尤其是 AI、機器學習模型訓練等等，也可以用作連接資料庫或一般檔案儲存，適用於結構化與非結構化資料。MinIO 本身相當輕量，稍後示範的安裝過程也可以看到其簡易性，適合運行於各式場景，包含雲端服務、邊緣設備、或本地設施

MinIO 也可以運行於不同的架構，包含：

1. Single-Node Single-Drive, SNSD or Standalone
2. Single-Node Multi-Drive, SNMD or Standalone Multi-Drive
3. Multi-Node Multi-Drive, MNMD or Distributed

從自建 NAS 到企業的伺服器機房都適用，且具高容錯性：在 SNMD 可以容錯至多半數硬碟損毀、在 MNMD 可以容錯至多半數機器或半數硬碟損毀。相比於傳統磁碟陣列如 RAID 5 或 RAID 6，其容錯性相當可觀。

### MinIO 的元件

#### Object

是檔案在 MinIO 中儲存的資料結構。Object 是二進制資料，可以是圖片、音訊檔、甚至是可執行的二進制機器碼等等。

#### Bucket

相當於 `C:\` 的最高級目錄或資料夾，使用者可以用不同的 bucket 來區隔不同用途的檔案。bucket 內含 object，兩者的關係相當於資料夾與其中儲存的檔案

### MinIO Client

MinIO Client 可以提供使用者以類 UNIX 指令，對 MinIO 中的檔案進行操作。如`mc ls`、`mc cp`等等

### s3fs-fuse

`s3fs-fuse` 可以透過 FUSE(使用者空間檔案系統) 掛載 s3 bucket。因 MinIO 相容 S3 API，所以我們也可以透過 s3fs 來掛載 MinIO Server 中的 bucket 並進行操作

## MinIO 安裝過程：以 SNSD 為例

本範例在 Alpine Linux 虛擬機中，以 Podman 建立 MinIO 的 Pod。另會安裝 `MinIO Client` 及 `s3fs-fuse`，並嘗試傳入檔案進行測試

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

建立 Pod 時，預先建立一個 Root 使用者 bigred12345。並將 MinIO 中檔案的儲存位置掛載到剛建立的目錄 `~/ms`，這一個目錄對 MinIO 來說相當於一個硬碟

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

登入後可以看到該 MinIO 伺服器的狀況

![MinIO_Web_With no Bucket](https://imgur.com/C8bAV8r.png)

### 安裝 MinIO Client

#### 下載並賦予執行權限

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc --create-dirs -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

mc --help
# 若安裝成功，可以看到 help 的內容
```

#### 將 MinIO Client 連接到 MinIO

使用 `alias` 與剛建立的 MinIO 連接並以 `mios` 代稱，在後續指令中加上 `mios` 即代表以這裡連線的 MinIO Server 為操作對象

```
mc alias set mios http://127.0.0.1:9000 bigred12345 bigred12345
# 對剛建立的 MinIO 建立連接、登入、並以 mios 代稱
# 若成功連接應可以看到 successfully 訊息
# mc: Configuration written to `/home/u462063/.mc/config.json`. Please update your access credentials.
# mc: Successfully created `/home/u462063/.mc/share`.
# mc: Initialized share uploads `/home/u462063/.mc/share/uploads.json` file.
# mc: Initialized share downloads `/home/u462063/.mc/share/downloads.json` file.
# Added `mios` successfully.

mc ls mios
# 因為剛建立所以沒有檔案
```

在 `mios` 建立一個 bucket 叫做 `mybucket`

```
mc mb mios/mybucket

mc ls mios
# 可以看到剛建立的 mybucket
```

#### 建立檔案並上傳測試

建立一個檔案 `file1` 並複製上傳到 `mybucket` 進行測試

```
dd if=/dev/zero of=file1 bs=10485760 count=100
# 建立一個 1G 的檔案 (10485760 byte * 100)
# dd, data duplicator 是一用於複製及轉換格式的指令
# if 是來源檔案, of 是目的檔案
# bs 是一次讀寫的資料大小(byte)
# count 則是處理幾個區塊，每個區塊大小如 bs
# if 的 /dev/zero 是含無限空字元的檔案

ls -alh
# 查看 file1 大小(1G)

mc cp file1 mios/mybucket
# 將檔案複製到 mybucket

mc ls mios/mybucket/
# 若上傳成功，可以在 mybucket 中看到 file1
# [2024-03-25 20:30:04 CST]1000MiB STANDARD file1

ls ms/mybucket/
# 在被掛載的 ms/ 目錄中也可以看到剛剛上傳的 file1
```

到 MinIO 的管理頁面中點進 `mybucket` 看到該檔案

![](https://imgur.com/kbkfn9D.png)

到此 SNSD 的 MinIO Pod 就建立成功了。

### s3fs-fuse

#### 安裝
```
sudo apk add s3fs-fuse --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted

sudo apk add mailcap --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/main/ --allow-untrusted

sudo apk add fuse-overlayfs
```

#### 準備工作

需要為 s3fs-fuse 建立密碼檔案來連線至 MinIO Server，並建立一個目錄供 s3fs 掛載 bucket。這裡的 `bigred12345` 對應建立 MinIO Pod 時設定的 Root user

```
echo 'bigred12345:bigred12345' >.passwd-s3fs; chmod 600 .passwd-s3fs

mkdir -p mydata
```

#### 連線到 MinIO Server

把 mybucket 掛載到 `/home/bigred/mydata`，就可以用 Linux 指令對檔案進行操作

```
s3fs mybucket /home/bigred/mydata -o passwd_file=.passwd-s3fs -o url=http://127.0.0.1:9000 -o use_path_request_style -o dbglevel=info -f -o curldbg &>/dev/null &
# 把 mybucket 掛載到 /home/bigred/mydata
# 就可以用 Linux 指令進行對檔案操作

ls mydata/
# 這裡也可以看到剛剛上傳至 MinIO Server 的 file1
```
## MinIO 掛載在隨身碟

### 掛載隨身碟作為 MinIO 的儲存位置


首先在使用者家目錄下建立一個目錄 `~/ms` 作為 MinIO 的儲存位置

```
sudo rm -r ~/ms; mkdir ~/ms
```

接著將隨身碟插入電腦，並看是否有讀取的隨身碟

```
lsblk
```

若有讀取到隨身碟，則可以看到類似以下的資訊：

```
sdb      8:16   1  14.9G  0 disk
└─sdb1   8:17   1  14.9G  0 part
```



接著將隨身碟掛載到 `~/ms` 目錄下

```
sudo mount /dev/sdb1 ~/ms
```

若要卸載隨身碟，則可以使用以下指令

```
sudo umount /dev/sda1
```

### 建立 MinIO 的 container

建立 MinIO 的 container 時，將剛剛掛載的目錄 `~/ms` 掛載到 container 中的 `/data` 目錄下

```
sudo podman run --name m1 -d -p 9000:9000 -p 9001:9001 -v ~/ms:/data -e MINIO_SERVER_ACCESS_KEY=$MINIO_ACCESS_KEY -e MINIO_SERVER_SECRET_KEY=$MINIO_SECRET_KEY -e MINIO_ROOT_USER='bigred12345' -e MINIO_ROOT_PASSWORD='bigred12345' quay.io/minio/minio server --console-address ":9001" /data
# 9000 Port 用於連接 MinIO 的 API
# 9001 Port 連接 MinIO 的管理介面
# 同時建立 Root 使用者帳號密碼為 bigred12345
```

