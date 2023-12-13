import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def histplot(*, data: pd.DataFrame, column: str) -> Figure:
    sns.set_style('darkgrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(3, 3)
    sns.histplot(data[column], ax=ax)
    return fig


def target_countplot(data: pd.DataFrame) -> Figure:
    sns.set_style('darkgrid')
    fig = plt.figure(figsize=(3, 3))
    sns.countplot(x='TARGET', data=data, alpha=.80, palette=['grey', 'lightgreen'])
    plt.title('TARGET 0 vs TARGET 1')
    plt.ylabel('Количество записей')
    return fig
