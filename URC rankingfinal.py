import json
import numpy as np



with open("urc_2024_25_results.json") as f: # Load the scraped match data
    matches = json.load(f)

print(f"Loaded {len(matches)} matches.\n")



# Teams ordered by their final official standing
TEAMS = [
    "Leinster", "Bulls",    "Sharks",          "Glasgow Warriors",
    "Stormers", "Munster",  "Edinburgh",       "Scarlets",
    "Cardiff",  "Benetton", "Lions",           "Ospreys",
    "Connacht", "Ulster",   "Zebre Parma",     "Dragons",
]

OFFICIAL_PTS = [76, 68, 62, 59, 55, 51, 49, 48, 47, 46, 40, 40, 39, 38, 29, 9]

n   = len(TEAMS)
idx = {team: i for i, team in enumerate(TEAMS)}   # This function matches team names to their index in the matrix


epsilon = 0.01                                     # small value to ensure A is positive (no zero rows/columns)
A = np.full((n, n), epsilon)

for match in matches:
    home    = match["home_team"]
    away    = match["away_team"]
    h_score = match["home_score"]
    a_score = match["away_score"]
    margin  = abs(h_score - a_score)

    if h_score > a_score:                    # home win
        A[idx[home]][idx[away]] += margin

    elif a_score > h_score:                  # away win
        A[idx[away]][idx[home]] += margin

    else:                                    # draw - 0.5 each way
        A[idx[home]][idx[away]] += 0.5
        A[idx[away]][idx[home]] += 0.5


v = np.ones(n)             # Starting vector: all teams equal at the start

for k in range(500):
    v_new = A @ v       # Matrix-vector multiply: new_score[i] = sum over j of A[i][j] * v[j]
    v_new = v_new / v_new.max() # Normalise so the largest score = 1 (prevents numbers growing without bound)

    # Print this iteration
    print(f"--- Iteration {k + 1} ---")
    for i, team in enumerate(TEAMS):
        print(f"  {team:<18}  {v_new[i]:.4f}")
    print()

    if np.max(np.abs(v_new - v)) < 1e-8:   # Check for convergence: if the vector barely changed, we have our eigenvector                                            
        print(f"Converged after {k + 1} iterations.\n")
        break

    v = v_new

scores = v_new



eigen_order = np.argsort(-scores)  # Sort teams by eigenvector score, highest first
eigen_rank  = {TEAMS[i]: rank + 1 for rank, i in enumerate(eigen_order)} # Map team name to its rank in the eigenvector ordering

print(f"{'Off':>4}  {'Team':<18}  {'Pts':>4}  {'Score':>6}  {'Eigen':>5}  {'Shift'}") 
print("-" * 56)

for off_rank, (team, pts) in enumerate(zip(TEAMS, OFFICIAL_PTS), start=1): 
    e_rank = eigen_rank[team]
    score  = scores[idx[team]]
    delta  = off_rank - e_rank
    shift  = f"up {delta}" if delta > 0 else (f"dn {abs(delta)}" if delta < 0 else "-") # Describe how much the eigenvector ranking differs from the official ranking
    print(f"{off_rank:>4}  {team:<18}  {pts:>4}  {score:>6.3f}  {e_rank:>5}  {shift}")