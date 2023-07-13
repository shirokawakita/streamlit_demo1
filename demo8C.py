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
    :param secondary_y: 2つ目のY軸に表示する列の名前。
    """
    # プロットオブジェクトを作成します。
    fig = go.Figure()

    # 各列のデータをプロットします。
    for col in df.columns[1:]:  # TIME以外の全ての列をプロットします。
        fig.add_trace(
            go.Scatter(
                x=df['TIME'], 
                y=df[col], 
                mode='lines', 
                name=col,
                yaxis='y2' if col == secondary_y else 'y1'
            )
        )

    # グラフのサイズと2つ目のY軸を設定します。
    fig.update_layout(
        autosize=False,
        width=1000,  # 幅
        height=600,  # 高さ
        yaxis2=dict(
            overlaying='y',
            side='right'
        )
    )

    return fig

def main():
    st.sidebar.title('CSV File Upload')
    file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if file is not None:
        # CSVファイルからデータを読み込み、DataFrameに格納します。
        df = read_csv_file(file)
        
        if df is not None:  # dfがNoneでないことを確認します。
            # ユーザーがCH1, CH2, CH3, CH4の名前を変更できるようにします。
            ch1_name = st.sidebar.text_input("Enter the name for CH1", "CH1")
            ch2_name = st.sidebar.text_input("Enter the name for CH2", "CH2")
            ch3_name = st.sidebar.text_input("Enter the name for CH3", "CH3")
            ch4_name = st.sidebar.text_input("Enter the name for CH4", "CH4")
            
            # DataFrameの列名を更新します。
            df.rename(columns={'CH1': ch1_name, 'CH2': ch2_name, 'CH3': ch3_name, 'CH4': ch4_name}, inplace=True)
            
            # ユーザーが2つ目のY軸にプロットするデータを選択できるようにします。
            secondary_y = st.sidebar.selectbox("Choose the data for the secondary Y axis", df.columns[1:])
            
            # データを前半と後半に分割します。
            df_first_half = df.iloc[:len(df)//2]
            df_second_half = df.iloc[len(df)//2:]
            
            # ユーザーが表示するデータを選択できるようにします。
            data_choice = st.sidebar.selectbox("Choose the data to display", ["First half", "Second half"])
            
            # 選択に基づいて表示するデータを変更します。
            if data_choice == "First half":
                fig = plot_data(df_first_half, secondary_y)
            else:
                fig = plot_data(df_second_half, secondary_y)

            # プロットを表示します。
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()