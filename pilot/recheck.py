import sys, os, warnings; sys.path.insert(0,'/home/claude/v2'); warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse.domains import DOMAINS
from recourse import core as C, exact as E
ds,seed='OULAD',0
dom=DOMAINS[ds]().load(); df=dom.df; cfg=dom.cfg
tr,te=next(GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed).split(df,df[dom.y],df[dom.group]))
f=P.cat(seed).fit(df.iloc[tr][dom.features],df.iloc[tr][dom.y]); enc=E.parse_model(f,dom.features)
predict=lambda x: f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0]
d=pd.read_csv('pilot/exact_OULAD_s0.csv')
for i,r0 in d[d.accepted==0].iterrows():
    row=df.loc[r0.query]; x0=row[dom.features].astype(float).copy(); k=r0.stage
    if k: x0[cfg.tests[k:]]=0.0
    spec=dom.spec(row,k,r0.regime)[0]; pol=dom.policy()
    r=E.solve_exact(enc,x0,spec,pol,lam_spar=0.5,time_limit=120)
    ok,reasons,_=C.gate(r.x,x0,spec,pol,predict) if r.x is not None else (False,[r.status],None)
    d.loc[i,['status','accepted','reasons','seconds','effort','sparsity']]=[r.status,int(ok),';'.join(reasons),r.seconds,C.effort(r.x,x0,spec),C.sparsity(r.x,x0,spec)]
    print(r0.regime,k,r0.query,r.status,ok,reasons,flush=True)
d.to_csv('pilot/exact_OULAD_s0.csv',index=False)
print(d.groupby(['regime','stage']).accepted.mean())
