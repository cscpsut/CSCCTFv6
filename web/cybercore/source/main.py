import re
import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlite3 import connect

# FLAG = 'CSCCTF{sql_m4p_c0uldnt_h3lp_y0u_w1th_th1s_0ne}'
FLAG = os.getenv('FLAG', 'CSCCTF{sql_m4p_c0uldnt_h3lp_y0u_w1th_th1s_0ne}')

app = FastAPI()
templates = Jinja2Templates(directory="templates")
static = StaticFiles(directory="static")

db_connection = connect(":memory:", check_same_thread=False)
cursor = db_connection.cursor()

INIT_SQL = f'''
    CREATE TABLE legacy_devices (
        device_id INTEGER PRIMARY KEY,
        model_name TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        release_date TEXT NOT NULL,
        processor_speed TEXT,
        memory_size TEXT,
        storage_capacity TEXT,
        last_firmware_update TEXT,
        status TEXT
    );

    CREATE TABLE system_logs (
        log_id INTEGER PRIMARY KEY,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        log_level TEXT NOT NULL,
        source_ip TEXT,
        user_agent TEXT,
        action_type TEXT,
        description TEXT,
        success INTEGER
    );

    CREATE TABLE user_profiles (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT,
        join_date TEXT,
        last_login TEXT,
        access_level INTEGER,
        department TEXT,
        is_active INTEGER
    );

    CREATE TABLE chat_rooms (
        room_id INTEGER PRIMARY KEY,
        room_name TEXT NOT NULL,
        created_date TEXT,
        max_users INTEGER,
        current_users INTEGER,
        room_type TEXT,
        is_moderated INTEGER,
        description TEXT
    );

    CREATE VIEW secret_view AS
        SELECT '{FLAG}' AS secret;

    INSERT INTO legacy_devices VALUES
        (1, 'PalmPilot Pro', 'Palm Computing', '1997-03-10', '16 MHz', '512 KB', '1 MB', '1999-12-31', 'archived'),
        (2, 'iPod Classic', 'Apple', '2001-10-23', '90 MHz', '32 MB', '5 GB', '2002-03-15', 'active'),
        (3, 'BlackBerry 5810', 'RIM', '2002-03-04', '133 MHz', '8 MB', '8 MB', '2003-06-20', 'maintenance'),
        (4, 'Nokia 3310', 'Nokia', '2000-09-01', '84 MHz', '2 MB', '2 MB', '2001-01-01', 'active'),
        (5, 'Sony Ericsson T68', 'Sony Ericsson', '2001-03-19', '75 MHz', '1 MB', '1 MB', '2002-05-15', 'archived');

    INSERT INTO system_logs VALUES
        (1, '2002-12-31 23:59:59', 'WARNING', '192.168.1.100', 'Mozilla/4.0', 'login_attempt', 'Multiple failed login attempts', 0),
        (2, '2002-12-31 23:58:59', 'INFO', '192.168.1.101', 'Mozilla/5.0', 'file_access', 'User accessed system configuration', 1),
        (3, '2002-12-31 23:57:59', 'ERROR', '192.168.1.102', 'Mozilla/4.0', 'data_breach', 'Unauthorized data access', 0),
        (4, '2002-12-31 23:56:59', 'DEBUG', '192.168.1.103', 'Mozilla/5.0', 'system_check', 'System check completed', 1),
        (5, '2002-12-31 23:55:59', 'CRITICAL', '192.168.1.104', 'Mozilla/4.0', 'system_failure', 'System failure detected', 0);

    INSERT INTO user_profiles VALUES
        (1, 'admin', 'admin@cybercore.local', '2000-01-01', '2002-12-31 23:59:59', 5, 'IT', 1),
        (2, 'j.smith', 'john.smith@cybercore.local', '2001-03-15', '2002-12-30 15:45:22', 3, 'Engineering', 1),
        (3, 'a.jones', 'alice.jones@cybercore.local', '2001-06-20', '2002-11-25 10:30:00', 2, 'HR', 1),
        (4, 'm.brown', 'michael.brown@cybercore.local', '2001-09-10', '2002-10-15 08:20:00', 4, 'Finance', 1),
        (5, 'e.davis', 'emma.davis@cybercore.local', '2001-12-05', '2002-09-05 14:50:00', 1, 'Marketing', 1);

    INSERT INTO chat_rooms VALUES
        (1, 'Tech Support', '2001-01-15', 50, 23, 'support', 1, 'Official technical support chat room'),
        (2, 'Lobby', '2001-01-15', 100, 45, 'general', 0, 'General discussion room'),
        (3, 'Development', '2001-02-20', 30, 15, 'development', 1, 'Development team chat room'),
        (4, 'HR', '2001-03-25', 20, 10, 'hr', 0, 'HR department chat room'),
        (5, 'Finance', '2001-04-30', 25, 12, 'finance', 1, 'Finance department chat room');
'''

cursor.executescript(INIT_SQL)
db_connection.commit()

global censored_flag
censored_flag = False

def censor(query: str) -> str:
    global censored_flag
    pattern = r'CSCCTF\{([^}]*)\}'

    def replace_with_redacted(match):
        return 'CSCCTF{REDACTED}'
    
    censored = re.sub(pattern, replace_with_redacted, query, flags=re.IGNORECASE)
    if censored != query:
        censored_flag = True
    return censored


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/viewer", response_class=HTMLResponse)
async def viewer(request: Request):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    tables_with_data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        tables_with_data[table] = {"columns": columns, "rows": rows}
    
    return templates.TemplateResponse("viewer.html", {
        "request": request,
        "tables": tables_with_data
    })


@app.get("/interactive", response_class=HTMLResponse)
async def interactive_get(request: Request):
    cursor.executescript("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    return templates.TemplateResponse("interactive.html", {
        "request": request,
        "tables": tables
    })


@app.post("/interactive", response_class=HTMLResponse)
async def interactive_query(request: Request, columns: str = Form(...), table: str = Form(...), condition: str = Form(...)):
    global censored_flag
    try:
        queries = f"SELECT {columns}"
        if table:
            queries += f" FROM {table}"
        if condition:
            queries += f" WHERE {condition}"
        queries += ";"

        if re.search(r'\b(hex|replace|substr|substring|trim|rtrim|ltrim)\b', queries, re.IGNORECASE):
            raise Exception("Not that easy pal :)")

        statements = queries.split(';')
        statements = [s.strip() for s in statements if s.strip()]
        
        if len(statements) > 1:
            cursor.executescript(';'.join(statements[:-1]) + ';')
        
        cursor.execute(statements[-1])

        res_columns = [description[0] for description in cursor.description]
        res_rows = cursor.fetchall()
        censored_rows = [
            [censor(str(cell)) for cell in row] for row in res_rows
        ]
        results = [dict(zip(res_columns, row)) for row in censored_rows]

        if censored_flag:
            censored_flag = False
            return templates.TemplateResponse("interactive.html", {
                "request": request,
                "columns": columns,
                "table": table,
                "condition": condition,
                "results": results,
                "warning": "Some sensitive information has been redacted."
            })
        
        else:            
            return templates.TemplateResponse("interactive.html", {
                "request": request,
                "columns": columns,
                "table": table,
                "condition": condition,
                "results": results
            })

    except Exception as e:
        return templates.TemplateResponse("interactive.html", {
            "request": request,
            "columns": columns,
            "table": table,
            "condition": condition,
            "error": str(e)
        })


@app.get("/joke", response_class=HTMLResponse)
async def joke(request: Request):
    return templates.TemplateResponse("joke.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1337)