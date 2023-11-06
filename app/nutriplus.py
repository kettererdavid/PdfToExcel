import tabula
import pandas as pd


def nutri1(input_path):
    area = [250, 66, 470, 391]
    df = tabula.read_pdf(input_path, pages="1", area=area)
    df1 = df[0]
    df1.columns = ['Untersuchung', 'Ergebnis']
    df2 = df[1]
    df2.loc[-1] = df2.columns
    df2.index = df2.index + 1
    df2 = df2.sort_index()
    df2.columns = ['Untersuchung', 'Ergebnis']
    df3 = pd.concat([df1, df2], axis=0)
    return df3
