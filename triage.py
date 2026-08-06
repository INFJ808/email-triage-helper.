import sys
import json
from pathlib import Path

# ----- Configuration -----

CATEGORY_RULES = {
    "URGENT": ["urgent", "asap", "immediately", "right away", "critical"],
    "MONEY": ["bill", "billing", "invoice", "payment", "rent", "due", "past due"],
    "JOB_LEAD": ["job", "position", "opening", "apply", "application", "hiring"],
    "PERSONAL": ["mom", "dad", "family", "friend", "birthday", "dinner"],
    "SPAM": ["winner", "lottery", "crypto", "investment opportunity", "click here"],
}

DEFAULT_CATEGORY = "OTHER"

SNIPPETS_FILE = "snippets.json"


# ----- Core logic -----

def load_lines(input_path: Path):
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    # Split on blank lines to allow multi-line items
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    return blocks


def classify_item(text: str) -> str:
    """Assign a category based on simple keyword rules."""
    lower = text.lower()
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in lower:
                return category
    return DEFAULT_CATEGORY


def triage_file(input_path: Path):
    items = load_lines(input_path)
    results = []

    for idx, item in enumerate(items, start=1):
        category = classify_item(item)
        results.append({
            "id": idx,
            "category": category,
            "text": item,
        })

    # Save JSON results
    json_path = input_path.parent / "triage_results.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    # Save human-readable summary
    summary_lines = []
    for r in results:
        summary_lines.append(f"[{r['id']:03}] [{r['category']}] {r['text']}")
    summary_text = "\n\n".join(summary_lines)

    summary_path = input_path.parent / "triage_summary.txt"
    summary_path.write_text(summary_text, encoding="utf-8")

    print(f"Triage complete. {len(results)} items processed.")
    print(f"- JSON:    {json_path}")
    print(f"- Summary: {summary_path}")


def load_snippets(snippets_path: Path):
    if not snippets_path.exists():
        print(f"Snippets file not found: {snippets_path}")
        sys.exit(1)
    data = json.loads(snippets_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("snippets.json must contain a list of snippet objects.")
        sys.exit(1)
    return data


def find_snippet(query: str, snippets):
    """Very simple search: look for query in title or tags, then in text."""
    q = query.lower()

    # First pass: title or tags
    matches = []
    for s in snippets:
        title = s.get("title", "")
        tags = " ".join(s.get("tags", []))
        haystack = f"{title} {tags}".lower()
        if q in haystack:
            matches.append(s)

    # If no matches, search in the text itself
    if not matches:
        for s in snippets:
            text = s.get("text", "")
            if q in text.lower():
                matches.append(s)

    if not matches:
        return None
    # For now, just return the first match
    return matches[0]


def snippet_mode(query: str, snippets_path: Path):
    snippets = load_snippets(snippets_path)
    snippet = find_snippet(query, snippets)
    if not snippet:
        print(f"No snippet found for query: {query!r}")
        return
    print(f"--- {snippet.get('title', 'Snippet')} ---")
    print(snippet.get("text", "").strip())
    print("\n(tags: " + ", ".join(snippet.get("tags", [])) + ")")


# ----- CLI entry point -----

def print_usage():
    print("Usage:")
    print("  python triage.py triage <input_file>")
    print("  python triage.py snippet <search text>")
    print("")
    print("Examples:")
    print("  python triage.py triage sample_items.txt")
    print('  python triage.py snippet "technical summary"')


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "triage":
        if len(sys.argv) < 3:
            print("Error: triage mode requires an input file path.\n")
            print_usage()
            sys.exit(1)
        input_path = Path(sys.argv[2])
        if not input_path.exists():
            print(f"Input file not found: {input_path}")
            sys.exit(1)
        triage_file(input_path)

    elif mode == "snippet":
        if len(sys.argv) < 3:
            print("Error: snippet mode requires a search string.\n")
            print_usage()
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        snippets_path = Path(SNIPPETS_FILE)
        snippet_mode(query, snippets_path)

    else:
        print(f"Unknown mode: {mode}\n")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
