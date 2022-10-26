from fpdf import FPDF
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def _draw_as_table(df, pagesize):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                        rowLabels=df.index,
                        colLabels=df.columns,
                        rowColours=['lightblue']*len(df),
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center')
    return fig
  

def dataframe_to_pdf(df, filename, numpages=(1, 1), pagesize=(11, 8.5)):
  with PdfPages(filename) as pdf:
    nh, nv = numpages
    rows_per_page = len(df) // nh
    cols_per_page = len(df.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(df.columns))]
            fig = _draw_as_table(page, pagesize)
            if nh > 1 or nv > 1:
                # Add a part/page number at bottom-center of page
                fig.text(0.5, 0.5/pagesize[0],
                         "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                         ha='center', fontsize=8)
            pdf.savefig(fig, bbox_inches='tight')
            
            plt.close()

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
        pdf.cell(35,10,header,1,0,'C')
    pdf.cell(35,10,columnNameList[-1],1,2,'C')
    pdf.cell(-140)
    pdf.set_font('arial','',11)
    for row in range(0,len(data_list_df)):
        
        for col_num,col_name in enumerate(columnNameList):
            if col_num!= len(columnNameList)-1:                
                pdf.cell(35,10,str(data_list_df['%s'%(col_name)].iloc[row]),1,0,'C')
            else:                
                pdf.cell(35,10,str(data_list_df['%s'%(col_name)].iloc[row]),1,2,'C')
                pdf.cell(-140)
            

    pdf.output('sample.pdf')