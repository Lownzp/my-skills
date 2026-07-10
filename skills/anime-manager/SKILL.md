---
name: anime-manager
description: Personal anime and seasonal watchlist management. Use when the user asks to record or update anime preferences, manage watched/watching/planned/dropped shows, recommend anime or seasonal shows, summarize anime reception, compare shows, track episode progress, choose what to watch next, or handle any anime/bangumi-related task, especially using Japanese and Chinese community signals such as Bangumi, Bahamut, Bilibili, Japanese X/Niconico/ABEMA/Filmarks/Anikore rather than relying only on English MAL/AniList scores.
---

# Anime Manager

## Core Workflow

1. Identify the task type: preference update, watchlist update, seasonal recommendation, show-specific summary, episode progress, or comparison.
2. Read `references/profile.md` before making personalized recommendations or updating taste assumptions.
3. Read `references/sources.md` when choosing sources, scores, or community signals.
4. Read `references/watchlist.md` when the task involves watched/watching/planned/dropped status.
5. Browse for current-season data, episode counts, schedules, scores, or community reception because these are time-sensitive.
6. State the date used for "current" episode counts and recommendations.
7. When the user gives a durable preference or correction, update the relevant reference file in this skill if the user explicitly asks to remember it or if the request is clearly an update to this skill.

## Recommendation Rules

- Prefer Japanese and Chinese community signals for this user: Bangumi, Bahamut Anime, Bilibili, Douban, Japanese X, Niconico, ABEMA, Filmarks, and Anikore.
- Use MAL, AniList, IMDb, and Reddit as secondary context, especially for international-scale IPs.
- Separate score, popularity, and discussion heat. A weird or polarizing show can be a strong recommendation if it matches the user's community-following taste.
- Do not treat early-season scores as settled. Mention when sample sizes are small or only 1-2 episodes have aired.
- Include episode progress when recommending currently airing shows.
- Group recommendations by likely fit: must-watch, community/topic pick, try one episode, wait-and-see, or skip unless the user likes the niche.

## Personalization

Use the profile as a living note, not a rigid rulebook. When evidence conflicts, prefer the user's latest explicit correction.

Current known preference highlights:

- The user wants anime recommendations based mainly on Japanese and Chinese community reception, not only English-language ranking sites.
- The user values community discussion, memes, and "what people are actually talking about" alongside quality.
- The user is interested in seasonal anime and episode progress.

## Output Style

- Answer in Chinese unless the user asks otherwise.
- Be concise but concrete: show title, current episode count, reason to watch, caveats, and source basis.
- For seasonal lists, use a compact table plus a short watch-order recommendation.
- When uncertain about a translated title, map Chinese, Japanese, and English names before judging.

## Updating This Skill

When the user asks to improve this anime-management skill, edit the reference files first if possible:

- `references/profile.md`: user taste, source preferences, ranking logic, disliked patterns.
- `references/watchlist.md`: watched, watching, planned, dropped, and notes.
- `references/sources.md`: source hierarchy and evaluation method.

Keep `SKILL.md` lean. Add only durable workflow rules here.
