from setuptools import find_packages, setup

setup(
    name="navigateur",
    version="1.0.1",
    description="Navigation ferroviaire et exploration de graphes",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "Unidecode>=1.3,<2",
        "Flask>=3.0,<4",
        "matplotlib>=3.8,<4",
        "scikit-learn>=1.3,<2",
        "numpy>=1.26,<3",
    ],
)
