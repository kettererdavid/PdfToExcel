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
            return value.replace(f"{base}{exponent}", f"({base}**{exponent})")
    return value


def enteropage1(input_path):
    area = [300, 52, 616, 347]
    page1 = tabula.read_pdf(input_path, pages="1", area=area)
    page1 = page1[0]
    page1.rename(columns={'Aerobe Flora': 'Untersuchung', 'Unnamed: 1': 'Ergebnis'}, inplace=True)
    page1 = page1[['Untersuchung', 'Ergebnis']]
    page1["Ergebnis"] = page1["Ergebnis"].str.replace('.', '*')
    page1['Ergebnis'] = page1['Ergebnis'].apply(convert_exp)

    # Move Stuhl ph result to result column
    index1 = page1[page1['Untersuchung'] == 'Stuhl-pH'].index[0]
    page1.at[index1, 'Ergebnis'] = page1.at[index1 + 1, 'Untersuchung']
    page1.drop(index1 + 1, inplace=True)
    page1.reset_index(drop=True, inplace=True)

    # Move Intestinale Ökobilanz Result to result column
    index2 = page1[page1['Untersuchung'] == 'Intestinale Ökobilanz'].index[0]
    page1.at[index2, 'Ergebnis'] = page1.at[index2 + 1, 'Untersuchung']
    page1.drop(index2 + 1, inplace=True)
    page1.reset_index(drop=True, inplace=True)
    page1 = page1.replace(['', '\-\-\-', '\+\+\+', '\(\-\)', '\(\+\)', '\+', '\-'], '', regex=True)

    return page1.dropna()


def enteropage2(input_path):
    pdf_info = tabula.read_pdf(input_path, pages='all', multiple_tables=True, stream=True, output_format='json')
    if len(pdf_info) > 1:

        area = [300, 60, 638, 210]
        page2 = tabula.read_pdf(input_path, pages="2", area=area)
        page2 = page2[0]
        page2['Untersuchung'] = page2['VERDAUUNGSPARAME'].str.extract(r'^(.*?)(?:\.{2,})')
        page2['Ergebnis'] = page2['VERDAUUNGSPARAME'].str.extract(r'\.{2,}(.*)$')
        page2 = page2[['Untersuchung', 'Ergebnis']]

        return page2.dropna()
    else:
        return DataFrame({})


def enteroname(input_path):
    area = [55, 101, 75, 290]
    page = tabula.read_pdf(input_path, pages="1", area=area)
    page = page[0]
    return page
