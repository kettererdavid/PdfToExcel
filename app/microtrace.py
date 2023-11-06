import tabula


def micro1(input_path):
    area = [213, 16, 740, 303]
    df = tabula.read_pdf(input_path, pages="1", area=area)[0]
    df.loc[-1] = df.columns
    df.index = df.index + 1
    df = df.sort_index()
    df.columns = ['Untersuchung', 'NewName2', 'Ergebnis']
    df = df[['Untersuchung', 'Ergebnis']]
    df["Ergebnis"] = df["Ergebnis"].str.replace('<', '')
    df["Ergebnis"] = df["Ergebnis"].str.lstrip()
    return df.dropna(how='any')


def micro2(input_path):
    area = [171, 15, 584, 305]
    df = tabula.read_pdf(input_path, pages="2", area=area)[0]
    df.loc[-1] = df.columns
    df.index = df.index + 1
    df = df.sort_index()
    df.columns = ['Untersuchung', 'NewName2', 'Ergebnis']
    df = df[['Untersuchung', 'Ergebnis']]
    df["Ergebnis"] = df["Ergebnis"].str.replace('<', '')
    df['Untersuchung'] = df['Untersuchung'].str.replace('\r', '')
    df["Ergebnis"] = df["Ergebnis"].str.lstrip()
    return df.dropna(how='any')


def microname(input_path):
    area = [153, 134, 167, 302]
    df = tabula.read_pdf(input_path, pages="1", area=area)
    return df[0].columns[0]