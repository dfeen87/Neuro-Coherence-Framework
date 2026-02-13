"""Setup script for Neuro-Coherence Framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neuro-coherence-framework",
    version="0.1.0",
    author="Don Michael Feeney Jr.",
    description="A Computational Systems Neuroscience Approach to Affective Stability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfeen87/Neuro-Coherence-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.0",
    ],
    extras_require={
        "full": [
            "mne>=0.24.0",
            "nilearn>=0.8.0",
            "plotly>=5.0.0",
            "dash>=2.0.0",
            "networkx>=2.6.0",
        ],
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
    },
)
