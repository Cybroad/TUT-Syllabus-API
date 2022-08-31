# syllabus_backend

## 概要

東京工科大学の学外シラバスより時間割コード，単位数諸々を取得し，API 化する。  
「単位計算一発くん」などのプロダクションで使用。

## ファイル構造

```
syllabus_backend/
┣ lecture_Data/ … 講義データのjsonファイル(単位数含む)
┣ timeTableId_Data/ … 時間割データのjsonファイル
┣ getData.py … 講義データと時間割データを取得するコアファイル(基本的にはここをいじる)
┣ main.py … 手動取得ツール
┣ server.py … APIサーバー(gunicornで立ち上げるファイル(server:app))
┣ requirements.txt … 必要なライブラリ
┣ settings.py … 設定ファイル
┣ README.md … このファイル
```

## 導入

1. 必要なパッケージを pip を使いインストールすること。

```
$ pip install -r requirements.txt
```

2. 次に gricorn を使って永続起動(デーモン化)させる

```
$ gunicorn -D -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 127.0.0.1:8080
```

3. Nginx でリバースプロキシを組み，実行する

```
$ sudo systemctl start nginx
```
