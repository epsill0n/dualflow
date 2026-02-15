import time

class maxVectors:
    def __init__(self, C, V):
        self.V = V
        self.C = C
        self.Zsets = []
        self.MAX_VECS_PRUNED = None
        self.stats = {
            'iterations': [],      # list of iteration indices (1..k)
            'before': [],          # size before pruning at each iteration
            'after': [],           # size after pruning at each iteration
            'peak_before': 0,      # max of 'before' over all iterations
            'runtime': 0.0,
            'final_output_size': 0
        }
        self.MAX_VECS_PRUNED = self.compute()

    def remove_duplicates(self, a):
        combined = a.copy()
        unique_sets = []
        seen = set()
        for item in combined:
            t = tuple(item)
            if t not in seen:
                seen.add(t)
                unique_sets.append(item)
        return unique_sets

    def g(self, a):
        return max(0, a - 1)

    def getZSet(self, vec):
        Zset = []
        for comp in range(len(vec)):
            if vec[comp] != 0:
                Zvec = self.C.copy()
                Zvec[comp] = self.g(vec[comp])
                Zset.append(Zvec)
        return Zset

    def minVec(self, a, b):
        return [min(a[i], b[i]) for i in range(len(a))]

    def isDominated(self, x, y):
        # returns  1 if x dominates y
        #         -1 if y dominates x
        #          0 if incomparable
        flagx = True
        flagy = True
        for i in range(len(x)):
            if x[i] < y[i]:
                flagx = False
            elif x[i] > y[i]:
                flagy = False
        if flagx and not flagy:
            return 1
        if not flagx and flagy:
            return -1
        return 0

    def pruneSet(self, Q):
        i = 0
        while i < len(Q):
            j = 0
            remove_i = False
            while j < len(Q):
                if i != j:
                    isDom = self.isDominated(Q[i], Q[j])
                    if isDom == -1:          # Q[i] dominated by Q[j]
                        remove_i = True
                        break
                    elif isDom == 1:          # Q[i] dominates Q[j]
                        Q.pop(j)
                        if j < i:
                            i -= 1
                        continue
                j += 1
            if remove_i:
                Q.pop(i)
            else:
                i += 1
        return Q

    def compute(self):
        start_time = time.time()

        # Build all Z-sets
        Zsets = []
        for vec in self.V:
            Zsets.append(self.getZSet(vec))
        self.Zsets = Zsets

        if not Zsets:
            self.stats['runtime'] = time.time() - start_time
            return []

        # Start with the first Z-set (iteration 1)
        current = Zsets[0]
        self.stats['iterations'].append(1)
        self.stats['before'].append(len(current))
        self.stats['after'].append(len(current))
        self.stats['peak_before'] = len(current)

        # Process remaining Z-sets
        for j in range(1, len(Zsets)):
            # Cartesian product and min
            combined = []
            for u in current:
                for v in Zsets[j]:
                    combined.append(self.minVec(u, v))
            before = len(combined)
            # Prune
            pruned = self.pruneSet(combined)
            after = len(pruned)
            # Record
            self.stats['iterations'].append(j + 1)
            self.stats['before'].append(before)
            self.stats['after'].append(after)
            if before > self.stats['peak_before']:
                self.stats['peak_before'] = before
            current = pruned

        self.stats['final_output_size'] = after
        self.stats['runtime'] = time.time() - start_time
        return current

    def get_max_vectors(self):
        return self.MAX_VECS_PRUNED

    def get_stats(self):
        return self.stats