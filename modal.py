from pydantic import BaseModel , Field;
from typing import List , Tuple;
# Models
class Student(BaseModel):
   id: int
   name :str = Field(None, title="The description of the item", max_length=15)
   subjects: List[str] = []
   marks: List[int] = [] 
   percent_marks: float

class Percent(BaseModel):
   id:int
   name :str = Field(None, title="name of student", max_length=15)
   percent_marks: float


class Supplier(BaseModel):
   supplierID:int
   supplierName:str

class Product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:Supplier

class Customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[Product]

class Book(BaseModel):
   id: int
   title: str
   author: str
   publisher: str


class Query_Dependency:
   def __init__(self, id: str, name: str, age: int):
      self.id = id
      self.name = name
      self.age = age 