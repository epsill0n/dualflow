import random
import csv
import matplotlib.pyplot as plt
from algorithm_stats import maxVectors

def generate_instance(m, k, capacity_range=(1,3), sparsity=0.3):
    """
    Generate a random multi-state instance.
    - m: number of edges
    - k: number of minimal path vectors
    - capacity_range: each edge's capacity chosen uniformly from this range
    - sparsity: probability that a component in a minimal path vector is non-zero
    Returns: (C, V) where C is list of capacities, V is list of lists (minimal path vectors)
    """
    C = [random.randint(capacity_range[0], capacity_range[1]) for _ in range(m)]
    V = []
    for _ in range(k):
        vec = [0]*m
        for i in range(m):
            if random.random() < sparsity:
                vec[i] = random.randint(1, C[i])
        while all(v == 0 for v in vec):
            vec = [random.randint(1, C[i]) if random.random() < sparsity else 0 for i in range(m)]
        V.append(vec)
    return C, V

def run_experiments():
    configs = [
        (10, 5),
        (10, 10),
        (12, 10),
        (12, 15),
        (15, 15)
    ]
    summary = []
    iteration_details = None

    for idx, (m, k) in enumerate(configs):
        print(f"Running m={m}, k={k}...")
        C, V = generate_instance(m, k)
        mv = maxVectors(C, V)
        stats = mv.get_stats()
        summary.append({
            'm': m,
            'k': k,
            'final_size': stats['final_output_size'],
            'runtime': stats['runtime'],
            'peak_before': stats['peak_before']
        })
        if idx == 2:
            iteration_details = {
                'iterations': stats['iterations'],
                'before': stats['before'],
                'after': stats['after']
            }

    with open('ir_summary.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['m','k','final_size','runtime','peak_before'])
        writer.writeheader()
        writer.writerows(summary)

    if iteration_details:
        with open('ir_iteration_detail.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Iteration','Before','After'])
            for i, b, a in zip(iteration_details['iterations'],
                                iteration_details['before'],
                                iteration_details['after']):
                writer.writerow([i, b, a])

    if iteration_details:
        plt.figure(figsize=(8,5))
        plt.plot(iteration_details['iterations'], iteration_details['before'], 'o-', label='Before pruning')
        plt.plot(iteration_details['iterations'], iteration_details['after'], 's-', label='After pruning')
        plt.xlabel('Iteration')
        plt.ylabel('Set size')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.title('Intermediate candidate set growth (m=12, k=10)')
        plt.tight_layout()
        plt.savefig('growth_plot.pdf')
        plt.close()

    print("Done. Results saved to ir_summary.csv, ir_iteration_detail.csv, growth_plot.pdf")

if __name__ == '__main__':
    run_experiments()