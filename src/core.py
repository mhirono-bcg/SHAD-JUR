import click
from src.jur import JUR
from src.constants import (
    ATTR_TO_REMOVE,
    CAPACITY_BIN,
    CAPACITY_LABEL,
    COLS_TO_MAP,
    DATA_PATH,
    QUESTIONS_TO_MAP,
)


@click.command()
def cli():
    """ツールのエントリポイント"""

    # JUR SSデータベースのロード
    jur = JUR(data_path=DATA_PATH)
    db = jur.load_jur_db()

    # JUR SSデータベースのクリーニング
    cleaned_db = jur.clean_jur_db(
        db,
        cols_to_map=COLS_TO_MAP,
        capacity_bins=CAPACITY_BIN,
        capacity_labels=CAPACITY_LABEL,
        attr_to_remove=ATTR_TO_REMOVE,
    )

    # クリーニング済みのJUR SSデータベースの作図用に加工
    processed_db_all_median = jur.update_jur_db_to_plot(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="median",
        only_effective_survey=False,
    )

    processed_db_all_mean = jur.update_jur_db_to_plot(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="mean",
        only_effective_survey=False,
    )

    processed_db_effective_median = jur.update_jur_db_to_plot(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="median",
        only_effective_survey=True,
    )

    processed_db_effective_mean = jur.update_jur_db_to_plot(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="mean",
        only_effective_survey=True,
    )

    # output 1~4
    jur.create_boxplot(processed_db_all_median, file_name="アウトプット1_規模別1枚シート_全参加大学_中央値")
    jur.create_boxplot(processed_db_all_mean, file_name="アウトプット2_規模別1枚シート_全参加大学_平均値")
    jur.create_boxplot(
        processed_db_effective_median, file_name="アウトプット3_規模別1枚シート_有効回答到達大学のみ_中央値"
    )
    jur.create_boxplot(
        processed_db_effective_mean, file_name="アウトプット4_規模別1枚シート_有効回答到達大学のみ_平均値"
    )

    # output 5~6
    jur.create_boxplot_values(
        processed_db_all_median, file_name="アウトプット5_1_箱ひげ図の値_全参加大学_中央値"
    )
    jur.create_boxplot_values(
        processed_db_all_mean, file_name="アウトプット5_2_箱ひげ図の値_全参加大学_平均値"
    )
    jur.create_boxplot_values(
        processed_db_effective_median, file_name="アウトプット6_1_箱ひげ図の値_有効回答到達大学のみ_中央値"
    )
    jur.create_boxplot_values(
        processed_db_effective_mean, file_name="アウトプット6_2_箱ひげ図の値_有効回答到達大学のみ_平均値"
    )

    # output 7~10
    jur.summarize_score_question(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="median",
        only_effective_survey=False,
        file_name="アウトプット7_回答者全体_中央値_全参加大学",
    )
    jur.summarize_score_question(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="median",
        only_effective_survey=True,
        file_name="アウトプット8_回答者全体_中央値_有効回答到達大学のみ",
    )
    jur.summarize_score_question(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="mean",
        only_effective_survey=False,
        file_name="アウトプット9_回答者全体_平均値_全参加大学",
    )
    jur.summarize_score_question(
        cleaned_db,
        questions_to_map=QUESTIONS_TO_MAP,
        calc_mode="mean",
        only_effective_survey=True,
        file_name="アウトプット10_回答者全体_平均値_有効回答到達大学のみ",
    )
