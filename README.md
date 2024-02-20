# YAMLd

**YAMLd** is a tiny subset of *YAML* designed specifically for representing tabular data (for now, only *CSV*). It is particularly useful for datasets with numerous features or lengthy sequences that are hard to read. The **D** stands for data!

### YAMLd Rules:

- The hyphen symbol (`-`) is  only used to list the dataset. Other use cases are not permited.
- Each file contains only one dataset and optional meta data.
- Meta data are listed before the dataset.
- Meta data does not contain nested dictionaries, only key-value maps.
    
### Example

``` yaml
features_description:
  name: 'embloyee name'
  age: 'age'
  city: 'closest city to adress'

extra: 3.4

whatever_name_for_your_data:
  - name: 'John Doe'
    age: 30
    city: 'New York'
  - name: 'Jane Smith'
    age: 25
    city: 'San Francisco'
  - name: 'Bob Johnson'
    age: 35
    city: 'Chicago'
```

Using a 'mini' version of this, you can remove the feature names from each line as follows.

``` yaml
data:
  - - name:
    - age: 
    - city:
  - - 'John Doe'
    - 30
    - 'New York'
  - - 'Jane Smith'
    - 25
    - 'San Francisco'
  - - 'Bob Johnson'
    - 35
    - 'Chicago'
```

**Note:** It is still experimental, use it with caution.

## Convert CSV to YAMLd and vice versa:
```console
csv2yamld <your-csv-file>
```

```console
yamld2csv <your-yamld-file>
```

For more details use `csv2yamld -h` or `yamld2csv -h`.

## Open CSV files with VIM/NVIM
Reading *CSV* can be annoying, here is a simple solution:

```console
csv2yamld <your-csv-file> --stdout | nvim -c 'set filetype=yaml' -
```

Of course, you can edit it, save it, and convert it back to *CSV* using `yamld2csv`.


## Setup
```console 
pip install -U yamld
```

To install without virtual environments, you can use [*pipx*](https://github.com/pypa/pipx). Another option is to pass `--break-system-packages` to *pip*, but it's not advisable.

## Details
The main goal is to edit and view your data files with nothing but your text editor. Consequently, a lot of YAML features are not supported, as their inclusion could either introduce clutter or hinder the parsing efficiency for datasets.

### Data Types:
- Dataset data types:
    - List: surrounded with `[]`
    - String: surrounded with `""` or `''` 
    - Number
- Meta data has one extra data type:
    - key-value maps: value can only be one of the other types used for the dataset.
    
 **Note:** YAML explicit types marking and comments are not supported.
