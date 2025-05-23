import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def visualize_vectors(vectors, output_path):
    reduced = PCA(n_components=2).fit_transform(vectors)
    plt.figure(figsize=(8, 6))
    plt.scatter(reduced[:, 0], reduced[:, 1], alpha=0.7)
    plt.title("Semantic Chunk Embeddings (PCA)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid(True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
