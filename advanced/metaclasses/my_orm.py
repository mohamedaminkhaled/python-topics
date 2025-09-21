
"""
tiny Django-like ORM in pure Python using metaclasses so you see the real power.

We’ll implement:
    A Model base class (with a metaclass).
    Auto-registration of models.
    A fake database backend (just a dictionary).
    A .save() method.
    A .filter() query method.
"""

# Step 1: Fake Database
FAKE_DB = {}

# Step 2: Define the Metaclass
class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        if name != "Model":
            print(f"Registering model: {name}")

            # Collect fields (ignore dunder methods)
            fields = {k: v for k, v in dct.items() if not k.startswith("__")}
            dct["_fields"] = fields

            # Register model
            FAKE_DB[name] = []
        return super().__new__(cls, name, bases, dct)

# Step 3: Define Base Model
class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        # Assign values to fields
        for field in self._fields:
            setattr(self, field, kwargs.get(field))

    def save(self):
        """Save object to fake DB."""
        table = FAKE_DB[self.__class__.__name__]
        row = {field: getattr(self, field) for field in self._fields}
        table.append(row)

    @classmethod
    def all(cls):
        """Return all rows of this model."""
        return FAKE_DB[cls.__name__]

    @classmethod
    def filter(cls, **kwargs):
        """Simple filter by field equality."""
        results = []
        for row in FAKE_DB[cls.__name__]:
            if all(row.get(k) == v for k, v in kwargs.items()):
                results.append(row)
        return results

# Step 4: Define Models
class Book(Model):
    title = "CharField"
    pages = "IntegerField"

class Author(Model):
    name = "CharField"
    age = "IntegerField"

# Step 5: Use the ORM
# Create instances
b1 = Book(title="Python 101", pages=200)
b2 = Book(title="Django Deep Dive", pages=500)
a1 = Author(name="Alice", age=30)

# Save to DB
b1.save()
b2.save()
a1.save()

# Query
print("All Books:", Book.all())
print("Books with 500 pages:", Book.filter(pages=500))
print("Authors named Alice:", Author.filter(name="Alice"))

