## -*- coding: utf-8 -*-
Die *Kollektive IT-Security Awareness* (**CITSA**) ist abhängig von der Größe
der Organisation in Mitarbeitern mit Bildschirmarbeitsplatz $n$. Sie basiert
auf der Wahrscheinlichkeit, dass ein Angriff der ein Nutzer-wahrnehmbares
Artefakt bei $x\, (1 \le x \le n)$ Nutzern bedingt, erfolgreich ist. Das ist genau
dann der Fall, wenn mindestens ein Nutzer mit dem Artefakt interagiert, es
selbst nicht meldet und auch kein anderer der $x$ Nutzer es meldet:
$$
P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1} * P(x = \#artifacts)
$$
Da die Größe des Angriffs unklar ist, muss $x$ als gleichverteilt angenommen
werden und es wird $P(x = \#artifacts) = 1$ für alle $x$ gesetzt. Dies lässt
sich nun aufsummieren und mitteln:
$$
\frac{1}{n} * \sum_{x=1}^{n} P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1}
$$
Um hieraus die Wahrscheinlichkeit für einen verhinderten Angriff zu ermitteln,
wird dieser Wert von 1 abgezogen. Somit ergibt sich die CITSA wie folgt:
$$
1 - \frac{1}{n} * \sum_{x=1}^{n} P(\neg pos \, \cap \, neg) * P(\neg pos)^{x-1}
$$
Die CITSA liegt zwischen 0 und 1. Je höher der Wert, um so besser ist die
Kollektive IT-Security Awareness.
