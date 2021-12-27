import logging
import os

import japanize_matplotlib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.cbook import boxplot_stats


class JUR:
    def __init__(self, data_path: str = None, data_name: str = None) -> None:
        """JURクラス初期化

        Args:
            data_path (str, optional): JURデータが格納されているディレクトリ名
            data_name (str, optional): JURデータのファイル名
        """
        self.data_path = data_path
        self.data_name = os.path.splitext(data_name)[0]

    def load_jur_db(self) -> pd.DataFrame:
        """JURデータの読み込み
        xlsxファイルをデフォルトで読み込む
        もしxlsxファイルがない場合、エラーを返す

        Returns:
            pd.DataFrame: JUR Student Surveyデータ
        """
        xlsx_db = os.path.join(self.data_path, self.data_name + ".xlsx")

        if os.path.exists(xlsx_db):
            logging.info(f"JUR SSデータ読み込み: {xlsx_db}")
            jur_db = pd.read_excel(xlsx_db)

        else:
            logging.error("ERROR: JUR SSデータが存在するか確認してください")
            return None

        return jur_db

    def clean_jur_db(
        self,
        jur_db: pd.DataFrame,
        cols_to_map: dict,
        capacity_bins: list,
        capacity_labels: list,
        attr_to_remove: list,
    ) -> pd.DataFrame:
        """JURデータのクリーニング

        Args:
            jur_db (pd.DataFrame): JUR Student Surveyデータ
            cols_to_map (dict): 旧カラム名と新カラム名の辞書
            capacity_bins (list): 大学定員数の境界値のリスト
            capacity_labels (list): 大学定員数に基づく規模のラベルリスト
            attr_to_remove (list): 除外する学生の属性リスト

        Returns:
            pd.DataFrame: クリーニング済みのJUR Student Surveyデータ
        """

        # Flat-liner算出ロジックは、全て同じ回答の場合、分散がゼロとなる性質を利用
        jur_db_cleaned = (
            jur_db.rename(columns=cols_to_map)
            .loc[:, cols_to_map.values()]
            # 全て同じ回答の場合、分散がゼロである性質を利用
            .assign(
                flat_liner_flag=lambda df: df.loc[
                    :, df.columns.str.startswith("q_")
                ].apply(np.var, axis=1)
                == 0
            )
            .assign(
                institutional_size=lambda df: pd.cut(
                    df["institutional_capacity"],
                    bins=capacity_bins,
                    labels=capacity_labels,
                )
            )
            .assign(
                effective_survey_size=lambda df: df.groupby("university_code")[
                    "response_id"
                ].transform("nunique")
            )
            .assign(
                institutional_type_size=lambda df: np.where(
                    df["institutional_type"].isin(["国立", "公立"]),
                    df["institutional_type"],
                    df[["institutional_type", "institutional_size"]].apply(
                        lambda x: "・".join(x), axis=1
                    ),
                )
            )
            .query("student_title in @attr_to_remove")
            .query("flat_liner_flag == False")
        )

        return jur_db_cleaned

    def update_jur_db_to_plot(
        self,
        jur_db: pd.DataFrame,
        questions_to_map: dict,
        calc_mode: str,
        only_effective_survey: bool = False,
    ) -> pd.DataFrame:
        """図表作成用のデータに加工

        Args:
            jur_db (pd.DataFrame): クリーニング済みJUR Student Surveyデータ
            questions_to_map (dict): 図表用の質問和英対応辞書
            calc_mode (str): 各大学の回答集約方法（meanかmedianを選択可能）
            only_effective_survey (bool, optional): 有効回答数に到達した大学のみを対象とするか否か
        """

        cols_to_select = [
            "response_id",
            "university_code",
            "institutional_type_size",
        ] + list(questions_to_map.keys())

        if only_effective_survey:
            jur_db = jur_db.query("effective_survey_size >= 50")

        db_to_plot = (
            jur_db.loc[:, cols_to_select]
            .rename(columns=questions_to_map)
            .assign(
                category_size=lambda df: df.groupby("institutional_type_size")[
                    "university_code"
                ].transform("nunique")
            )
            .assign(
                institutional_type_size=lambda df: df.apply(
                    lambda x: x["institutional_type_size"]
                    + " (n = "
                    + str(x["category_size"])
                    + ")",
                    axis=1,
                )
            )
            .drop(["response_id", "category_size"], axis=1)
        )

        if calc_mode == "median":
            db_to_plot = (
                db_to_plot.groupby(["institutional_type_size", "university_code"])
                .median()
                .reset_index()
                .melt(
                    id_vars=["institutional_type_size", "university_code"],
                    var_name="questions",
                    value_name="rating",
                )
            )

        elif calc_mode == "mean":
            db_to_plot = (
                db_to_plot.groupby(["institutional_type_size", "university_code"])
                .mean()
                .reset_index()
                .melt(
                    id_vars=["institutional_type_size", "university_code"],
                    var_name="questions",
                    value_name="rating",
                )
            )

        return db_to_plot

    def create_boxplot(self, jur_db: pd.DataFrame, file_name: str):
        """箱ひげ図の作成

        Args:
            jur_db (pd.DataFrame): 作図用に加工したJUR Student Surveyデータ
            file_name (str): プロット保存時のファイル名
        """

        matplotlib.style.use("tableau-colorblind10")
        plot_to_show = sns.FacetGrid(
            jur_db, col="questions", size=5, aspect=1.5, col_wrap=4
        )
        plot_to_show.map(
            sns.boxplot, "rating", "institutional_type_size", showfliers=False
        )

        for index in plot_to_show.axes:
            index.axvline(5, ls="--", color="red")

        plot_to_show.set(xlabel=None)
        plot_to_show.set(ylabel=None)

        plt.savefig(f"../deliverables/{file_name}.pdf")

    def create_boxplot_values(
        self, jur_db: pd.DataFrame, file_name: str
    ) -> pd.DataFrame:
        """箱ひげ図の各統計量算出・保存

        Args:
            jur_db (pd.DataFrame): 作図用に加工したJUR Student Surveyデータ
            file_name (str): データフレーム保存時のファイル名

        Returns:
            pd.DataFrame: 設問・設置区分ごとの箱ひげ図の統計量データフレーム
        """
        output_dict = {
            "設問番号_内容": [],
            "設置区分・規模": [],
            "ヒゲの最小値": [],
            "箱の最小値": [],
            "中央値": [],
            "箱の最大値": [],
            "ヒゲの最大値": [],
            "平均値": [],
        }

        for q in jur_db["questions"].unique():
            for i in jur_db["institutional_type_size"].unique():
                output_dict["設問番号_内容"].append(q)
                output_dict["設置区分・規模"].append(i)

                jur_db_filtered = jur_db.query("questions == @q").query(
                    "institutional_type_size == @i"
                )
                boxplot_stats = boxplot_stats(jur_db_filtered["rating"])[0]

                output_dict["ヒゲの最小値"].append(boxplot_stats["whislo"])
                output_dict["箱の最小値"].append(boxplot_stats["q1"])
                output_dict["中央値"].append(boxplot_stats["med"])
                output_dict["箱の最大値"].append(boxplot_stats["q3"])
                output_dict["ヒゲの最大値"].append(boxplot_stats["whishi"])
                output_dict["平均値"].append(boxplot_stats["mean"])

                output_tbl = pd.DataFrame(output_dict)

        output_tbl.to_csv(
            f"../deliverables/{file_name}.csv", index=False, encoding="utf-8_sig"
        )

    def summarize_score_question(
        self,
        jur_db: pd.DataFrame,
        questions_to_map: dict,
        calc_mode: str,
        file_name: str,
    ) -> pd.DataFrame:
        """各質問の回答スコアの集約値を算出

        Args:
            jur_db (pd.DataFrame): クリーニング済みJUR Student Surveyデータ
            questions_to_map (dict): 図表用の質問和英対応辞書
            calc_mode (str): 各大学の回答集約方法（meanかmedianを選択可能）
            file_name (str): データフレーム保存時のファイル名

        Returns:
            pd.DataFrame: 各質問におけるスコアの平均値/中央値のデータフレーム
        """

        cols_to_select = ["response_id"] + list(questions_to_map.keys())

        res = (
            jur_db.loc[:, cols_to_select]
            .rename(columns=questions_to_map)
            .melt(id_vars="response_id", var_name="questions", value_name="rating")
        )

        if calc_mode == "median":
            res = (
                res.groupby("questions")["rating"]
                .median()
                .reset_index()
                .rename(columns={"questions": "質問項目", "rating": "中央値"})
            )

        elif calc_mode == "mean":
            res = (
                res.groupby("questions")["rating"]
                .mean()
                .reset_index()
                .rename(columns={"questions": "質問項目", "rating": "中央値"})
            )

        res.to_csv(
            f"../deliverables/{file_name}.csv", index=False, encoding="utf-8_sig"
        )
