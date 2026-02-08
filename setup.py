from pathlib import Path
from setuptools import setup, find_packages

this_dir = Path(__file__).parent
long_desc = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="dynatrace-dpl-helper",
    version="0.1.1",
    description="Generate Dynatrace log parsing (DPL) rules from sample logs",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dynatrace-dpl-helper=dt_log_helper.cli:main"
        ]
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
