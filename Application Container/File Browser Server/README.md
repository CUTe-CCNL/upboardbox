### FileBrowser Server

使用 Podman 以 Dockerfile 建立一 FileBrowser Server 的 Pod

#### 建立 Dockerfile

首先建立一目錄存放後續建立的設定檔

`mkdir -p ~/fbs`
 - p：若缺少父目錄則一並建立

建立 Dockerfile

`nano ~/fbs/Dockerfile`
```dockerfile
# 以 alpine 的 image 為基底來改造
FROM quay.io/cloudwalker/alp.base
# 下載 bash 和 curl 套件，新增使用者 app
# 使用 crul 從網址抓取 .sh 給 bash 執行，下載 filebrowser 的相關 shallscript(指令)
RUN apk --update add ca-certificates bash curl \
    && adduser -h /opt/app -D app \
    && curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash

# 將自己的應用程式複製進去
COPY entrypoint /opt/app/entrypoint
# 並給予該程式執行權限
RUN chmod a+x /opt/app/entrypoint

# 為應用程式產生儲存空間
VOLUME /srv
# 開 4000 port
EXPOSE 4000
# 將使用者設給 app
USER app
# 工作目錄在 /opt/app
WORKDIR /opt/app

# entrypoint 檔案含 Container 被建立時會被執行的指令等
ENTRYPOINT [ "/opt/app/entrypoint" ]
```

#### 建立 entrypoint

```dockerfile
#!/bin/bash
# filebrowser 權限設定：相關操作權限都是 False -> 唯讀
filebrowser config init --port 4000 --address "" --baseurl "" --log "stdout" --root="/srv" --auth.method='noauth' --commands "" --lockPassword --perm.admin=false --perm.create=false --perm.delete=false --perm.execute=false --perm.modify=false --perm.rename=false --signup=false
# 允許匿名登入，不須先建立使用者才能使用
filebrowser users add anonymous "anonymous"
filebrowser
```

#### 依上述設定檔建立 Image

**指令中只需提供上述設定檔所在的目錄**
（範例中是 ~/fbs/）

`sudo podman build -t alp.fbs ~/fbs/`

可查看是否建立成功

`sudo podman image list`

![image](https://hackmd.io/_uploads/rJrXjXJ0T.png)

#### 以該 Image 建立 Pod

`sudo podman run --name f1 -d -p 80:4000 --volume /tmp:/srv:ro alp.fbs`
 - n：Pod 命名為 f1
 - d：背景執行
 - p：將本機的 80 port 連接至 Pod 的 4000 Port
 - volume：將本機的 /tmp 掛載給 Pod 的 /srv （見 Dockerfile 的 VOLUME）
 在本機 /tmp 中的檔案應出現在 FileBrowser 的網站中
 - 使用的 Image：剛建立的 alp.fbs

可查看是否建立成功

`sudo podman ps -a`

![image](https://hackmd.io/_uploads/HyENpmkRp.png)

也可以開啟網頁查看
使用 `ip addr` 查看 IP 後直接至瀏覽器輸入即可

![image](https://hackmd.io/_uploads/HkGzNV10p.png)

![image](https://hackmd.io/_uploads/rk8mVNy06.png)
