import io
import os
import pandas as pd
from yamld.write import write_dataframe

# Sample DataFrame
data = {
    'name': ['Sami Aker', 'Jane Smith', 'Bob Johnson', 'Test'],
    'age': [30, 25, 35, 35],
    'city': ['New York', 'San Francisco', 'Chicago', 'Chicago']
}

df = pd.DataFrame(data)
df.attrs['config1'] = {'key1': 'value1',
                       'key2': 'value2'}

df.attrs['config2'] = {'keyA': 'valueA', 
                       'keyB': 'valueB'}

def normalize_yaml(text):
    return os.linesep.join([s.strip() for s in text.splitlines() if s])

def test_dataframe_to_yaml_mini():
    outio = io.StringIO()
    # Convert DataFrame to YAML
    write_dataframe(outio, df, is_mini=True)


    # Test case 1: Check if the generated YAML has the correct structure
    expected_yaml = """
config1:
  key1: 'value1'
  key2: 'value2'

config2:
  keyA: 'valueA'
  keyB: 'valueB'

data:
  - - name:
    - age: 
    - city:

  - - 'Sami Aker'
    - 30
    - 'New York'
  - - 'Jane Smith'
    - 25
    - 'San Francisco'
  - - 'Bob Johnson'
    - 35
    - 'Chicago'
  - - 'Test'
    - 35
    - 'Chicago'
"""

    outio.seek(0)
    assert normalize_yaml(outio.read()) == normalize_yaml(expected_yaml)
