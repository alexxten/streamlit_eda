import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import PairGrid


def correlation_heatmap(data: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    sns.heatmap(data.corr(), ax=ax)
    return fig


def pairplot(data: pd.DataFrame) -> PairGrid:
    fig = sns.pairplot(data)
    return fig

