from fpdf import FPDF
import os


def generate_payment_report(data_list_df):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('arial','B',11)
    pdf.cell(60)
    pdf.cell(75,10,'Payment Data:',0,2,'C')
    pdf.cell(90,10,' ',0,2,'C')
    pdf.cell(-55)
    columnNameList = list(data_list_df.columns)
    for header in columnNameList[:-1]:
        pdf.cell(35,10,columnNameList[-1],1,2,'C')
    pdf.cell(35,10,columnNameList[-1],1,2,'C')
    pdf.cell(-140)

    pdf.output('sample.pdf')