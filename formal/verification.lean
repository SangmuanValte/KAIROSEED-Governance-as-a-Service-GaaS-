/-!
KAIROSEED Verification Inequality v0.1

Formal scope:
  C ⊆ E ∧ E ⊆ S_auth
  stale epoch tokens have no active authority under exact epoch binding

This file proves properties of this abstract model only. It does not prove the
correctness of eBPF, OPA, TPM hardware, runtime telemetry, or production code.
-/

namespace Kairoseed

abbrev Atom := String
abbrev AtomSet := Atom → Prop

def Subset (a b : AtomSet) : Prop := ∀ x, a x → b x

structure VerificationEnvelope where
  C : AtomSet
  E : AtomSet
  SAuth : AtomSet

def ValidEnvelope (v : VerificationEnvelope) : Prop :=
  Subset v.C v.E ∧ Subset v.E v.SAuth

theorem claim_lte_evidence (v : VerificationEnvelope)
    (h : ValidEnvelope v) : Subset v.C v.E := by
  exact h.1

theorem evidence_lte_scope (v : VerificationEnvelope)
    (h : ValidEnvelope v) : Subset v.E v.SAuth := by
  exact h.2

theorem claim_lte_scope (v : VerificationEnvelope)
    (h : ValidEnvelope v) : Subset v.C v.SAuth := by
  intro x hx
  exact h.2 x (h.1 x hx)

structure Token where
  epoch : Nat

def TokenAuthorized (t : Token) (activeEpoch : Nat) : Prop :=
  t.epoch = activeEpoch

theorem historical_zero_authority (t : Token) (activeEpoch : Nat)
    (h : t.epoch ≠ activeEpoch) : ¬ TokenAuthorized t activeEpoch := by
  intro hAuth
  exact h hAuth

def CBad : AtomSet := fun x => x = "c1" ∨ x = "c2"
def EOnlyC1 : AtomSet := fun x => x = "c1"

theorem C_not_subset_E_counterexample : ¬ Subset CBad EOnlyC1 := by
  intro h
  have hc2 : CBad "c2" := by
    exact Or.inr rfl
  have he := h "c2" hc2
  simp [EOnlyC1] at he

def EBadScope : AtomSet := fun x => x = "seq" ∨ x = "prohibited_enclave"
def SAuthSeqOnly : AtomSet := fun x => x = "seq"

theorem E_not_subset_SAuth_counterexample : ¬ Subset EBadScope SAuthSeqOnly := by
  intro h
  have hp : EBadScope "prohibited_enclave" := by
    exact Or.inr rfl
  have hs := h "prohibited_enclave" hp
  simp [SAuthSeqOnly] at hs

def staleToken : Token := { epoch := 6 }

theorem transitive_zero_authority : ¬ TokenAuthorized staleToken 7 := by
  simp [TokenAuthorized, staleToken]

end Kairoseed
