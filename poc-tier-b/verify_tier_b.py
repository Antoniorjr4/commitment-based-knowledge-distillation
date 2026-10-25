import json, hashlib, numpy as np, sys
def canon(o): return json.dumps(o,sort_keys=True,separators=(",",":")).encode()
def h(b): return hashlib.sha256(b).hexdigest()
def row_leaf(i,row): return h(canon({"row":int(i),"values":[int(v) for v in row]}))
def vm(leaf,proof,root):
    x=bytes.fromhex(leaf)
    for p in proof:
        s=bytes.fromhex(p["hash"])
        x=hashlib.sha256(s+x if p["side"]=="L" else x+s).digest()
    return x.hex()==root
r=json.load(open(sys.argv[1] if len(sys.argv)>1 else "tier_b_results.json"))
a=r["single_step_arbitration"]
leaf=row_leaf(a["row"],a["weight_row"])
ok=(leaf==a["weight_row_leaf"] and vm(leaf,a["weight_merkle_proof"],a["weight_root"]))
print("MERKLE_OPENING_VALID" if ok else "INVALID_OPENING")
print("isolated transition:",r["binary_bisection"]["isolated_transition"])
print("publisher claim:",a["publisher_claimed_output"],"arbiter recomputation:",a["computed_output"])
print("verdict:",a["verdict"] if ok else "UNRESOLVED")
