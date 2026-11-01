"""Plots computed inside the Jupyter kernel from the episode's actual arrays."""
import numpy as np
import matplotlib.pyplot as plt
COL=['#167c9d','#de7189','#8d69b2','#da9b35','#329a84']
plt.rcParams.update({'font.size':18,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#17384b','text.color':'#17384b','figure.facecolor':'white','axes.facecolor':'white','figure.dpi':110})
def new(title):
    fig,ax=plt.subplots(figsize=(12.7,3.9),layout='constrained');ax.set_title(title,pad=15);return fig,ax
def plot_dataset(frames):
    fig,ax=new('Each frame keeps its case identity')
    for i,row in enumerate(frames):
        ax.plot(np.arange(len(row)),row,color=COL[i],lw=2.5)
        ax.text(101,row[-1],f'Case {i}',color=COL[i],fontsize=14,va='center')
    ax.set(xlabel='Frame position within each case',ylabel='Synthetic value',xlim=(0,112),xticks=[0,20,40,60,80,100]);plt.show()
def plot_case_means(values):
    fig,ax=new('Five equally weighted case means')
    ax.barh([f'Case {i}' for i in range(5)],values,color=COL);ax.axvline(np.mean(values),color='#17384b',ls='--',label=f'Overall mean = {np.mean(values):.2f}');ax.set_xlabel('Case mean');ax.invert_yaxis();ax.legend(fontsize=15);plt.show()
def plot_standard_errors(row,case):
    fig,ax=new('The independent unit changes the standard-error calculation')
    ax.barh(['All rows treated as independent','Cases treated as independent'],[row,case],color=COL[:2]);ax.set_xlim(0,.56)
    for y,v in enumerate([row,case]):ax.text(v+.012,y,f'{v:.6f}',va='center')
    ax.set_xlabel('Standard error of the mean');ax.invert_yaxis();plt.show()
def plot_duplication(frames,duplicated):
    fig,ax=new('Copying observations does not add independent cases');ax.axis('off')
    def vals(x):return [str(x.size),str(x.shape[0]),f'{x.mean():.6f}',f'{x.ravel().std(ddof=1)/np.sqrt(x.size):.6f}',f'{x.mean(axis=1).std(ddof=1)/np.sqrt(x.shape[0]):.6f}']
    a,b=vals(frames),vals(duplicated);tab=ax.table(cellText=list(zip(['Stored rows','Independent cases','Mean','Row SEM','Case SEM'],a,b)),colLabels=['','Original','Duplicated ×10'],loc='center',cellLoc='left',colWidths=[.46,.26,.26]);tab.auto_set_font_size(False);tab.set_fontsize(19);tab.scale(1,1.6)
    for (r,c),cell in tab.get_celld().items():cell.set_edgecolor('#d7e0e5');cell.set_facecolor('#eff6f8' if r==0 else 'white')
    plt.show()
def plot_covariance(G,m,rho):
    fig,ax=new('A conditional, variance-equivalent sample size');r=np.linspace(0,1,301);N=G*m
    ax.plot(r,N/(1+(m-1)*r),color=COL[0],lw=3);v=N/(1+(m-1)*rho);ax.scatter([rho],[v],color=COL[1],s=90,zorder=3)
    ax.annotate(f'ρ = {rho} → n ≈ {v:.3f}',(rho,v),xytext=(.45,165),arrowprops={'arrowstyle':'->','color':COL[1]},color=COL[1]);ax.set(xlabel='Assumed within-group correlation ρ',ylabel='Variance-equivalent n',xlim=(0,1),ylim=(0,520));plt.show()
def plot_weights(counts,equal,weighted):
    fig,ax=new(f'Equal-case mean = {equal:.3f}    |    Row-weighted mean = {weighted:.3f}')
    ax.bar([f'Case {i}' for i in range(5)],counts,color=COL)
    for i,n in enumerate(counts):ax.text(i,n+5,str(n),ha='center')
    ax.set(ylabel='Rows (weight in a row average)',ylim=(0,230));plt.show()
def plot_partitions(groups,partitions,names):
    fig,ax=new('Which cases appear in each partition?');matrix=np.array([[g in set(groups[p]) for p in partitions] for g in range(5)])
    for i in range(5):
        for j in range(len(partitions)):
            ax.scatter(j,i,s=950,marker='s',color=COL[i] if matrix[i,j] else '#edf1f3');ax.text(j,i,'✓' if matrix[i,j] else '—',ha='center',va='center',color='white' if matrix[i,j] else '#a1b1bb',fontweight='bold')
    ax.set(xticks=range(len(names)),xticklabels=names,yticks=range(5),yticklabels=[f'Case {i}' for i in range(5)],xlim=(-.6,len(names)-.4),ylim=(4.6,-.6));ax.tick_params(length=0)
    for sp in ax.spines.values():sp.set_visible(False)
    plt.show()
def plot_intervals(case,row,B):
    fig,ax=new(f'95% percentile intervals from {B:,} resamples per method')
    for y,ci,col in [(1,case,COL[0]),(0,row,COL[1])]:
        ax.plot(ci,[y,y],color=col,lw=7);ax.scatter(ci,[y,y],marker='|',s=600,color=col);ax.text(ci[1]+.04,y,f'[{ci[0]:.3f}, {ci[1]:.3f}]',va='center',color=col,fontsize=16)
    ax.set(yticks=[0,1],yticklabels=['Individual rows','Whole cases'],xlabel='Bootstrap mean — same scale for both methods',xlim=(-1.3,1.7),ylim=(-.5,1.5));plt.show()
