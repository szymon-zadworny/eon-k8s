# Kubernetes-based EON testing
This repository contains a generator for Kubernetes-based simulation scenarios.

To use it first generate a scenario:
```
$ uv run generate.py <time_step> <node_count>
```

Then apply it:
```
# kubectl apply -k scenario
```
