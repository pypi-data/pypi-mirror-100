## -*- coding: utf-8 -*-
The *Collective IT-Security Awareness* (**CITSA**) is depending on the size of
the organization in employees with a VDU workstation $n$. It is based on the
probability, that an attack which depends on a user perceptible artifact is
successful for $x \, (1 \le x \le n)$ users. This is the case if and only if at
least one user interacts with the artifact, does not report it, and none of the
other $x$ users report it either:
$$
P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1} * P(x = \#artifacts)
$$
Since the size of the attack is unknown, we have to assume $x$ as uniformly
distributed. Thus, we assume $P(x = \#artifacts) = 1$ for all $x$. Now, we can
sum everything up and take the average:
$$
\frac{1}{n} * \sum_{x=1}^{n} P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1}
$$
To determine the probability of a prevented attack, we subtract this value
from 1. Thus, the CITSA results as follows:
$$
1 - \frac{1}{n} * \sum_{x=1}^{n} P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1}
$$
The CITSA ranges from 0 to 1. The higher the value, the better is the
Collective IT-Security Awareness.
