import pandas as pd
import streamlit as st
from pickle import load

from vars import DATA_PREPARED, MODEL_WEIGHTS


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PREPARED)


def data_statistics(data: pd.DataFrame) -> pd.DataFrame:
    return data.describe().T


def load_model_and_predict(data: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    with open(MODEL_WEIGHTS, 'rb') as file:
        model = load(file)

    prediction = model.predict(data)[0]
    prediction_proba = model.predict_proba(data)[0]

    encode_prediction = {
        0: 'Вероятнее клиент не откликнется на предложение банка',
        1: 'Вероятнее клиент откликнется на предложение банка',
    }
    encode_prediction_proba = {
        0: 'Вероятность отклика',
        1: "Вероятность отсутствия отклика",
    }

    prediction_data = {}
    for key, value in encode_prediction_proba.items():
        prediction_data.update({value: prediction_proba[key]})

    prediction_df = pd.DataFrame(prediction_data, index=[0])
    prediction = encode_prediction[prediction]

    return prediction, prediction_df


def get_predict(*, columns_order: list, input_data: dict) -> tuple[str, pd.DataFrame]:
    rules = {
        'gender': {'Женский': 0, 'Мужской': 1},
        'socstatus_work_fl': {'Работает': 1, 'Не работает': 0},
        'socstatus_pens_fl': {'Пенсионер': 1, 'Не пенсионер': 0},
        'fl_presence_fl': {'Есть': 1, 'Нет': 0},
    }

    data = {k.upper(): (rules[k][v] if k in rules else v) for k, v in input_data.items()}
    data = pd.DataFrame(data, index=[0])
    prediction, prediction_df = load_model_and_predict(data)
    return prediction, prediction_df
