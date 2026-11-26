"""Empirical checks of the theory (docs/THEORY_v3.md, Section 8) from results_v3/bounds/."""
import glob, os, sys
import numpy as np, pandas as pd

RES = 'results_v3'
OUT = f'{RES}/tables'
TOL = 1e-4
SEPARABLE = {'HMDA', 'PIMA'}            # single-feature rule constraints, no links, no disjunction
SINGLE = {'OULAD'}                      # one monotone '>=' constraint


def load():
    B = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f'{RES}/bounds/v3_*.csv'))], ignore_index=True)
    k = ['dataset', 'model', 'seed', 'stage', 'query', 'regime']
    files = sorted({f'{RES}/v3_{d}_{m}_s{s}.csv.gz' for d, m, s in B[['dataset', 'model', 'seed']].drop_duplicates().itertuples(index=False)})
    D = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    W = D.pivot_table(index=k, columns='condition', values=['accepted', 'cost'], aggfunc='first')
    W.columns = [f'{a}_{b}' for a, b in W.columns]
    st = D[D.condition == 'exact'].set_index(k).exact_status.rename('exact_status')
    return B.set_index(k).join(W).join(st).reset_index()


def main():
    d = load(); md = []
    g = d.groupby(['dataset', 'regime', 'model'])
    # (a) validity of the lower bounds (Prop. 4.1)
    acc = d.accepted_exact == 1
    v_rule = (acc & (d.lb_rule > d.cost_exact + TOL)).sum()
    mb = d.model_bound.where(d.model_status != 'skipped')
    v_model = (acc & (mb > d.cost_exact + TOL)).sum()
    md += [f'## (a) Bound validity (Prop. 4.1)', f'queries: {len(d)}; LB_R > exact cost: {v_rule}; model dual bound > exact cost: {v_model}', '']
    # abstention decomposition (Theorem 2)
    inf = d.exact_status == 'infeasible'
    md += ['## Certified abstention (Theorem 2)',
           f'exact infeasible: {inf.sum()}; of which rule-infeasible (R empty): {(inf & (d.rule_status == "infeasible")).sum()}; '
           f'rule-feasible but A empty: {(inf & (d.rule_status != "infeasible")).sum()}', '']
    # (b) rule-binding share and Prop. 4.2 / 5
    rows = []
    for key, t in g:
        a = t[t.accepted_exact == 1]
        opt = a.exact_status == 'optimal'
        binding = (a.cost_exact <= a.lb_rule + TOL) & opt
        r0 = t[(t.repair0_model == 1) & (t.accepted_exact == 1) & (t.exact_status == 'optimal')]
        sep = key[0] in SEPARABLE
        rows.append(dict(dataset=key[0], regime=key[1], model=key[2], n=len(a),
                         rule_binding_pct=round(100 * binding.mean(), 1),
                         repair0_accepted_by_f=len(r0),
                         repair0_is_opt_pct=round(100 * (r0.repair0_cost <= r0.cost_exact + 1e-3).mean(), 1) if sep and len(r0) else np.nan,
                         repair_esc_opt_pct=round(100 * ((a.accepted_repair_esc == 1) & (a.cost_repair_esc <= a.cost_exact + 1e-3)).sum() / max((a.accepted_repair_esc == 1).sum(), 1), 1)))
    T = pd.DataFrame(rows); T.to_csv(f'{OUT}/rule_binding_v3.csv', index=False)
    md += ['## (b) Rule-binding queries (OPT = LB_R) and repair optimality (Props. 4.2, 5)', T.to_markdown(index=False), '']
    # (c) Theorem 7: escalation end-point test on linear models
    rows = []
    for key, t in g:
        if key[2] != 'lr' or not (key[0] in SEPARABLE or key[0] in SINGLE):
            continue
        for s, u in [('all', t)] + [(f'seed {x}', t[t.seed == x]) for x in sorted(t.seed.unique())]:
            agree = (u.accepted_repair_esc == u.esc_end_ok)
            rows.append(dict(dataset=key[0], regime=key[1], subset=s, n=len(u), esc_success_pct=round(100 * u.accepted_repair_esc.mean(), 1),
                             end_point_ok_pct=round(100 * u.esc_end_ok.mean(), 1), agreement_pct=round(100 * agree.mean(), 2),
                             esc_fail_but_end_ok=int(((u.accepted_repair_esc == 0) & (u.esc_end_ok == 1)).sum()),
                             esc_ok_but_end_fail=int(((u.accepted_repair_esc == 1) & (u.esc_end_ok == 0)).sum())))
    E7 = pd.DataFrame(rows); E7.to_csv(f'{OUT}/escalation_theorem_v3.csv', index=False)
    md += ['## (c) Escalation end-point test, linear models (Theorem 7.2)', E7.to_markdown(index=False), '']
    # (d) price of compliance
    rows = []
    for key, t in g:
        u = t[(t.accepted_exact == 1) & (t.exact_status == 'optimal') & (t.model_status == 'optimal')]
        if not len(u):
            continue
        poc = u.cost_exact - u.opt_model
        rows.append(dict(dataset=key[0], regime=key[1], model=key[2], n=len(u), cost_exact=round(u.cost_exact.mean(), 3),
                         cost_model_only=round(u.opt_model.mean(), 3), poc_mean=round(poc.mean(), 3),
                         poc_pct=round(100 * (u.cost_exact.mean() / u.opt_model.mean() - 1), 1),
                         rule_free_pct=round(100 * (poc <= TOL).mean(), 1)))
    PC = pd.DataFrame(rows); PC.to_csv(f'{OUT}/price_of_compliance_v3.csv', index=False)
    md += ['## (d) Price of compliance: OPT - LB_F (both proven optimal)', PC.to_markdown(index=False), '']
    # (e) a-posteriori gap certificate for heuristics (Prop. 4.3)
    rows = []
    for key, t in g:
        for m in ['repair_esc', 'framework']:
            if f'accepted_{m}' not in t:
                continue
            u = t[(t[f'accepted_{m}'] == 1) & (t.accepted_exact == 1) & (t.exact_status == 'optimal')]
            if not len(u):
                continue
            lb = np.fmax(u.lb_rule, u.model_bound.where(u.model_status != 'skipped'))
            rows.append(dict(dataset=key[0], regime=key[1], model=key[2], method=m, n=len(u),
                             true_gap=round((u[f'cost_{m}'] - u.cost_exact).mean(), 3),
                             certified_gap=round((u[f'cost_{m}'] - lb).mean(), 3),
                             certificate_tight_pct=round(100 * ((lb >= u.cost_exact - TOL)).mean(), 1)))
    GC = pd.DataFrame(rows); GC.to_csv(f'{OUT}/gap_certificate_v3.csv', index=False)
    md += ['## (e) A-posteriori gap certificate (Prop. 4.3): mean true vs certified gap', GC.to_markdown(index=False), '']
    open(f'{OUT}/theory_checks_v3.md', 'w').write('\n'.join(md)); print('\n'.join(md))


if __name__ == '__main__':
    main()
