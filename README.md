# FireLab: balance is not an execution

An exact finite resource-planning inspector for ordinary weighted Petri nets. A proposed firing-count vector can balance every token and still have no executable order. That does **not** necessarily make its goal unreachable: extra helper transitions may supply the missing catalyst and return it later.

The original default has initial `(A,B,R)=(0,0,2)` and goal `(0,1,1)`. Transition `t0: A+R -> A+B` has net effect `(0,+1,-1)` but still requires one A. The supplied counts `(1,0,0)` satisfy the equation and cannot execute. The same net reaches the goal with `t1,t0,t2`: borrow A from R, act, return A. A separate control removes both helpers and makes the balanced target truly unreachable.

## Inspect the complete evidence

- Every nonnegative marking of the conserved token total, every enabled/blocked transition and exact missing-token guard. Unreachable markings remain visible.
- Exact initial and goal distances, all shortest next-transition ties, shortest-prefix counts and a canonical shortest witness. Duplicate transition IDs remain distinct; no-ops are not called deadlocks.
- Every supplied-subcount vector, including negative algebraic vectors, every remaining transition decision, legal prefix/suffix counts and canonical schedules. Suffix feasibility alone does not establish a legal prefix.
- Every reachable enabling state per transition, distinguishing dead transitions from ones unused by a selected shortest plan.
- A checked all-ones place invariant that proves finite bounds without imposing artificial capacities.

Browser assets are in `docs/`; the native CLI and independent checker run without third-party runtime packages. Deployment and check status live in the repository's Actions and Pages settings; local test evidence is recorded separately in [EVIDENCE.md](EVIDENCE.md).

## Reproduce

```sh
python -m unittest discover -s tests -v
node --test tests/test_engine.cjs tests/test_browser.cjs
python tools/check_installed.py
python -m firelab run examples/borrow.json > /tmp/firelab-evidence.json
python -m firelab verify /tmp/firelab-evidence.json
python -m http.server 8000 --directory docs
# Optional external reference, isolated from the runtime:
python -m pip install pm4py==2.7.23
python tools/check_reference.py
```

Node22+ and Chrome are needed for browser tests (`CHROME_BIN` can name the executable). The installed check builds a wheel and runs both entry points outside the checkout. CLI failures return2 without partial stdout; JSON duplicate keys, floats/constants, unknown fields and bool-as-int inputs are rejected.

## Boundaries and credit

2-4 places, up to4 transitions, arc weights0-2, each transition strictly conserves token total, initial total0-3, each proposed count0-3 and sum at most8. This gives at most20 possible markings and81 subcount rows. Interleaved ordinary untimed firing, not concurrent steps, timed/colored/inhibitor nets or fairness.

Established Petri-net theory, original bounded implementations and synthetic controls. Not a new algorithm, an unrestricted integer marking-equation solver, scalable planner, deployment guarantee, benchmark win or formal proof. The generator and independent native replay share only strict input validation. Browser replay regenerates with its own browser engine and is not an independent checker. The optional PM4Py reference is installed separately and no reference code is vendored. See [MODEL.md](MODEL.md), [SOURCES.md](SOURCES.md) and [EVIDENCE.md](EVIDENCE.md).
