; P(cr⇒r) = 2 ∗ P(cr⇒m)

(declare-fun p_CR-R () Real)
(declare-fun p_CR-M () Real)

(assert (= p_CR-R (* 2 p_CR-M)))


; P(cr⇒r ∨ cr⇒m | cr) ≥ 0.98
; P((cr⇒r ∨ cr⇒m) ∧ cr) ≥ 0.98 ∗ P(cr)
; P(cr⇒r ∧ cr) + P(cr⇒m ∧ cr) ≥ 0.98 ∗ P(cr)

(declare-fun p_CR_CR-R () Real)
(declare-fun p_CR_CR-M () Real)
(declare-fun p_CR () Real)

(assert (>= (+ p_CR_CR-R p_CR_CR-M) (* 0.98 p_CR)))
