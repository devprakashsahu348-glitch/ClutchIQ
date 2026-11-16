"""ClutchIQ pressure model. Usage: python analysis/pressure_model.py "<path to Data Pack>" """
import sys, json, numpy as np, pandas as pd
D = sys.argv[1] if len(sys.argv) > 1 else "Data Pack"
WICKET_VALUE = 8.0   # runs a wicket is worth in T20
SHRINK_K = 60        # empirical-Bayes prior, in balls
b = pd.read_csv(f"{D}/ball_by_ball.csv")
m = pd.read_csv(f"{D}/matches.csv")
c = pd.read_csv(f"{D}/competitions.csv")[["comp_id", "match_format"]]
m = m.merge(c, on="comp_id", how="left")
b = b[b.innings.isin([1, 2])].merge(
    m[["match_id", "match_format", "knock_out", "revised_target", "first_inn_revised_overs", "second_inn_revised_overs"]], on="match_id")
b = b.sort_values(["match_id", "innings", "innings_ball_num"]).reset_index(drop=True)
b["extras_type"] = b.extras_type.fillna("")
b["total"] = b.runs + b.extras1_runs.fillna(0) + b.extras_2_runs.fillna(0)
b["legal"] = ~b.extras_type.isin(["wide", "Overstep"])
b["conceded"] = b.runs + np.where(b.extras_type.isin(["wide", "Overstep"]), b.extras1_runs.fillna(0) + b.extras_2_runs.fillna(0), 0)
dt = b.dismissal_type.fillna("").str.lower()
b["bat_out"] = b.is_wicket & (b.dismissed_player_id == b.striker_id)
b["bowl_wkt"] = b.is_wicket & ~dt.str.contains("run out|retired|obstruct")
g = b.groupby(["match_id", "innings"])
b["score_before"] = g.total.cumsum() - b.total
b["wkts_before"] = g.is_wicket.cumsum() - b.is_wicket.astype(int)
b["legal_before"] = g.legal.cumsum() - b.legal.astype(int)
ov = np.where(b.innings == 1, b.first_inn_revised_overs, b.second_inn_revised_overs)
b["max_balls"] = np.where(pd.isna(ov), 120, ov * 6)
inn1 = b[b.innings == 1].groupby("match_id").total.sum().rename("inn1_total")
b = b.merge(inn1, on="match_id", how="left")
b["target"] = np.where(b.revised_target.notna(), b.revised_target, b.inn1_total + 1)
# ---- pressure index (0..1) ----
wk = b.wkts_before / 10
late = (b.legal_before / b.max_balls).clip(0, 1)
balls_left = (b.max_balls - b.legal_before).clip(lower=1)
rrr = (b.target - b.score_before).clip(lower=0) * 6 / balls_left
req = ((rrr - 7.5) / 6).clip(0, 1)
chase = 0.55 * req + 0.25 * wk + 0.20 * late
first = 0.6 * (0.5 * wk + 0.5 * late)
b["P"] = np.where(b.innings == 2, chase, first) + 0.1 * b.knock_out.fillna(0)
b["P"] = b.P.clip(0, 1)
thr = float(b.P.quantile(0.80))
b["press"] = b.P >= thr
b["phase"] = pd.cut(b.legal_before / b.max_balls * 20, [-1, 6, 15, 21], labels=["PP", "MID", "DEATH"]).astype(str)
b["fmt"] = np.where(b.match_format == "T20I", "T20I", "LEAGUE")
cell = ["fmt", "innings", "phase", "press"]
exp = b.groupby(cell).agg(e_runs=("runs", "mean"), e_conc=("conceded", "mean"), e_out=("bat_out", "mean"), e_wkt=("bowl_wkt", "mean")).reset_index()
b = b.merge(exp, on=cell, how="left")
cmp = b.groupby("press").agg(runs_per_ball=("total", "mean"), wicket_rate=("is_wicket", "mean"), balls=("total", "size")).round(4)
bt = b[b.extras_type != "wide"].copy()
bt["imp"] = (bt.runs - bt.e_runs) - WICKET_VALUE * (bt.bat_out - bt.e_out)
bw = b.copy()
bw["imp"] = (bw.e_conc - bw.conceded) + WICKET_VALUE * (bw.bowl_wkt - bw.e_wkt)
names = pd.concat([b[["striker_id", "striker_name"]].set_axis(["id", "name"], axis=1),
                   b[["bowler_id", "bowler_name"]].set_axis(["id", "name"], axis=1)]).drop_duplicates("id").set_index("id").name

def rate(df, pid, who, min_balls, min_matches):
    rows = []
    for p, d in df.groupby(pid):
        pr, no = d[d.press], d[~d.press]
        n = len(pr)
        if n < min_balls: continue
        sz = pr.groupby("match_id").size()
        pm = pr.groupby("match_id").imp.sum()[sz >= 6]
        if len(pm) < min_matches: continue
        raw = pr.imp.mean() * 100
        shr = raw * n / (n + SHRINK_K)
        base = no.imp.mean() * 100 if len(no) >= 60 else np.nan
        r = dict(id=int(p), name=names[p], matches=int(len(pm)), pressure_balls=int(n), impact100=round(raw, 2),
                 shrunk100=round(shr, 2), consistency=round(float((pm > 0).mean()), 3),
                 lift=round(raw - base, 2) if base == base else 0.0)
        if who == "bat":
            r.update(runs=int(pr.runs.sum()), sr_pressure=round(pr.runs.sum() / n * 100, 1),
                     sr_normal=round(no.runs.sum() / max(len(no), 1) * 100, 1), outs=int(pr.bat_out.sum()))
        else:
            r.update(wickets=int(pr.bowl_wkt.sum()), econ_pressure=round(pr.conceded.sum() / n * 6, 2),
                     econ_normal=round(no.conceded.sum() / max(len(no), 1) * 6, 2))
        rows.append(r)
    o = pd.DataFrame(rows)
    z = lambda s: (s - s.mean()) / s.std()
    o["rating"] = (0.60 * z(o.shrunk100) + 0.25 * z(o.consistency) + 0.15 * z(o.lift)).round(3)
    o = o.sort_values("rating", ascending=False).reset_index(drop=True)
    o.insert(0, "rank", o.index + 1)
    return o

bat = rate(bt, "striker_id", "bat", 120, 15)
bowl = rate(bw, "bowler_id", "bowl", 120, 15)
out = dict(
    meta=dict(threshold=round(thr, 3), matches=int(b.match_id.nunique()), deliveries=int(len(b)), pressure_deliveries=int(b.press.sum()),
              eligible_batters=len(bat), eligible_bowlers=len(bowl), wicket_value=WICKET_VALUE, shrink_k=SHRINK_K,
              compare={str(k): v for k, v in cmp.to_dict("index").items()}),
    batters=bat.head(25).to_dict("records"), bowlers=bowl.head(25).to_dict("records"))
json.dump(out, open("data/rankings.json", "w"), indent=1)
print(json.dumps(out["meta"], indent=1)); print(bat.head(12).drop(columns=["id"]).to_string()); print(bowl.head(12).drop(columns=["id"]).to_string())
