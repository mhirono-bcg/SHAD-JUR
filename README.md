## ディレクトリ構成

```
├── README.md          <- XXX
│
├── data
│   ├── interim        <- XXX
│   ├── processed      <- XXX
│   └── raw            <- XXX
│
├── tests              <- XXX
│
├── logs               <- XXX
│
├── references         <- XXX
│
├── environment.yml    <- XXX
│
├── setup.py           <- XXX
│
└── src
    ├── data           <- XXX
    └── visualize      <- XXX
```

---

## 仮想環境再現方法

### 仮想環境の新規作成
* ルートディレクトリから下記コマンドをターミナルに入力し、仮想環境をセットアップ
  
  ```conda env create -f environment.yml```

* 同様に下記コマンドをターミナルに入力し、`src`内のカスタムパッケージをインストール

   ```pip install -e .```

※ 上記コマンドにより、どのスクリプト・ノートブックからも`import src`あるいは`import src.xxx`が可能となる

### 仮想環境の更新

* 同様に下記コマンドをターミナルにて入力し、 仮想環境をアップデート 

```conda env update -f environment.yml```

※ 新しいパッケージを追加する場合は、`environment.yml`をマニュアルにて更新することを推奨。`conda env export --from-history`を参照

---

## パイプラインの実行

### アウトプットの取得

* 下記コマンドをルートディレクトリにて実行尾

```
bash run_all.sh
```
＿＿＿＿＿＿＿＿＿＿＿
