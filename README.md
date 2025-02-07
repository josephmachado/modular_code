Code for blog [How to turn a 1000-line messy SQL into a modular, & easy-to-maintain data pipeline?](https://www.startdataengineering.com//post/quick-scalable-business-value-pipeline/)

# Setup 

Clone the repo and setup a virtual environment:

```bash
git clone https://github.com/josephmachado/modular_code.git
cd modular_code
python -m venv ./env
source env/bin/activate
pip install -r requirements
python setup.py
```

# Run ETL

The ETL can be run as a [query](./messy_query.sql) or as our modular code at [modular_code.py](./modular_code.py).

```bash
duckdb database.db < messy_query.sql
python modular_code.py
```

# Compare data

We use `datacompy` to compare datasets, we can run this using the following command:

```bash
python compare_dataset.py
```

# Run tests

We have tests defined at [test_modular_code.py](./test_modular_code.py) which we can run as shown below:

```bash
pytest test_modular_code.py
```
