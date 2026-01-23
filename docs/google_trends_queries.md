# Google Trends Query Taxonomy
# --------------------------------
# Recommended Google Trends keywords for each disease
#
# Purpose:
#   Use these keywords with pytrends to capture symptom-related
#   search interest for early warning signals.
#
# Strategy:
#   - Symptom clusters (most predictive)
#   - Disease name alone (confirmation / awareness)
#   - Symptom + disease combinations
#   - Outbreak / concern-related terms
#   - Selected local-language (Hindi) terms for India relevance
#
# Target:
#   6–10 effective terms per disease after filtering for volume

## Influenza (ILI – Influenza-Like Illness)
# Strongest evidence for early detection (7–14 day lead typical)

- fever cough
- cough fever
- sore throat
- body aches fever
- fever headache
- muscle aches
- fatigue fever
- flu symptoms
- flu
- influenza
- सर्दी जुकाम (sardi jukam – common Hindi search for cold/flu)
- फ्लू के लक्षण (flu ke lakshan)

## Malaria
# Moderate correlation in endemic regions (2–3 week lag possible)
# Fever + chills/shivering are key indicators

- fever chills
- high fever shivering
- chills fever
- headache fever
- night sweats
- malaria symptoms
- malaria fever
- malaria
- मलेरिया के लक्षण (malaria ke lakshan)
- मलेरिया बुखार (malaria bukhar)

## Cholera
# Strong signals during outbreaks and monsoon seasons
# Focus on severe watery diarrhea and dehydration

- watery diarrhea
- severe diarrhea
- diarrhea vomiting
- dehydration diarrhea
- acute diarrhea
- cholera symptoms
- cholera outbreak
- cholera
- हैजा के लक्षण (haija ke lakshan)
- दस्त उल्टी (dast ulti – diarrhea + vomiting in Hindi)

## Zika
# Useful during outbreaks and public concern spikes
# Core cluster: rash + fever + joint pain

- fever rash
- joint pain fever
- joint pain rash
- rash fever
- conjunctivitis zika
- zika symptoms
- zika fever
- zika virus
- mosquito rash
- zika
- ज़िका वायरस (zika virus in Hindi)
- ज़िका के लक्षण (zika ke lakshan)

# Usage Notes
# --------------------------------
# 1. Use pytrends with kw_list = these terms.
# 2. Aggregate by disease:
#      - Symptom terms: higher weight (e.g., ×1.5)
#      - Disease-name terms: baseline weight (×1.0)
# 3. Test each term manually on trends.google.com:
#      - Remove terms with insufficient volume.
# 4. For global models:
#      - Prefer English terms.
#      - Include local-language terms only for country-specific analyses (e.g., India).
# 5. If a term is too sparse:
#      - Replace it with a broader proxy, but note increased noise.
#
# Important:
#   Google Trends reflects search behavior, not clinical diagnosis.
#   These signals are used as complementary early indicators,
#   not as substitutes for official surveillance data.
