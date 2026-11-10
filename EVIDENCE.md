# Local reproduction evidence

Run from this source on November10,2026. These are bounded synthetic test results, not deployed-agent results. Publication, Actions and Pages status must be checked separately against their exact public commits; this file does not label unchecked jobs or assets green.

| Check | Result |
|---|---|
| Native unittest |18 tests pass, including all4704 two-place/two-transition cases defined below,350 seeded requests and all14 controls |
| Exhaustive domain |14 conservative two-place transitions whose pre/post totals are0..2; every ordered pair, all6 initial markings of total0..2, each count0..1, goal equal to reversed initial vector:196×6×4=4704 |
| Independent native replay | Full reports reconstructed without importing generation, via all-pairs shortest paths, incoming shortest-word counts and explicit legal multiset-word enumeration. Shared strict validation is disclosed. |
| Cross-language |114 full reports,629 marking rows and806 count-lattice rows agree exactly. This includes14 controls plus100 independently seeded requests. |
| Mutation rejection | All197 noninput primitive leaves in the default report are independently changed and rejected by native replay; the browser same-engine replay also rejects all197. Extra fields and bool/int substitutions are tested separately. Inputs are requests, not authenticated truth. |
| Optional real PM4Py2.7.23 |164 requests,771 full-state enabling checks,1541 transition-result checks,2834 accepted fixed-count words. Each complete initially reachable graph and exact-goal shortest distance also agrees. All nets are constructed from input arcs, not our generated incidence/edges. |
| Isolated installed0.1.0 wheel |6 module origins verified outside checkout,14 controls through2 CLI entry points;28 forged CLI reports rejected with return2 and no stdout. |
| Node / actual Chrome |4 tests pass.56 control/width views at1440,768,390,320.268 state selections,664 move rows,496 count-lattice selections,1016 remaining-count decisions. All retained tables and summary answers match native reports. |
| Trusted downloaded evidence |14 actual Chrome report-button clicks; complete downloaded bytes matched expected reports and all14 were accepted by independent native CLI. Browser input editing clears stale tables and disables evidence export before recomputation; invalid/duplicate/oversized/deep inputs stay cleared. |
| Visual check |Actual desktop hero,390px three-verdict panel and320px count-lattice/guard view inspected. No horizontal page overflow at any tested width/control. Table horizontal scrolling is intentional. |

The PM4Py check independently compares actual enabling/firing, global reachable sets, goal distances and fixed-count word counts; it does not certify every report field or formal equivalence. Cross-language parity alone is not the independent native check. Boundary control counts(2,2,2,2) produce2520 legal distinct ID words, while the zero-token zero-arc control still enables its transition. Zero-length goal plans do not make goals absorbing; no-op stalling is not a deadlock.

Commands are in README.md. `tools/check_assets.py` checks all14 browser control requests and both checked-in native example requests against native control definitions. Generated parity reports are built during tests, not checked in as self-proving fixtures. Browser tests can target an observed deployed URL with `FIRELAB_URL`; their outputs and screenshots should be compared against the same source before claiming live equivalence.
