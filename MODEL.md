# FireLab model and execution rules

## Ordinary net semantics

Input has exactly `version=1`, `places`, `initial`, `goal`, `transitions` and `counts`. Places are positional integers. Each transition has exactly `pre` and `post` nonnegative integer vectors. A transition is enabled iff the marking dominates its entire pre-vector; firing first consumes all pre-tokens then produces all post-tokens. Shared pre/post arcs do not disappear from the enabling test, even if they cancel in the incidence column. A zero-arc transition is enabled even at zero tokens. Positional duplicate transitions remain distinct action identities.

2<=places<=4, 0<=transitions<=4, arc entries 0..2, sum(pre)=sum(post) for every transition. Initial entries 0..3 with sum<=3; goal entries 0..3 need not have the same total. Counts match transition length, each 0..3, sum<=8. Only strict integers, not bools, decimals, constants or coercions. Unknown/missing fields and duplicate JSON keys are rejected. Native input size 64 KiB and report size 8 MiB. Browser editable input 64 KiB. Neither engine mutates the supplied request.

## Complete ordinary state graph

The all-ones vector annihilates every incidence column C=post-pre. Thus every reachable marking is nonnegative and has the initial total T; each place is bounded by T without an extra capacity rule. Enumerate every such marking in lexicographic vector order. With 4 places and T=3 there are 20. All enabled transition edges, including self-loops and duplicate-ID parallel edges, are retained.

BFS from initial and reverse BFS from the exact goal yield shortest distances. A goal with another total is absent, not silently projected. A goal remains a nonterminal marking in the graph. Distance null means unreachable, 0 is the empty sequence. Shortest-prefix counts count distinct transition-ID words at minimum length; canonical witnesses are lexicographically smallest ID words among shortest words. `optimal_next` keeps every edge whose goal distance decreases by 1. Its empty list at the goal is a shortest-path statement, not a ban on subsequent firings. Deadlock means no enabled transition, independent of whether a goal is reached. A dead transition has no enabling state in the initially reachable region, not merely no use by the canonical plan. Activity prefixes are the lexicographically least minimum-length enabling prefixes.

## Fixed-count lattice

For each vector k with 0<=k<=counts, retain its unique algebraic vector m(k)=initial+Ck. Rows sort by (sum(k),lex(k)). Entries can be negative; such rows are not ordinary markings. Retain every remaining transition j with k[j]<counts[j], its target k+e_j, every positive pre-token deficit and whether the entire current vector is nonnegative and the guard holds. Negative rows cannot fire even when an empty pre-vector would otherwise look satisfied.

`prefix_count` counts every distinct legal word using exactly k from initial. `suffix_count` counts every distinct legal word using exactly counts-k starting at this row's marking, regardless of whether that marking has a legal prefix. Empty prefix/suffix is one valid word at a nonnegative marking. Repeated occurrences of the same ID are indistinguishable: counts(2,2,2,2) yield 8!/(2!^4)=2520 words when all four no-ops are enabled, not 8! labeled permutations. Canonical prefix/suffix is the lexicographically smallest legal word, with no length optimization needed because all words use the same multiset. At most 81 rows under the coupled count bounds, attained at (2,2,2,2).

`balance` means the supplied complete count vector lands exactly at goal. `count_realizable` means some legal ordering uses that vector, regardless of its endpoint. `count_goal_schedule_count` is zero unless balance holds. `goal_reachable` is decided by the complete ordinary graph with arbitrary counts, not by a bounded count search. In particular fixed-count failure cannot establish global unreachability. No unrestricted integer feasibility computation is claimed. Only the all-ones invariant is returned; it is not called a full invariant basis.

## Replay and trust

Native generation uses BFS/reverse BFS and forward/backward lattice DP. Separate native replay recursively distributes token totals, builds ordinary firing results with a token bag, uses Floyd-Warshall plus incoming-shortest recursion, and independently enumerates transition-ID words for each partial and residual multiset. It imports input validation only, not the engine. It reconstructs every field and compares exact recursive types, including booleans versus integers. Browser implementation uses all-pairs distances and its own lattice DP. Browser replay uses that same implementation, so is not an independent verifier. All share this written contract and controls. Reports are unsigned, not authenticated claims about real systems. Tests and cross-engine agreement are evidence, not machine-checked mathematical proof.
