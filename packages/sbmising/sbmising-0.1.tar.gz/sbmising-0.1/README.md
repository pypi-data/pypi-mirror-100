# SBM Ising
This repository uses Ising model (simulated annealing) to recover labels of stochastic block model.

## Note
The code in this repository can only recover symmetric SBM.
Symmetric SBM means that the communities have equal size.

The SBM generator is $\textrm{SBM}(n, k, \frac{a \log n}{n}, \frac{b \log n}{n})$.

## Sample code
```Python
from sbmising import SIBM, sbm_graph
G = sbm_graph(100, 2, 16, 4)
X = SIBM(G, k=2)
print(X)
```

## Reference
[1] Zhao, Feng, Min Ye, and Shao-Lun Huang. "Exact Recovery of Stochastic Block Model by Ising Model." Entropy 23.1 (2021): 65.