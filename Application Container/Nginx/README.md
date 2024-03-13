##### 建立測試用的 Pod(Nginx)

`sudo podman run --name n1 -d nginx`
 - name：Pod 名稱
 - d：在背景執行

`sudo podman exec n1 hostname -i`
在 Pod n1 使用指令 hostname -i 顯示 IP
`curl http://<Pod 的 IP>`
查看是否成功啟用 nginx



## Application Container

#### 管理方便

透過 Container 架設服務，可以避免修改本機系統
減少系統上日以俱增且難以控管的變化
增加管理時的方便性與資源使用率

#### 安全性

為每個服務建立 Container 可以對網路連接加以控管
每個 Container 也僅開啟該服務所必須的 Port
可以避免多個 Port 的設定麻煩與可能帶來的安全問題

#### 機動性

只要留有對應的 Dockerfile 及相關設定檔
每次建立該 Container 僅需再下少許指令
也可依需求快速的增減與修改服務所需要的資源
