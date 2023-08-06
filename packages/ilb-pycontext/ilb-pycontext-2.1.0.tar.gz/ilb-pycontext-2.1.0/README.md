# pycontext

Build application context from context.xml/web.xml/env and so

```python
from pycontext import ContextVariable
from pycontext.context import AppContext
from pycontext.reader import ContextXmlReader, EnvironmentReader

context = AppContext.from_readers([ContextXmlReader(), EnvironmentReader()])
variable: ContextVariable = context.get("key")
variable.name # == key
variable.value # == value
```
