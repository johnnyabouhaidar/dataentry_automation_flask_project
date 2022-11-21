from fpdf import FPDF
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
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
                        rowColours=['lightgreen']*len(df),
                        colColours=['lightgreen']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center')
    return fig
  

def dataframe_to_pdf(dfs,pnl,year, filename, numpages=(1, 1), pagesize=(11, 8.5)):
  with PdfPages(filename) as pdf:
    nh, nv = numpages


    plt.figure() 
    plt.axis('off')
    plt.text(0.5,0.5,"Rapport de paiement consolidé pour: {0}".format(year),ha='center',va='center',size=20)
    plt.text(0.5,0.1,"\nDate: {0}".format(datetime.datetime.now()),ha='center',va='bottom',size=8)
    pdf.savefig()
    plt.close()
    for i in range(0, nh):
        for j in range(0, nv):
            for df in dfs:
                rows_per_page = len(df) // nh
                cols_per_page = len(df.columns) // nv
                page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df)),
                            (j*cols_per_page):min((j+1)*cols_per_page, len(df.columns))]
                try:
                    fig = _draw_as_table(page, pagesize)
                    '''
                    if True:
                        # Add a part/page number at bottom-center of page
                        fig.text(0.5, 0.5/pagesize[0],
                                "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                                ha='center', fontsize=8)
                    '''
                    pdf.savefig(fig, bbox_inches='tight')
                
                    #df.plot()
                    #df["somme"].value_counts().plot.bar()
                    df.plot(y=["somme"], kind="bar",color="blue")
                    
                    plt.xticks(rotation=10)
                    pdf.savefig()
                    plt.close()
                except:
                    plt.figure() 
                    plt.axis('off')
                    plt.text(0.5,0.5,"NO DATA AVAILABLE!",ha='center',va='center',size=20)
                    pdf.savefig()
                    plt.close()


    plt.figure() 
    plt.axis('off')
    plt.text(0.5,0.5,"Pnl: {0}".format(pnl),ha='center',va='center',size=20)
    pdf.savefig()
    plt.close()

