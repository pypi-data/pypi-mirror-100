## -*- coding: utf-8 -*-

---
title: 'Report der Serien "${series_pre_info['title']}" und "${series_post_info['title']}"'
% if author is not None:
author: '${author}'
% endif
mainfont: TeX Gyre Pagella
papersize: a4
date: ${date}
lang: de-DE
---

# Studiendesign

Die Studie fand in zwei verschiedenen Phasen statt. In der ersten Phase wurden
**${series_pre_info['#participants']} Teilnehmern** zwischen dem
**${series_pre_info['start']}** und dem **${series_pre_info['end']}**
nacheinander jeweils **${series_pre_info['#artifacts']} Artefakte**
zugespielt, und relevante Aktionen im Bezug auf das jeweilige Artefakt
aufgezeichnet.  
Die Teilnehmer erhielten in der ersten Phase die folgenden Artefakte:

% for artifact in artifacts_pre:
-  ${artifact['recipe_id']}
% endfor

Anschließend wurde eine Intervention mit einem Teil der Teilnehmer durchgeführt
(für Details siehe Abschnitt "Teilnahmen").

Danach gab es eine zweite Phase, in welcher
**${series_post_info['#participants']} Teilnehmern** zwischen dem
**${series_post_info['start']}** und dem **${series_post_info['end']}** jeweils
**${series_post_info['#artifacts']} Artefakte** zugespielt wurden. Hier wurden
ebenfalls die relevanten Aktionen im Bezug auf das jeweilige Artefakt
aufgezeichnet.  
In der zweiten Phase erhielten die Teilnehmer folgende Artefakte:

% for artifact in artifacts_post:
-  ${artifact['recipe_id']}
% endfor

# Teilnahme

- Anzahl der Teilnehmer in Phase 1: **${participation_stats['#pre_participants']}**
- Anzahl der Teilnehmer in Phase 2: **${participation_stats['#post_participants']}**
- Phase 1 ∩ Phase 2: **${participation_stats['#pre_x_post']}**
- Phase 1 \\ Phase 2 (%): **${participation_stats['#pre_only']}**
- Phase 2 \\ Phase 1 (%): **${participation_stats['#post_only']}**
- Anzahl der Interventionsteilnehmer (%): **${participation_stats['#schooled']}**
- Anzahl der Interventionsteilnehmer in Phase 1 (%): **${participation_stats['#schooled_pre']}**
- Anzahl der Interventionsteilnehmer in Phase 2 (%): **${participation_stats['#schooled_post']}**
- Anzahl der Interventionsteilnehmer in (Phase 1 ∩ Phase 2) (%): **${participation_stats['#schooled_pre_post']}**
- Anzahl der nicht gearmten Teilnehmer in Phase 1 (%): **${participation_stats['#missed_pre']}**
- Anzahl der gearmten Teilnehmer in Phase 1 (%): **${participation_stats['#armed_pre']}**
- Anzahl der Artefakte pro Teilnehmer in Phase 1 (avg, std, min, max): **${participation_stats['#pre_artifacts']}**
- Anzahl der nicht gearmten Teilnehmer in Phase 2 (%): **${participation_stats['#missed_post']}**
- Anzahl der gearmten Teilnehmer in Phase 2 (%): **${participation_stats['#armed_post']}**
- Anzahl der Artefakte pro Teilnehmer in Phase 2 (avg, std, min, max): **${participation_stats['#post_artifacts']}**

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

| Phase | -pos | pos ∩ neg | pos ∩ -neg | -pos ∩ neg | -pos ∩ -neg |
| :---- | ---: | --------: | ---------: | ---------: | ----------: |
| Phase 1 | ${reaction_stats['p_nopos_pre']} | ${reaction_stats['p_pos_neg_pre']} | ${reaction_stats['p_pos_noneg_pre']} | ${reaction_stats['p_nopos_neg_pre']} | ${reaction_stats['p_nopos_noneg_pre']} |
| Phase 2 | ${reaction_stats['p_nopos_post']} | ${reaction_stats['p_pos_neg_post']} | ${reaction_stats['p_pos_noneg_post']} | ${reaction_stats['p_nopos_neg_post']} | ${reaction_stats['p_nopos_noneg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['p_nopos']} | ${reaction_stats['p_pos_neg']} | ${reaction_stats['p_pos_noneg']} | ${reaction_stats['p_nopos_neg']} | ${reaction_stats['p_nopos_noneg']} |
: Reaktionen aller Teilnehmer.

| Phase | -pos | neg | -pos ∩ neg |
| :---- | ---: | --: | ---------: |
| Phase 1 | ${reaction_stats['iv_p_nopos_pre']} | ${reaction_stats['iv_p_neg_pre']} | ${reaction_stats['iv_p_nopos_neg_pre']} |
| Phase 2 | ${reaction_stats['iv_p_nopos_post']} | ${reaction_stats['iv_p_neg_post']} | ${reaction_stats['iv_p_nopos_neg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_p_nopos']} | ${reaction_stats['iv_p_neg']} | ${reaction_stats['iv_p_nopos_neg']} |
: Reaktionen von Interventionsteilnehmern.

| Phase | -pos | neg | -pos ∩ neg |
| :---- | ---: | --: | ---------: |
| Phase 1 | ${reaction_stats['noiv_p_nopos_pre']} | ${reaction_stats['noiv_p_neg_pre']} | ${reaction_stats['noiv_p_nopos_neg_pre']} |
| Phase 2 | ${reaction_stats['noiv_p_nopos_post']} | ${reaction_stats['noiv_p_neg_post']} | ${reaction_stats['noiv_p_nopos_neg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['noiv_p_nopos']} | ${reaction_stats['noiv_p_neg']} | ${reaction_stats['noiv_p_nopos_neg']} |
: Reaktionen von Nicht-Interventionsteilnehmern.

![Nutzer Aktionen als Reaktion auf Artefakte.](img/fig_reactions_by_artifact_relative.pdf)

![Kerndichteschätzung der Korrelationen zwischen positiven Reaktionen verschiedener Artefakte. Cronbach's Alpha dieser Korrelationen beträgt ${cronbachs_alpha['positive_action']}.](img/fig_positive_action_correlation_distplot.pdf)

# Evaluationen

Teilnehmer können verschieden auf ein Artefakt reagieren. Die gesamte
Konfrontation mit dem Artefakt wird als **negative Evaluation** gewertet,
falls der Teilnehmer mit dem Artefakt interagiert, aber keine positive Aktion
wie z.B. die Benachrichtigung eines Helpdesks ausführt (**neg ∩ -pos**).
Ansonsten wird sie als **positive Evaluation** gewertet.

Alle Werte beziehen sich auf die relative Häufigkeit von Evaluationen pro
Teilnehmer.  
**μ**: Durchschnitt  
**σ**: Standardabweichung  
**min**: Minimum  
**max**: Maximum

| Phase | Typ | Gruppe | $\mu$ | $\sigma$ | min | max |
| :---- | --: | -----: | ----: | -------: | --: | --: |
| Phase 1 | Positiv | Alle | ${reaction_stats['good_evals_pre_mean']} | ${reaction_stats['good_evals_pre_std']} | ${reaction_stats['good_evals_pre_min']} | ${reaction_stats['good_evals_pre_max']} |
| | | iv | ${reaction_stats['good_evals_iv_pre_mean']} | ${reaction_stats['good_evals_iv_pre_std']} | ${reaction_stats['good_evals_iv_pre_min']} | ${reaction_stats['good_evals_iv_pre_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_pre_mean']} | ${reaction_stats['good_evals_noiv_pre_std']} | ${reaction_stats['good_evals_noiv_pre_min']} | ${reaction_stats['good_evals_noiv_pre_max']} |
| | Negativ | Alle | ${reaction_stats['bad_evals_pre_mean']} | ${reaction_stats['bad_evals_pre_std']} | ${reaction_stats['bad_evals_pre_min']} | ${reaction_stats['bad_evals_pre_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_pre_mean']} | ${reaction_stats['bad_evals_iv_pre_std']} | ${reaction_stats['bad_evals_iv_pre_min']} | ${reaction_stats['bad_evals_iv_pre_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_pre_mean']} | ${reaction_stats['bad_evals_noiv_pre_std']} | ${reaction_stats['bad_evals_noiv_pre_min']} | ${reaction_stats['bad_evals_noiv_pre_max']} |
| Phase 2 | Positiv | Alle | ${reaction_stats['good_evals_post_mean']} | ${reaction_stats['good_evals_post_std']} | ${reaction_stats['good_evals_post_min']} | ${reaction_stats['good_evals_post_max']} |
| | | iv | ${reaction_stats['good_evals_iv_post_mean']} | ${reaction_stats['good_evals_iv_post_std']} | ${reaction_stats['good_evals_iv_post_min']} | ${reaction_stats['good_evals_iv_post_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_post_mean']} | ${reaction_stats['good_evals_noiv_post_std']} | ${reaction_stats['good_evals_noiv_post_min']} | ${reaction_stats['good_evals_noiv_post_max']} |
| | Negativ | Alle | ${reaction_stats['bad_evals_post_mean']} | ${reaction_stats['bad_evals_post_std']} | ${reaction_stats['bad_evals_post_min']} | ${reaction_stats['bad_evals_post_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_post_mean']} | ${reaction_stats['bad_evals_iv_post_std']} | ${reaction_stats['bad_evals_iv_post_min']} | ${reaction_stats['bad_evals_iv_post_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_post_mean']} | ${reaction_stats['bad_evals_noiv_post_std']} | ${reaction_stats['bad_evals_noiv_post_min']} | ${reaction_stats['bad_evals_noiv_post_max']} |
| Phase 1 ∪ Phase 2 | Positiv | Alle | ${reaction_stats['good_evals_mean']} | ${reaction_stats['good_evals_std']} | ${reaction_stats['good_evals_min']} | ${reaction_stats['good_evals_max']} |
| | | iv | ${reaction_stats['good_evals_iv_mean']} | ${reaction_stats['good_evals_iv_std']} | ${reaction_stats['good_evals_iv_min']} | ${reaction_stats['good_evals_iv_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_mean']} | ${reaction_stats['good_evals_noiv_std']} | ${reaction_stats['good_evals_noiv_min']} | ${reaction_stats['good_evals_noiv_max']} |
| | Negativ | Alle | ${reaction_stats['bad_evals_mean']} | ${reaction_stats['bad_evals_std']} | ${reaction_stats['bad_evals_min']} | ${reaction_stats['bad_evals_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_mean']} | ${reaction_stats['bad_evals_iv_std']} | ${reaction_stats['bad_evals_iv_min']} | ${reaction_stats['bad_evals_iv_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_mean']} | ${reaction_stats['bad_evals_noiv_std']} | ${reaction_stats['bad_evals_noiv_min']} | ${reaction_stats['bad_evals_noiv_max']} |
: Evaluationen der Teilnehmer, gruppiert nach Studienphase, Typ der Evaluation
und Interventionsteilnahme.

![Kerndichteschätzung für Korrelationen zwischen positiven Evaluationen verschiedener Artefakte. Cronbach's Alpha dieser Korrelationen beträgt ${cronbachs_alpha['good_eval']}.](img/fig_good_eval_correlation_distplot.pdf)

# Ergebnisse

\## CITSA

<%include file="citsa_de_DE.md"/>
**iv**: Durchschnittliche CITSA von Interventionsteilnehmern.  
**-iv**: Durchschnittliche CITSA von Nicht-Interventionsteilnehmern.  
**-iv &rarr; iv**: CITSA Verbesserung zwischen Nicht-Interventionsteilnehmern
und Interventionsteilnehmern.  

| Phase | iv | -iv | **-iv &rarr; iv** |
| :---- | -: | --: | ------------: |
| Phase 1 | ${reaction_stats['iv_citsa_pre']} | ${reaction_stats['noiv_citsa_pre']} | **${reaction_stats['citsa_increase_pre']}** |
| Phase 2 | ${reaction_stats['iv_citsa_post']} | ${reaction_stats['noiv_citsa_post']} | **${reaction_stats['citsa_increase_post']}** |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_citsa']} | ${reaction_stats['noiv_citsa']} | **${reaction_stats['citsa_increase']}** |
: CITSA der Teilnehmer, gruppiert nach Studienphase und Interventionsteilnahme.

\## IITSA

<%include file="iitsa_de_DE.md"/>
**iv**: Durchschnittliche IITSA von Interventionsteilnehmern.  
**-iv**: Durchschnittliche IITSA von Nicht-Interventionsteilnehmern.  
**-iv &rarr; iv**: IITSA Verbesserung zwischen Nicht-Interventionsteilnehmern
und Interventionsteilnehmern.  

| Phase | iv | -iv | **-iv &rarr; iv** |
| :---- | -: | --: | ------------: |
| Phase 1 | ${reaction_stats['iv_iitsa_pre']} | ${reaction_stats['noiv_iitsa_pre']} | **${reaction_stats['iitsa_increase_pre']}** |
| Phase 2 | ${reaction_stats['iv_iitsa_post']} | ${reaction_stats['noiv_iitsa_post']} | **${reaction_stats['iitsa_increase_post']}** |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_iitsa']} | ${reaction_stats['noiv_iitsa']} | **${reaction_stats['iitsa_increase']}** |
: IITSA der Teilnehmer, gruppiert nach Studienphase und Interventionsteilnahme.

![Kerndichteschätzung der durchschnittlichen IITSA für Artefakte der ersten Phase, getrennt nach
Interventionsteilnahme.](img/fig_phase_1_iitsa_kde.pdf)

![Kerndichteschätzung der durchschnittlichen IITSA für Artefakte der zweiten Phase, getrennt nach
Interventionsteilnahme.](img/fig_phase_2_iitsa_kde.pdf)

# Artefakte

% for artifact in artifacts_pre:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*Keine Screenshots verfügbar*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
% for artifact in artifacts_post:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*Keine Screenshots verfügbar*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
