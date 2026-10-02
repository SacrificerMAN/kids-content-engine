import json, sqlite3, time, uuid
from pathlib import Path

class JobStore:
    def __init__(self, root):
        self.root=Path(root)
        self.root.mkdir(parents=True,exist_ok=True)
        self.db=self.root/"jobs.sqlite3"
        with sqlite3.connect(self.db) as con:
            con.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, created_at REAL NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL)")
            con.commit()

    def create(self,payload):
        job_id=uuid.uuid4().hex
        now=time.time()
        data={"id":job_id,"created_at":now,"status":"queued","request":payload}
        with sqlite3.connect(self.db) as con:
            con.execute("INSERT INTO jobs VALUES (?,?,?,?)",(job_id,now,"queued",json.dumps(data)))
            con.commit()
        return data

    def update(self,job_id,**changes):
        current=self.get(job_id)
        if not current:
            raise KeyError(job_id)
        current.update(changes)
        with sqlite3.connect(self.db) as con:
            con.execute("UPDATE jobs SET status=?, payload=? WHERE id=?",(current.get("status","unknown"),json.dumps(current),job_id))
            con.commit()
        return current

    def get(self,job_id):
        with sqlite3.connect(self.db) as con:
            row=con.execute("SELECT payload FROM jobs WHERE id=?",(job_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list(self,limit=50):
        with sqlite3.connect(self.db) as con:
            rows=con.execute("SELECT payload FROM jobs ORDER BY created_at DESC LIMIT ?",(int(limit),)).fetchall()
        return [json.loads(row[0]) for row in rows]
