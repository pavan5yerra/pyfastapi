from typing import List;
from pydantic import BaseModel ,Field;


class Student(BaseModel):
   id: int
   name :str = Field(None, title="The description of the item", max_length=10)
   subjects: List[str] = []


data = {
   "id" : 1,
   "name" : "pavan",
   "subjects": ["maths" , "histroty"]
}
s1 : Student = Student(** data)


class rectangle:
    def __init__(self, w:int, h:int) ->None:
      self.width=w
      self.height=h
    

def area(r:rectangle)-> int:
    return r.width*r.height
    
r1=rectangle(10,20)
print ("area = ", area(r1))


