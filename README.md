Code for blog [How to turn a 1000-line messy SQL into a modular, & easy-to-maintain data pipeline?](https://www.startdataengineering.com//post/quick-scalable-business-value-pipeline/)

# Setup 

```bash
python -m venv ./env
source env/bin/activate
pip install -r requirements
python setup.py
```

# Run ETL

```bash
duckdb database.db < messy_query.sql
python modular_code.py
```

# Run tests

```bash
pytest test_modular_code.py
```
