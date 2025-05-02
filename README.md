# Origin Project
![](https://img.shields.io/badge/Python-3.8-blue)
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)
![](https://img.shields.io/badge/lastest-2025--02--27-green)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)

Clonable referential to initialize a Python project with the best practice.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
  - [For Linux](#for-linux)
  - [For Windows](#for-windows)
- [Usage](#uage)
- [Features](#features)
- [Tests](#tests)
- [To contribute](#to-contribute)
- [Licence](#licence)
- [Contact](#contact)


## Description

My Python project is a simple application that allows users to create, read,
update and delete the tasks. It is designed to be easy to use and expand.

## Installation

To install the project, make sure you have Python 3.8 or later version
and `pip` installed on your machine. And then run the following command lines.

### For Linux

```bash
git clone git@github.com:mokira3d48/PyOrigin.git my_project
cd my_project
sudo rm -r .git
git init
```

And then,

1. `sudo apt install cmake python3-venv` Install *Cmake* and *Virtual env*;
2. `make venv` or `python3 -m venv env` create a virtual env into directory
named `env`;
3. `source env/bin/activate` activate the virtual environment named `env`;
4. `make install` install the requirements of this package;
5. `make dev` install the package in dev mode in virtual environment;
6. `make test` run the unit test scripts located at `tests` directory;
7. `make run` run script located at `src/package_name/__main__.py`.
8. Or Run `mycmd` as a command line to run `src/package_name/__main__.py`.

### For Windows

```bash
git clone git@github.com:mokira3d48/PyOrigin.git my_project
cd my_project
```

And then, delete the hidden directory named `.git` located at the root
of the directory project.

And then,

1. Install python for windows;
2. Open your command prompt;
3. Run `python3 -m venv env` to create a virtual env into directory
named `env`;
4. Run `pip install -r requirements` to install the requirements
of this package or project;
5. Run `pip install -e .` install the package in dev mode in virtual
environment;
6. Run `python3 -m package_name` to run main script located
at `src/package_name/__main__.py`. Or Run `mycmd` as a command line
to run `src/package_name/__main__.py` and start the application.


---

## Usage

Here is an example how to add a new task:

```python
from package_name.utils import get_file_paths_list


def main():
    """Main function
    """
    file_paths = get_file_paths_list('./')
    file_paths = sorted(file_paths)
    print("List of file paths:", file_paths)


if __name__ == '__main__':
    main()

```

## Features

- Add tasks.
- Mark tasks as complete.
- Delete tasks.
- Show all the tasks.

## Tests

To execute the unittest, make sure you have `pytest` package installed,
and then run the following command line:

```bash
make test 
```
or

```shell
pytest
```

---

## To contribute

Contributions are welcome! Please follow these steps:

1. Create a new branch for your feature (`git checkout -b feature/my-feature`);
2. Commit your changes (`git commit -m 'Adding a new feature'`);
3. Push toward the branch (`git push origin feature/my-feature`);
4. Create a new *Pull Request* or *Merge Request*.

## Licence

This project is licensed under the MIT License. See the file [LICENSE](LICENSE)
for more details, contact me please.

## Contact

For your question or suggestion, contact me please :

- **Name** : Your name (Arnold Mokira)
- **Email** : Your email address (dr.mokira@gmail.com)
- **GitHub** : [Your GitHub or Gitlab profile](https://github.com/mokira3d48)


### Explications des sections : (A supprimer du README.md)

- **Titre et description** : Le titre du projet et une brève description de ce qu'il fait.
- **Table des matières** : Une liste de sections pour faciliter la navigation.
- **Installation** : Instructions claires sur la façon d'installer le projet.
- **Utilisation** : Exemples d'utilisation pour aider les utilisateurs à démarrer rapidement.
- **Fonctionnalités** : Une liste des fonctionnalités principales du projet.
- **Tests** : Instructions sur la façon d'exécuter les tests.
- **Contribuer** : Un guide sur la façon de contribuer au projet.
- **Licence** : Informations sur la licence du projet.
- **Contact** : Informations pour contacter le développeur ou l'équipe du projet.


Cet exemple de `README.md` est structuré et informatif, ce qui le rend utile
pour les utilisateurs et les contributeurs potentiels.
