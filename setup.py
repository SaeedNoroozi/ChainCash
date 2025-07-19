from setuptools import setup, find_packages

setup(
    name="chaincash",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "web3>=6.0.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ]
    },
    python_requires=">=3.9",
    description="ChainCash - Crypto payments library for BEP20",
    author="Saeed Noroozi",
    license="MIT",
    url="https://github.com/SaeedNoroozi/ChainCash",
)
