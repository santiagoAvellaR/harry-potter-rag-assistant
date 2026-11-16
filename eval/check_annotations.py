"""Validate phase-1b review artifacts without retrieval, model calls or metrics."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'eval'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-pdfs', action='store_true')
    args = parser.parse_args()
    raw = (EVAL / 'questions.jsonl').read_bytes()
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines()]
    side = read_json(EVAL / 'evidence_annotations.json')
    changes = read_json(EVAL / 'phase1b_changes.json')
    manifest = read_json(EVAL / 'corpus_manifest.json')
    books = {b['source']: b for b in manifest['books']}
    by_id = {q['id']: q for q in rows}
    baseline_raw = subprocess.check_output(
        ['git', 'show', '4c63bc9:eval/questions.jsonl'], cwd=ROOT)
    before = [json.loads(line) for line in baseline_raw.decode('utf-8').splitlines()]
    require(len(rows) == len(by_id) == 60, 'Expected 60 unique preserved IDs')
    require([q['id'] for q in rows] == [q['id'] for q in before], 'IDs/order changed')
    require(len({q['question'] for q in rows}) == 60, 'Duplicate question')
    require(side['schema_version'] == 1 and side['audit_baseline'] == '4c63bc9',
            'Wrong schema/baseline')
    require(side['selection_status'] == 'proposed_for_human_review', 'Wrong state')
    require(side['questions_sha256'] == digest(raw), 'Stale sidecar binding')
    require(changes['before_questions_sha256'] == digest(baseline_raw), 'Wrong baseline hash')
    require(changes['after_questions_sha256'] == digest(raw), 'Stale change log')
    expected_changes = []
    references = set()

    def check_ref(ref):
        require(set(ref) == {'source', 'page'}, 'Invalid reference schema')
        source, page = ref['source'], ref['page']
        require(source in books and type(page) is int, 'Invalid source/page type')
        require(0 <= page < books[source]['pages'], 'Out-of-range page')
        references.add((source, page))
        return source, page

    fields = {'id', 'question', 'category', 'gold_answer', 'gold_pages', 'notes', 'status'}
    for old, q in zip(before, rows):
        require(set(q) == fields and q['status'] == 'candidate', 'Schema/status mismatch')
        require(q['category'] == old['category'], 'Category changed')
        require(q['gold_pages'] == old['gold_pages'], 'Historical flat references changed')
        for key in ('id', 'question', 'category', 'gold_answer', 'notes'):
            require(isinstance(q[key], str) and q[key].strip(), 'Empty field')
        require(bool(q['gold_pages']) == (q['category'] != 'unanswerable'), 'Gold/negative mismatch')
        pairs = [check_ref(r) for r in q['gold_pages']]
        require(len(pairs) == len(set(pairs)), 'Duplicate flat reference')
        if old != q:
            expected_changes.append({'id': q['id'], 'fields': {
                k: {'before': old[k], 'after': q[k]} for k in q if q[k] != old[k]}})
    require(changes['changes'] == expected_changes, 'Change log differs from actual changes')
    require({c['id'] for c in expected_changes} == {
        'F01', 'F09', 'M02', 'M03', 'M05', 'M08', 'M11', 'C03', 'C06', 'C09', 'P06'},
        'Unexpected edited candidate')
    selected = side['proposed_ids']
    excluded = side['excluded_ids']
    require(len(selected) == len(set(selected)) == 45, 'Expected 45 proposed IDs')
    require(len(excluded) == len(set(excluded)) == 15, 'Excluded IDs mismatch')
    require(set(selected).isdisjoint(excluded) and set(selected) | set(excluded) == set(by_id),
            'Selection is not a partition')
    require('U04' in excluded, 'U04 decision mismatch')
    require(set(side['annotations']) == set(selected), 'Annotation selection mismatch')
    for id, annotation in side['annotations'].items():
        require(set(annotation) == {'needs', 'context_only', 'counterchecks',
                                   'evidence_complete', 'human_review', 'notes'}, 'Annotation schema')
        require(annotation['human_review'] == 'pending' and annotation['evidence_complete'] is False,
                'Unapproved validation/completeness claim')
        support = set()
        claims = []
        for need in annotation['needs']:
            require(set(need) == {'claim', 'required', 'any_of'}, 'Need schema')
            require(need['required'] is True and need['claim'].strip() and need['any_of'],
                    'Invalid required need')
            claims.append(need['claim'])
            routes = []
            for route in need['any_of']:
                require(set(route) == {'all_of'} and route['all_of'], 'Empty/invalid route')
                pairs = [check_ref(r) for r in route['all_of']]
                require(len(pairs) == len(set(pairs)), 'Duplicate page in bundle')
                support.update(pairs)
                routes.append(frozenset(pairs))
            require(len(routes) == len(set(routes)), 'Duplicate alternative route')
        require(len(claims) == len(set(claims)), 'Duplicate need')
        context = [check_ref(r) for r in annotation['context_only']]
        counter = [check_ref(r) for r in annotation['counterchecks']]
        require(len(context) == len(set(context)) and len(counter) == len(set(counter)),
                'Duplicate context/countercheck')
        require(support.isdisjoint(context) and support.isdisjoint(counter), 'Conflicting page roles')
        if by_id[id]['category'] == 'unanswerable':
            require(not support and not context and counter, 'Invalid negative annotation')
        else:
            require(support and not counter, 'Invalid positive annotation')
            require({(g['source'], g['page']) for g in by_id[id]['gold_pages']} <= support | set(context),
                    'Historical evidence omitted from annotation')
    packet = (EVAL / 'VALIDATION_PACKET.md').read_text(encoding='utf-8')
    require(re.findall(r'^### ([A-Z]\d\d) —', packet, re.M) == selected, 'Packet cohort mismatch')
    require(side['questions_sha256'] in packet, 'Packet hash stale')
    for id in selected:
        section = packet.split('### ' + id + ' —', 1)[1].split('\n### ', 1)[0]
        require(by_id[id]['question'] in section and by_id[id]['gold_answer'] in section,
                'Stale packet question/answer')
    for doc in ('VALIDATION_PACKET.md', 'REVIEW.md', 'README.md', 'EVIDENCE.md', 'SHORTLIST.md'):
        text = (EVAL / doc).read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            # Corpus links are structurally valid offline; only require their files in PDF mode.
            path = EVAL / target.split('#')[0]
            if path.suffix != '.pdf' or args.verify_pdfs:
                require(path.exists(), 'Broken link: ' + target)
    for line in (EVAL / 'REVIEW.md').read_text(encoding='utf-8').splitlines():
        match = re.match(r'^\| ([A-Z]\d\d) \|', line)
        if match:
            require(by_id[match[1]]['question'] in line, 'Stale review wording')
            require(line.endswith('|  |  |'), 'Human decision cell filled')
    categories = Counter(by_id[id]['category'] for id in selected)
    require(categories == dict(factual_simple=11, rare_detail=9, multi_passage=10,
                               cross_book=7, paraphrase=5, unanswerable=3), 'Distribution mismatch')
    if args.verify_pdfs:
        out = ROOT / 'data/output/eval/phase1b'
        out.mkdir(parents=True, exist_ok=True)
        for source, book in books.items():
            pdf = ROOT / 'data/input' / source
            require(digest(pdf.read_bytes()) == book['sha256'], 'PDF hash mismatch: ' + source)
            info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
            require(int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1]) == book['pages'],
                    'PDF page count mismatch')
        references.add((next(s for s,b in books.items() if b['book'] == 5), 259))
        opened = []
        for source, page in sorted(references):
            pdf = ROOT / 'data/input' / source
            target = out / f"B{books[source]['book']}-PDF-{page+1}.txt"
            subprocess.run(['pdftotext', '-f', str(page+1), '-l', str(page+1),
                            '-layout', str(pdf), str(target)], check=True)
            require(target.read_text(encoding='utf-8').replace('\f', '').strip(), 'Empty evidence page')
            opened.append(dict(source=source, page=page, sha256=digest(target.read_bytes())))
        (out / 'opened_pages.json').write_text(json.dumps(opened, indent=2) + '\n', encoding='utf-8')
        print(f'Verified seven PDF hashes/counts and reopened {len(opened)} pages.')
    print('PASS: 60 preserved candidates, 11 logged edits, 45 proposed annotations, no validations.')
    print('Category counts:', dict(categories))


if __name__ == '__main__':
    main()
