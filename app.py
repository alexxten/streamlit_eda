import time
import os

import streamlit as st
import pandas as pd
from PIL import Image
from utils.utils import load_data, data_statistics, get_predict
from utils.visualization import histplot, target_countplot
from vars import STATIC


def preload_content() -> dict:
    clients_img = Image.open(os.path.join(STATIC, 'clients.jpg'))
    corr_img = Image.open(os.path.join(STATIC, 'corr.png'))
    feature_imp_img = Image.open(os.path.join(STATIC, 'feature_imp.png'))
    return {
        'main_img': clients_img,
        'corr': corr_img,
        'feature_imp_img': feature_imp_img,
    }


# def highlight_weighs(s):
#     """ generate colors to highlight weights """
#
#     return ['background-color: #E6F6E4']*len(s) if s['Вес'] > 0 else ['background-color: #F6EBE4']*len(s)


# def pack_input(sex, age, loyalty, distance, p_class, travel_type, dep_delay, arr_delay, wifi, fun,
#                time_conv, onboard_service, booking, leg, gate_loc, baggage, food, checkin,
#                online_boarding, inflight_service, seat, cleanliness):
#     """ translate input values to pass to model """
#
#     rule = {'Женский': 1,
#             'Мужской': 0,
#             'Личная': 0,
#             'По работе': 1,
#             'Лояльный': 1,
#             'Нелояльный': 0}
#
#     data = {'Gender': rule[sex],
#             'Age': age,
#             'Flight Distance': distance,
#             'Departure Delay in Minutes': dep_delay,
#             'Arrival Delay in Minutes': arr_delay,
#             'Inflight wifi service': wifi,
#             'Departure/Arrival time convenient': time_conv,
#             'Ease of Online booking': booking,
#             'Gate location': gate_loc,
#             'Food and drink': food,
#             'Online boarding': online_boarding,
#             'Seat comfort': seat,
#             'Inflight entertainment': fun,
#             'On-board service': onboard_service,
#             'Leg room service': leg,
#             'Baggage handling': baggage,
#             'Checkin service': checkin,
#             'Inflight service': inflight_service,
#             'Cleanliness': cleanliness,
#             'Loyalty': rule[loyalty],
#             'Business_travel': rule[travel_type],
#             'Eco': 1 if p_class == 'Эко' else 0,
#             'Eco Plus': 1 if p_class == 'Эко плюс' else 0}
#
#     return pd.DataFrame(data, index=[0])


def render_page(
        *,
        data: pd.DataFrame,
        static: dict,
) -> None:
    """ creates app page with tabs """

    st.title('Отклики клиентов банка на предложения')
    st.subheader('Исследуем оценки, предсказываем отклики, оцениваем важность факторов')
    st.write('Материал - данные о клиентах банка')
    st.image(static['main_img'])

    tab1, tab2, tab3 = st.tabs(
        [':mag: Исследовать', ':mage: Предсказать', ':vertical_traffic_light: Оценить'],
    )

    with tab1:
        st.write(
            'Exploratory data analysis: исследуем наши данные, '
            'предварительно очищенные и обработанные',
        )
        st.sidebar.header('Управление настройками')
        st.sidebar.subheader('Исследование')

        show_df = st.sidebar.checkbox('Показать датасет', disabled=False)
        if show_df:
            st.subheader('Датасет')
            st.write('CSV-файл с данными вы можете найти по ссылке ')
            st.write(data)

        show_statistics = st.sidebar.checkbox('Показать статистики')
        if show_statistics:
            st.subheader('Статистики по данным')
            st.write(data_statistics(data))
            st.write(
                '**По статистикам видно что есть выбросы в LOAN_NUM_TOTAL, LOAN_NUM_CLOSED, '
                'DEPENDANTS, OWN_AUTO. Избавляться от них не будем - возможно они значимые(?)'
                'Большинство признаков бинарные, так что кажется что статистики не '
                'особо "говорящие"**'
            )

        show_corr = st.sidebar.checkbox('Показать матрицу корреляций')
        if show_corr:
            st.subheader('Матрица корреляций')
            st.image(static['corr'])
            st.write(
                '**Корреляция с TARGET очень слабая. '
                'Самый коррелирующий признак - PERSONAL_INCOME**'
            )

        show_hist = st.sidebar.checkbox('Показать распределения признаков')
        options = st.sidebar.multiselect(
            'Выберите по каким переменным вывести распределения',
            [i for i in data.columns if i != 'TARGET'],
        )
        if show_hist:
            st.subheader('Графики распределения признаков')
            if not options:
                st.warning('Не выбраны переменные для вывода распределений')
            else:
                for opt in options:
                    st.pyplot(histplot(data=data, column=opt), use_container_width=False)

        show_target_counts = st.sidebar.checkbox(
            'Показать распределение целевой переменной',
        )
        if show_target_counts:
            st.subheader('График распределения целевой переменной по классам')
            st.pyplot(target_countplot(data=data), use_container_width=False)

    with tab2:
        st.subheader('Предсказание отклика клиента')
        st.sidebar.subheader('Предсказание')
        btn = st.sidebar.button('Рассчитать')
        st.write('Введите данные вашего клиента:')

        col1, col2, col3 = st.columns(3)
        with col1:
            gender = st.selectbox('Пол', ['Женский', 'Мужской'])
            age = st.number_input('Возраст')
            child_total = st.number_input('Количество детей клиента')
            dependants = st.number_input('Количество иждивенцев клиента')
        with col2:
            socstatus_work_fl = st.selectbox(
                'Социальный статус клиента относительно работы',
                ['Работает', 'Не работает'],
            )
            socstatus_pens_fl = st.selectbox(
                'Cоциальный статус клиента относительно пенсии',
                ['Пенсионер', 'Не пенсионер'],
            )
            fl_presence_fl = st.selectbox(
                'Наличие в собственности квартиры',
                ['Есть', 'Нет'],
            )
            own_auto = st.number_input('Количество автомобилей в собственности')
        with col3:
            personal_income = st.number_input('Личный доход клиента (в рублях)')
            loan_num_total = st.number_input('Количество ссуд клиента')
            loan_num_closed = st.number_input('Количество погашенных ссуд клиента')

        if btn:
            with st.spinner('Считаем!'):
                time.sleep(1)
                pred, proba = get_predict(
                    input_data={
                        'age': age,
                        'gender': gender,
                        'child_total': child_total,
                        'dependants': dependants,
                        'socstatus_work_fl': socstatus_work_fl,
                        'socstatus_pens_fl': socstatus_pens_fl,
                        'fl_presence_fl': fl_presence_fl,
                        'own_auto': own_auto,
                        'personal_income': personal_income,
                        'loan_num_total': loan_num_total,
                        'loan_num_closed': loan_num_closed,
                    },
                )
                if pred == 1:
                    st.success(
                        'Вероятнее клиент откликнется на предложение банка '
                        ':thumbsup: :thumbsup:',
                    )
                    with st.expander('Подробнее'):
                        st.write(f'Вероятность этого: **`{round(max(proba[0]), 3)}`**')
                elif pred == 0:
                    st.error('Вероятнее клиент не откликнется на предложение банка')
                    with st.expander('Подробнее'):
                        st.write(f'Вероятность этого: **`{round(max(proba[0]), 3)}`**')
                else:
                    st.error('Что-то пошло не так...')

    with tab3:
        st.subheader('Значимость признаков для модели')
        st.image(static['feature_imp_img'])


def load_page() -> None:
    """ loads main page """

    static = preload_content()

    st.set_page_config(layout='wide', page_title='Отклики клиентов банка')
    data = load_data()

    render_page(static=static, data=data)


if __name__ == "__main__":
    load_page()
