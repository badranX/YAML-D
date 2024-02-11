import pandas as pd
from yamld.read import read_onelist_dataframe

# Sample YAML content
yaml_content = """
config1:
  key1: 'value1'
  key2: 'value2'
  key3: 'value3'

config2:
  keyA: 'valueA'
  keyB: 'valueB'
  keyC: 'valueC'

data:
  - name: 'John Doe'
    age: 30
    city: 'New York'
  - name: 'Jane Smith'
    age: 25
    city: 'San Francisco'
  - name: 'Bob Johnson'
    age: 35
    city: 'Chicago'
  - name: 'Test'
    age: 35.0
    city: 'Chicago'
"""

def test_read_onelist_dataframe():
    # Test case 1: Check if the function returns a DataFrame
    df = read_onelist_dataframe(yaml_content.splitlines())
    assert isinstance(df, pd.DataFrame)

    # Test case 2: Check if the DataFrame has the correct number of rows
    assert len(df) == 4

    # Test case 3: Check if the DataFrame columns are correct
    expected_columns = ['name', 'age', 'city']
    assert all(col in df.columns for col in expected_columns)

    # Test case 4: Check if the values in the DataFrame are correct
    expected_values = [
        ['John Doe', 30, 'New York'],
        ['Jane Smith', 25, 'San Francisco'],
        ['Bob Johnson', 35, 'Chicago'],
        ['Test', 35.0, 'Chicago']
    ]
    for i, row in enumerate(df.itertuples(index=False)):
        assert list(row) == expected_values[i]


if __name__ == "__main__":
  test_read_onelist_dataframe()