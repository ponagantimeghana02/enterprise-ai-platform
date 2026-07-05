# Retrieval Benchmark Report

|Embedding Model|Chunk Size|Overlap|Latency(s)|Accuracy|Build Time(s)|
|---|---|---|---|---|---|
|all-MiniLM-L6-v2|256|20|0.012|1.0|0.2535|
|all-MiniLM-L6-v2|256|50|0.0093|1.0|0.0201|
|all-MiniLM-L6-v2|256|100|0.0096|1.0|0.0207|
|all-MiniLM-L6-v2|512|20|0.0077|1.0|0.0181|
|all-MiniLM-L6-v2|512|50|0.0081|1.0|0.0184|
|all-MiniLM-L6-v2|512|100|0.0087|1.0|0.0182|
|all-MiniLM-L6-v2|1024|20|0.0091|1.0|0.0201|
|all-MiniLM-L6-v2|1024|50|0.0085|1.0|0.0191|
|all-MiniLM-L6-v2|1024|100|0.0077|1.0|0.0183|
|all-mpnet-base-v2|256|20|0.0508|1.0|0.7673|
|all-mpnet-base-v2|256|50|0.0462|1.0|0.114|
|all-mpnet-base-v2|256|100|0.0507|1.0|0.1188|
|all-mpnet-base-v2|512|20|0.0471|1.0|0.1062|
|all-mpnet-base-v2|512|50|0.0465|1.0|0.1059|
|all-mpnet-base-v2|512|100|0.0471|1.0|0.1099|
|all-mpnet-base-v2|1024|20|0.0534|1.0|0.1226|
|all-mpnet-base-v2|1024|50|0.0505|1.0|0.1157|
|all-mpnet-base-v2|1024|100|0.0462|1.0|0.1154|

## Best Configuration

- Embedding Model: all-MiniLM-L6-v2
- Chunk Size: 256
- Chunk Overlap: 20
- Accuracy: 1.0
- Average Latency: 0.012 sec
