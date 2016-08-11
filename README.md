# python-visitor

Simple Visitor Pattern implementation for Python 3

```python
import visitor

class MyVisitor(metaclass=visitor.Visitor):

    def visit(self, node: str):
        print('Do something with string', node)

    def visit(self, node: int):
        print('Do something with int', int)

    def default(self, node):
        print('handle default case')
        
v = MyVisitor()
v.visit('Hello')
v.visit(42)
```
