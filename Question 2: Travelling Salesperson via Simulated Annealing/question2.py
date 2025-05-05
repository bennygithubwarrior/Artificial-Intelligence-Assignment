import random    # for random shuffling and sampling
import math      # for exponential and trigonometry
import matplotlib.pyplot as plt  # for plotting results
import numpy as np             # for numerical operations

class TSP:
    def __init__(self, towns, dist_matrix):
        self.towns = towns          # list of town names
        self.dist = dist_matrix     # distance lookup table

    def total_distance(self, route):
        """Compute the total distance of a given route."""
        d = 0.0
        for i in range(len(route) - 1):
            a, b = route[i], route[i+1]
            # look up distance between consecutive towns
            d += self.dist[self.towns.index(a)][self.towns.index(b)]
        return d

class SimulatedAnnealingSolver:
    def __init__(self, tsp, T0=10000, alpha=0.995, stopping_T=1e-3, max_iters=100000):
        self.tsp = tsp              # TSP problem instance
        self.T0 = T0                # initial temperature
        self.alpha = alpha          # cooling rate
        self.stopping_T = stopping_T# temperature threshold to stop
        self.max_iters = max_iters  # maximum iterations

    def _initial_route(self):
        """Generate a random starting route (Windhoek fixed endpoints)."""
        mids = self.tsp.towns[1:]
        random.shuffle(mids)
        return ['Windhoek'] + mids + ['Windhoek']

    def _neighbor(self, route):
        """Create a neighbor by swapping two intermediate towns."""
        r = route[1:-1][:]         # copy intermediate segment
        i, j = random.sample(range(len(r)), 2)
        r[i], r[j] = r[j], r[i]
        return ['Windhoek'] + r + ['Windhoek']

    def solve(self):
        """Run simulated annealing to find a near-optimal TSP route."""
        current = self._initial_route()
        initial_route = list(current)
        curr_cost = self.tsp.total_distance(current)
        best, best_cost = list(current), curr_cost

        history = [best_cost]
        T, it = self.T0, 0

        while T > self.stopping_T and it < self.max_iters:
            candidate = self._neighbor(current)
            cand_cost = self.tsp.total_distance(candidate)
            delta = cand_cost - curr_cost

            # accept if better or by Metropolis criterion
            if delta < 0 or random.random() < math.exp(-delta / T):
                current, curr_cost = candidate, cand_cost
                if curr_cost < best_cost:
                    best, best_cost = list(current), curr_cost

            history.append(best_cost)
            T *= self.alpha  # cool down
            it += 1

        return {
            'initial_route': initial_route,
            'initial_cost': self.tsp.total_distance(initial_route),
            'best_route': best,
            'best_cost': best_cost,
            'history': history
        }

def main():
    # list of Namibian towns for the TSP
    towns = [
        'Windhoek', 'Swakopmund', 'Walvis Bay', 'Otjiwarongo', 'Tsumeb',
        'Grootfontein', 'Mariental', 'Keetmanshoop', 'Ondangwa', 'Oshakati'
    ]
    # symmetric distance matrix between towns
    dist_matrix = [
        [0,    361,  395,  249,  433,  459,  268,  497,  678,  712],
        [361,  0,    35.5, 379,  562,  589,  541,  859,  808,  779],
        [395,  35.5, 0,    413,  597,  623,  511,  732,  884,  855],
        [249,  379,  413,  0,    260,  183,  519,  768,  514,  485],
        [433,  562,  597,  260,  0,    60,   682,  921,  254,  288],
        [459,  589,  623,  183,  60,   0,    708,  947,  308,  342],
        [268,  541,  511,  519,  682,  708,  0,    231,  909,  981],
        [497,  859,  732,  768,  921,  947,  231,  0,    1175, 1210],
        [678,  808,  884,  514,  254,  308,  909,  1175, 0,    30 ],
        [712,  779,  855,  485,  288,  342,  981,  1210, 30,   0  ]
    ]

    tsp = TSP(towns, dist_matrix)
    solver = SimulatedAnnealingSolver(tsp, T0=10000, alpha=0.995, stopping_T=1e-3, max_iters=200000)
    result = solver.solve()

    # display initial and best routes with their costs
    print("Initial route:")
    print(" → ".join(result['initial_route']))
    print("Initial route cost:", result['initial_cost'], "\n")
    print("Best route found:")
    print(" → ".join(result['best_route']))
    print("Best route cost:", result['best_cost'])

    # plot convergence history
    plt.figure()
    plt.plot(result['history'])
    plt.xlabel('Iteration')
    plt.ylabel('Best cost so far')
    plt.title('Simulated Annealing Convergence')
    plt.grid(True)

    # simple circular layout for route visualization
    angles = np.linspace(0, 2 * np.pi, len(towns), endpoint=False)
    coords = {town: (math.cos(a), math.sin(a)) for town, a in zip(towns, angles)}
    xs = [coords[t][0] for t in result['best_route']]
    ys = [coords[t][1] for t in result['best_route']]

    plt.figure()
    plt.plot(xs, ys, marker='o')
    for town, (x, y) in coords.items():
        plt.text(x, y, town, ha='center', va='center')
    plt.title('Best Route Visualization')
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    main()
