#!/bin/bash
# Download arXiv PDFs and convert them to text for full-text judging.
# Usage: scripts/judging/fetch_fulltext.sh <ids.txt> <out_dir>
#   ids.txt: one arXiv id per line (e.g. 2505.12224). Writes <out_dir>/<id>.txt; skips ids already done.
#   Needs curl and pdftotext (poppler-utils). Waits 3 s between papers (arXiv asks for polite crawling);
#   about 6 s per paper in practice. Log lines: "ok <id> <bytes>" or "FAIL <id>"; "DONE" at the end.
IDS=$1; D=$2
[ -f "$IDS" ] && [ -n "$D" ] || { echo "usage: $0 <ids.txt> <out_dir>"; exit 1; }
mkdir -p "$D"
while read -r id; do
  [ -z "$id" ] && continue
  [ -s "$D/$id.txt" ] && continue
  ok=0
  for t in 1 2 3; do
    if curl -sS -L --max-time 120 -o "$D/tmp.pdf" "https://arxiv.org/pdf/$id" \
       && pdftotext -q "$D/tmp.pdf" "$D/$id.txt" 2>/dev/null && [ -s "$D/$id.txt" ]; then ok=1; break; fi
    sleep $((t*5))
  done
  rm -f "$D/tmp.pdf"
  [ $ok = 1 ] && echo "ok $id $(wc -c < "$D/$id.txt")" || echo "FAIL $id"
  sleep 3
done < "$IDS"
echo DONE
