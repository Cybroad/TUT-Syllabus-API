# syllabus_backend

## 概要
東京工科大学の学外シラバスより時間割コード，単位数諸々を取得し，API化する。  
「単位計算一発くん」などのプロダクションで使用。

## 導入
1. 必要なパッケージをpipを使いインストールすること。  
```
$ pip install -r requirements.txt
```

2. 次にgricornを使って永続起動(デーモン化)させる
```
$ gunicorn -D -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 127.0.0.1:8080
```

3. Nginxでリバースプロキシを組み，実行する
```
$ sudo systemctl start nginx
```
