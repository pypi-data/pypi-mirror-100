# Getting Started
## CommandLine
```bash
$ pip install csirtgsdk~=2.0a6
$ csirtg 1.1.1.1
```

## Python SDK
```python

from pprint import pprint
from csirtgsdk import search, risk

for i in search('1.1.1.1'):
    pprint(i)
    
    
i = risk('1.1.1.1')
pprint(i)
```

# Getting Involved
There are many ways to get involved with the project. If you have a new and exciting feature, or even a simple bugfix, simply [fork the repo](https://help.github.com/articles/fork-a-repo), create some simple test cases, [generate a pull-request](https://help.github.com/articles/using-pull-requests) and give yourself credit!

If you've never worked on a GitHub project, [this is a good piece](https://guides.github.com/activities/contributing-to-open-source) for getting started.

# COPYRIGHT AND LICENSE

Copyright (C) 2021 [the CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [Mozilla Public License (MPLv2)](https://www.mozilla.org/en-US/MPL/2.0/).
