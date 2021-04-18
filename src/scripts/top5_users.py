import json

with open('david_madras_1_scores.json') as f:
  data = json.load(f)

  scores = data['production']
  ranked_ids = list(sorted(scores, key=scores.get, reverse=True))
  print(ranked_ids[0:4])
