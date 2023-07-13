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

    print(df.head())

    return df

def plot_data(df, secondary_y):
    """
    この関数はDataFrameからデータをプロットします。
    :param df: プロットするデータを含むDataFrame。
    :param secondary_y: 2つ目のY軸にプロットする列名。
    """
    # プロットオブジェクトを作成します。
    fig = go.Figure()

    # データをプロットします。
    for col in ['CH1', 'CH2', 'CH3', 'CH4']:
        if col == secondary_y:
            fig.add_trace(go.Scatter(x=df['TIME'], y=df[col], mode='lines', name=col, yaxis='y2'))
        else:
            fig.add_trace(go.Scatter(x=df['TIME'], y=df[col], mode='lines', name=col))

    # 2つ目のY軸を追加します。
    fig.update_layout(
        yaxis2=dict(
            title=secondary_y,
            overlaying='y',
            side='right',
        ),
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
        
        if df is not None:  # dfがNoneでないことを確認します。
            # データを前半と後半に分割します。
            df_first_half = df.iloc[:len(df)//2]
            df_second_half = df.iloc[len(df)//2:]
            
            # ユーザーが表示するデータを選択できるようにします。
            data_choice = st.sidebar.selectbox("Choose the data to display", ["First half", "Second half"])
            
            # ユーザーが2つ目のY軸にプロットするデータを選択できるようにします。
            secondary_y = st.sidebar.selectbox("Choose the data for the secondary Y axis", ['CH1', 'CH2', 'CH3', 'CH4'])
            
            # 選択に基づいて表示するデータを変更します。
            if data_choice == "First half":
                fig = plot_data(df_first_half, secondary_y)
            else:
                fig = plot_data(df_second_half, secondary_y)

            # プロットを表示します。
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()