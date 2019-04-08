# MQTT_over_TCP-for-SIM7000-in-Python
A python method for sending MQTT through TCP from SIM7000 using NBIOT


## TL;DR
這是一個因為SIM7000(NBIOT) 原生MQTT功能會當機才產生的小專案
在做的事很簡單，就是將MQTT的各個步驟拆開，並且組成封包
並透過SIM7000的其他指令來傳輸(原生TCP指令)
所以會變成:
原本的MQTT訊息 -> 打包好的封包 -> 透過NBIOT模組發送 -> 到大平台接收

## TODO
我其實只寫完了我會用到的部分
好像還有很多要做
就先放TODO吧
- [ ] 自訂使用者/密碼 (目前要自己編碼)
- [ ] 長度16383 Byte以上的封包 ~~如果真的用到 那你是不是弄錯了什麼?~~
- [ ] 自訂參數(QoS/Keepalive/)
- [ ] MQTT訂閱
~~除非用到 回來補的機會不大了~~

## 緣起
會開始寫這個就是因為"應該要對的東西不對" 
而且這方面的資料好像不太多
順便紀錄過程中遇到的各種問題~~還有抱怨~~
提供給想拿NBIOT來做快速Prototype的各位


## 硬體需求

目前這個小專案是提供SIM7000系列的晶片來撰寫
你會需要:

- SIM7000系列模組(我用7000E)
- USB-TTL轉接線
- 你會用的開發版(目前採用Linkit7688)


## 環境需求

開發環境你基本上需要:
- 可以執行Python的系統
- 序列埠軟體(MobaXterm好用)
~~不過我大多時候用Arduino的序列埠小視窗~~


## MQTT說明
MQTT是一種輕量化的通訊協定，同時具備負載性高、頻道制、廣播等等特性。
大略可以分成3個部分:

- Broker
負責管理每個Client的訊息發布與訂閱狀態

- Publisher
發送者，在系統上發布訊息
根據發布的Topic不同 Broker會送到不同的訂閱者手上

- Subscriber 
訂閱者，向Broker訂閱，若是訂閱的頻道有新訊息發布
Broker就會送到該訂閱者手上

![image alt](https:// "title") 圖片下次補

## 指令流程

首先
```
AT+CIPCLOSE   //確認晶片是關閉的

AT+CIPSENDHEX=1 //切換到16進制 我們要輸入Byte

AT+CSTT="nbiot" //遠傳的APN名稱

AT+CIICR  //啟動數據網路

AT+CIFSR  //檢查分配到的IP

AT+CIPSTART="TCP","IP.add.re.ss","port"  //替換掉目標主機的IP port

AT+CIPSEND  //此時會進入輸入模式 以Byte輸入 結尾用1A結束
>msg

//訊息分為兩個部分 connect_pack + publish_pack
//connect_pack目前是固定的 包含MQTT Client ID/Username/Password
//publish_pack則是要發布的頻道以及訊息
//最後都會轉換成Byte模式 所以送出的東西會像 Byte(connect_pack)+Byte(publish_pack)+1A

AT+CIPCLOSE //完成傳輸後關閉連線
```

## 疑難雜症與常用指令

Q:SIM 7000E 沒有反應?
檢查鮑率 我拿到這批預設57600 

檢查SIM卡:
```
AT+CPIN?
+CPIN: READY 
```
READY代表SIM卡沒問題

檢查天線訊號:
```
AT+CSQ
+CSQ: 18,99
```
第一個數字小於14可能就要換地方了



## 補充資料
讓 Raspberry PI 聯網：使用 SIM7000C NB-IoT 模組:
https://frankchang.me/2018/12/18/sim7000c/

MQTT over TCP:
https://www.raviyp.com/embedded/224-mqtt-protocol-tutorial-using-mosquitto-and-cloudmqtt
https://www.raviyp.com/embedded/226-mqtt-protocol-tutorial-using-sim900-sim800-modules-mqtt-over-tcp

NB-IoT SIM7000C调试笔记 01 NB-IoT及GPRS加网测试:
https://blog.csdn.net/iotisan/article/details/78704608

用AT命令建立/调试SIM800C的GPRS连接:
https://blog.csdn.net/aLife2P6/article/details/82704371#fnref:6

SIM7000C在NB模式下的非透传模式的TCPIP:
https://blog.csdn.net/putiputiti/article/details/80661342

## 測試結果
AT+CIPSENDHEX=1

AT+CSTT="nbiot"

AT+CIICR

AT+CIFSR

AT+CIPSTART="TCP","IP.add.re.ss","port"

AT+CIPSEND

AT+CIPCLOSE
