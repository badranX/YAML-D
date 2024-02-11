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
    return os.linesep.join([s.rstrip() for s in text.splitlines() if s])

def test_dataframe_to_yaml():
    outio = io.StringIO()
    # Convert DataFrame to YAML
    write_dataframe(outio, df)


    # Test case 1: Check if the generated YAML has the correct structure
    expected_yaml = """
config1:
  key1: 'value1'
  key2: 'value2'

config2:
  keyA: 'valueA'
  keyB: 'valueB'

data:
  - name: 'Sami Aker'
    age: 30
    city: 'New York'
  - name: 'Jane Smith'
    age: 25
    city: 'San Francisco'
  - name: 'Bob Johnson'
    age: 35
    city: 'Chicago'
  - name: 'Test'
    age: 35
    city: 'Chicago'
"""
    outio.seek(0)
    assert normalize_yaml(outio.read()) == normalize_yaml(expected_yaml)
    
if __name__ == "__main__":
  test_dataframe_to_yaml()