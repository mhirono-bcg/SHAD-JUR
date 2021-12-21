## Module Import
import numpy as np
import pandas as pd

## Data Import
ss_df = pd.read_excel("../data/raw/SS元データ_完全版(1万件)_0228_imputed.xlsx")

## Data Preprocessing
## Flat-linerの回答を抽出するために分散を利用
## Flat-linerの回答は分散がゼロという特徴を利用


# rename the columns
col_to_map = {
    "Panel": "panel_name",
    "resonse_id": "response_id",
    "response time (sec)": "survey_response_time_sec",
    "uni_code": "university_code",
    "wur_id": "WUR_code",
    "DJM": "DJM_code",
    "uni_name": "university_name",
    "div": "institutional_classification",
    "type": "institutional_type",
    "area": "institutional_area",
    "prefecture": "institutional_prefecture",
    "selectivity": "institutional_selectivity",
    "quota": "institutional_capacity",
    "course_delivery": "method_course_delivery",
    "year_of_birth": "birth_year_month",
    "gender": "gender",
    "location": "in_out_bound_type",
    "status": "student_title",
    "grade_now": "current_grade",
    "year_in": "admission_year",
    "grade_in": "admission_grade",
    "subject": "student_major",
    "primary_reason": "admission_primary_reason",
    "secondary_reason": "admission_secondary_reason",
    "q_interact": "q01_interact",
    "q_collaborative_learning": "q02_collaborative_learning",
    "q_critical_thinking": "q03_critical_thinking",
    "q_making_connections": "q04_making_connections",
    "q_applying_learnings": "q05_applying_learning",
    "q_challenge": "q06_challenge",
    "q_recommend": "q07_recommend",
    "q_suggest": "q08_suggest",
    "q_suggest_act": "q09_suggest_act",
    "q_confidence": "q10_confidence",
    "q_community": "q11_community",
    "no.12通っている大学を選びますか": "q12_select_again_future",
    "no.13自分が成長したと思いますか": "q13_your_development",
    "no.14グローバル人材の育成に力を入れていると思いますか": "q14_global_development",
    "no.15社会の変化に対応したカリキュラムになっていると思いますか": "q15_flexible_curricula",
    "no.16専攻以外の知識や経験を積み重ねていくことに対する支援がありますか": "q16_supportive_environment",
    "no.21満足": "comment_satisfaction",
    "no.22改善": "comment_improvement",
}

# このマッピングはテストが必要か？
# 加えて、effective survey sizeの数を検証する
capacity_bin = [0, 999, 1999, np.Inf]
capacity_label = ["小規模", "中規模", "大規模"]

(
    ss_df.rename(columns=col_to_map)
    .loc[:, col_to_map.values()]
    .assign(
        q_flat_answer_flag=lambda df: df.loc[:, df.columns.str.startswith("q_")].apply(
            np.var, axis=1
        )
        == 0
    )
    .assign(
        institutional_size=lambda df: pd.cut(
            df["institutional_capacity"], bins=capacity_bin, labels=capacity_label
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
)
