# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
VibeFinder 1.0

---

## 2. Goal / Task
This recommender suggests the top 5 songs from an 18-song catalog that best 
match a user's taste profile. It predicts which songs a user will enjoy based 
on how closely each song's genre, mood, and energy match the user's preferences.

---

## 3. Data Used
The catalog contains 18 songs in a CSV file. Each song has these features: 
genre, mood, energy (0.0–1.0), tempo_bpm, valence, danceability, and 
acousticness. Genres include pop, lofi, rock, ambient, jazz, synthwave, 
indie pop, country, electronic, r&b, hip-hop, and classical. The original 
starter file had 10 songs — 8 more were added to improve diversity. Some 
genres like lofi and pop have multiple entries while jazz and classical 
have only one, which limits the system for users who prefer those genres.

---

## 4. Algorithm Summary
The system scores every song against the user's taste profile using three rules. 
A genre match awards 2 points — the highest reward. A mood match awards 1 point. 
Energy proximity awards between 0 and 1 point depending on how close the song's 
energy level is to the user's ideal. The maximum possible score is 4.0. All songs 
are scored, sorted from highest to lowest, and the top 5 are returned with a plain 
language explanation of why each was chosen.

---

## 5. Observed Behavior / Biases
Genre dominates the scoring. Because genre is worth 2 points and mood is only 
worth 1, a song that matches the user's genre but not their mood will almost 
always outscore a song that matches their mood but not their genre. This was 
confirmed when Gym Hero (pop/intense) consistently ranked above better mood 
matches for the pop/happy profile. Additionally, the edge case test showed that 
users whose preferred mood has no matching songs in the catalog receive 
emotionally wrong recommendations — the system just falls back to genre and 
energy proximity with no way to signal the gap.

---

## 6. Evaluation Process
Four user profiles were tested: pop/happy/0.8 energy (default), lofi/chill/0.4, 
rock/intense/0.9, and an edge case of electronic/sad/0.95. Results were compared 
against intuition for each profile. A weight shift experiment was also run — 
doubling energy weight and halving genre weight — which caused meaningful ranking 
changes, confirming the system is sensitive to weight choices. No numeric metrics 
were used; evaluation was based on whether the top results felt like reasonable 
recommendations for each profile.

---

## 7. Intended Use and Non-Intended Use
**Intended use:** Classroom exploration of how content-based recommendation 
systems work. This tool is for learning and demonstration only.

**Not intended for:** Real music discovery, commercial use, or any situation 
where recommendations affect real users. The catalog is too small, the scoring 
too simple, and there is no personalization beyond a single static taste profile.

---

## 8. Ideas for Improvement
- Add tempo as a scored feature to better capture musical feel
- Balance the dataset so every genre has at least 3 representative songs
- Add a diversity rule so the top 5 results always span at least 2 different genres
- Support mixed preferences — for example, a user who likes both pop and r&b
- Use listening history to learn weights automatically instead of hardcoding them

---

## 9. Personal Reflection
The biggest learning moment was the edge case experiment. A user who likes sad 
electronic music got recommendations that were genre-correct but emotionally wrong, 
simply because the dataset had no sad electronic songs. This made it clear that 
even a well-designed algorithm can feel broken if the data has gaps — and that 
real apps like Spotify must spend enormous effort making sure their catalogs are 
diverse enough to serve everyone.

Using AI tools helped speed up the coding and brainstorming, but I still needed 
to understand the logic myself to catch issues like the missing CSV header row 
and the wrong import path. The most surprising thing was how a formula with just 
three rules could already produce recommendations that feel almost reasonable — 
it made me realize why simple models are still so widely used in industry.