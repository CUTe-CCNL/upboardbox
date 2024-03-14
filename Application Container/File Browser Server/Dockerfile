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
# 將使用者切換為 app
USER app
# 工作目錄在 /opt/app
WORKDIR /opt/app

# entrypoint 檔案含 Container 被建立時會被執行的指令等
ENTRYPOINT [ "/opt/app/entrypoint" ]