#!/usr/bin/env python3
"""Offline documentary replay. Does not import or execute archived experiment code."""
import argparse
import collections
import csv
import hashlib
import json
import math
import platform
import sys
import tarfile
from pathlib import Path, PurePosixPath

import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import beta, chi2_contingency, fisher_exact, hypergeom

ARCHIVE_SHA = '92a6fcedc7561c78e9159c50a2709862d0b2b86e22c25c466ece38bb49b4c2a4'
PREFIX = 'experiments/audit_large_v1/'
PINNED = {
 'population.json':'719f66a571b90bd2cb7429d859b391ca0b66bc177e5c56c63d85f8aab8dd52f3',
 'execution_settings.json':'7eee96fd3fba6a6d740ce24a1be85775508ef938a15a8df6d889b425d819c738',
 'student_table.json':'d8e79ce6f2bc3586cb08f7e76e18f10c033f484ec863cabbd2047d285d2ff3cf',
 'pre_beacon_commitment.json':'da33afecc5fad0bc2edbf1beaf72dba9484965030acbcf776819da8f29e4f5c2',
 'beacon_plan.json':'ea9bd5b0cedf25c9ede26b4b579b47d45f6f7670c56afb8d13df42bb173dcf38',
 'sample.json':'b8844711818b2c3e59f11f61c437275f976c58532540ba576ed8cf3a347b9ae2',
 'primary_certificate.json':'e18b66541f302f55050439715364286e60557eb2fecefd57ef0f51e2b380b831',
 'full_reference.json':'d7f8d919f35a1486ef0fcc7a4a109e627b20b01cb5439b8ad180f33fcae66eff',
}
checks = 0

def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def upper(k, n, N=2048, delta=.05):
    # Exhaustive grid, independently of the archived binary search.
    totals = np.arange(k, N-n+k+1)
    keep = totals[hypergeom.cdf(k, N, totals, n) > delta]
    return int(keep[-1])

def verify_bls(beacon, info):
    # quicknet: signature in G1; key in G2; SHA256(round as 8-byte BE).
    from py_ecc.bls.g2_primitives import pubkey_to_G1, signature_to_G2
    from py_ecc.bls.hash_to_curve import hash_to_G1
    from py_ecc.optimized_bls12_381 import G2, curve_order, is_inf, multiply, pairing
    sig = bytes.fromhex(beacon['signature'])
    key = bytes.fromhex(info['public_key'])
    require(info['schemeID']=='bls-unchained-g1-rfc9380', 'BLS scheme')
    require(len(sig)==48 and len(key)==96, 'BLS byte sizes')
    require(sha(sig)==beacon['randomness'], 'Randomness/signature link')
    point = pubkey_to_G1(sig)
    public = signature_to_G2(key)
    for item in (point, public):
        require(not is_inf(item) and is_inf(multiply(item, curve_order)), 'BLS subgroup')
    def matches(r):
        msg = hashlib.sha256(int(r).to_bytes(8,'big')).digest()
        hashed = hash_to_G1(msg,b'BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_',hashlib.sha256)
        return pairing(public,hashed)==pairing(G2,point)
    require(matches(beacon['round']), 'BLS signature')
    require(not matches(beacon['round']+1), 'Wrong-round negative control')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,default=Path(__file__).resolve().parents[1]/'evidence/audit_large_review.tar.gz')
    parser.add_argument('--output',type=Path,default=Path('results/replayed'))
    parser.add_argument('--permutations',type=int,default=100000)
    args=parser.parse_args()
    if args.permutations<1: parser.error('--permutations must be positive')
    require(sha(args.archive.read_bytes())==ARCHIVE_SHA,'Evidence archive hash')
    data={}
    with tarfile.open(args.archive,'r:gz') as archive:
        for member in archive:
            name=PurePosixPath(member.name)
            require(not name.is_absolute() and '..' not in name.parts,'Unsafe archive member')
            if member.isdir(): continue
            require(member.isfile(),'Non-regular archive entry')
            require(member.name not in data,'Duplicate archive entry')
            data[member.name]=archive.extractfile(member).read()
    inventory=json.loads(data['review_inventory.json'])
    require(len(inventory)==6336,'Inventory count')
    for name,record in inventory.items():
        require(name in data,'Missing inventoried file: '+name)
        require(len(data[name])==record['bytes'] and sha(data[name])==record['sha256'],'Inventory hash: '+name)
    def read(name):return json.loads(data[PREFIX+name])
    def digest(name):return sha(data[PREFIX+name])
    for name,h in PINNED.items():require(digest(name)==h,'Pinned hash: '+name)
    pop,settings,table,commit,plan,beacon,sample,primary,full=[read(n) for n in ['population.json','execution_settings.json','student_table.json','pre_beacon_commitment.json','beacon_plan.json','beacon.json','sample.json','primary_certificate.json','full_reference.json']]
    for name,h in commit['artifact_sha256'].items():require(digest(name)==h,'Commitment: '+name)
    adapter=settings['adapter_path']
    for name,h in commit['adapter_sha256'].items():require(sha(data[adapter+'/'+name])==h,'Adapter: '+name)
    require(sha(data['experiments/scaling_1p5b/selected_adapter.json'])==commit['selection_sha256'],'Adapter selection')
    require(sample['commitment_sha256']==digest('pre_beacon_commitment.json')==plan['commitment_sha256'],'Commitment link')
    require(sample['beacon_plan_sha256']==digest('beacon_plan.json'),'Beacon plan link')
    require(beacon['round']==sample['round']==plan['target_round']==33515062,'Beacon round')
    require(plan['observed_beacon']['round']+100==beacon['round'],'Future offset')
    require(plan['scheduled_unix_seconds']==commit['chain_info']['genesis_time']+(beacon['round']-1)*3,'Round schedule')
    verify_bls(plan['observed_beacon'],commit['chain_info'])
    verify_bls(beacon,commit['chain_info'])
    require(sample['randomness']==beacon['randomness'],'Sample randomness')
    seed=hashlib.sha256(b'anna-audit-large-v1'+bytes.fromhex(digest('population.json'))+bytes.fromhex(beacon['randomness'])).digest()
    order=list(range(2048));counter=0
    for size in range(2048,1,-1):
        cutoff=(1<<256)//size*size
        while True:
            draw=int.from_bytes(hashlib.sha256(seed+counter.to_bytes(8,'big')).digest(),'big');counter+=1
            if draw<cutoff:break
        j=draw%size;order[size-1],order[j]=order[j],order[size-1]
    ids=[pop['rows'][i]['id'] for i in order]
    require(ids==sample['ordered_ids'] and ids[:768]==sample['selected_ids'],'Independent permutation')
    lookup={r['id']:r for r in pop['rows']};student={r['id']:r['response'] for r in table['rows']}
    require(len(lookup)==len(student)==len(ids)==2048,'Unique row counts')
    require(collections.Counter(r['manual_label'] for r in pop['rows'])=={'ELETRICA':1024,'MECANICA':1024},'Class balance')
    results=[];tokens={};fps=collections.defaultdict(lambda:[0,0,0,0]);windows=collections.defaultdict(lambda:[0,0]);starts=[]
    for pos,identifier in enumerate(ids):
        row=lookup[identifier];sr=read('student_responses/'+identifier+'.json');tr=read('teacher_responses/'+identifier+'.json')
        require(sha(data[PREFIX+'student_responses/'+identifier+'.json'])==table['response_file_sha256'][identifier+'.json'],'Student hash')
        require(sr['id']==identifier and sr['input_text']==row['text'] and sr['response']==student[identifier],'Student row binding')
        require(sr['settings_sha256']==digest('execution_settings.json') and sr['executor_sha256']==digest('code/student_executor.py') and sr['population_sha256']==digest('population.json'),'Student provenance')
        expected={'model':settings['teacher_request']['model'],'temperature':0,'max_completion_tokens':1024,'messages':[{'role':'user','content':settings['prompt_prefix']+row['text']}]}
        require(tr['id']==identifier and tr['request']==expected,'Teacher request')
        require(tr['commitment_sha256']==digest('pre_beacon_commitment.json') and tr['sample_sha256']==digest('sample.json') and tr['executor_sha256']==digest('code/teacher_executor.py'),'Teacher provenance')
        response=tr['response'];choice=response['choices'][0]
        require(choice['finish_reason']=='stop' and response['model']==settings['teacher_request']['model'],'Teacher completion')
        label=settings['teacher_normalization']['mapping'][choice['message']['content'].strip()]
        out={'id':identifier,'family_id':row['family_id'],'student':student[identifier],'teacher':label,'manual':row['manual_label'],'disagreement':student[identifier]!=label}
        results.append(out);tokens[identifier]=response['usage']['total_tokens']
        phase=0 if pos<768 else 1;fp=response['system_fingerprint'];require(isinstance(fp,str) and fp!='','Fingerprint missing')
        fps[fp][2*phase]+=1;fps[fp][2*phase+1]+=int(out['disagreement'])
        window=('sample' if phase==0 else 'complement')+'_'+tr['started_utc'][:10]
        windows[window][0]+=1;windows[window][1]+=int(out['disagreement'])
        if phase==0:starts.append((fp,tr['started_utc'],tr['ended_utc']))
    require(results==full['results'] and results[:768]==primary['results'],'Stored results independently reconstructed')
    require(sum(r['disagreement'] for r in results)==158 and sum(r['disagreement'] for r in results[:768])==64,'Counts')
    for report in [primary,full]:
        rr=report['results'];cert=report['certificate'];n=len(rr);k=sum(r['disagreement'] for r in rr)
        expected_upper=upper(k,n)
        require(cert['N']==2048 and cert['n']==n and cert['k']==k and cert['delta']==.05,'Certificate counts/settings')
        require(cert['upper_population_disagreements']==expected_upper and cert['exact_hypergeometric_upper']==expected_upper/2048,'Exhaustive confidence inversion')
        require(report['teacher_total_tokens']==sum(tokens[r['id']] for r in rr),'Token sums')
    require(upper(65,768)<=204<upper(66,768),'Acceptance boundary')
    require(primary['certificate']['primary_acceptance'] is True and full['certificate']['census'] is True,'Recorded decision')
    families=collections.defaultdict(list)
    for r in results:families[r['family_id']].append(r)
    counts=collections.Counter(sum(r['disagreement'] for r in rows) for rows in families.values())
    require(len(families)==1024 and all(len(r)==2 for r in families.values()),'Family sizes')
    require(counts=={0:890,1:110,2:24},'Family disagreement counts')
    require(sum(v[0]['student']!=v[1]['student'] for v in families.values())==106 and sum(v[0]['teacher']!=v[1]['teacher'] for v in families.values())==10,'Variant changes')
    require(sum(r['student']==r['manual'] for r in results)==1892 and sum(r['teacher']!=r['manual'] for r in results)==12,'Manual reference counts')
    diagnosis=read('diagnostics/post_census_diagnosis.json')
    for label,metric in diagnosis['by_manual_class'].items():
        rr=[r for r in results if r['manual']==label]
        require(sum(r['student']==label for r in rr)==metric['student_manual_correct'] and sum(r['disagreement'] for r in rr)==metric['teacher_student_disagreements'],'Class metrics')
    # No uncertainty is inferred from fingerprint identities themselves.
    vals=np.array([fps[fp] for fp in sorted(fps)]);sizes=vals[:,0]+vals[:,2];errors=vals[:,1]+vals[:,3];rate=158/2048
    obs=float(np.sum((errors-sizes*rate)**2/(sizes*rate*(1-rate))))
    asym=chi2_contingency(np.array([errors,sizes-errors]).T,correction=False)
    rng=np.random.default_rng(20261031);hits=0
    for start in range(0,args.permutations,5000):
        draw=rng.multivariate_hypergeometric(sizes,158,size=min(5000,args.permutations-start))
        stats=np.sum((draw-sizes*rate)**2/(sizes*rate*(1-rate)),axis=1)
        hits+=int(np.sum(stats>=obs-1e-12))
    pperm=(hits+1)/(args.permutations+1)
    phat=64/768
    kl=lambda q:phat*math.log(phat/q)+(1-phat)*math.log((1-phat)/(1-q))
    bounds={'fixed_table_hypergeom':upper(64,768)/2048,'iid_clopper_pearson':float(beta.ppf(.95,65,704)),'iid_chernoff_kl':float(brentq(lambda q:768*kl(q)-math.log(20),phat,1-1e-10)),'iid_hoeffding':phat+math.sqrt(math.log(20)/(2*768))}
    coverage=[]
    for K in range(2049):
        # Acceptance is fixed at k <= 65; false-acceptance risk over H0.
        if K>=205:coverage.append(float(hypergeom.cdf(65,2048,K,768)))
    require(max(coverage)<=.05,'False-acceptance risk over all null totals')
    summary={'status':'PASS','checks_passed':checks,'inventory_files':len(inventory),'raw_student_records':2048,'raw_teacher_records':2048,'N':2048,'n':768,'sample_k':64,'census_K':158,'upper_total':200,'primary_acceptance':True,'census_inside_primary_bound':158<=200,'family_counts':dict(counts),'teacher_tokens_primary':168640,'teacher_tokens_census':447733,'primary_token_fraction':168640/447733,'distinct_fingerprints':len(fps),'minimum_sample_records_per_fingerprint':int(min(vals[:,0])),'windows':dict(windows),'fingerprint_test':{'chi2':obs,'df':int(asym.dof),'asymptotic_p':float(asym.pvalue),'permutation_p':pperm,'permutations':args.permutations,'seed':20261031,'mc_se':math.sqrt(pperm*(1-pperm)/args.permutations)},'sample_complement_fisher_p':float(fisher_exact([[64,704],[94,1186]]).pvalue),'three_window_pearson_p':float(chi2_contingency([[64,704],[50,586],[44,600]],correction=False).pvalue),'hypothesis_sensitivity':bounds,'approval_power':{str(K):{str(n):float(hypergeom.cdf(c,2048,K,n)) for n,c in [(512,41),(768,65)]} for K in [143,158]},'max_false_acceptance_over_K205_to_2048':max(coverage),'scope':'Documentary replay; no training, model inference, API call, authentication of API origin, public timestamp or proof of Teacher stationarity.','replay_environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}}
    require(len(fps)==36 and min(vals[:,0])==6,'Fingerprint totals')
    args.output.mkdir(parents=True,exist_ok=True)
    summary['checks_passed']=checks
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    with (args.output/'fingerprints.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['fingerprint','sample_n','sample_d','complement_n','complement_d'])
        writer.writerows([fp,*fps[fp]] for fp in sorted(fps))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
