import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

def read_csv_file(file):
    """
    この関数は特定の構造を持つCSVファイルを読み込みます。
    :param file: CSVファイルへのパス。
    :return: CSVファイルの内容を含むpandasのDataFrame。
    """
    # ヘッダー行を探します。
    lines = file.getvalue().decode('shift-jis').splitlines()
    for i, line in enumerate(lines, start=1):
        if line.startswith('TIME'):
            header_row = i - 1  # Pythonのインデックスは0から始まるため、1を引きます。
            print(f'ヘッダー行は {i} 行目です。')
            break
    else:
        raise ValueError('ヘッダー行が見つかりませんでした。')

    # CSVファイルを読み込みます。
    file.seek(0)
    df = pd.read_csv(file, encoding="shift-jis", skiprows=range(header_row), header=0)

    return df

def plot_data(df):
    """
    この関数はDataFrameからデータをプロットします。
    :param df: プロットするデータを含むDataFrame。
    """
    # データフレームを前半と後半に分割します。
    df_first_half = df.iloc[:len(df)//2]
    df_second_half = df.iloc[len(df)//2:]

    # サブプロットを作成します。
    fig = make_subplots(rows=2, cols=1)

    # 各列のデータをプロットします。
    for col in ['CH1', 'CH2', 'CH3', 'CH4']:
        fig.add_trace(go.Scatter(x=df_first_half['TIME'], y=df_first_half[col], mode='lines', name=f'First half {col}'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_second_half['TIME'], y=df_second_half[col], mode='lines', name=f'Second half {col}'), row=2, col=1)

    # グラフのサイズを指定します。
    fig.update_layout(
        autosize=False,
        width=1000,  # 幅
        height=1200,  # 高さ
    )

    return fig


def main():
    st.sidebar.title('CSV File Upload')
    file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if file is not None:
        # CSVファイルからデータを読み込み、DataFrameに格納します。
        df = read_csv_file(file)

        # データをプロットします。
        fig = plot_data(df)
        
        # プロットを表示します。
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()