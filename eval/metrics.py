"""Page and evidence-need retrieval metrics. No generation or judge dependencies."""
from pathlib import PurePath


def page_pair(ref):
    """Missing/malformed references never match; their original rank remains occupied."""
    if not isinstance(ref, dict):
        return None
    source, page = ref.get('source'), ref.get('page')
    if not isinstance(source, str) or not source or type(page) is not int or page < 0:
        return None
    return PurePath(source.replace('\\', '/')).name, page


def score_question(ranked, gold, annotation, ks=(1, 3, 5, 12)):
    """Score prefixes of one fixed ranking; MRR is truncated at its supplied depth."""
    relevant = {page_pair(r) for r in gold}
    if not relevant or None in relevant:
        raise ValueError('Recall requires nonempty valid gold references; exclude negatives')
    needs = annotation.get('needs', [])
    if not needs:
        raise ValueError('Answerable question requires evidence needs')
    for need in needs:
        if not need.get('any_of'):
            raise ValueError('Need has no support routes')
        for route in need['any_of']:
            if not route.get('all_of') or any(page_pair(r) is None for r in route['all_of']):
                raise ValueError('Invalid support bundle')
    pairs = [page_pair(r) for r in ranked]
    result = {'mrr': next((1 / i for i, p in enumerate(pairs, 1) if p in relevant), 0.0)}
    for k in ks:
        if k < 1:
            raise ValueError('k must be positive')
        covered = set(pairs[:k]) - {None}
        hits = len(covered & relevant)
        satisfied = [any({page_pair(r) for r in route['all_of']} <= covered
                         for route in need['any_of']) for need in needs]
        result.update({f'hit@{k}': float(hits > 0), f'recall@{k}': hits / len(relevant),
                       f'need_coverage@{k}': sum(satisfied) / len(needs),
                       f'all_needs@{k}': float(all(satisfied))})
    return result


def summarize(rows, samples=10000, seed=42, confidence=0.95):
    """Macro means and percentile CIs. Shared question resamples preserve metric covariance."""
    import numpy as np
    if not rows:
        return {'n': 0, 'metrics': {}}
    if samples < 1 or not 0 < confidence < 1:
        raise ValueError('Invalid bootstrap parameters')
    names = sorted(rows[0])
    if any(set(row) != set(names) for row in rows):
        raise ValueError('Inconsistent metric columns')
    matrix = np.array([[row[n] for n in names] for row in rows], dtype=float)
    indices = np.random.default_rng(seed).integers(0, len(rows), (samples, len(rows)))
    means = matrix[indices].mean(axis=1)
    tail = (1 - confidence) / 2
    bounds = np.quantile(means, [tail, 1-tail], axis=0, method='linear')
    return {'n': len(rows), 'metrics': {name: {'mean': float(matrix[:, j].mean()),
             'ci95': [float(bounds[0, j]), float(bounds[1, j])]} for j, name in enumerate(names)}}
