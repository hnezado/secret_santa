# Secret Santa app

#### Randomizes relations between different members following certain rules.
## Configuration tab
1. The input file can be opened from this tab clicking on *Open configuration file*.
2. Once opened, ***config.json*** must be filled with the following format:\
  "john": {\
    "name": "john",\
    "family_id": 1,\
    "age": "adult",\
    "exceptions": [\
      "allan",\
      "marie",\
      ...\
    ]\
  },
3. **Update** after any saved change in the config file.
## Run tab
1. Then **Roll** to display the randomized relationships.
2. You can **Clear** the results.
## Details
There are two types of members:
- Adults
- Children