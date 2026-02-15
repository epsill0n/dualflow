class maxVectors:
    def __init__(self, C, V):
        self.V = V
        self.C = C
        self.Zsets = []
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
        # Build all Z-sets
        Zsets = []
        for vec in self.V:
            Zsets.append(self.getZSet(vec))
        self.Zsets = Zsets

        if not Zsets:
            return []

        # Start with the first Z-set
        current = Zsets[0]

        # Process remaining Z-sets
        for j in range(1, len(Zsets)):
            # Cartesian product and min
            combined = []
            for u in current:
                for v in Zsets[j]:
                    combined.append(self.minVec(u, v))
            # Prune
            current = self.pruneSet(combined)

        return current

    def get_max_vectors(self):
        return self.MAX_VECS_PRUNED