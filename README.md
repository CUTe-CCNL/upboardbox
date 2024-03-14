# 2024年電腦基礎概論📝

# 首頁

本專案主要以 Podman 建立 Application Container 運行服務為主題，逐步增加範圍進行教學與介紹。在學習各 Application Container 範例之前，建議先參考 System Build 相關頁面確認系統架設完成。

- System build

  - [Alpine](https://github.com/CUTe-CCNL/upboardbox/blob/main/System%20Build/Build%20Alpine/README.md)

  - [Podman](https://github.com/CUTe-CCNL/upboardbox/blob/main/System%20Build/Podman/README.md)

- Applicaation container

  - [FileBrowser Server](https://github.com/CUTe-CCNL/upboardbox/blob/main/Application%20Container/File%20Browser%20Server/README.md)

  - [MySQL](https://github.com/CUTe-CCNL/upboardbox/blob/main/Application%20Container/MySQL/README.md)

## 準備工作

使用的系統為 `Alpine Linux`、`Podman`

## Container
### 簡介

Container 相當於以一個程序作為一虛擬電腦。通常多在一 Container 建立一項服務，該 Container 包含運行該服務必須的資料、環境、及相關的函式庫等等。以此增加管理服務的方便性、安全性、及機動性。

### Container 的特色

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
