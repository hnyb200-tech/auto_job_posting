# 求人原稿ドラフト自動生成システム

## 開発の経緯  
1本の原稿の作成に8時間を要しており、効率化できないかと考えたことがきっかけ。  
文字起こしはLLMで的確なプロントを送れば100％自動化することができたので、  
文字起こしの情報を基に、原稿全体のドラフトを生成できるシステムを作成することにした。

## 結果
1原稿の作成時間を約2時間に短縮（約75％減）  
取材内容を基に大まかな原稿ドラフトを組めるようになったので、  
時短しつつもユーザー側はよりクリエイティブな部分に時間を割くことができるようになった。  

## 生成対象となる原稿の大まかな構成
1. 企業からのメッセージ
2. 仕事内容
3. アピールポイント（クライアント企業側が11項目から3個選択する　※システム内ではAP／当システムのAPのリスト内を参照）

## 当システムの特長
フロントエンドとバックエンドを分離することにより、プロンプトの管理&更新を行いやすい仕様にしている。  
フロントエンドに関してはstreamlitを採用しており、直感的でスピード感のある実装が可能になっている。  
バックエンド側のプロンプトは適宜更新できるので、当媒体の大まかな方向性からずれることはない。  
LLMが大きな役割を担っている。当システムではgeminiだが、sambanovaをモジュールとして外部でLLMの比較検証も行っている。  
※当システムではテンプレのデータを全てダミーテキストに差し替えています。

##  仮想環境構築を想定した運用手順  
リポジトリのクローン  
git clone: [https://github.com/hnyb200-tech/auto_job_posting.git](https://github.com/あなたのユーザー名/リポジトリ名.git)

cd auto_job_posting

---

### 1. 仮想環境を構築
**仮想環境の作成:**
```bash
python -m venv venv
```

**仮想環境の有効化:**
* **Windows の場合:**
  ```cmd
  venv\Scripts\activate
  ```
* **Mac/Linux の場合:**
  ```bash
  source venv/bin/activate
  ```

### 2. 必要なパッケージのインストール
アプリの動作に必要なモジュールをインポート。

```bash
pip install streamlit google-generativeai python-dotenv
```
> **※補足:** もし `requirements.txt` を作成している場合は、上記の代わりに以下のコマンドを実行。
> ```bash
> pip install -r requirements.txt
> ```

### 3. APIキーの設定 (Secrets)
このアプリは Streamlit の Secrets 機能を使用して API キーを安全に管理。

1. プロジェクトのルート（`app.py` と同じ階層）に `.streamlit` という名前のフォルダを作成。
2. そのフォルダの中に `secrets.toml` というファイルを作成。
3. `secrets.toml` の中に、取得した Gemini API キーを以下のように記述して保存。

**.streamlit/secrets.toml の中身:**
```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

> **※確認:**
>  `.gitignore` ファイルに `.streamlit/` を追加

### 4. アプリケーションの起動
以下のコマンドでアプリを起動します。

```bash
streamlit run app.py
```
