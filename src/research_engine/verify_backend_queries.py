import os

from moteur import SearchEngine
from traitement_requete import process_request
from spell_checker import SpellChecker
from tokenizer import Tokenizer


QUERIES = [
    "Hermione",
    "Harry",
    "Voldemort",
    "Hermione ou Harry",
    "Hermione ou Harry mais pas Voldemort",
    "baguette",
    "magie",
    "baguette et non pas magie",
    "balai",
    "Je voudrais les extraits parlant de magie",
]


class _SimpleTokenizer:
    @staticmethod
    def tokenize(text):
        return [t for t in text.lower().replace("'", " ").split() if t]


class _SimpleSpellChecker:
    def __init__(self):
        self.tokenizer = _SimpleTokenizer()

    @staticmethod
    def process_query(token, logger=None):
        return [token]


def _load_runtime_components(base_dir):
    xml_td1 = os.path.join(base_dir, "data", "output", "TD1", "xml.xml")
    td2_dir = os.path.join(base_dir, "data", "output", "TD2")
    anti_dic = os.path.join(td2_dir, "anti_dic.txt")
    td3_dir = os.path.join(base_dir, "data", "output", "TD3")
    stem_lexicon = os.path.join(td3_dir, "stem_nltk.txt")

    required = [xml_td1, anti_dic, stem_lexicon, td3_dir]
    inverse_files = [
        os.path.join(td3_dir, "inverse_title.txt"),
        os.path.join(td3_dir, "inverse_text.txt"),
    ]

    if all(os.path.exists(p) for p in required) and all(os.path.exists(p) for p in inverse_files):
        tokenizer = Tokenizer(xml_filepath=xml_td1, output_dir=td2_dir)
        spell_checker = SpellChecker(lexicon_file=stem_lexicon)
        stop_words = tokenizer.load_dictionary(anti_dic)
        mode = "real"
    else:
        spell_checker = _SimpleSpellChecker()
        stop_words = set()
        mode = "fallback"

    return {
        "mode": mode,
        "xml_td1": xml_td1,
        "td3_dir": td3_dir,
        "spell_checker": spell_checker,
        "stop_words": stop_words,
    }


def main():
    print("=== Structured query checks ===")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    runtime = _load_runtime_components(base_dir)
    spell_checker = runtime["spell_checker"]
    stop_words = runtime["stop_words"]
    print(f"Component mode : {runtime['mode']}")

    for q in QUERIES:
        structured = process_request(q, stemmer=None, spell_checker=spell_checker, stop_words=stop_words)
        print(f"\nOriginal query : {q}")
        print(f"  keywords     : {structured.get('keywords')}")
        print(f"  equation     : {structured.get('equation')}")
        print(f"  operators    : {structured.get('operateur')}")
        print(f"  search_field : {structured.get('search_field')}")

    index_dir = runtime["td3_dir"]
    xml_path = runtime["xml_td1"]

    if not (os.path.isdir(index_dir) and os.path.isfile(xml_path)):
        print("\n=== Result counts ===")
        for q in QUERIES:
            print(f"- {q}\n  results_count: N/A (index/xml not available)")
        print("\n[INFO] Index/XML outputs not found; skipping engine verification.")
        print("Expected:")
        print(f"  - {index_dir}")
        print(f"  - {xml_path}")
        return

    print("\n=== Result counts ===")
    engine = SearchEngine(index_dir=index_dir, xml_path=xml_path)
    for q in QUERIES:
        structured = process_request(q, stemmer=None, spell_checker=spell_checker, stop_words=stop_words)
        results = engine.search(structured)
        print(f"\n- query        : {q}")
        print(f"  keywords     : {structured.get('keywords')}" )
        print(f"  equation     : {structured.get('equation')}" )
        print(f"  operators    : {structured.get('operateur')}" )
        print(f"  search_field : {structured.get('search_field')}" )
        print(f"  results_count: {len(results)}")

        title_index = engine.indexes.get('title', {})
        text_index = engine.indexes.get('text', {})
        for term in structured.get('keywords', []):
            title_docs = set(title_index.get(term, {}).keys())
            text_docs = set(text_index.get(term, {}).keys())
            total_docs = title_docs | text_docs
            print(f"  term: {term}")
            print(f"    title_docs: {len(title_docs)}")
            print(f"    text_docs : {len(text_docs)}")
            print(f"    total_docs: {len(total_docs)}")


if __name__ == "__main__":
    main()
