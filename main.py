
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database init
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    type TEXT,
                    location TEXT,
                    cost REAL,
                    revenue REAL,
                    profit_estimate REAL,
                    break_even TEXT,
                    risk_score TEXT
                )''')
    # Insert demo project
    c.execute("INSERT INTO projects (user_id, name, type, location, cost, revenue, profit_estimate, break_even, risk_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (1, 'Demo Project', 'Service', 'Riyadh', 100000, 180000, 80000, '1.5 years', 'Low'))
    conn.commit()
    conn.close()

init_db()

# Project model
class Project(BaseModel):
    user_id: int
    name: str
    type: str
    location: str
    cost: float
    revenue: float

@app.post("/create_project")
def create_project(project: Project):
    profit = project.revenue - project.cost
    break_even = "1.5 years"
    risk_score = "Medium"
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO projects (user_id, name, type, location, cost, revenue, profit_estimate, break_even, risk_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (project.user_id, project.name, project.type, project.location, project.cost, project.revenue, profit, break_even, risk_score))
    conn.commit()
    conn.close()
    return {"message": "Project created successfully"}

@app.get("/projects")
def get_projects():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    rows = c.fetchall()
    conn.close()
    return rows
