import datetime
import uvicorn;
from fastapi import FastAPI, HTTPException , Path , Header ,Depends, Request;
from fastapi.responses import HTMLResponse;
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional;

from modal import Student , Percent , Customer , Book , Query_Dependency;

app = FastAPI()

origin : list[str] = {
   "http://localhost",
   "http://localhost:8080",
   "http://127.0.0.1:8000"
}

# Events
@app.on_event("startup")
async def startup_event():
   print('Server started :', datetime.datetime.now())
@app.on_event("shutdown")
async def shutdown_event():
   print('server Shutdown :', datetime.datetime.now())
   

#middlewares
app.add_middleware(
   CORSMiddleware,
   allow_origins=origin,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.middleware("http")
async def addmiddleware(request: Request, call_next):
   print("Middleware works!")
   response = await call_next(request)
   return response

#Default method
@app.get("/")
async def index():
    return {"Hello": "Pavan Welcome to Fast API"}

#Returning html Element
@app.get("/hellohtml")
async def welcome_html():
     html='''
         <html>
            <body>
                <h2>Hello World!</h2>
            </body>
        </html>
    '''
     return HTMLResponse(content=html) 


# Path with params
@app.get("/hello/{name}/{age}")
async def hello(name : str = Path(...,min_length=3,
max_length=10), age : int = Path(..., ge=1, le=100)):
    return {"name" : name , "age" : age}

@app.post("/students/")
async def post_student_data(s1:Student):
    return s1

@app.post("/marks", response_model=Percent)
async def get_marks(s1:Student):
    s1.percent_marks = sum(s1.marks)/2
    return s1


#reading values from headers
@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
   return {"Accept-Language": accept_language} 


@app.post('/invoice')
async def getInvoice(c1:Customer):
   return c1


# Dependency injection on function and decorators

async def validate(dep: Query_Dependency = Depends(Query_Dependency)):
   if dep.age > 18:
      raise HTTPException(status_code=400, detail="You are not eligible")
   
@app.get("/userquery" , dependencies=[Depends(validate)])
async def user():
    return {"message": "You are eligible"}

@app.get("/user")
async def user(dep : Query_Dependency = Depends(Query_Dependency)):
    return dep


@app.get("/admin/")
async def admin(dep: Query_Dependency = Depends(Query_Dependency)):
   return dep 


#CURD Operations
data: list =[]

@app.post("/book")
def add_book(book: Book):
   data.append(dict(book))
   return data

@app.get("/list")
def get_books():
   return data

@app.get("/book/{id}")
def get_book(id: int):
   id = id - 1
   return data[id]

@app.put("/book/{id}")
def add_book(id: int, book: Book):
   data[id-1] = book
   return data

@app.delete("/book/{id}")
def delete_book(id: int):
   data.pop(id-1)
   return data

# Instaed of running this command on console "uvicorn main:app --reload"
if __name__== "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)