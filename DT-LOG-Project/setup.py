# Dynatrace Rule Helper – package metadata

from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent

setup(
    name="dynatrace-rule-helper",
    version="0.1.1",
    description="Generate Dynatrace PARSE (DPL) rules from sample log lines.",
    long_description=(this_dir / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Mahi (User)",
    url="https://github.com/technomonstert/dt-log-helper",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["PyYAML>=5.4"],
    entry_points={"console_scripts": ["dynatrace-rule-helper=dynatrace_rule_helper.cli:main"]},
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
