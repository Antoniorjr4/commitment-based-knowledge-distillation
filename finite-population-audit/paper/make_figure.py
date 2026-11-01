import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import hypergeom
from pathlib import Path
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(8,3.15),layout='constrained')
vals=[8.333333,9.765625,7.714844]
ax[0].bar(['Sample\n64/768','Upper bound\n200/2,048','Census\n158/2,048'],vals,color=['#7298b5','#184e77','#45836f'],width=.6)
ax[0].axhline(10,color='#a94c40',linestyle='--',linewidth=1.2,label='Prespecified target')
for i,v in enumerate(vals):ax[0].text(i,v+.22,f'{v:.2f}%',ha='center',fontsize=8)
ax[0].set_ylim(0,12);ax[0].set_ylabel('Teacher-Student disagreement (%)');ax[0].set_title('(a) Primary certificate and later census',loc='left',fontsize=10)
ax[0].legend(loc='upper right',fontsize=7,frameon=False)
K=np.arange(70,230)
for n,c,col in [(512,41,'#7298b5'),(768,65,'#184e77')]:
 ax[1].plot(100*K/2048,100*hypergeom.cdf(c,2048,K,n),label=f'n = {n}',color=col,lw=1.8)
ax[1].axvline(100*158/2048,color='#45836f',lw=1,linestyle=':',label='Census rate')
ax[1].scatter([100*158/2048],[100*hypergeom.cdf(65,2048,158,768)],color='#184e77',s=20,zorder=3)
ax[1].set_ylim(0,103);ax[1].set_xlabel('Hypothetical fixed-table disagreement (%)');ax[1].set_ylabel('Probability of passing target (%)');ax[1].set_title('(b) Fixed-design acceptance probability',loc='left',fontsize=10)
ax[1].legend(fontsize=7,frameon=False)
for ext in ['pdf','png']:fig.savefig(Path(__file__).resolve().parent / ('figures/audit_summary.'+ext),dpi=180)
