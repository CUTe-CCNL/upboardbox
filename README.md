# 2024年電腦基礎概論📝

# 首頁

## 簡介
本專案主要以 `Podman` 建立 Application Container 運行服務為主題，逐步增加範圍進行教學與介紹。除機制講解以外，也提供範例的安裝過程教學供練習參考。

## 安裝及建立服務操作流程


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

Container 相當於以一個程序作為一個虛擬電腦。通常多在一個 Container 建立一項服務，該 Container 包含運行該服務必須的資料、環境、及相關的函式庫等等。以此增加管理服務的方便性、安全性、及機動性。

### Container 的特色

#### 管理方便

透過 Container 架設服務，可以避免修改本機系統。減少系統上日以俱增且難以控管的變化，增加管理時的方便性與資源使用率

#### 安全性

為每個服務建立 Container 可以對網路連接加以控管，每個 Container 也僅開啟該服務所必須的 Port。如此可以避免多個 Port 的設定麻煩與可能帶來的安全問題

#### 機動性

只要留有對應的 Dockerfile 及相關設定檔，每次建立該 Container 僅需再下少許指令，也可依需求快速的增減與修改服務所需要的資源

### Container 的組成

![Container_Layer](https://imgur.com/wCmxGTK.png)

#### Namespace

Container 與一般虛擬電腦不同之處之一，是依賴於本機的 OS Kernel，同時與其他 Container 共用而非運行自己的 Kernel。然而為此也需要有區隔各個 Container 所使用的內核資源的機制

#### Overlay

Overlay 文件系統是一種特殊的文件系統，用於支持對文件的修改和讀取操作，而不改變底層的物理文件。這對於 container 非常重要，因為它允許容器在不影響基礎主機系統的情況下，獨立讀取、修改其內部文件系統。在 podman 等 container 技術中，Overlay 文件系統使得容器在執行應用程序時，可以擁有自己的文件系統視圖，同時共享主機的 OS Kernel。

#### Cgroup

group 是 Linux 內核的一個特性，它可以限制、記賬和隔離進程群體（process groups）所使用的物理資源（如 CPU、記憶體、I/O 等）。在容器化中，Cgroup 用於確保每個 container 都在其分配的資源限制內運行，從而防止任何一個 container 使用過多的資源而影響到系統或其他 container 的運行。這對於維持多個 container 在同一個主機上的資源分配和隔離至關重要。

#### Chroot

Chroot 是一種將執行環境改變為特定目錄的操作。這允許程序與其子程序在這個目錄下運行，就像它是系統的根目錄一樣。在 container 技術中，Chroot 用於將 container 的根文件系統隔離開，使得 container 內的程序只能訪問到指定的文件系統範圍，從而增加了系統的安全性。Chroot 是建立 container 隔離環境的一個基本步驟，但它並不提供強隔離，通常會與其他技術（如 Namespace 和 Cgroup）結合使用以增強隔離效果。

### Container 的建立

![Container_Build](https://imgur.com/NpXkQBE.png)

1. **建立（Build）**:
   - 首先你需要一個 **Dockerfile**，它包含了建立 Docker 映像檔（image）所需的指令。
   - 使用 `podman build` 命令根據 Dockerfile 來建立一個新的映像檔。

2. **運行（Run）**:
   - 有了映像檔後，你可以使用 `podman run` 命令來創建一個新的container 實例。
   - 這個 container 將基於你所建立的映像檔運行。

3. **標籤（Tag）**:
   - 你可以對建立的映像檔進行標籤，使用 `podman tag` 命令給映像檔加上有意義的名字和標籤。

4. **提交（Commit）**:
   - 對運行中的 container 做出變更後，可以使用 `podman commit` 命令將 container 的狀態保存為新的映像檔。

5. **推送（Push）**:
   - 使用 `podman push` 命令將映像檔推送到 Docker 註冊中心（registry），比如 Docker Hub，讓其他人可以下載和使用你的映像檔。

6. **拉取（Pull）**:
   - 可以使用 `podman pull` 命令從 Docker 註冊中心下載映像檔。

7. **儲存（Save）**與**加載（Load）**:
   - 使用 `podman save` 命令將映像檔儲存為 tar 檔案，以進行備份或轉移。
   - 使用 `podman load` 命令從 tar 檔案加載映像檔。

8. **管理 container**:
   - 使用 `podman start`、`podman stop` 和 `podman restart` 命令來管理 container 的運行狀態。


## Podman

>Podman is an open source container, pod, and container image management engine. Podman makes it easy to find, run, build, and share containers.
>-- Podman Official Web

Podman 的設計思路是去中心化和保安，這為需要高安全性和多用戶環境的組織提供了一個強大的工具。它的無 daemon 架構和對非 root 用戶的支持使其成為企業和雲環境中的一個受歡迎的選擇。

![imgur](https://imgur.com/uPx2eDb.png)

相比 Docker 在建立並運行 Container 時，
會開啟 dockerd 以及 containerd 兩個 daemon；Podman 並不會啟動背景程序，稱為 Daemonless，如此可避免運行 Daemon 可能帶來的安全漏洞。

