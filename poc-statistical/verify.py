import json, hashlib, math, random, sys

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
def sha256(data):
    return hashlib.sha256(data).hexdigest()
def verify_merkle(leaf_hex, proof, root_hex):
    h = bytes.fromhex(leaf_hex)
    for p in proof:
        s = bytes.fromhex(p["hash"])
        h = hashlib.sha256(s+h if p["side"]=="L" else h+s).digest()
    return h.hex() == root_hex

def verify(path):
    c=json.load(open(path,encoding="utf-8"))
    roots=c["commitments"]
    seed=c["sampling"]["beacon_seed"]
    n=c["sampling"]["n"]
    N=c["config"]["N"]

    # Re-derive selected indices from public seed.
    rr=random.Random(int(seed,16))
    expected=sorted(rr.sample(range(N),n))
    if expected != c["sampling"]["indices"]:
        return False,"sample indices do not match beacon seed"

    losses=[]
    for op in c["openings"]:
        i=op["index"]
        rec=op["record"]
        # Recompute committed leaves, not merely trust fields in certificate.
        eval_leaf=sha256(canonical({"id":rec["id"],"x":rec["x"]}))
        out_leaf=sha256(canonical(rec))
        if eval_leaf != op["eval_leaf"]:
            return False,f"evaluation leaf mismatch at {i}"
        if out_leaf != op["teacher_output_leaf"]:
            return False,f"teacher output leaf mismatch at {i}"
        if not verify_merkle(eval_leaf,op["eval_proof"],roots["evaluation_merkle_root"]):
            return False,f"bad evaluation Merkle proof at {i}"
        if not verify_merkle(out_leaf,op["teacher_output_proof"],roots["teacher_output_merkle_root"]):
            return False,f"bad teacher-output Merkle proof at {i}"
        expected_loss=int(op["student_y"] != rec["teacher_y"])
        if expected_loss != op["loss"]:
            return False,f"loss mismatch at {i}"
        losses.append(expected_loss)

    d=sum(losses)/n
    delta=c["statistics"]["delta"]
    rad=math.sqrt(math.log(1/delta)/(2*n))
    ub=min(1.0,d+rad)
    if abs(d-c["statistics"]["empirical_disagreement"]) > 1e-12:
        return False,"empirical statistic mismatch"
    if abs(ub-c["statistics"]["hoeffding_upper_bound"]) > 1e-12:
        return False,"Hoeffding bound mismatch"
    return True,{"empirical_disagreement":d,"upper_bound":ub,"delta":delta}

if __name__=="__main__":
    ok,msg=verify(sys.argv[1] if len(sys.argv)>1 else "certificate.json")
    print("VALID" if ok else "INVALID",msg)
    raise SystemExit(0 if ok else 1)
