
# (YAPOWF) Yet Another Power Factory API
This project contains a new python - power factory API. \
It is still in progress...

# How to install

```
$ pip install yapowf
```

# Connect Power Factory

```python
from yapowf import Network

## Connect to PF
credentials = {
    "path": r"pathon_module_path",
    "username": "your_username",
    "password": "your_password_if_needed",
}
pf = Network(**credentials)


## Activate a project
pf.activate_project("project_name_here")


## Activate a study case
pf.activate_study_case("studycase_name_here")


## Get grid params
bus_df = pf.get_bus_params()
line_df = pf.get_line_params()
gen_df = pf.get_gen_params()
trafo3_df = pf.get_3wtrafo_params()
trafo2_df = pf.get_2wtrafo_params()
shunt_df = pf.get_shunt_params()


## Search for an element name
## Allowed types: "line", "gen", "load", "trafo3w", "trafo2w", "shunt"
elems = pf.search_element_name("elem_name_here", "line")


## Want to run a power flow ??
res = pf.run_load_flow()

## Gettting results in dataframe
ld_gen_df = res.gen
ld_gen_pu_df = res.gen_pu


## Want to run a dynamic simulation ??
res = pf.run_dynamic_sim()

## Gettting results in dataframe
res_gen_df = res.gen
res_bus_df = res.bus


## All methods have associated DocStrings
help(pf.run_dynamic_sim)
```

# License
`GNU GNU GPLv3`
