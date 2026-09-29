import os, json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
try:
    from hindsight_client import Hindsight
except Exception:
    Hindsight = None
try:
    from groq import Groq
except Exception:
    Groq = None
BASE=Path(__file__).resolve().parent.parent
DATA=BASE/'data/demo_signals.json'
HKEY=os.getenv('HINDSIGHT_API_KEY',''); HURL=os.getenv('HINDSIGHT_BASE_URL','https://api.hindsight.vectorize.io'); BANK=os.getenv('HINDSIGHT_BANK_ID','compmind-demo'); GKEY=os.getenv('GROQ_API_KEY','')
app=FastAPI(title='CompMind API')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
class Signal(BaseModel):
    competitor:str; title:str; category:str='Other'; date:str; details:str=''
class Req(BaseModel):
    competitor:str; question:str; latest_signal:Signal|None=None
def client(): return Hindsight(base_url=HURL,api_key=HKEY) if Hindsight and HKEY else None
def ensure(c):
    try: c.create_bank(bank_id=BANK,name='CompMind Competitive Intelligence',background='Remember competitor pricing, launches, features, messaging and deployment signals. Connect new events with historical events.',disposition={'skepticism':4,'literalism':3,'empathy':1})
    except Exception: pass
def demo(cmp): return [x for x in json.loads(DATA.read_text()) if x['competitor'].lower()==cmp.lower()]
@app.get('/')
def home(): return FileResponse(BASE/'static/index.html')
@app.get('/api/health')
def health(): return {'status':'ok','hindsight_configured':bool(HKEY and Hindsight),'groq_configured':bool(GKEY and Groq),'bank_id':BANK}
@app.post('/api/seed')
def seed():
    c=client()
    if not c: return {'mode':'demo','stored':0}
    ensure(c); items=json.loads(DATA.read_text())
    for x in items:
        c.retain(bank_id=BANK,content=f"{x['date']} | {x['competitor']} | {x['category']} | {x['title']} | {x['details']}",context='Competitive intelligence signal',metadata={'competitor':x['competitor'],'category':x['category']})
    c.close(); return {'mode':'hindsight','stored':len(items)}
@app.post('/api/analyze')
def analyze(r:Req):
    c=client()
    if c:
        try:
            ensure(c)
            if r.latest_signal:
                s=r.latest_signal; c.retain(bank_id=BANK,content=f"{s.date} | {s.competitor} | {s.category} | {s.title} | {s.details}",context='New competitor signal',metadata={'competitor':s.competitor,'category':s.category})
            q=c.recall(bank_id=BANK,query=f"{r.competitor} pricing product features deployment strategy",max_tokens=3000,budget='mid')
            mem=[{'text':m.text,'type':getattr(m,'type','memory')} for m in q.results]
            c.close()
            return {'mode':'hindsight','answer':f'Hindsight recalled {len(mem)} relevant memories for {r.competitor}. The latest event is connected to persistent historical signals instead of being treated as an isolated announcement.','memories':mem,'connections':['New signal connected to persistent Hindsight memory','Pricing + product + deployment timeline can be compared']}
        except Exception:
            try: c.close()
            except Exception: pass
    mem=demo(r.competitor)
    if r.latest_signal: mem.append(r.latest_signal.model_dump())
    cats=sorted(set(x.get('category','Other') for x in mem)); con=[]
    if 'Pricing' in cats and 'Product' in cats: con.append('Pricing change + product launch')
    if 'Deployment' in cats and 'Product' in cats: con.append('Deployment + product launch')
    if len(mem)>=3: con.append('Multiple events form a longer-term strategy pattern')
    return {'mode':'demo','answer':f'CompMind connected {len(mem)} signals for {r.competitor}. The current move should be read with the earlier pricing, deployment and product events. Pattern categories: {", ".join(cats)}.','memories':mem,'connections':con}
