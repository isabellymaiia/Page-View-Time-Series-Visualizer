import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar dados (certifique-se de analisar as datas. Considere definir a coluna de índice como 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date') 

# Limpar os dados removendo os 2.5% mais altos e os 2.5% mais baixos
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


# Objetivo: Visualizar a evolução das visitas diárias ao fórum.
def draw_line_plot():
    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(12, 6))

    # Desenhar o gráfico de linha com o DataFrame filtrado
    ax.plot(df.index, df['value'], color='tab:red', linewidth=1)

    # Definir título e rótulos
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Ajustar layout para que tudo se encaixe corretamente
    fig.tight_layout()

    # Salvar a imagem como 'line_plot.png' e retornar a figura
    fig.savefig('line_plot.png')
    return fig

# Objetivo: Mostrar a média de visitas diárias por mês agrupadas por ano.
def draw_bar_plot():
    # Copiar e modificar os dados para o gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupar os dados por ano e mês e calcular a média
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Definir os meses para o eixo x
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Desenhar o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 6)).figure

    # Configurar o rótulo dos eixos e o título da legenda
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title="Months", labels=months)
    
    # Salvar a imagem e retornar o objeto fig
    fig.savefig('bar_plot.png')
    return fig

# Objetivo: Comparar a distribuição de visitas ao longo dos anos e meses.
def draw_box_plot():
    # Preparar os dados para os gráficos box plot (já feito no boilerplate)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Definir a figura com dois gráficos lado a lado
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Desenhar o gráfico Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Desenhar o gráfico Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Ajustar o layout para melhor visualização
    plt.tight_layout()

    # Salvar a imagem e retornar o objeto fig
    fig.savefig('box_plot.png')
    return fig
