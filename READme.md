# Who Really Finished Where?
### Using Linear Algebra to Re-rank the 2024–25 URC Season

*MA283 Linear Algebra Project - Liam McNamee, University of Galway, 2024–25*

---

## What this project is

The URC ranks teams by league points, treating all wins equally. This project builds an alternative ranking using the **dominant eigenvector** of a weighted dominance matrix, where each entry represents the point margin of a win. The approach is grounded in the **Perron-Frobenius theorem** and uses the same mathematical idea as Google's PageRank algorithm.

## Files

| File | Description |
|---|---|
| `URC rankingfinal.py` | Builds the matrix and runs power iteration |
| `urc_2024_25_results.json` | All 144 regular-season match results |
| `URC Linear ALgebra` | Full project write-up |

## How to run

```bash
pip install numpy
python urc_ranking.py
```

Both files must be in the same folder.

## References

- Bryan & Leise (2006). The $25,000,000,000 eigenvector. *SIAM Review*, 48(3).
- Cornell University. The mathematics of Google search. `pi.math.cornell.edu`
- Gregory & Kirkland (1999). Singular values of tournament matrices. *Electronic Journal of Linear Algebra*, 5.
- Wikipedia. Perron–Frobenius theorem.
