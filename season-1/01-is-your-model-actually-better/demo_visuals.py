"""Animated outputs for the executed lesson notebooks; all plotted values are computed."""
from pathlib import Path
import json,itertools,subprocess,hashlib,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from IPython.display import Video,HTML,display
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'animations';OUT.mkdir(exist_ok=True)
COL=['#126b91','#ea6880','#8e69bd','#1b9d93','#e5a443']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#ffffff','axes.facecolor':'#f7f9fb','axes.labelcolor':'#17364a','text.color':'#17364a','xtick.color':'#526677','ytick.color':'#526677','axes.edgecolor':'#bccbd5','savefig.facecolor':'white'})
def emit(name,init,update,seconds=14,fps=15):
 p=OUT/(name+'.mp4')
 # Reuse only exactly matching numerical/signature input prepared by this module.
 if not p.exists():
  fig,axes=init();canvas=FigureCanvasAgg(fig);w,h=canvas.get_width_height()
  proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(p)],stdin=subprocess.PIPE)
  for i in range(int(seconds*fps)):
   update(fig,axes,i/(seconds*fps-1));canvas.draw();proc.stdin.write(np.asarray(canvas.buffer_rgba())[:,:,:3].tobytes())
  proc.stdin.close();assert proc.wait()==0;plt.close(fig)
 aliases={'paired-':'paired_plot','pairs-':'resample_pairs','bootstrap-':'bootstrap_convergence','clt-':'central_limit','exact-':'exact_sign_flips','residuals-':'dependent_frames','comparison-':'interval_and_test'}
 alias=next((v for k,v in aliases.items() if name.startswith(k)),name)
 shutil.copy2(p,ROOT/(alias+'.mp4'))
 webm=ROOT/(alias+'.webm')
 if not webm.exists():subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(p),'-c:v','libvpx-vp9','-crf','32','-b:v','0','-threads','2',str(webm)],check=True)
 return Video(str(p),embed=True,html_attributes='controls autoplay loop muted playsinline',width=1220,height=440)
def paired_table(b,c):
 rows=''.join(f'<tr><td>S{i+1}</td><td>{x:.3f}</td><td>{y:.3f}</td><td style="color:#167f81">{y-x:+.3f}</td></tr>' for i,(x,y)in enumerate(zip(b,c)))
 markup='<style>.scores{font:23px DejaVu Sans;border-collapse:collapse;width:100%;max-width:1050px}.scores th{background:#17364a;color:white}.scores td,.scores th{padding:10px 28px;text-align:right;border-bottom:1px solid #d5e0e7}.scores tr:nth-child(even){background:#edf4f7}</style><table class="scores"><tr><th>Specimen</th><th>Baseline RMSE</th><th>Candidate RMSE</th><th>Difference</th></tr>'+rows+'</table>'
 (ROOT/'case_table.html').write_text('<h2 style="font:26px DejaVu Sans;color:#17364a">Five paired specimens · synthetic teaching data</h2>'+markup+'<p style="font:23px DejaVu Sans;color:#17364a">Candidate − baseline &lt; 0 means lower error.</p>')
 return HTML(markup)

def paired_plot(b,c):
 key=hashlib.sha256(np.r_[b,c].tobytes()).hexdigest()[:10]
 def init():return plt.subplots(figsize=(12.2,4.4),dpi=100)
 def update(fig,ax,p):
  ax.clear();k=min(5,p*6);ax.set(xlim=(-.2,1.7),ylim=(.07,.21),xticks=[0,1],xticklabels=['Baseline','Candidate'],ylabel='Case RMSE',title='Same five cases: candidate − baseline')
  for i,(a,z)in enumerate(zip(b,c)):
   q=np.clip(k-i,0,1)
   if q<=0:continue
   ax.plot([0,q],[a,a+(z-a)*q],color=COL[i],lw=3);ax.scatter([0,q],[a,a+(z-a)*q],c=COL[i],s=75,zorder=4)
   if q==1:ax.text(1.07,z,f'S{i+1}   {z-a:+.3f}',va='center',fontsize=15)
  fig.tight_layout(pad=1.5)
 return emit('paired-'+key,init,update)
def bootstrap_movie(samples,ci):
 samples=np.asarray(samples);key=hashlib.sha256(samples.tobytes()).hexdigest()[:10]
 bins=np.linspace(-.0205,-.0095,23)
 def init():return plt.subplots(figsize=(12.2,4.4),dpi=100)
 def update(fig,ax,p):
  ax.clear();n=min(len(samples),max(10,int(10*(len(samples)/10)**min(1,p*1.2))))
  ax.hist(samples[:n],bins=bins,color=COL[0],alpha=.85,weights=np.ones(n)/n)
  ax.axvline(ci[0],color=COL[1],ls='--',lw=2);ax.axvline(ci[1],color=COL[1],ls='--',lw=2)
  ax.set(xlim=(-.022,.002),ylim=(0,.20),xlabel='Mean paired difference (candidate − baseline)',ylabel='Fraction',title=f'Paired bootstrap: {n:,} resamples  |  5 independent cases')
  ax.axvline(0,color='#536a79',lw=1);ax.text(.04,.88,f'Illustrative 95% interval: [{ci[0]:.3f}, {ci[1]:.3f}]',transform=ax.transAxes,fontsize=15)
  fig.tight_layout(pad=1.5)
 return emit('bootstrap-'+key,init,update,18)
def pair_selection(b,c):
 from matplotlib.patches import Polygon
 idx=np.random.default_rng(20261013).integers(0,5,(4,5))
 key=hashlib.sha256(idx.tobytes()).hexdigest()[:10]+'-geometry-v3'
 def init():return plt.subplots(figsize=(12.2,4.4),dpi=100)
 def update(fig,ax,p):
  ax.clear();ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
  phase=min(3.999,p*4);i=int(phase);step=min(4,int((phase-i)*5));pick=idx[i]
  ax.text(.02,.93,'Resample whole pairs',fontsize=22,weight='bold')
  ax.text(.98,.93,'One draw at a time · with replacement',fontsize=12,ha='right')
  for j in range(5):
   x=.04+j*.19;k=pick[j]
   ax.add_patch(plt.Rectangle((x,.55),.16,.23,fc=COL[j],alpha=.28 if j==pick[step] else .13))
   ax.text(x+.08,.71,f'S{j+1}',ha='center',color=COL[j],weight='bold',fontsize=19)
   ax.text(x+.08,.60,f'{b[j]:.3f} / {c[j]:.3f}',ha='center',fontsize=13)
   ax.add_patch(plt.Rectangle((x,.21),.16,.20,fc=COL[k] if j<=step else '#dfe7eb',alpha=.16))
   ax.text(x+.08,.32,f'S{k+1}' if j<=step else '…',ha='center',color=COL[k] if j<=step else '#748795',weight='bold',fontsize=19)
   if j<=step:ax.text(x+.08,.24,f'{b[k]:.3f} / {c[k]:.3f}',ha='center',fontsize=12)
  # One connector only, as one filled polygon in display-space proportions.
  fig.tight_layout(pad=.7)
  start=ax.transData.transform((.12+pick[step]*.19,.53));end=ax.transData.transform((.12+step*.19,.43))
  u=(end-start)/np.linalg.norm(end-start);v=np.array([-u[1],u[0]]);base=end-u*13
  verts=[start+v*1.9,base+v*1.9,base+v*6,end,base-v*6,base-v*1.9,start-v*1.9]
  ax.add_patch(Polygon(ax.transData.inverted().transform(verts),closed=True,color=COL[pick[step]],linewidth=0))
  label=f'Resample {i+1:02} · draw {step+1}/5 · source S{pick[step]+1}'
  if step==4:label+=f' · mean difference {(c[pick]-b[pick]).mean():+.3f}'
  ax.text(.02,.07,label,fontsize=16)
 return emit('pairs-'+key,init,update,20)
def exact_movie(difference):
 signs=np.array(list(itertools.product([-1,1],repeat=5)));null=(signs*difference).mean(1);obs=difference.mean();key=hashlib.sha256(null.tobytes()).hexdigest()[:10]
 def init():return plt.subplots(1,2,figsize=(12.2,4.4),dpi=100,gridspec_kw={'width_ratios':[.9,1.5]})
 def update(fig,axes,p):
  a,b=axes;a.clear();b.clear();n=min(32,max(1,int(p*36)))
  row=signs[n-1];a.axis('off');a.text(.04,.92,f'Assignment {n:02} / 32',fontsize=22,weight='bold',transform=a.transAxes)
  for i in range(5):a.text(.05+i*.19,.66,'+' if row[i]>0 else '−',fontsize=42,color=COL[i],transform=a.transAxes);a.text(.05+i*.19,.48,f'S{i+1}',fontsize=16,transform=a.transAxes)
  a.text(.04,.22,f'Mean = {null[n-1]:+.3f}',fontsize=23,transform=a.transAxes);a.text(.04,.08,'All assignments, no random subset',fontsize=13,transform=a.transAxes)
  b.hist(null[:n],bins=np.linspace(-.016,.016,18),color=COL[2],alpha=.9);b.axvline(obs,color=COL[1],ls='--',lw=2);b.axvline(-obs,color=COL[1],ls='--',lw=2)
  b.set(xlim=(-.018,.018),ylim=(0,6),xlabel='Mean signed difference',ylabel='Assignments',title='Exact null distribution')
  if n==32:b.text(.17,.88,'Two-sided p = 2 / 32 = 0.0625',transform=b.transAxes,fontsize=16)
  fig.tight_layout(pad=1.2)
 return emit('exact-'+key,init,update,18)
def clt_movie():
 rng=np.random.default_rng(20261015);pop=rng.uniform(-1,1,(20000,100));ns=[1,2,5,10,20,50,100];values={n:pop[:,:n].mean(1)*np.sqrt(3*n) for n in ns}
 def init():return plt.subplots(figsize=(12.2,4.4),dpi=100)
 def update(fig,ax,p):
  ax.clear();n=ns[min(len(ns)-1,int(p*len(ns)))];ax.hist(values[n],bins=np.linspace(-4,4,40),density=True,color=COL[3],alpha=.6)
  x=np.linspace(-4,4,400);ax.plot(x,np.exp(-x*x/2)/np.sqrt(2*np.pi),color=COL[1],lw=2,label='Standard Gaussian reference')
  ax.set(xlim=(-4,4),ylim=(0,.52),xlabel='Standardised mean',ylabel='Density',title=f'Separate illustration: {n} independent uniform observations per mean')
  ax.legend(loc='upper right',fontsize=12);ax.text(.02,.93,'20,000 simulated samples from a known population',transform=ax.transAxes,fontsize=12)
  fig.tight_layout(pad=1.5)
 return emit('clt-uniform-seed20261015',init,update,18)
def residual_movie(b,c):
 phase=np.linspace(0,1,100,endpoint=False);shape=np.sin(2*np.pi*phase)+.5*np.cos(4*np.pi*phase);shape/=np.sqrt(np.mean(shape**2));rb=b[:,None]*shape;rc=c[:,None]*shape
 def init():return plt.subplots(1,2,figsize=(12.2,4.4),dpi=100,gridspec_kw={'width_ratios':[1.5,1]})
 def update(fig,axes,p):
  a,z=axes;a.clear();z.clear();n=max(2,min(100,int(p*150)))
  for i in range(5):a.plot(phase[:n],rc[i,:n],c=COL[i],lw=2,label=f'S{i+1}')
  a.set(xlim=(0,1),ylim=(-.32,.32),xlabel='Sequence phase',ylabel='Frame residual',title='Shared within-specimen pattern');a.legend(ncol=5,fontsize=9,loc='lower left')
  factor=1 if p<.5 else 10;z.imshow(np.repeat(rc,factor,axis=1),aspect='auto',cmap='RdBu_r',vmin=-.32,vmax=.32);z.set(yticks=range(5),yticklabels=[f'S{i+1}'for i in range(5)],xlabel='Frame columns',title=f'Array shape: (5, {100*factor})')
  fig.suptitle('Repeating frames does not add independent specimens',fontsize=17);fig.tight_layout(pad=1.5)
 return emit('residuals-five-cases-v1',init,update,16)
def comparison_movie(samples,ci,d):
 signs=np.array(list(itertools.product([-1,1],repeat=5)));null=(signs*d).mean(1)
 def init():return plt.subplots(1,2,figsize=(12.2,4.4),dpi=100)
 def update(fig,axes,p):
  a,b=axes;a.clear();b.clear();n=max(100,int(min(1,p*1.5)*len(samples)))
  a.hist(samples[:n],bins=np.linspace(-.021,-.009,25),color=COL[0]);a.set(xlim=(-.024,.003),xlabel='Resampled mean difference',title='Percentile interval below zero');a.axvline(0,c=COL[1],ls='--');a.axvspan(*ci,color=COL[3],alpha=.15)
  b.hist(null,bins=np.linspace(-.016,.016,18),color=COL[2]);b.axvline(d.mean(),c=COL[1],ls='--');b.set(xlabel='Null mean signed difference',title='Exact sign-flip test: p = 0.0625')
  fig.suptitle('Different constructions; no contradiction',fontsize=20);fig.tight_layout(pad=1.5)
 return emit('comparison-v1',init,update,14)
