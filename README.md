# nsw_covid_rules

This repository contains COVID related rules for NSW, as described in the Public Health Orders (PHO).

PHO coded in this repo can be found at: https://www.legislation.nsw.gov.au/file/Public%20Health%20(COVID-19%20Additional%20Restrictions%20for%20Delta%20Outbreak)%20Order%20(No%202)%202021_210829.pdf

## Installing

> We recommend that you use a virtualenv to install OpenFisca. If you don't,
you may need to add `--user` at the end of all commands starting by `pip`.

```sh
python3 -m venv covid
deactive
source covid/bin/activate

```
To install your extension, run:

```sh
make install
```

## Testing

You can make sure that everything is working by running the provided tests:

```sh
make test
```

To add your extension to the NSW API, update the openfisca-nsw-API repo's makefile with your
extension's name, and add your extension as a dependency.

> [Learn more about tests](http://openfisca.org/doc/coding-the-legislation/writing_yaml_tests.html).

Your extension package is now installed and ready!
