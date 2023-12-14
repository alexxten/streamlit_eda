import pandas as pd
import streamlit as st
from pickle import load

from vars import DATA_PREPARED, MODEL_WEIGHTS


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PREPARED)


def data_statistics(data: pd.DataFrame) -> pd.DataFrame:
    return data.describe().T


def load_model_and_predict(data: pd.DataFrame) -> tuple[int, dict]:
    with open(MODEL_WEIGHTS, 'rb') as file:
        model = load(file)
    prediction = model.predict(data)[0]
    prediction_proba = model.predict_proba(data)[0]

    encode_prediction = {
        1: 'Клиент откликнется с вероятностью',
        0: 'Клиент не откликнется с вероятностью',
    }
    encode_prediction_proba = {
        encode_prediction[i]: prediction_proba[i] for i in model.classes_
    }

    return prediction, encode_prediction_proba


def get_predict(*, columns_order: list, input_data: dict) -> tuple[int, dict]:
    rules = {
        'gender': {'Женский': 0, 'Мужской': 1},
        'socstatus_work_fl': {'Работает': 1, 'Не работает': 0},
        'socstatus_pens_fl': {'Пенсионер': 1, 'Не пенсионер': 0},
        'fl_presence_fl': {'Есть': 1, 'Нет': 0},
    }

    data = {k.upper(): (rules[k][v] if k in rules else v) for k, v in input_data.items()}
    data = {c: data[c] for c in columns_order}
    data = pd.DataFrame(data, index=[0])
    prediction, proba = load_model_and_predict(data)
    return prediction, proba
