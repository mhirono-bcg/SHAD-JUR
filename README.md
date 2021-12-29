## 1. ディレクトリ構成（各種設定ファイルは割愛）

```
├── data
│   └── raw            <- JUR Student Surveyデータの格納場所
│
├── deliverables       <- アウトプットである各種図表の格納場所
│
├── logs               <- スクリプト実行時のログ格納場所
│
├── references         <- お見積りや各種提供資料の格納場所
│
├── src
│   ├── constants.py   <- パスやカラム名などの定数およびログの設定を記載; 特にデータ差し替え時はパス名を変更
│   ├── core.py        <- アプリケーションのエントリポイント
│   └── jur.py         <- JURクラスを定義し、クリーニングや図表作成をメソッドとして記載
│
├── environment.yml    <- 仮想環境のスペック
├── README.md          <- 本アプリケーションのフォルダ構成や利用方法を記載
├── main.py            <- 動作確認用のスクリプト
└── setup.py           <- スクリプトインターフェースへの登録を実行

```

---

## 2. セットアップ

### 2-1. ANACONDAのインストール

ローカルマシンにANACONDAがインストールされていない場合は、[公式HP](https://www.anaconda.com/products/individual)からANACONDAをインストールしてください

参考：[Windows版Anacondaのインストール](https://www.python.jp/install/anaconda/windows/install.html)

### 2-2. 統合開発環境 -IDE のインストール（オプション）

アプリケーションの運用・保守が容易となるため、必要に応じてIDEのインストールを推奨します

* [Pycharm](https://www.jetbrains.com/pycharm/)
* [VS Code](https://code.visualstudio.com/)

### 2-3. 仮想環境の作成
ルートディレクトリから下記コマンドをターミナルに入力し、仮想環境をセットアップ
  
  ```conda env create -f environment.yml```

### 2-4. 仮想環境のアクティブ化
同様にして下記コマンドをターミナルに入力し、仮想環境をアクティブ化

```conda activate SHAD-JUR```

### 2-5. Pythonコマンドの登録
同様にして下記コマンドをターミナルに入力し、`generate_jur_ss_outputs`コマンドを実行できるようにします

```pip install -e .```

---

## 3. 実行

### 3-1. データの確認
`../SHAD-JUR/data/raw`に対象となるJUR Student Surveyデータが格納されているか確認する

### 3-2. パスの確認
`../SHAD-JUR/src/constants.py`のパスが正しく3-1.のデータを指しているか確認する

### 3-3. コマンドラインの実行
ルートディレクトリから下記コマンドをターミナルに入力し、各種アウトプットを作成

```generate_jur_ss_outputs```

### 3-4. アウトプットの確認
`../SHAD-JUR/deliverables`に最新のアウトプットが格納されているか確認する