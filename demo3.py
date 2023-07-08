import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def read_csv_file(file):
    """
    この関数は特定の構造を持つCSVファイルを読み込みます。
    :param file: CSVファイルへのパス。
    :return: CSVファイルの内容を含むpandasのDataFrame。
    """
    # インデックスを1から始まるものから0から始まるものに変換します。
    # CSVファイルの行と列の番号は1から始まりますが、Pythonでは0から始まります。
    header_row = 14 - 1  
    data_start_row = 16 - 1

    # CSVファイルを読み込みます。
    # header_rowより前の行と、header_rowとdata_start_rowの間の行をスキップします。
    df = pd.read_csv(file, encoding="shift-jis", header=header_row, skiprows=range(header_row + 1, data_start_row))

    return df

def plot_data(df):
    """
    この関数はDataFrameからデータをプロットします。
    :param df: プロットするデータを含むDataFrame。
    """
    # プロットオブジェクトを作成します。
    fig = go.Figure()

    # 各列のデータをプロットします。
    for col in ['CH1', 'CH2', 'CH3', 'CH4']:
        fig.add_trace(go.Scatter(x=df['TIME'], y=df[col], mode='lines', name=col))

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