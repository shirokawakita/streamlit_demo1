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

def plot_data(df, secondary_y, y1_range, y2_range):
    """
    この関数はDataFrameからデータをプロットします。
    :param df: プロットするデータを含むDataFrame。
    :param secondary_y: 2つ目のY軸に表示する列の名前。
    :param y1_range: 1つ目のY軸の表示範囲。
    :param y2_range: 2つ目のY軸の表示範囲。
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
        width=800,  # 幅
        height=400,  # 高さ
        xaxis=dict(
            title_text="TIME",  # X軸のラベルを設定します。
            title_font=dict(size=18),  # X軸のラベルのフォントサイズを設定します。
            tickfont=dict(size=18),  # X軸の目盛りのフォントサイズを設定します。
        ),
        yaxis=dict(
            range=y1_range,  # 1つ目のY軸の表示範囲を設定します。
            tickfont=dict(size=18),  # 1つ目のY軸の目盛りのフォントサイズを設定します。
        ),
        yaxis2=dict(
            title_text=secondary_y,  # 2つ目のY軸のラベルを設定します。
            range=y2_range,  # 2つ目のY軸の表示範囲を設定します。
            title_font=dict(size=18),  # 2つ目のY軸のラベルのフォントサイズを設定します。
            tickfont=dict(size=18),  # 2つ目のY軸の目盛りのフォントサイズを設定します。
            overlaying='y',
            side='right'
        ),
        legend=dict(
            font=dict(size=18)  # 凡例のフォントサイズを設定します。
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
            
            # データを3つの部分に分割します。
            df_first_part = df.iloc[:len(df)//3]
            df_second_part = df.iloc[len(df)//3:(2*len(df))//3]
            df_third_part = df.iloc[(2*len(df))//3:]
            
            # ユーザーが表示するデータを選択できるようにします。
            data_choice = st.sidebar.selectbox("Choose the data to display", ["First part", "Second part", "Third part"])
            
            # スライダーから値を取得します。
            y1_range = st.sidebar.slider(
                "Range of Y1 axis", 
                float(df[df.columns.difference([secondary_y])].min().min()) - 0.5 * (float(df[df.columns.difference([secondary_y])].max().max()) - float(df[df.columns.difference([secondary_y])].min().min())), 
                1.5 * float(df[df.columns.difference([secondary_y])].max().max()), 
                (float(df[df.columns.difference([secondary_y])].min().min()), float(df[df.columns.difference([secondary_y])].max().max()))
            )

            # y1_rangeがタプルではない場合（つまり単一の値の場合）、それを範囲に変換します。
            if not isinstance(y1_range, tuple):
                y1_range = (y1_range, y1_range)

            # 同様にY2軸の範囲を設定します。
            y2_range = st.sidebar.slider(
                "Range of Y2 axis", 
                float(df[secondary_y].min()) - 0.5 * (float(df[secondary_y].max()) - float(df[secondary_y].min())), 
                1.5 * float(df[secondary_y].max()), 
                (float(df[secondary_y].min()), float(df[secondary_y].max()))
            )
            if not isinstance(y2_range, tuple):
                y2_range = (y2_range, y2_range)
            
            # 選択に基づいて表示するデータを変更します。
            if data_choice == "First part":
                fig = plot_data(df_first_part, secondary_y, y1_range, y2_range)
            elif data_choice == "Second part":
                fig = plot_data(df_second_part, secondary_y, y1_range, y2_range)
            else:
                fig = plot_data(df_third_part, secondary_y, y1_range, y2_range)

            
            # 1つ目のY軸のタイトルを設定します。
            y1_title = ', '.join([col for col in df.columns[1:] if col != secondary_y])
            fig.update_layout(yaxis1=dict(title_text=y1_title))

            # プロットを表示します。
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()
