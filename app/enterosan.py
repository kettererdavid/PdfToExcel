import tabula
import re
from pandas import DataFrame


def convert_exp(value):
    if isinstance(value, str):
        # Search for a '10' followed by any number of digits
        match = re.search(r'(10)(\d+)', value)
        if match:
            base = match.group(1)
            exponent = match.group(2)
            # Replace the original '10xx' pattern with '10^xx' in the value
            return '=' + value.replace(f"{base}{exponent}", f"({base}**{int(exponent)-1})")
    return value


def enteropage1(input_path):
    area = [290, 131, 616, 347]
    page1 = tabula.read_pdf(input_path, pages="1", area=area)
    page1 = page1[0]
    page1.rename(columns={'RA': 'Untersuchung', 'Unnamed: 0': 'Ergebnis'}, inplace=True)

    page1["Ergebnis"] = page1["Ergebnis"].str.replace('.', '*')
    page1["Ergebnis"] = page1["Ergebnis"].str.replace('<', '')
    page1["Ergebnis"] = page1["Ergebnis"].str.lstrip()
    page1['Ergebnis'] = page1['Ergebnis'].apply(convert_exp)

    page1.iloc[-3, 1] = page1.iloc[-3, 0]
    page1.iloc[-3, 0] = 'Stuhl-pH'

    # Delete the second to last row
    page1 = page1.drop(page1.index[-2])

    # Move the entry in column '1' to column '2' in the last row and add 'text2' to column '1'
    page1.iloc[-1, 1] = page1.iloc[-1, 0][:2]
    page1.iloc[-1, 0] = 'Intestinale Ökobilanz'

    return page1


def enteropage2(input_path):
    pdf_info = tabula.read_pdf(input_path, pages='all', multiple_tables=True, stream=True, output_format='json')
    if len(pdf_info) > 1:

        area = [300, 60, 638, 210]
        page2 = tabula.read_pdf(input_path, pages="2", area=area)
        page2 = page2[0]
        page2['Untersuchung'] = page2.iloc[:, 0].astype(str).str.extract(r'^(.*?)(?:\.{2,})')
        page2['Ergebnis'] = page2.iloc[:, 0].astype(str).str.extract(r'\.{2,}(.*)$')
        page2['Ergebnis'] = page2['Ergebnis'].str.replace('>', '')
        page2['Ergebnis'] = page2['Ergebnis'].str.replace('<', '')
        page2 = page2[['Untersuchung', 'Ergebnis']]

        return page2.dropna()
    else:
        return DataFrame({})


def enteroname(input_path):
    area = [55, 101, 75, 290]
    page = tabula.read_pdf(input_path, pages="1", area=area)
    page = page[0]
    return page
