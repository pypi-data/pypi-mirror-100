## -*- coding: utf-8 -*-

---
title: 'Report for series "${series_info['title']}"'
% if author is not None:
author: '${author}'
% endif
mainfont: TeX Gyre Pagella
papersize: a4
date: ${date}
lang: en-US
---

# Study design

In this study, **${series_info['#participants']} participants** were
presented with **${series_info['#artifacts']} artifacts** between
**${series_info['start']}** and **${series_info['end']}**, and the relevant
actions regarding each artifact were recorded. Some participants have
participated in an intervention beforehand.

# Participation

- Number of artifacts (avg, std, min, max): **${participation_stats['#artifacts']}**
- Number of intervention participants (%): **${participation_stats['#schooled']}**
- Number of armed participants (%): **${participation_stats['#armed']}**
- Number of non-armed participants (%): **${participation_stats['#missed']}**

# Reactions

## This reference is not set automatically and might need to be changed
## manually.
All values in the tables 1 to 3 state the average relative frequency for the
following events:  
**-pos**: no positive reaction  
**pos ∩ neg**: positive and negative reaction  
**pos ∩ -neg**: positive, but no negative reaction  
**-pos ∩ neg**: no positive, but negative reaction  
**-pos ∩ -neg**: neither positive, nor negative reaction  

| -pos | pos ∩ neg | pos ∩ -neg | -pos ∩ neg | -pos ∩ -neg |
| ---: | --------: | ---------: | ---------: | ----------: |
| ${reaction_stats['p_nopos']} | ${reaction_stats['p_pos_neg']} | ${reaction_stats['p_pos_noneg']} | ${reaction_stats['p_nopos_neg']} | ${reaction_stats['p_nopos_noneg']} |
: Reactions of all participants.

| -pos | neg | -pos ∩ neg |
| ---: | --: | ---------: |
| ${reaction_stats['iv_p_nopos']} | ${reaction_stats['iv_p_neg']} | ${reaction_stats['iv_p_nopos_neg']} |
: Reactions of intervention participants.

| -pos | neg | -pos ∩ neg |
| ---: | --: | ---------: |
| ${reaction_stats['noiv_p_nopos']} | ${reaction_stats['noiv_p_neg']} | ${reaction_stats['noiv_p_nopos_neg']} |
: Reactions of non-intervention participants.

![User actions in reaction to artifacts.](img/fig_reactions_by_artifact_relative.pdf)

![Kernel density estimation for correlations between positive actions of different artifacts. Cronbach's alpha for these correlations amounts to ${cronbachs_alpha['positive_action']}.](img/fig_positive_action_correlation_distplot.pdf)

# Evaluations

Participants can have different reactions to different artifacts. The overall
confrontation with the artifact will be considered a **negative evaluation**,
if the participant interacted with the artifact, but did not perform a positive
action like calling the helpdesk (**neg ∩ -pos**). Otherwise, it is considered
a **positive evaluation**.

All values refer to the relative frequencies of evaluations per participant.  
**μ**: Average  
**σ**: Standard deviation  
**min**: Minimum  
**max**: Maximum

| Group | Type | $\mu$ | $\sigma$ | min | max |
| :----- | :-- | ----: | -------: | --: | --: |
| all | positive | ${reaction_stats['good_evals_mean']} | ${reaction_stats['good_evals_std']} | ${reaction_stats['good_evals_min']} | ${reaction_stats['good_evals_max']} |
| | negative | ${reaction_stats['bad_evals_mean']} | ${reaction_stats['bad_evals_std']} | ${reaction_stats['bad_evals_min']} | ${reaction_stats['bad_evals_max']} |
| iv | positive | ${reaction_stats['good_evals_iv_mean']} | ${reaction_stats['good_evals_iv_std']} | ${reaction_stats['good_evals_iv_min']} | ${reaction_stats['good_evals_iv_max']} |
| | negative | ${reaction_stats['bad_evals_iv_mean']} | ${reaction_stats['bad_evals_iv_std']} | ${reaction_stats['bad_evals_iv_min']} | ${reaction_stats['bad_evals_iv_max']} |
| -iv | positive | ${reaction_stats['good_evals_noiv_mean']} | ${reaction_stats['good_evals_noiv_std']} | ${reaction_stats['good_evals_noiv_min']} | ${reaction_stats['good_evals_noiv_max']} |
| | negative | ${reaction_stats['bad_evals_noiv_mean']} | ${reaction_stats['bad_evals_noiv_std']} | ${reaction_stats['bad_evals_noiv_min']} | ${reaction_stats['bad_evals_noiv_max']} |
: Evaluations of participants, grouped by intervention participation and type
of evaluation.

![Kernel density estimation for the correlation between positive evaluations for different artifacts. Cronbach's alpha for these correlations amounts to ${cronbachs_alpha['good_eval']}.](img/fig_good_eval_correlation_distplot.pdf)

# Results

\## CITSA

<%include file="citsa_en_US.md"/>
**iv**: Average CITSA of intervention participants  
**-iv**: Average CITSA of non-intervention participants  
**-iv &rarr; iv**: CITSA increase from non-intervention participants to
intervention participants.  

| iv | -iv | **-iv &rarr; iv** |
| -: | --: | ------------: |
| ${reaction_stats['iv_citsa']} | ${reaction_stats['noiv_citsa']} | **${reaction_stats['citsa_increase']}** |
: CITSA of participants, grouped by intervention participation.

\## IITSA

<%include file="iitsa_en_US.md"/>
**iv**: Average IITSA of intervention participants  
**-iv**: Average IITSA of non-intervention participants  
**-iv &rarr; iv**: IITSA increase from non-intervention participants to
intervention participants.  

| iv | -iv | **-iv &rarr; iv** |
| -: | --: | ------------: |
| ${reaction_stats['iv_iitsa']} | ${reaction_stats['noiv_iitsa']} | **${reaction_stats['iitsa_increase']}** |
: IITSA of participants, grouped by intervention participation.

![Kernel density estimation for average individual IT security awareness separated by intervention
participation.](img/fig_iitsa_kde.pdf)

# Artifacts
% for artifact in artifacts:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*No screenshots available*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
