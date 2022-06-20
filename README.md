# DAWE RLP Controlled Vocabularies

> Will be rebranded to DAWE NRM Controlled Vocabularies.

Proposed base URI of DAWE NRM Controlled Vocabularies:

```
https://linked.data.gov.au/def/nrm/
```

## Running

Open the repository in Visual Studio Code in a devcontainer. This can be done by running `command + shift + p` and selecting `Remote-Containers: Rebuild Container`. Note that Docker Desktop needs to be installed.

### Run tests

Run tests and generate a HTML coverage report.

```
make test
```

View HTML coverage report in a browser. This runs a Python web server on `htmlcov/`.

```
make htmlcov
```

### Generate categorical values

Pull from the Strapi API endpoints defined in `src/api/categorical_values/endpoints.py` and write Turtle files to `vocab_files/categorical_collections/luts`.

```
make luts
```

## Contact

Edmond Chuc  
e.chuc@uq.edu.au

Junrong Yu  
junrong.yu@uq.edu.au
