## -*- coding: utf-8 -*-

---
title: 'Report for series "${series_pre_info['title']}" and "${series_post_info['title']}"'
% if author is not None:
author: '${author}'
% endif
mainfont: TeX Gyre Pagella
papersize: a4
date: ${date}
lang: en-US
---

# Study design

The study was conducted in two different phases. In the first phase,
**${series_pre_info['#participants']} participants** were presented with
**${series_pre_info['#artifacts']} artifacts** between
**${series_pre_info['start']}** and **${series_pre_info['end']}**.
Relevant actions related to each artifact were recorded.  
In the first phase, the participants received the following artifacts:

% for artifact in artifacts_pre:
-  ${artifact['recipe_id']}
% endfor

Afterwards, an Intervention was performed with some of the participants (for
details refer to the "Participation" section).

Then a second phase was realized, in which
**${series_post_info['#participants']} participants** were presented with
**${series_post_info['#artifacts']} artifacts** between
**${series_post_info['start']}** and **${series_post_info['end']}**.
Relevant actions related to each artifact were recorded.  
In the second phase, the participants received the following artifacts:

% for artifact in artifacts_post:
-  ${artifact['recipe_id']}
% endfor

# Participation

- Number of phase 1 participants: **${participation_stats['#pre_participants']}**
- Number of phase 2 participants: **${participation_stats['#post_participants']}**
- Phase 1 ∩ Phase 2: **${participation_stats['#pre_x_post']}**
- Phase 1 \\ Phase 2 (%): **${participation_stats['#pre_only']}**
- Phase 2 \\ Phase 1 (%): **${participation_stats['#post_only']}**
- Number of intervention participants (%): **${participation_stats['#schooled']}**
- Number of intervention participants in phase 1 (%): **${participation_stats['#schooled_pre']}**
- Number of intervention participants in phase 2 (%): **${participation_stats['#schooled_post']}**
- Number of intervention participants in (phase 1 ∩ phase 2) (%): **${participation_stats['#schooled_pre_post']}**
- Number of non-armed participants in phase 1 (%): **${participation_stats['#missed_pre']}**
- Number of armed participants in phase 1 (%): **${participation_stats['#armed_pre']}**
- Number of artifacts per participant in phase 1 (avg, std, min, max): **${participation_stats['#pre_artifacts']}**
- Number of non-armed participants in phase 2 (%): **${participation_stats['#missed_post']}**
- Number of armed participants in phase 2 (%): **${participation_stats['#armed_post']}**
- Number of artifacts per participant in phase 2 (avg, std, min, max): **${participation_stats['#post_artifacts']}**

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

| Phase | -pos | pos ∩ neg | pos ∩ -neg | -pos ∩ neg | -pos ∩ -neg |
| :---- | ---: | --------: | ---------: | ---------: | ----------: |
| Phase 1 | ${reaction_stats['p_nopos_pre']} | ${reaction_stats['p_pos_neg_pre']} | ${reaction_stats['p_pos_noneg_pre']} | ${reaction_stats['p_nopos_neg_pre']} | ${reaction_stats['p_nopos_noneg_pre']} |
| Phase 2 | ${reaction_stats['p_nopos_post']} | ${reaction_stats['p_pos_neg_post']} | ${reaction_stats['p_pos_noneg_post']} | ${reaction_stats['p_nopos_neg_post']} | ${reaction_stats['p_nopos_noneg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['p_nopos']} | ${reaction_stats['p_pos_neg']} | ${reaction_stats['p_pos_noneg']} | ${reaction_stats['p_nopos_neg']} | ${reaction_stats['p_nopos_noneg']} |
: Reactions of all participants.

| Phase | -pos | neg | -pos ∩ neg |
| :---- | ---: | --: | ---------: |
| Phase 1 | ${reaction_stats['iv_p_nopos_pre']} | ${reaction_stats['iv_p_neg_pre']} | ${reaction_stats['iv_p_nopos_neg_pre']} |
| Phase 2 | ${reaction_stats['iv_p_nopos_post']} | ${reaction_stats['iv_p_neg_post']} | ${reaction_stats['iv_p_nopos_neg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_p_nopos']} | ${reaction_stats['iv_p_neg']} | ${reaction_stats['iv_p_nopos_neg']} |
: Reactions of intervention participants.

| Phase | -pos | neg | -pos ∩ neg |
| :---- | ---: | --: | ---------: |
| Phase 1 | ${reaction_stats['noiv_p_nopos_pre']} | ${reaction_stats['noiv_p_neg_pre']} | ${reaction_stats['noiv_p_nopos_neg_pre']} |
| Phase 2 | ${reaction_stats['noiv_p_nopos_post']} | ${reaction_stats['noiv_p_neg_post']} | ${reaction_stats['noiv_p_nopos_neg_post']} |
| Phase 1 ∪ Phase 2 | ${reaction_stats['noiv_p_nopos']} | ${reaction_stats['noiv_p_neg']} | ${reaction_stats['noiv_p_nopos_neg']} |
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

| Phase | Type | Group | $\mu$ | $\sigma$ | min | max |
| :---- | :--- | :---- | ----: | -------: | --: | --: |
| Phase 1 | positive | all | ${reaction_stats['good_evals_pre_mean']} | ${reaction_stats['good_evals_pre_std']} | ${reaction_stats['good_evals_pre_min']} | ${reaction_stats['good_evals_pre_max']} |
| | | iv | ${reaction_stats['good_evals_iv_pre_mean']} | ${reaction_stats['good_evals_iv_pre_std']} | ${reaction_stats['good_evals_iv_pre_min']} | ${reaction_stats['good_evals_iv_pre_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_pre_mean']} | ${reaction_stats['good_evals_noiv_pre_std']} | ${reaction_stats['good_evals_noiv_pre_min']} | ${reaction_stats['good_evals_noiv_pre_max']} |
| | negative | all | ${reaction_stats['bad_evals_pre_mean']} | ${reaction_stats['bad_evals_pre_std']} | ${reaction_stats['bad_evals_pre_min']} | ${reaction_stats['bad_evals_pre_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_pre_mean']} | ${reaction_stats['bad_evals_iv_pre_std']} | ${reaction_stats['bad_evals_iv_pre_min']} | ${reaction_stats['bad_evals_iv_pre_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_pre_mean']} | ${reaction_stats['bad_evals_noiv_pre_std']} | ${reaction_stats['bad_evals_noiv_pre_min']} | ${reaction_stats['bad_evals_noiv_pre_max']} |
| Phase 2 | positive | all | ${reaction_stats['good_evals_post_mean']} | ${reaction_stats['good_evals_post_std']} | ${reaction_stats['good_evals_post_min']} | ${reaction_stats['good_evals_post_max']} |
| | | iv | ${reaction_stats['good_evals_iv_post_mean']} | ${reaction_stats['good_evals_iv_post_std']} | ${reaction_stats['good_evals_iv_post_min']} | ${reaction_stats['good_evals_iv_post_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_post_mean']} | ${reaction_stats['good_evals_noiv_post_std']} | ${reaction_stats['good_evals_noiv_post_min']} | ${reaction_stats['good_evals_noiv_post_max']} |
| | negative | all | ${reaction_stats['bad_evals_post_mean']} | ${reaction_stats['bad_evals_post_std']} | ${reaction_stats['bad_evals_post_min']} | ${reaction_stats['bad_evals_post_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_post_mean']} | ${reaction_stats['bad_evals_iv_post_std']} | ${reaction_stats['bad_evals_iv_post_min']} | ${reaction_stats['bad_evals_iv_post_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_post_mean']} | ${reaction_stats['bad_evals_noiv_post_std']} | ${reaction_stats['bad_evals_noiv_post_min']} | ${reaction_stats['bad_evals_noiv_post_max']} |
| Phase 1 ∪ Phase 2 | positive | all | ${reaction_stats['good_evals_mean']} | ${reaction_stats['good_evals_std']} | ${reaction_stats['good_evals_min']} | ${reaction_stats['good_evals_max']} |
| | | iv | ${reaction_stats['good_evals_iv_mean']} | ${reaction_stats['good_evals_iv_std']} | ${reaction_stats['good_evals_iv_min']} | ${reaction_stats['good_evals_iv_max']} |
| | | -iv | ${reaction_stats['good_evals_noiv_mean']} | ${reaction_stats['good_evals_noiv_std']} | ${reaction_stats['good_evals_noiv_min']} | ${reaction_stats['good_evals_noiv_max']} |
| | negative | all | ${reaction_stats['bad_evals_mean']} | ${reaction_stats['bad_evals_std']} | ${reaction_stats['bad_evals_min']} | ${reaction_stats['bad_evals_max']} |
| | | iv | ${reaction_stats['bad_evals_iv_mean']} | ${reaction_stats['bad_evals_iv_std']} | ${reaction_stats['bad_evals_iv_min']} | ${reaction_stats['bad_evals_iv_max']} |
| | | -iv | ${reaction_stats['bad_evals_noiv_mean']} | ${reaction_stats['bad_evals_noiv_std']} | ${reaction_stats['bad_evals_noiv_min']} | ${reaction_stats['bad_evals_noiv_max']} |
: Evaluations of participants, grouped by study phase, type of evaluation and
intervention participation.

![Kernel density estimation for the correlation between positive evaluations for different artifacts. Cronbach's alpha for these correlations amounts to ${cronbachs_alpha['good_eval']}.](img/fig_good_eval_correlation_distplot.pdf)

# Results

\## CITSA

<%include file="citsa_en_US.md"/>
**iv**: Average CITSA of intervention participants  
**-iv**: Average CITSA of non-intervention participants  
**-iv &rarr; iv**: CITSA increase from non-intervention participants to
intervention participants.  

| Phase | iv | -iv | **-iv &rarr; iv** |
| :---- | -: | --: | ------------: |
| Phase 1 | ${reaction_stats['iv_citsa_pre']} | ${reaction_stats['noiv_citsa_pre']} | **${reaction_stats['citsa_increase_pre']}** |
| Phase 2 | ${reaction_stats['iv_citsa_post']} | ${reaction_stats['noiv_citsa_post']} | **${reaction_stats['citsa_increase_post']}** |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_citsa']} | ${reaction_stats['noiv_citsa']} | **${reaction_stats['citsa_increase']}** |
: CITSA of participants, grouped by study phase and intervention participation.

\## IITSA

<%include file="iitsa_en_US.md"/>
**iv**: Average IITSA of intervention participants  
**-iv**: Average IITSA of non-intervention participants  
**-iv &rarr; iv**: IITSA increase from non-intervention participants to
intervention participants.  

| Phase | iv | -iv | **-iv &rarr; iv** |
| :---- | -: | --: | ------------: |
| Phase 1 | ${reaction_stats['iv_iitsa_pre']} | ${reaction_stats['noiv_iitsa_pre']} | **${reaction_stats['iitsa_increase_pre']}** |
| Phase 2 | ${reaction_stats['iv_iitsa_post']} | ${reaction_stats['noiv_iitsa_post']} | **${reaction_stats['iitsa_increase_post']}** |
| Phase 1 ∪ Phase 2 | ${reaction_stats['iv_iitsa']} | ${reaction_stats['noiv_iitsa']} | **${reaction_stats['iitsa_increase']}** |
: IITSA of participants, grouped by study phase and intervention participation.

![Kernel density estimation for average individual IT security awareness on artifacts of Phase 1
separated by intervention participation.](img/fig_phase_1_iitsa_kde.pdf)

![Kernel density estimation for average individual IT security awareness on artifacts of Phase 2
separated by intervention participation.](img/fig_phase_2_iitsa_kde.pdf)

# Artifacts

% for artifact in artifacts_pre:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*No screenshots available*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
% for artifact in artifacts_post:
-  ${artifact['recipe_id']}  
  % if len(artifact['images']) == 0:
*No screenshots available*
  % endif
  % for img in artifact['images']:
![${artifact['recipe_id']}](${img})
  % endfor
% endfor
