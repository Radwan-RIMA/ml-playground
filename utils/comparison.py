import pandas as pd
import numpy as np
from utils.models import MODEL_REGISTRY


def build_comparison_table(results: dict) -> pd.DataFrame:
    """Build a summary DataFrame from a dict of {model_name: metrics_dict}."""
    rows = []
    for name, res in results.items():
        rows.append({
            "Model": name,
            "Accuracy": f"{res.get('accuracy', 0)*100:.1f}%",
            "Precision": f"{res.get('precision', 0)*100:.1f}%",
            "Recall": f"{res.get('recall', 0)*100:.1f}%",
            "F1-Score": f"{res.get('f1', 0)*100:.1f}%",
            "Training Time": f"{res.get('training_time', 0):.4f}s",
            "Best For": MODEL_REGISTRY.get(name, {}).get("best_for", "—"),
        })
    return pd.DataFrame(rows)


def recommend_model(results: dict) -> str:
    """Return the name of the model with the best F1 score."""
    best = max(results, key=lambda n: results[n].get("f1", 0))
    return best


def pareto_frontier(results: dict):
    """Return list of model names on the accuracy/speed Pareto frontier."""
    names = list(results.keys())
    accs = np.array([results[n].get("accuracy", 0) for n in names])
    times = np.array([results[n].get("training_time", 1e-6) for n in names])

    pareto = []
    for i, name in enumerate(names):
        dominated = False
        for j in range(len(names)):
            if i == j:
                continue
            if accs[j] >= accs[i] and times[j] <= times[i] and (accs[j] > accs[i] or times[j] < times[i]):
                dominated = True
                break
        if not dominated:
            pareto.append(name)
    return pareto
