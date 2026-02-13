# Reading Guide: Understanding the Neuro-Coherence Framework

**Purpose**: Help you navigate this repository efficiently based on your role and interests.

---

## Quick Navigation by Role

### 👨‍🔬 **If You're a Researcher / Neuroscientist**

**Start Here:**
1. `FINDINGS_SUMMARY.md` - Quick overview (5 min read)
2. `README.md` - Full framework introduction (10 min)
3. `docs/theoretical-framework/02-neuro-coherence-function.md` - Mathematical details
4. `docs/theoretical-framework/03-operators.md` - Operator definitions
5. `AI_PERSPECTIVE_ANALYSIS.md` - Deep dive analysis (20 min)

**Then Explore:**
- `examples/quickstart.py` - Run basic simulation
- `examples/full_analysis.py` - See multimodal integration
- `tests/` - Understand validation approach

---

### 💻 **If You're a Developer / Data Scientist**

**Start Here:**
1. `README.md` - Installation and quick start
2. `examples/quickstart.py` - Working code example
3. `simulations/core/neuro_coherence.py` - Core implementation
4. `simulations/core/operators.py` - Mathematical operators

**Then Explore:**
- `analysis/eeg/` - EEG analysis modules
- `analysis/fmri/` - fMRI analysis modules
- `analysis/integration/` - Multimodal fusion
- `tests/` - Test suite for examples

**API Reference:**
- See docstrings in each module
- Run `pytest tests/ -v` to see test examples

---

### 🏥 **If You're a Clinician**

**Start Here:**
1. `FINDINGS_SUMMARY.md` - Executive overview
2. README.md sections:
   - "Conceptual Foundation"
   - "Biomarker Mapping"
   - "Key Predictions"
3. `AI_PERSPECTIVE_ANALYSIS.md` - "Clinical Interpretation" sections

**Key Points:**
- This is **research only**, not clinical tool
- Framework proposes testable predictions
- Biomarkers map to existing neuroimaging

**Understand the hypothesis:**
Bipolar disorder = coherence breakdown, not just chemical imbalance

---

### 🤖 **If You're Interested in AI/ML Perspective**

**Start Here:**
1. `AI_PERSPECTIVE_ANALYSIS.md` - Complete AI assessment
2. Focus on sections:
   - "AI-Specific Observations"
   - "Machine Learning Integration Opportunities"
   - "Interpretability vs Performance"

**Technical Deep Dive:**
- `simulations/core/` - Mathematical implementation
- `analysis/integration/multimodal_fusion.py` - Data fusion architecture
- Parameter sensitivity analysis in examples

---

### 📊 **If You Want to See Results First**

**Visual Evidence:**
Look at the generated PNG files:
1. `docs/figures/quickstart_results.png` - Basic Ψ across states
2. `docs/figures/longitudinal_analysis.png` - Temporal dynamics
3. `docs/figures/parameter_sensitivity.png` - Operator impacts
4. `docs/figures/multimodal_comparison.png` - EEG + fMRI integration
5. `docs/figures/perturbation_experiment.png` - Recovery curves
6. `docs/figures/recovery_comparison.png` - Healing dynamics
7. `docs/figures/operator_correlations.png` - How operators relate to Ψ

**Then Read:**
- `FINDINGS_SUMMARY.md` to understand what you're seeing
- Example scripts that generated these figures

---

## Document Hierarchy

### **Tier 1: Quick Start (5-10 minutes)**
```
FINDINGS_SUMMARY.md          ← Start here for overview
README.md (sections)         ← Framework introduction
```

### **Tier 2: Understanding (20-30 minutes)**
```
AI_PERSPECTIVE_ANALYSIS.md   ← Complete analysis
README.md (full)             ← Full documentation
IMPLEMENTATION_SUMMARY.md    ← What's been built
```

### **Tier 3: Theory (30-60 minutes)**
```
docs/theoretical-framework/
  ├── 02-neuro-coherence-function.md
  └── 03-operators.md
```

### **Tier 4: Implementation (1-2 hours)**
```
examples/
  ├── quickstart.py           ← Run first
  ├── custom_simulation.py    ← Then this
  └── full_analysis.py        ← Advanced

simulations/core/             ← Core math
analysis/                     ← Analysis tools
```

### **Tier 5: Deep Dive (2+ hours)**
```
tests/                        ← Validation
simulations/core/             ← Full implementation
analysis/                     ← All modules
data/synthetic/               ← Data generation
```

---

## Reading Paths by Goal

### **Goal: Understand the Hypothesis**
1. `FINDINGS_SUMMARY.md` → "What Makes This Significant"
2. `README.md` → "Conceptual Foundation"
3. `AI_PERSPECTIVE_ANALYSIS.md` → "Key Findings"

### **Goal: Evaluate Scientific Merit**
1. `FINDINGS_SUMMARY.md` → "Three Falsifiable Predictions"
2. `AI_PERSPECTIVE_ANALYSIS.md` → "AI Assessment"
3. `docs/theoretical-framework/02-neuro-coherence-function.md` → "Validation Strategy"

### **Goal: Use the Code**
1. `README.md` → "Installation" and "Quick Start"
2. `examples/README.md` → Usage patterns
3. `examples/quickstart.py` → Run and modify
4. `simulations/core/` → Study implementation

### **Goal: Understand the Math**
1. `README.md` → "The Neuro-Coherence Function (Ψ)"
2. `docs/theoretical-framework/02-neuro-coherence-function.md`
3. `docs/theoretical-framework/03-operators.md`
4. `simulations/core/operators.py` → Implementation

### **Goal: Plan a Validation Study**
1. `AI_PERSPECTIVE_ANALYSIS.md` → "Falsifiable Predictions"
2. `README.md` → "Biomarker Mapping"
3. `AI_PERSPECTIVE_ANALYSIS.md` → "Data Requirements"
4. `docs/theoretical-framework/02-neuro-coherence-function.md` → "Validation Strategy"

---

## Key Files Explained

| File | Purpose | Read Time | Priority |
|------|---------|-----------|----------|
| `FINDINGS_SUMMARY.md` | Quick reference, executive summary | 10 min | **HIGH** |
| `AI_PERSPECTIVE_ANALYSIS.md` | Complete AI assessment | 30 min | **HIGH** |
| `README.md` | Full framework documentation | 20 min | **HIGH** |
| `IMPLEMENTATION_SUMMARY.md` | What's been built | 10 min | Medium |
| `docs/theoretical-framework/*.md` | Mathematical theory | 30 min | Medium |
| `examples/quickstart.py` | Working code demo | 5 min run | **HIGH** |
| `simulations/core/*.py` | Core implementation | 1-2 hours | Low (unless coding) |
| `tests/*.py` | Validation tests | 30 min | Low |

---

## Common Questions

### "Is this clinically validated?"
**No.** This is a theoretical and computational framework. See "Research Status" in README.md.

### "Can I use this for diagnosis/treatment?"
**No.** This is research only. Not a clinical tool. See disclaimers in README.md.

### "What are the key findings?"
See `FINDINGS_SUMMARY.md` → "Key Computational Findings" section.

### "How does this differ from traditional views?"
See `README.md` → "From Chemical Suppression → Systemic Restoration" and `AI_PERSPECTIVE_ANALYSIS.md` → "Paradigm Shift".

### "What needs to happen for validation?"
See `AI_PERSPECTIVE_ANALYSIS.md` → "Falsifiable Predictions" and "Next Steps for Validation".

### "How do I run the code?"
See `README.md` → "Installation" → "Quick Start" → `examples/quickstart.py`.

### "What are the visualizations showing?"
Each PNG file corresponds to an example script. See `examples/README.md` for which script generates which figure.

---

## Suggested Reading Sequences

### **Sequence A: Quick Understanding (30 minutes)**
1. `FINDINGS_SUMMARY.md` (10 min)
2. `README.md` - skim key sections (10 min)
3. Look at `docs/figures/quickstart_results.png` (2 min)
4. `AI_PERSPECTIVE_ANALYSIS.md` - Executive Summary (8 min)

### **Sequence B: Evaluation for Research (1 hour)**
1. `FINDINGS_SUMMARY.md` (10 min)
2. `AI_PERSPECTIVE_ANALYSIS.md` - full read (30 min)
3. `docs/theoretical-framework/02-neuro-coherence-function.md` (10 min)
4. `docs/theoretical-framework/03-operators.md` (10 min)

### **Sequence C: Hands-On Exploration (2 hours)**
1. `README.md` → Installation (15 min)
2. `examples/quickstart.py` → Run and modify (30 min)
3. `examples/custom_simulation.py` → Experiment (45 min)
4. `simulations/core/neuro_coherence.py` → Study code (30 min)

### **Sequence D: Complete Deep Dive (4+ hours)**
1. All of Sequence A (30 min)
2. All of Sequence B (1 hour)
3. All of Sequence C (2 hours)
4. `tests/` → Run and study (30 min)
5. Full codebase exploration (varies)

---

## What to Skip (Initially)

Unless you have specific needs:
- `.github/` - CI/CD configuration
- `setup.py`, `setup.cfg`, `pyproject.toml` - Package configuration
- `CONTRIBUTING.md` - Only if contributing code
- `CITATION.cff` - Only if citing in paper
- `CI_SETUP_COMPLETE.md` - CI implementation notes
- `WORKFLOW_SUMMARY.md` - Development workflow

---

## Visual Summary of Repository

```
Neuro-Coherence-Framework/
│
├── 📄 FINDINGS_SUMMARY.md          ← START HERE (Quick overview)
├── 📄 AI_PERSPECTIVE_ANALYSIS.md   ← THEN HERE (Deep analysis)
├── 📄 README.md                    ← Main documentation
│
├── 📁 docs/theoretical-framework/  ← Mathematical theory
│   ├── 02-neuro-coherence-function.md
│   └── 03-operators.md
│
├── 📁 examples/                    ← Working code demos
│   ├── quickstart.py              ← Run this first
│   ├── custom_simulation.py
│   └── full_analysis.py
│
├── 📁 simulations/core/            ← Core math implementation
│   ├── neuro_coherence.py         ← Ψ function
│   └── operators.py               ← Γ, Θ, Δ, Λ
│
├── 📁 analysis/                    ← Data analysis modules
│   ├── eeg/                       ← EEG analysis
│   ├── fmri/                      ← fMRI analysis
│   └── integration/               ← Multimodal fusion
│
├── 📁 tests/                       ← Test suite
├── 📁 data/synthetic/              ← Data generators
│
└── 📁 docs/figures/                ← Generated visualizations
    ├── quickstart_results.png
    ├── longitudinal_analysis.png
    └── ... (7 total)
```

---

## Questions or Contributions?

See `CONTRIBUTING.md` for guidelines.

---

**Last Updated**: February 13, 2026  
**Version**: 1.0
