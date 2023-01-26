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
    alternating_colors = [['lightgray'] * len(df.columns), ['white'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #ax[0].axis('tight')
    ax.axis('off')
    rowcolors=["lightgray","white"]*len(df)
    #print(colors)
    
    the_table = ax.table(cellText=df.values,
                        rowLabels=df.index,
                        colLabels=df.columns,
                        rowColours=rowcolors,
                        #colColours=['gray']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center',
                        
                        
                        )
    for key, cell in the_table.get_celld().items():
        cell.set_linewidth(0)

    xtls = ax.get_xticklabels()
    xtls = [i.get_text() for i in xtls]

    ax.set_xticklabels([])

    t = ax.tables[0]
    for c in t.get_children():
        tobj = c.get_text()
        text = tobj.get_text()
        if text not in xtls:
         
            try: # some texts will be strings that are labels, we can't convert them
                s = '{:0,.2f}'.format(float(text))
                '''s=s.replace('.','|')
                s=s.replace(',','.')
                s=s.replace('|',',')'''
                tobj.set_text(s)
                #print(s)
            except:
                pass
    [t.auto_set_font_size(False) for t in [the_table]]
    #[t.set_fontsize(8) for t in [the_table]]
    the_table.auto_set_column_width(col=list(range(len(df.columns))))
    fig.suptitle("Résumé des informations sur le médecin",fontweight="bold")

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

 