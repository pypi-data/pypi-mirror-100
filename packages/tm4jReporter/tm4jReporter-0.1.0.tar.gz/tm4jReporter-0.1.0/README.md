# tm4j-reporter
TM4J (Zephyr Scale) Reporter

#### Support automation framework
- robotframework

#### Example
- Upload results into Zephyr Scale
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from tm4jReporter import Tm4jReporter


rb = Tm4jReporter(
    jira_url='https://jira.xxx.com',
    jira_user='will',
    jira_pass='password',
    jira_project='TM4J'
)
rb.robotframework('output.xml')
```

- Upload results into Zephyr Scale Cycle
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from tm4jReporter import Tm4jReporter


rb = Tm4jReporter(
    jira_url='https://jira.xxx.com',
    jira_user='will',
    jira_pass='password',
    jira_project='TM4J'
)
rb.robotframework(
    output_xml_file='output.xml', 
    cycle_key='TM4J-C1'
)
```
