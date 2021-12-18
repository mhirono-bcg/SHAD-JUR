# SHAD-JUR

---

## ディレクトリ構成

```
├── README.md          <- XXX
│
├── data
│   ├── interim        <- XXX
│   ├── processed      <- XXX
│   └── raw            <- XXX
│
├── logs               <- XXX
│
├── references         <- XXX
│
├── environment.yml    <- XXX
│
├── setup.py           <- XXX
│
└── src                <- 本プロジェクトにおけるソースコード
    │
    ├── __init__.py    <- XXX
    │
    ├── config         <- XXX
    │
    ├── data           <- XXX
    │
    ├── visualize      <- XXX
    │
    └── analysis       <- XXX
```

---

## 仮想環境再現方法


## Initial setup
* To create the conda env (e.g. initial creation of the env), run:
  
  ```conda env create -f environment.yml```

* To install the custom packages in `src` run:

   ```pip install -e .```

This enables you to `import src` or `import src.xx` in any script or notebook.  
The package is dynamically linked to the `src` folder so the *install* command only needs to be run once.

## Updating during development

* To update the conda env (e.g. when environment.yml was updated after merging someone else's branch), run:
  
  ```conda env update -f environment.yml```

* To add a package in environment.yml, manually edit the yml file. Do NOT use conda env export command, as the result will include OS-dependent low level packages. conda env export --from-history can be useful as a reference.



---

# Running the pipeline

## Data preparation

Run the following script from the root directory:

```
bash run_all.sh
```
＿＿＿＿＿＿＿＿＿＿＿
