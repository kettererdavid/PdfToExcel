import tabula
from pandas import DataFrame


def synpage1(input_path):
    area = [450, 50, 776, 300]
    page1 = tabula.read_pdf(input_path, pages="1", area=area)
    page1 = page1[0]
    page1.rename(columns={'Unnamed: 0': 'Alles'}, inplace=True)
    page1['Alles'] = page1['Alles'].astype(str).apply(lambda x: x.split('\r')[0])
    page1['Ergebnis'] = page1['Alles'].str.extract(r'(\d+\.\d+|\d+)')
    pattern = r'[^a-zA-ZäöüÄÖÜßα().^ -]'
    page1['Untersuchung'] = page1['Alles'].str.replace(pattern, '', regex=True)
    page1 = page1.dropna(subset=['Ergebnis'])
    return page1[['Untersuchung', 'Ergebnis']]


def synpage2(input_path):
    pdf_info = tabula.read_pdf(input_path, pages='all', multiple_tables=True, stream=True, output_format='json')
    if len(pdf_info) > 1:
        area = [145, 50, 725, 300]
        page1 = tabula.read_pdf(input_path, pages="2", area=area)
        page1 = page1[0]
        page1.rename(columns={'Unnamed: 0': 'Alles'}, inplace=True)
        page1['Alles'] = page1['Alles'].astype(str).apply(lambda x: x.split('\r')[0])
        page1['Ergebnis'] = page1['Alles'].str.extract(r'(\d+\.\d+|\d+)')
        pattern = r'[^a-zA-ZäöüÄÖÜßα()^ -]'
        page1['Untersuchung'] = page1['Alles'].str.replace(pattern, '', regex=True)
        page1 = page1.dropna(how='all')
        page1 = page1[['Untersuchung', 'Ergebnis']]
        page1['Untersuchung'] = page1['Untersuchung'].str.rstrip()
        mask = page1['Untersuchung'] == 'LDH-Isoenzym'

        # Update the 'left' column by appending the first character from the 'right' column
        page1.loc[mask, 'Untersuchung'] = page1.loc[mask, 'Untersuchung'] + page1.loc[mask, 'Ergebnis'].str[0]

        # Remove the first character from the 'right' column for those rows
        page1.loc[mask, 'Ergebnis'] = page1.loc[mask, 'Ergebnis'].str[1:]
        return page1.dropna(subset=['Ergebnis'])
    else:
        return DataFrame({})


def synpage3(input_path):
    pdf_info = tabula.read_pdf(input_path, pages='all', multiple_tables=True, stream=True, output_format='json')
    if len(pdf_info) > 2:
        area = [145, 50, 595, 300]
        page1 = tabula.read_pdf(input_path, pages="3", area=area)
        page1 = page1[0]
        page1.rename(columns={'Unnamed: 0': 'Alles'}, inplace=True)
        page1['Alles'] = page1['Alles'].astype(str).apply(lambda x: x.split('\r')[0])
        page1['Ergebnis'] = page1['Alles'].str.extract(r'(\d+\.\d+|\d+)')
        pattern = r'[^a-zA-ZäöüÄÖÜßα().^ -]'
        page1['Untersuchung'] = page1['Alles'].str.replace(pattern, '', regex=True)
        page1 = page1.dropna(how='all')
        page1 = page1[['Untersuchung', 'Ergebnis']]
        return page1.dropna(subset=['Ergebnis'])
    else:
        return DataFrame({})

def synname(input_path):
    area = [333, 90, 352, 300]
    page = tabula.read_pdf(input_path, pages="1", area=area)
    page = page[0]
    return page
