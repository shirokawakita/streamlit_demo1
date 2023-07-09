import pandas as pd
import plotly.graph_objects as go
import streamlit as st

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
    # プロットオブジェクトを作成します。
    fig = go.Figure()

    # 各列のデータをプロットします。
    for col in ['CH1', 'CH2', 'CH3', 'CH4']:
        fig.add_trace(go.Scatter(x=df['TIME'], y=df[col], mode='lines', name=col))

    # グラフのサイズを指定します。
    fig.update_layout(
        autosize=False,
        width=1000,  # 幅
        height=600,  # 高さ
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