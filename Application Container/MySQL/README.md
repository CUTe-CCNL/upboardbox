# MySQL

Dockerhub 可找到 MySQL 的 Dockerfile，可以直接 `pull` 後建立 Pod。也可以再編寫自己的 Dockerfile，並依需求加入額外設定。

此範例中在 Dockerfile 設定預先建立一個使用者與一個資料庫

### 取得 MySQL 的 Image 

```
sudo podman pull mysql
```

### 以該 Image 建立 container

```
sudo podman run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```
