from fpdf import FPDF
import os
import datetime
import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_pdf import PdfPages

def _draw_as_table(df, pagesize,title):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    
    the_table = ax.table(cellText=df.values,
                        rowLabels=df.index,
                        colLabels=df.columns,
                        rowColours=['lightgreen']*len(df),
                        colColours=['lightgreen']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center',
                        )
    
    rowss=len(df)
    ax.set_title(title,y=rowss*0.04+0.48)
    #the_table.set_title("Title Goes Here...")
    [t.auto_set_font_size(False) for t in [the_table]]
    #[t.set_fontsize(8) for t in [the_table]]
    the_table.auto_set_column_width(col=list(range(len(df.columns))))
    #ax.set_title("Your title",  pad=20)
    #plt.title("test",loc="left")
    
    #plt.text(-0.05,0.095,"Encaissement-Avance Totale:",ha='left',va='center',size=15)


    return fig

      
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def doctor_report(dfs,doctorname,year,filename, numpages=(1, 1), pagesize=(11, 8.5)):
  with PdfPages(filename) as pdf:
    nh, nv = numpages
    plt.figure() 
    plt.axis('off')
    plt.text(0.5,0.5,"Rapport du médecin pour :\n\n {0}\n\n pour l'année:{1}".format(doctorname,year),ha='center',va='center',size=17)
    plt.text(0.5,0.1,"\nDate: {0}".format(datetime.datetime.now()),ha='center',va='bottom',size=8)
    pdf.savefig()
    plt.close() 
    
    for i in range(0, nh):
        for j in range(0, nv):
            for df in dfs:
                try:
                    print(df[0].groupby(["month"]).sum())
                except:
                    pass
                rows_per_page = len(df[0]) // nh
                cols_per_page = len(df[0].columns) // nv
                
                page = df[0].iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df[0])),
                            (j*cols_per_page):min((j+1)*cols_per_page, len(df[0].columns))]
                try:
                    fig = _draw_as_table(page, pagesize,df[1])
                    '''
                    if True:
                        # Add a part/page number at bottom-center of page
                        fig.text(0.5, 0.5/pagesize[0],
                                "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                                ha='center', fontsize=8)
                    '''
                    pdf.savefig(fig, bbox_inches='tight')
                
                    plt.close()
                except:
                    plt.figure() 
                    plt.axis('off')
                    plt.text(0.5,0.5,"NO DATA AVAILABLE!",ha='center',va='center',size=20)
                    pdf.savefig()
                    plt.close()

 