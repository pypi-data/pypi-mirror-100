## -*- coding: utf-8 -*-

---
title: 'Report der Serie "${series_info['title']}"'
% if author is not None:
author: '${author}'
% endif
mainfont: TeX Gyre Pagella
papersize: a4
date: ${date}
lang: de-DE
---

# Studiendesign

In der Studie wurden **${series_info['#participants']} Teilnehmern**
zwischen dem **${series_info['start']}** und dem **${series_info['end']}**
nacheinander jeweils **${series_info['#artifacts']} Artefakte** zugespielt
und die relevanten Aktionen im bezug auf das jeweilige Artefakt aufgezeichnet.
Ein Teil der Teilnehmer hat vorher an einer Intervention teilgenommen.

# Teilnahme

- Anzahl der Artefakte (avg, std, min, max): **${participation_stats['#artifacts']}**
- Anzahl der Interventionsteilnehmer (%): **${participation_stats['#schooled']}**
- Anzahl der gearmten Teilnehmer (%): **${participation_stats['#armed']}**
- Anzahl der nicht-gearmten Teilnehmer (%): **${participation_stats['#missed']}**

# Reaktionen

## Diese Referenz ist nicht automatisch, und muss ggf manuell geändert werden.
Alle Werte der Tabellen 1 bis 3 geben die durchschnittliche relative Häufigkeit
für die folgenden Ereignisse an:  
**-pos**: keine positive Reaktion  
**neg**: negative Reaktion  
**pos ∩ neg**: sowohl positive, als auch negative Reaktion  
**pos ∩ -neg**: positive Reaktion, aber keine negative Reaktion  
**-pos ∩ neg**: keine positive Reaktion, aber negative Reaktion  
**-pos ∩ -neg**: weder positive, noch negative Reaktion  

| -pos | pos ∩ neg | pos ∩ -neg | -pos ∩ neg | -pos ∩ -neg |
| ---: | --------: | ---------: | ---------: | ----------: |
| ${reaction_stats['p_nopos']} | ${reaction_stats['p_pos_neg']} | ${reaction_stats['p_pos_noneg']} | ${reaction_stats['p_nopos_neg']} | ${reaction_stats['p_nopos_noneg']} |
: Reaktionen aller Teilnehmer.

| -pos | neg | -pos ∩ neg |
| ---: | --: | ---------: |
| ${reaction_stats['iv_p_nopos']} | ${reaction_stats['iv_p_neg']} | ${reaction_stats['iv_p_nopos_neg']} |
: Reaktionen von Interventionsteilnehmern.

| -pos | neg | -pos ∩ neg |
| ---: | --: | ---------: |
| ${reaction_stats['noiv_p_nopos']} | ${reaction_stats['noiv_p_neg']} | ${reaction_stats['noiv_p_nopos_neg']} |
: Reaktionen von Nicht-Interventionsteilnehmern.

![Nutzer Aktionen als Reaktion auf Artefakte.](img/fig_reactions_by_artifact_relative.pdf)

![Kerndichteschätzung der Korrelationen zwischen positiven Reaktionen verschiedener Artefakte. Cronbach's Alpha dieser Korrelationen beträgt ${cronbachs_alpha['positive_action']}.](img/fig_positive_action_correlation_distplot.pdf)

# Evaluationen

Teilnehmer können verschieden auf ein Artefakt reagieren. Die gesamte
Konfrontation mit dem Artefakt wird als **negative Evaluation** gewertet,
falls der Teilnehmer mit dem Artefakt interagiert, aber keine positive Aktion
wie z.B. die Benachrichtigung eines Helpdesks ausführt (**-pos ∩ neg**).
Ansonsten wird sie als **positive Evaluation** gewertet.

Alle Werte beziehen sich auf die relative Häufigkeit von Evaluationen pro
Teilnehmer.  
**μ**: Durchschnitt  
**σ**: Standardabweichung  
**min**: Minimum  
**max**: Maximum  

| Gruppe | Typ | $\mu$ | $\sigma$ | min | max |
| :----- | :-- | ----: | -------: | --: | --: |
| Alle | Positiv | ${reaction_stats['good_evals_mean']} | ${reaction_stats['good_evals_std']} | ${reaction_stats['good_evals_min']} | ${reaction_stats['good_evals_max']} |
| | Negativ | ${reaction_stats['bad_evals_mean']} | ${reaction_stats['bad_evals_std']} | ${reaction_stats['bad_evals_min']} | ${reaction_stats['bad_evals_max']} |
| iv | Positiv | ${reaction_stats['good_evals_iv_mean']} | ${reaction_stats['good_evals_iv_std']} | ${reaction_stats['good_evals_iv_min']} | ${reaction_stats['good_evals_iv_max']} |
| | Negativ | ${reaction_stats['bad_evals_iv_mean']} | ${reaction_stats['bad_evals_iv_std']} | ${reaction_stats['bad_evals_iv_min']} | ${reaction_stats['bad_evals_iv_max']} |
| -iv | Positiv | ${reaction_stats['good_evals_noiv_mean']} | ${reaction_stats['good_evals_noiv_std']} | ${reaction_stats['good_evals_noiv_min']} | ${reaction_stats['good_evals_noiv_max']} |
| | Negativ | ${reaction_stats['bad_evals_noiv_mean']} | ${reaction_stats['bad_evals_noiv_std']} | ${reaction_stats['bad_evals_noiv_min']} | ${reaction_stats['bad_evals_noiv_max']} |
: Evaluationen der Teilnehmer, gruppiert nach Interventionsteilnahme und Typ
der Evaluation.

![Kerndichteschätzung für Korrelationen zwischen positiven Evaluationen verschiedener Artefakte. Cronbach's Alpha dieser Korrelationen beträgt ${cronbachs_alpha['good_eval']}.](img/fig_good_eval_correlation_distplot.pdf)

# Ergebnisse

\## CITSA

<%include file="citsa_de_DE.md"/>
**iv**: Durchschnittliche CITSA von Interventionsteilnehmern.  
**-iv**: Durchschnittliche CITSA von Nicht-Interventionsteilnehmern.  
**-iv &rarr; iv**: CITSA Verbesserung zwischen Nicht-Interventionsteilnehmern
und Interventionsteilnehmern.  

| iv | -iv | **-iv &rarr; iv** |
| -: | --: | ----------------: |
| ${reaction_stats['iv_citsa']} | ${reaction_stats['noiv_citsa']} | **${reaction_stats['citsa_increase']}** |
: CITSA der Teilnehmer, gruppiert nach Interventionsteilnahme.

\## IITSA

<%include file="iitsa_de_DE.md"/>
**iv**: Durchschnittliche IITSA von Interventionsteilnehmern.  
**-iv**: Durchschnittliche IITSA von Nicht-Interventionsteilnehmern.  
**-iv &rarr; iv**: IITSA Verbesserung zwischen Nicht-Interventionsteilnehmern
und Interventionsteilnehmern.  

| iv | -iv | **-iv &rarr; iv** |
| -: | --: | ----------------: |
| ${reaction_stats['iv_iitsa']} | ${reaction_stats['noiv_iitsa']} | **${reaction_stats['iitsa_increase']}** |
: IITSA der Teilnehmer, gruppiert nach Interventionsteilnahme.

![Kerndichteschätzung der durchschnittlichen IITSA getrennt nach Interventionsteilnahme.](img/fig_iitsa_kde.pdf)

# Artefakte
% for artifact in artifacts:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*Keine Screenshots verfügbar*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
