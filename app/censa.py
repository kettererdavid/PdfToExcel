import tabula


def censa1(input_path):
    page1 = tabula.read_pdf(input_path, pages="1")[0]
    page1 = page1[['Laborparameter', 'e  s  swert', 'Vergleichsbereich']]
    page1.rename(columns={'e  s  swert': 'Messwert'}, inplace=True)
    return page1