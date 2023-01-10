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
    rowcolors=["white","lightgray"]*len(df)
    
    
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
    
    rowss=len(df)
    if title=="Encaissement":
        ax.set_title("{0}".format(title),y=rowss*0.03+0.48,color="white",backgroundcolor='gray')
    else:
        ax.set_title("                                                                {0}                                                                ".format(title),y=rowss*0.03+0.48,color="white",backgroundcolor='gray')
    
    #the_table.set_title("Title Goes Here...")
    [t.auto_set_font_size(False) for t in [the_table]]
    #[t.set_fontsize(8) for t in [the_table]]
    the_table.auto_set_column_width(col=list(range(len(df.columns))))
    #ax.set_title("Your title",  pad=20)
    #plt.title("test",loc="left")
    
    #plt.text(-0.05,0.095,"Encaissement-Avance Totale:",ha='left',va='center',size=15)


    return fig

def _draw_as_graph(df):
    pass
  

  
      
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def dataframe_to_pdf(dfs,pnl,year, filename,enctot,paytot, numpages=(1, 1), pagesize=(1, 1)):
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

                try:
                    print(df[0].groupby(["month"]).sum())
                except:
                    pass
                rows_per_page = len(df[0]) // nh
                cols_per_page = len(df[0].columns) // nv
                
                page = df[0].iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df[0])),
                            (j*cols_per_page):min((j+1)*cols_per_page, len(df[0].columns))]
                try:
                    fig, axis = plt.subplots(2)
                    figg = _draw_as_table(page, pagesize,df[2])
                
                    #df.plot()
                    #df["somme"].value_counts().plot.bar()
                
                    #df=df.groupby(df.columns[0])
                    #print(df)
                    c = ['blue','orange','gray', 'yellow','red','green','purple','brown','black','violet']
                    try:
                        del df[1]["year"]
                    except:
                        pass
                    ax=df[1].T.plot( kind="bar",color=c,width=5,figsize=(11,11),title="Graphique informatif")
                    for p in ax.patches:
                        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
                    #plt.ticklabel_format(style='plain') 
                    #ax.grid(axis='y')
                    plt.ticklabel_format(style='plain', useOffset=False, axis='y')                    
                    plt.subplots_adjust(bottom=0.3)
                    rows=df[1].somme.values                 
                    '''
                    if True:
                        # Add a part/page number at bottom-center of page
                        fig.text(0.5, 0.5/pagesize[0],
                                "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                                ha='center', fontsize=8)
                    '''
                    pdf.savefig(figg, bbox_inches='tight')
                    

                    #addlabels(rows,rows)


                    #plt.xticks(rotation=90)
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
    plt.text(0.5,0.5,"Encaissement-Avance Totale: {0}".format(enctot),ha='center',va='center',size=15)
    plt.text(0.5,0.4,"-",ha='center',va='center',size=15)
    plt.text(0.5,0.3,"Paiements Totale: {0}".format(paytot),ha='center',va='center',size=15)
    plt.text(0.5,0.2,"-------------------------------------------------------------------",ha='center',va='center',size=15)
    if pnl<0:
        plt.text(0.5,0.1,"P&l: {0}".format(pnl),ha='center',va='center',size=20,backgroundcolor="red",color="white")
    else:
        plt.text(0.5,0.1,"P&l: {0}".format(pnl),ha='center',va='center',size=20,backgroundcolor="green",color="Black")
    pdf.savefig()
    plt.close()

