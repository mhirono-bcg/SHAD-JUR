import numpy as np

# JUR SSデータ格納場所
DATA_PATH = "data/raw/SS元データ_完全版(1万件)_0228_imputed.xlsx"

# 列名の対応
COLS_TO_MAP = {
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

# 除外する回答者属性
ATTR_TO_REMOVE = {
    "Bachelor's degree student (e.g. BA or BS)",
    "Master's degree student (excluding MBA)",
    "Exchange student (e.g. study abroad or summer school)",
    "MBA student",
    "Associate degree student (e.g. AA or AS)",
}

# 定員の分割用パラメータ
CAPACITY_BIN = [0, 999, 1999, np.Inf]
CAPACITY_LABEL = ["小規模", "中規模", "大規模"]

# Student Survey質問の英訳対応リスト
QUESTIONS_TO_MAP = {
    "q01_interact": "q01_教員との交流",
    "q02_collaborative_learning": "q02_協働学習",
    "q03_critical_thinking": "q03_クリティカル・シンキング",
    "q04_making_connections": "q04_学びの関連付け",
    "q05_applying_learning": "q05_社会との接続",
    "q06_challenge": "q06_挑戦／やりがい",
    "q07_recommend": "q07_他者への推奨",
    "q08_suggest": "q08_大学運営への提案機会",
    "q09_suggest_act": "q09_提案へのフィードバック",
    "q10_confidence": "q10_自信の獲得",
    "q11_community": "q11_参画意識",
    "q12_select_again_future": "q12_自己への推奨",
    "q13_your_development": "q13_成長実感",
    "q14_global_development": "q14_グローバル人材育成",
    "q15_flexible_curricula": "q15_カリキュラム改善",
    "q16_supportive_environment": "q16_副専攻",
}
