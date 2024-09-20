# TUT-Syllabus-API
東京工科大学の[学外シラバス](https://kyo-web.teu.ac.jp/campussy)をWebAPIとして提供するプロジェクトです。

Github Actionsを用いて定期実行されるPythonソースファイルにより、学外シラバスのデータ(時間割コード、講義概要など)を取得し、JSON形式で本レポジトリにコミット&プッシュします。
プッシュされたデータは、CloudFlare Pagesを用いて静的JSONファイルとして配信されます。

## API仕様
### エンドポイント
#### 全体検索(GET)
`{時間割コード}`は、一意に講義を特定できる英数字のコードです。(例: `11040C1`)
```
https://tut-syllabus-api.pages.dev/api/v1/all/{時間割コード}.json
```

#### 学部指定検索(GET)
`{時間割コード}`は、一意に講義を特定できる英数字のコードです。(例: `11040C1`)  
`{学部名}`は、学内で広く認知されている略称を使用し指定します。  

以下のリストのいずれかを指定してください。(2024年9月20日時点)  
`["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS", "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]`
```
https://tut-syllabus-api.pages.dev/api/v1/{学部名}/{時間割コード}.json
```

### レスポンス
レスポンスボディにステータスコード等は含めていません。ステータスコードで200が返却された場合は成功です。  
時間割コードに対応するページデータが1対1で返却されます。
#### 成功時
```
{
    "lectureCode": "<時間割コード>"
    "courseName": "<講義名>",
    "lecturer": [
        "<担当教員>"
    ],
    "regularOrIntensive": "<科目種別>"
    "courseType": "<科目区分>",
    "courseStart": "<開講時期>",
    "classPeriod": [
        "<曜日><時限>"
    ],
    "targetDepartment": "<学部名>",
    "targetGrade": [
        "<対象学年>"
    ],
    "numberOfCredits": <単位数>,
    "classroom": [
        "<教室>"
    ],
    "courceDetails": {
        "courseOverview": "<概要>",
        "outcomesMeasuredBy": "<目標>",
        "learningOutcomes": "<到達目標>",
        "teachingMethod": "<授業計画>",
        "notices": "<履修上の注意>",
        "preparatoryStudy": "<事前学習>",
        "gradingGuidelines": "<成績評価>",
        "textbook": "<教科書>",
        "referenceMaterials": "<参考書>",
        "courseSchedule": "",
        "courseDataUpdatedAt": "<講義詳細更新日>"
    },
    "updateAt": "<レコード更新日>"
}
```

> [!NOTE]
> 404 Not Foundが返却された場合は、時間割コードが存在しないか、指定された学部名が存在しない可能性があります。
> また、その他のエラーはCloudFlare Pagesのエラーページが返却されます。

## データ更新
データの更新は、Github Actionsにより、3ヶ月毎のJST 15:40 (UTC 6:40)に行われます。

## 貢献
バグの報告や機能の提案、コードの改善など、どんな形でも貢献を歓迎します。

## ライセンス
MITライセンスです。詳細は[LICENSE](LICENSE)を参照してください。

## 利用にあたって
本プロジェクトは非公式のものであり、片柳学園および東京工科大学とは一切関係ありません。  
本APIを利用したことによるいかなる損害も、本プロジェクトの作成・運営者は責任を負いません。  
また、本APIを利用した派生物の責任も利用者が負うものとします。

### 東京工科大学または片柳学園関係者の方へ
本APIは、システムに負荷がかからない間隔で学外シラバスをスクレイピングし、収集したデータを使用しております。  
万一、本APIの運用に問題がある場合は、ご連絡いただければ対応いたします。
