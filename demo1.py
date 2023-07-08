import pandas as pd
import matplotlib.pyplot as plt

def read_csv_file(file_path):
    """
    この関数は特定の構造を持つCSVファイルを読み込みます。
    :param file_path: CSVファイルへのパス。
    :return: CSVファイルの内容を含むpandasのDataFrame。
    """
    # インデックスを1から始まるものから0から始まるものに変換します。
    # CSVファイルの行と列の番号は1から始まりますが、Pythonでは0から始まります。
    header_row = 14 - 1 
    data_start_row = 16 - 1

    # CSVファイルを読み込みます。
    # header_rowより前の行と、header_rowとdata_start_rowの間の行をスキップします。
    df = pd.read_csv(file_path, encoding="shift-jis", header=header_row, skiprows=range(header_row + 1, data_start_row))

    return df


def plot_data(df):
    """
    この関数はDataFrameからデータをプロットします。
    :param df: プロットするデータを含むDataFrame。
    """
    # DataFrameのデータをプロットします。
    df.plot(kind='line', x='TIME', y=['CH1', 'CH2', 'CH3', 'CH4'])

    # プロットを表示します。
    plt.show()


def main(file_path):
    """
    メイン関数。
    :param file_path: CSVファイルへのパス。
    """
    # CSVファイルからデータを読み込み、DataFrameに格納します。
    df = read_csv_file(file_path)

    print(len(df))

    # DataFrameの列名を出力します。
    print(df.columns)

    # データをプロットします。
    plot_data(df)


if __name__ == "__main__":
    # あなたのCSVファイルへのパスに置き換えてください。
    main("../data/TEK00005.CSV")