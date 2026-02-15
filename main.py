from algorithm import maxVectors

if __name__ == '__main__':
    capacities = [2, 2, 2, 2, 1]
    min_vectors = [
        [2, 2, 0, 0, 0],
        [0, 0, 2, 2, 0],
        [1, 1, 1, 1, 0],
        [2, 1, 0, 1, 1],
        [0, 2, 1, 1, 1],
        [0, 1, 2, 1, 1],
        [1, 0, 1, 2, 1]
    ]

    MV = maxVectors(capacities, min_vectors)
    max_vectors = MV.get_max_vectors()

    print('MAX Vectors:')
    for vec in max_vectors:
        print(vec)