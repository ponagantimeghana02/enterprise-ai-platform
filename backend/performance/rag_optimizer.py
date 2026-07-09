import random
import time
from dataclasses import dataclass
from typing import List


# ----------------------------------------------------
# Benchmark Configuration
# ----------------------------------------------------

@dataclass
class RAGConfig:

    chunk_size: int
    overlap: int
    embedding_model: str
    top_k: int
    hybrid_weight: float
    rerank_threshold: float


@dataclass
class BenchmarkResult:

    config: RAGConfig

    accuracy: float
    latency: float
    tokens: int
    estimated_cost: float


# ----------------------------------------------------
# Optimizer
# ----------------------------------------------------

class RAGOptimizer:

    def __init__(self):

        self.results: List[BenchmarkResult] = []

    # ------------------------------------------

    def simulate_retrieval(self, config: RAGConfig):

        start = time.perf_counter()

        # Simulate retrieval
        time.sleep(random.uniform(0.05, 0.20))

        latency = time.perf_counter() - start

        # ------------------------
        # Simulated Metrics
        # ------------------------

        accuracy = (
            75
            + config.top_k * 1.5
            + config.hybrid_weight * 6
            - config.rerank_threshold * 3
            + random.uniform(-2, 2)
        )

        accuracy = min(99, accuracy)

        tokens = (
            config.chunk_size // 2
            * config.top_k
        )

        estimated_cost = tokens * 0.000002

        return BenchmarkResult(

            config=config,

            accuracy=round(accuracy, 2),

            latency=round(latency * 1000, 2),

            tokens=tokens,

            estimated_cost=round(
                estimated_cost,
                5
            )
        )

    # ------------------------------------------

    def run(self):

        chunk_sizes = [256, 512, 1024]

        overlaps = [32, 64, 128]

        embedding_models = [

            "all-MiniLM-L6-v2",

            "bge-small-en",

            "all-mpnet-base-v2"
        ]

        top_k_values = [3, 5, 10]

        hybrid_weights = [

            0.3,

            0.5,

            0.7
        ]

        rerank_thresholds = [

            0.4,

            0.6,

            0.8
        ]

        for chunk in chunk_sizes:

            for overlap in overlaps:

                for model in embedding_models:

                    for topk in top_k_values:

                        for hybrid in hybrid_weights:

                            for threshold in rerank_thresholds:

                                config = RAGConfig(

                                    chunk_size=chunk,

                                    overlap=overlap,

                                    embedding_model=model,

                                    top_k=topk,

                                    hybrid_weight=hybrid,

                                    rerank_threshold=threshold
                                )

                                result = self.simulate_retrieval(config)

                                self.results.append(result)

    # ------------------------------------------

    def print_best(self):

        best = max(
            self.results,
            key=lambda x: x.accuracy
        )

        print("\nBEST CONFIGURATION\n")

        print(best)

    # ------------------------------------------

    def benchmark_table(self):

        print()

        print("-" * 140)

        print(
            f"{'Chunk':<10}"
            f"{'Overlap':<10}"
            f"{'Embedding':<25}"
            f"{'TopK':<8}"
            f"{'Hybrid':<10}"
            f"{'Threshold':<12}"
            f"{'Accuracy':<12}"
            f"{'Latency(ms)':<15}"
            f"{'Tokens':<12}"
            f"{'Cost($)':<10}"
        )

        print("-" * 140)

        for r in self.results:

            print(

                f"{r.config.chunk_size:<10}"

                f"{r.config.overlap:<10}"

                f"{r.config.embedding_model:<25}"

                f"{r.config.top_k:<8}"

                f"{r.config.hybrid_weight:<10}"

                f"{r.config.rerank_threshold:<12}"

                f"{r.accuracy:<12}"

                f"{r.latency:<15}"

                f"{r.tokens:<12}"

                f"{r.estimated_cost:<10}"

            )


# ----------------------------------------------------

if __name__ == "__main__":

    optimizer = RAGOptimizer()

    optimizer.run()

    optimizer.benchmark_table()

    optimizer.print_best()