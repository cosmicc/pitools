
import yaml

newdata = {'lat': 34.65, 'lon': 52.25, 'moar':'ffuts'}

with open('data.yml','r') as yamlfile:
    for data in yaml.safe_load_all(yamlfile): # Note the safe_load
        cur_yaml = data
    cur_yaml['Galaxy'].update(newdata)
    print(cur_yaml)
    

if cur_yaml:
    with open('data.yml','w') as yamlfile:
        yaml.safe_dump(cur_yaml, yamlfile, default_flow_style=False) # Also note the safe_dump
