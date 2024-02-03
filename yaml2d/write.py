import itertools 
LIST = True

class Write():
    def __init__(self):
        self.buffer = ""
        self.last_keys = None
        self.max_buffer_size = 400
        self.is_writing_list = False
    
    def write_entry(self, entry):
        if type(entry) is list:
            assert self.is_writing_list
            entry = dict(zip(self.last_keys, entry))

        if type(entry) is dict:
            self.last_keys = entry.keys()
            for i, keyval in enumerate(entry.items()):
                key, val = keyval
                if i == 0 and self.is_writing_list:
                    key = '- ' + key
                item = '  ' + key + ': ' + str(val)
                self.buffer += item + '\n'
        elif type(entry) is tuple:
            parent_name, islist = entry
            self.is_writing_list =  islist
            self.buffer += parent_name + ':' + '\n'
            
    def write(self, entries, path):
        with open(path, 'w') as f:
            for entry in entries:
                self.write_entry(entry)
                if len(self.buffer) > self.max_buffer_size:
                    f.write(self.buffer)
                    f.buffer = ""
            f.write(self.buffer)
                    
            
def write_dataframe(df, name, path):
    itr = df.iterrows()
    itr = df.to_dict(orient="records")
    itr = itertools.chain([(name, LIST)], itr)
    write = Write()
    write.write(itr, path)

if __name__ == "__main__":

    import pandas as pd

    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 22],
            'City': ['New York', 'San Francisco', 'Los Angeles']}

    df = pd.DataFrame(data)
    write_dataframe(df, "dataie", './out.yaml')

    # Note: In practice, it's important to be mindful of performance implications when iterating over rows in large dataframes. There are often more efficient vectorized operations that can be used in pandas.