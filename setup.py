from setuptools import setup, find_packages

def read_long_description():
    try:
        return open("README.md", encoding="utf-8").read()
    except UnicodeDecodeError:
        return open("README.md", encoding="utf-8", errors="ignore").read()

def read_requirements():
    raw = open("requirements.txt", encoding="utf-8", errors="ignore").read().splitlines()
    return [r.lstrip('\ufeff').strip() for r in raw if r.strip()]

setup(
    name="sistema_senhas_web2",
    version="0.1.0",
    author="Kalebe do Carmo Caldas",
    author_email="kalebe.caldas@hotmail.com",
    description="Sistema de senhas para clínica: geração, triagem e display",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/sistema_senhas_web2",
    packages=find_packages(exclude=["venv", "instance", "__pycache__"]),
    # adiciona o run.py como módulo top‐level
    py_modules=["run"],
    include_package_data=True,
    install_requires=read_requirements(),
        entry_points={
        "console_scripts": [
            "senhas-web = run:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
