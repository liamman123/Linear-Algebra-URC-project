# Who Really Finished Where?
### Using Linear Algebra to Re-rank the 2024–25 URC Season

*MA283 Linear Algebra Project — University of Galway, 2024–25*

---

## Overview

The United Rugby Championship (URC) ranks its 16 teams using a points system: 4 for a win, 2 for a draw, plus bonus points. It's simple and transparent, but it treats all wins equally — beating Leinster earns the same 4 points as beating Dragons, regardless of the margin.

This project asks: **what if we ranked teams by the quality of who they beat, not just that they beat them?**

The answer comes from linear algebra. We build a **dominance matrix** from the season's 144 match results, where each entry encodes the point margin of a win. We then find the **dominant eigenvector** of that matrix using **power iteration**. The entries of that eigenvector give a quality-adjusted ranking, grounded in the **Perron-Frobenius theorem**, which guarantees the process converges to a unique positive solution.

The same mathematical idea underlies Google's PageRank algorithm.

---

## Files

| File | Description |
|---|---|
| `urc_ranking.py` | Main script — builds the matrix, runs power iteration, prints results |
| `urc_2024_25_results.json` | All 144 regular-season match results |
| `urc_scraper.py` | Optional — scrapes match data directly from Wikipedia |

---

## How to Run

**1. Install the only dependency**

```bash
pip install numpy
```

**2. Make sure the JSON file is in the same folder as the script**

```
your-folder/
├── urc_ranking.py
└── urc_2024_25_results.json
```

**3. Run it**

```bash
python urc_ranking.py
```

**Expected output:**

```
Loaded 144 matches.

Matrix built.
  Shape : (16, 16)
  Min   : 0.01
  Max   : 71.0

Converged after 21 iterations.

 Off  Team                Pts   Score  Eigen  Shift
------------------------------------------------------
   1  Leinster             76   1.000      1  —
   2  Bulls                68   0.530      5  dn 3
   3  Sharks               62   0.464      8  dn 5
   4  Glasgow Warriors     59   0.756      2  up 2
   5  Stormers             55   0.664      3  up 2
   6  Munster              51   0.383     11  dn 5
  ...
```

---

## How it Works

### Step 1 — Build the matrix

We create a 16×16 matrix **A** where entry `A[i][j]` is the point margin by which team *i* beat team *j* over the season. If team *i* lost to team *j*, the entry stays at a small constant ε = 0.01.

```python
epsilon = 0.01
A = np.full((n, n), epsilon)

for match in matches:
    if home_score > away_score:
        A[idx[home]][idx[away]] += margin
```

The ε ensures every entry is strictly positive, which is required for the Perron-Frobenius theorem to apply.

### Step 2 — Power iteration

We start with an equal score vector (all ones) and repeatedly multiply by **A**, renormalising after each step:

```python
v = np.ones(n)

for k in range(500):
    v_new = A @ v
    v_new = v_new / v_new.max()

    if np.max(np.abs(v_new - v)) < 1e-8:
        break

    v = v_new
```

Each multiplication updates a team's score to reflect the quality of the opponents it beat. The **Perron-Frobenius theorem** guarantees this converges to a unique dominant eigenvector — regardless of the starting vector.

### Step 3 — Read off the ranking

The final vector `v` contains a score for each team between 0 and 1. Sorting by these scores gives the eigenvector ranking.

---

## Results

The code converges in **21 iterations**. Key findings:

- **Leinster** unchanged at 1st — dominant across the board
- **Glasgow Warriors** rise from 4th to 2nd (score 0.756) — their wins came against strong opposition by large margins
- **Stormers** rise from 5th to 3rd (score 0.664)
- **Bulls** drop from 2nd to 5th — many big wins came against weaker sides
- **Sharks** drop from 3rd to 8th — similar pattern, largely within the South African pool
- **Munster** drop from 6th to 11th — wins concentrated against lower-ranked teams
- **Benetton** and **Lions** both rise 4 places — wins against stronger opposition than their official rank suggests

---

## The Maths

The method works because of the **Perron-Frobenius theorem**: any strictly positive square matrix has a unique largest real eigenvalue, and a corresponding eigenvector with all positive entries. Power iteration converges to this eigenvector from any positive starting point.

Adding ε = 0.01 to every matrix entry is the same trick used in Google's PageRank — it makes the matrix strictly positive so the theorem applies, even if some matchups theoretically never occurred (in this dataset, every team played every other team at least once, so the ε was precautionary).

The connection to PageRank is exact: a webpage is important if important pages link to it; a rugby team is strong if strong teams lose to it. The eigenvector captures both recursively.

---

## Data

The JSON file contains all 144 URC regular-season matches from the 2024–25 season (rounds 1–18). Each entry looks like:

```json
{
  "round": 1,
  "date": "20 September 2024",
  "home_team": "Cardiff",
  "home_score": 22,
  "away_score": 17,
  "away_team": "Zebre Parma",
  "home_bp": true,
  "away_bp": true,
  "venue": "Cardiff Arms Park, Cardiff"
}
```

Win counts for all 16 teams were verified against the official final standings before the analysis was run.

---

## References

- Bryan, K. & Leise, T. (2006). The $25,000,000,000 eigenvector: the linear algebra behind Google. *SIAM Review*, 48(3), 569–581.
- Cornell University. (2009). PageRank algorithm — the mathematics of Google search. `pi.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture3/lecture3.html`
- Gregory, D.A. & Kirkland, S.J. (1999). Singular values of tournament matrices. *Electronic Journal of Linear Algebra*, 5, 39–52.
- Wikipedia. Perron–Frobenius theorem. `en.wikipedia.org/wiki/Perron-Frobenius_theorem`
- 2024–25 United Rugby Championship results. Wikipedia. `en.wikipedia.org/wiki/2024-25_United_Rugby_Championship`
