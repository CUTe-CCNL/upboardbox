### Alpine

#### Alpine 特色

Alpine Linux 相當輕量化，重視安全性、簡潔、及資源效率
預設安裝的套件包較少，方便於客製化以建立服務

#### Alpine 安裝設定

首次進入 Alpine 時需登入 root（無密碼）進行後續設定

![image](https://imgur.com/M7oQZho.png)

##### 開始安裝

使用 `setup-alpine` 指令開始安裝並設定 Alpine
![image](https://imgur.com/kWq62La.png)

##### 選擇鍵盤配置

不同鍵盤配置依語言有不同的變體
範例選擇美式鍵盤 us/us

![image](https://imgur.com/yJVCUhx.png)

##### 設定主機名稱

主機名稱只能包含小寫字母、0-9、'0'、'-'
範例使用 alpine-settest

![image](https://imgur.com/OZt3BPq.png)

##### 設定網路

 - 使用的網路卡：預設使用 eth0
 - IP 設定：預設使用 DHCP
    - 手動設定需輸入 IP、Subnet Mask、Gateway
 - 是否手動設定網路：預設否

若之後有修改需求，可修改設定檔 /etc/network/interfaces

![image](https://imgur.com/HPOD3eo.png)

##### 設定 root 密碼

![image](https://imgur.com/danwDkP.png)

##### 設定時區

範例選擇 Asia / Taipei

![image](https://imgur.com/aYcD6KJ.png)

##### 設定 Proxy


預設 none

![image](https://imgur.com/mh3TIWO.png)

##### 設定網路教時方式

預設 Chrony

![image](https://imgur.com/w0U00Ad.png)

##### 設定 APK 的鏡像站、套件儲存庫

 - (f) 連接最快速的鏡像站
 - (s) 顯示鏡像站的列表
 - \(r) 使用隨機鏡像站
 - (e) 以文字編輯器編輯 repositories（含鏡像站等網址）
 - \(c) 使用社群鏡像站
 - (skip) 略過設定

預設使用 (f)
若之後有修改需求，可修改設定檔 /etc/apk/repositories

預設的設定檔中，社群鏡像站(community repositories)被註解覆蓋。對於非特定用途，建議取消註解來啟用該套件儲存庫

也有許多機構、大學有提供套件儲存庫，可依需求選擇或修改

![image](https://imgur.com/pdH4Zve.png)


##### 設定使用者

 - 是否先新建（root 以外的）使用者？
這裡先建立一使用者 bigred
 - 使用的 SSH 伺服器
使用預設的 openssh

![image](https://imgur.com/48wbMYL.png)


##### 設定硬碟使用

 - 使用哪個硬碟
sda
 - 該硬碟的用途
sys 系統：傳統的硬碟安裝方案
會建立磁碟分區如：/boot、/、swap
 - **是否格式化該硬碟**
y
若是安裝實體電腦的 os 時，應注意硬碟是否含其他資料來決定是否進行格式化

![image](https://imgur.com/eC7qbt3.png)

##### 安裝完成

安裝完成後需重新開機

![image](https://imgur.com/Gh5aVt7.png)


##### 後續設定

**對於非特定用途**，可先下載常用的套件
預設的 Alpine 中有許多常用指令並未安裝，如 sudo
為此，進行下列操作需登入 root

若安裝 Alpine 時未啟用社群套件儲存庫
需先下載文件編輯器將社群庫納入設定檔中

###### 安裝文字編輯器

依習慣可以選擇 vim、nano 等等編輯器
範例使用 nano
`apk add nano`

###### 修改鏡像站的設定檔

把社群庫（community）的註解取消
`nano /etc/apk/repositories`
找到`#http://dl-cdn.alpinelinux.org/alpine/版本/community`
刪掉最前面的 "#" 來取消註解
若預設的設定檔中沒有該行網址
則再補上即可

###### 更新套件清單、現有套件

`apk update;apk upgrade`

###### 安裝常用套件

```bash
apk add tree unzip curl wget zip grep bash procps sudo util-linux-misc dialog go udev
```

###### 建立一使用者
範例使用 bigred

`echo -e "bigred\nbigred" | adduser -s /bin/bash bigred`

###### 給予權限
給予該使用者 bigred 使用 sudo 的權限：加入 wheel 群組
`addgroup bigred wheel`

若想在連續執行重複指令時不需重複輸入密碼，需修改 sudoers 權限設定
`nano /etc/sudoers`
找到 `Allows people in group wheel to run all commands`
並將底下的`% wheel (...)`取消註解
找到 `# Same thing without password`
並將底下的`% wheel ALL (...)`取消註解

###### 設定完成

接下來便可切換至設定好的使用者 bigred 繼續操作
