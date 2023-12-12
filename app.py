import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from utils.utils import load_data
from utils.visualization import correlation_heatmap, pairplot

st.title('EDA данных о клиентах банка')
st.write('Данный дашборд предлагает визуализацию данных о клиентах банка')

# # Titles and Mode selections
# st.sidebar.title("About")
# st.sidebar.info(
#     """
#     COVID 19 IN THE WORLD DASHBOARD
#     """
# )

# Load data
data = load_data()

# show_data = st.sidebar.checkbox('Показать датасет')
# if show_data:
#     st.subheader('Датасет')
#     st.markdown('#### CSV-файл с данными вы можете найти по ссылке')
#     st.write(df)

# st.write(correlation_heatmap(data))
# st.pyplot(pairplot(data))
