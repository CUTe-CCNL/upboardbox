### Podman

#### Podman 特色

相比 Docker 在建立並運行 Container 時
會開啟 dockerd 以及 containerd 兩個 daemon

Podman 並不會啟動背景程序，稱為 Daemonless
如此可避免運行 Daemon 可能帶來的安全漏洞

#### Podman 安裝過程

##### 更新套件清單及套件

`sudo apk update;sudo apk upgrade`

##### 安裝 podman

`sudo apk add podman`

##### 重開機

`reboot`

##### 掛載 cgroup2

因新版 Podman 改 cgroup 使用 cgroup2
需掛載 cgroup2

確認有無 cgroup2
`mount | grep cgroup`
`grep cgroup /proc/filesystems`

掛載 cgroup2
`sudo mount -t cgroup2 none /sys/fs/cgroup`
`sudo mount -t類型 cgroup2 掛載的設備(無) 掛載的目錄`

##### 檢視相關程序及測試

`ps aux | grep -v grep | grep podman`
顯示運行中程序的資訊並抓取 podman 相關程序
因 podman 不使用 daemon
這裡應抓不到資訊
 - a：all
 - u：該使用者啟動的 process
 - x：含其他系統中的 process 如各 daemon

`sudo podman run quay.io/podman/hello`
啟動測試用 Pod

##### 檢視 pod

顯示已建立的 Pod
`sudo podman ps -a`

刪除 Pod
`sudo podman rm <Pod 的 ID>`