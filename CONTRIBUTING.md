# Contributing to Neuro-Coherence Framework

## Current Development Status

**This project is currently in private development and validation.**

We're taking time to build a solid foundation before opening to public contributions. This approach ensures:
- Scientific rigor and reproducibility
- Thorough validation of core concepts
- High-quality codebase from the start
- Responsible claims and framing

## Private Development Phase

### What This Means

During this phase, we are:
- ✅ Working with select domain experts
- ✅ Validating computational models
- ✅ Building comprehensive documentation
- ✅ Ensuring reproducibility
- ❌ Not accepting public pull requests
- ❌ Not seeking open collaboration yet

### Why This Approach?

**Quality Over Speed**
- Time to identify and fix fundamental issues
- Opportunity for expert peer review
- Build proper testing infrastructure
- Ensure scientific integrity

**Responsible Science**
- Avoid premature claims or hype
- Validate assumptions before public release
- Get medical disclaimers right
- Ensure framework is testable and falsifiable

**Professional Development**
- Establish coding standards
- Create comprehensive documentation
- Build reproducible workflows
- Set clear scope and limitations

## How You Can Help (Currently)

### If You're a Researcher

If you have relevant expertise in:
- Computational neuroscience
- Bipolar disorder research
- Network dynamics modeling
- Neuroimaging analysis
- Psychiatric computational modeling

**You can:**
1. Review the theoretical framework in `/papers/original/`
2. Identify potential issues or limitations
3. Reach out privately to discuss (see Contact section below)
4. Understand this is early-stage, theoretical work

**Please don't:**
- Submit pull requests (they won't be merged yet)
- Share publicly as validated science
- Make clinical recommendations based on this work
- Oversell or hype the framework

### If You're Interested in This Work

**You can:**
- ⭐ Star the repository to follow development
- 📖 Read the documentation and theoretical framework
- 🤔 Think critically about the approach
- 💭 Form your own opinions about viability

**Please understand:**
- This is theoretical, unvalidated work
- No timeline for public release
- Quality gates must be met first
- We're building carefully, not quickly

## Future Public Contribution Phase

Once core validation is complete and quality gates are met, we will welcome:

### Types of Contributions We'll Need

**Code Contributions**
- Simulation improvements and optimizations
- Analysis pipeline enhancements
- Visualization tools
- Testing and validation code
- Bug fixes and performance improvements

**Documentation**
- Tutorial notebooks and examples
- Method comparisons and explanations
- Literature synthesis and reviews
- Translation to other languages
- API documentation improvements

**Scientific Contributions**
- Parameter validation studies
- Model comparison analyses
- Literature meta-analyses
- Statistical validation methods
- Biomarker operationalization

**Data Contributions**
- Synthetic dataset generation
- Literature value extraction
- Meta-analysis data compilation
- (NOT raw patient data - privacy concerns)

### Contribution Standards (When We Open)

When we do accept contributions, we'll require:

**Code Standards**
```python
# Clear, documented code
def calculate_gamma(plv_data, baseline, perturbation_window):
    """
    Calculate adaptive gain (Γ) from phase-locking values.
    
    Parameters
    ----------
    plv_data : ndarray
        Phase-locking values over time
    baseline : float
        Pre-perturbation baseline PLV
    perturbation_window : tuple
        (start_time, end_time) of perturbation
        
    Returns
    -------
    gamma_score : float
        Adaptive gain coefficient (0-1)
        
    References
    ----------
    .. [1] Feeney, D.M. (2025). Neuro-Coherence Framework.
    """
    # Implementation...
    pass
```

**Documentation Standards**
- Clear explanations of methods
- Proper citations to literature
- Examples and use cases
- Limitations and assumptions stated

**Testing Requirements**
- Unit tests for all functions
- Integration tests for workflows
- Validation against known results
- Reproducibility verification

**Scientific Rigor**
- Transparent methodology
- Stated assumptions and limitations
- Proper statistical methods
- Reproducible results

## Code of Conduct

### Our Standards

**Scientific Integrity**
- Honest about limitations and uncertainties
- Transparent about theoretical nature of work
- Proper attribution and citations
- No overselling or hype

**Respectful Communication**
- Professional and courteous discourse
- Constructive criticism welcomed
- Disagreement is fine; disrespect is not
- Focus on ideas, not individuals

**Responsible Research**
- Patient safety and wellbeing paramount
- Clear medical disclaimers
- No clinical recommendations
- Emphasis on validation requirements

**Collaborative Spirit**
- Credit where credit is due
- Open to diverse perspectives
- Building together, not competing
- Science serves humanity

### Unacceptable Behavior

- Making clinical recommendations based on unvalidated work
- Sharing as validated science prematurely
- Plagiarism or lack of attribution
- Harassment or unprofessional conduct
- Overselling or hyping the framework
- Ignoring medical disclaimers

## Development Workflow (Future)

When we open to contributions, the workflow will be:

### 1. Discussion First
- Open an issue describing proposed contribution
- Discuss approach and feasibility
- Get feedback before coding
- Ensure alignment with project goals

### 2. Fork and Branch
```bash
git clone https://github.com/yourusername/neuro-coherence-framework.git
git checkout -b feature/your-feature-name
```

### 3. Develop with Tests
```bash
# Make changes
# Write tests
pytest tests/

# Ensure code quality
black simulations/
pylint simulations/
```

### 4. Document
- Update relevant documentation
- Add docstrings to functions
- Include examples if applicable
- Update CHANGELOG.md

### 5. Submit Pull Request
- Clear description of changes
- Link to related issue
- Include test results
- Follow PR template

### 6. Review Process
- Maintainers will review
- May request changes
- Discussion and iteration
- Merge when approved

## Technical Setup (Future)

When contributing becomes available:

### Development Environment
```bash
# Clone repository
git clone https://github.com/dfeen87/neuro-coherence-framework.git
cd neuro-coherence-framework

# Create environment
conda env create -f simulations/environment.yml
conda activate neurocoherence

# Install in development mode
pip install -e .

# Run tests
pytest tests/
```

### Coding Standards
- **Python**: PEP 8, type hints encouraged
- **Docstrings**: NumPy style
- **Testing**: pytest framework
- **Formatting**: black, isort
- **Linting**: pylint, flake8

### Commit Messages
```
type(scope): Brief description

Longer explanation if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

## Project Structure

Contributions should respect the modular structure:

```
neuro-coherence-framework/
├── simulations/        # Core computational models
├── analysis/          # Data analysis tools (EEG, fMRI, integration)
├── data/             # Data generation and resources
├── docs/             # Documentation, summaries, and figures
├── examples/         # Usage examples and demos
└── tests/            # Test suite
```

## Questions?

### During Private Development

If you have questions or want to discuss the framework:
- Review existing documentation first
- Understand this is theoretical work
- Contact privately if you have relevant expertise

### Current Focus Areas

We're currently working on:
- Validating computational models
- Parameter sensitivity analysis
- Comprehensive documentation
- Reproducibility testing
- Expert peer review

## Timeline

**There is no public timeline.** 

We will open to contributions when:
- Core simulations are validated
- Documentation is comprehensive
- Testing infrastructure is solid
- Quality gates are met
- We're confident in the foundation

**Quality over speed. Always.**

## Recognition

When we do open to contributions, all contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in relevant documentation
- Acknowledged in publications (where appropriate)
- Appreciated for their time and expertise

## Contact

For private discussion of the framework:
- **Not ready**: Public issues or PRs
- **Appropriate**: Private email to Don Feeney (dfeen87@gmail.com)
- **Expected**: Understanding of early-stage nature

---

## Summary

**Right Now:**
- ❌ Not accepting public contributions
- ✅ Building foundation carefully
- ✅ Working with select experts
- ✅ Welcome to follow development

**Future:**
- ✅ Will welcome contributions when ready
- ✅ High standards for quality
- ✅ Collaborative and respectful
- ✅ Serving science and patients

**Always:**
- 🧠 Scientific integrity first
- 🔬 Validation before claims
- 🤝 Respect and professionalism
- ❤️ Patient wellbeing paramount

---

Thank you for understanding our careful, responsible approach to development.

**We're building something that matters. We're taking the time to do it right.**

<div align="center">

*Last Updated: February 2026*  
*Status: Private Development*

</div>
