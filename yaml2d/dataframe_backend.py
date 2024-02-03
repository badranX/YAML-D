from ast import literal_eval
import pandas as pd

if __name__ == "__main__":
    from read import Read
else:
    from .read import Read


class DictReader():
    def __init__(self):
        self.parents_with_objlist = set()
        self.parents = {}
        self.parents_types = {}


def _python_eval(value):
    return literal_eval(value)


def _cast_dataframe_types(df, obj_ytypes):
    for column, ytype in obj_ytypes.items():
        if ytype != list:
            ytype = pd.StringDtype() if ytype is str else ytype
            df[column] = df[column].astype(ytype)
    return df


def _python_dict_backend(out, is_last, current_parent, yaml_obj,  list_counter, ytypes):
    if is_last:
        return out
    yaml_obj = {k: _python_eval(v) for k, v in yaml_obj.items()}
    out = out if out else DictReader()
    if list_counter:
        out.parents_with_objlist.add(current_parent)
        tmp = out.parents.get(current_parent, {k: [v] for k, v in yaml_obj.items()})
        if list_counter > 1:
            for k, v in yaml_obj.items():
                try:
                    tmp[k].append(v)
                except (KeyError, IndexError) as e:
                    raise type(e)('KeyError, probably violating fixed features in a list \n' + str(e)) from e
        out.parents[current_parent] = tmp
    else:
        out.parents[current_parent] = yaml_obj

    return out


def _dataframe_backend(out, is_last, current_parent, yaml_obj, list_counter, ytypes):
    out = _python_dict_backend(out, is_last, current_parent, yaml_obj, list_counter, ytypes)
    if is_last:
        for k, v in out.parents.items():
            if k in out.parents_with_objlist:
                df = pd.DataFrame(v)
                obj_types = ytypes[k]
                df = _cast_dataframe_types(df, obj_types)
                out.parents[k] = df
        return out.parents
    return out


def _dataframe_backend_onelist(out, is_last, current_parent, yaml_obj, list_counter, ytypes):
    out = _python_dict_backend(out, is_last, current_parent, yaml_obj, list_counter, ytypes)
    if is_last:
        assert len(out.parents_with_objlist) <= 1
        objlist_parent = out.parents_with_objlist.pop()
        df = None
        for k, v in out.parents.items():
            if k == objlist_parent:
                df = pd.DataFrame(v)
                obj_types = ytypes[k]
                df = _cast_dataframe_types(df, obj_types)

        del out.parents[objlist_parent]
        df.attrs.update(out.parents)

            
def read2dataframe(path):
    read = Read(_dataframe_backend)
    with open(path, 'r') as f:
        return read.read(f)


def str2dataframe(stryaml2d):
    lines = stryaml2d.splitlines()
    read = Read(_dataframe_backend, is_onelist=False)

    return read.read(lines)


def read2gen(stryaml2d):
    lines = stryaml2d.splitlines()

if __name__ == "__main__": 
    yamlf = """
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
    out = str2dataframe(yamlf)
    print(out['config1'])
    print(out['config2'])
    print(out['data'])
    print(out['data'].dtypes)