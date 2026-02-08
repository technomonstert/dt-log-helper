# setup.py for internal Dynatrace Alert-Insights
from pathlib import Path
from setuptools import setup, find_packages

this_dir = Path(__file__).parent
long_desc = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="dt-alert-insights",
    version="0.0.1",
    description="Multi‑tenant Dynatrace alert‑diagnostic tool (internal only)",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28",
        "pyyaml>=6.0"
    ],
    entry_points={"console_scripts": ["dt-alert-insights=dt_alert_insights.cli:main"]},
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
)
