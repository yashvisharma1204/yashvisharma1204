#!/usr/bin/env python3
"""Build animated SVG profile cards. STATIC=1 renders still frames."""
import base64, calendar, json, os, subprocess, urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'cards'; DATA=ROOT/'data/contributions.json'
USER='yashvisharma1204'; BG='#0A0A0A'; FG='#F2F2F2'; MUTED='#A3A3A3'; LINE='#383838'; PANEL='#242424'; GREEN='#22C55E'
LINKS=[('PORTFOLIO','heyashv.in','https://heyashv.in/'),('RESEARCH AGENT','live project','https://extraordinary-axolotl-c63e93.netlify.app/'),('OPEN SOURCE','issues & PRs','https://gist.github.com/yashvisharma1204/02f2962ebc64e93068507b372db61fa3')]
PROJECTS=[('research-agent','Research Agent','A self-evolving research agent — a knowledge graph that reads and learns while you sleep.','Python · Gemini · Neo4j · RAG','https://extraordinary-axolotl-c63e93.netlify.app/'),('neural-y','neural.y','Neural networks research — building and studying architectures from the ground up.','Deep learning · paper notes · experiments','https://heyashv.in/')]
STATIC=os.getenv('STATIC','0').lower() in ('1','true','yes')

def refresh():
 token=os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
 if not token: raise SystemExit('GITHUB_TOKEN is required with --refresh-data')
 q='query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t){contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}'
 today=date.today(); start=today-timedelta(days=364)
 payload={'query':q,'variables':{'u':USER,'f':datetime.combine(start,datetime.min.time(),timezone.utc).isoformat(),'t':datetime.combine(today+timedelta(days=1),datetime.min.time(),timezone.utc).isoformat()}}
 req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'profile-cards'})
 with urllib.request.urlopen(req,timeout=30) as r: obj=json.load(r)
 cal=obj['data']['user']['contributionsCollection']['contributionCalendar']
 DATA.parent.mkdir(parents=True,exist_ok=True); DATA.write_text(json.dumps({'username':USER,'updated_at':datetime.now(timezone.utc).isoformat(),'total_contributions':cal['totalContributions'],'days':[d for w in cal['weeks'] for d in w['contributionDays']]},indent=2)+'\n')

def font_uri():
 try:
  f=ROOT/'.font-cache/JetBrainsMono-Regular.ttf'; f.parent.mkdir(exist_ok=True)
  if not f.exists():
   u='https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Regular.ttf'
   with urllib.request.urlopen(u,timeout=25) as r:f.write_bytes(r.read())
  w=f.with_suffix('.woff2')
  subprocess.run(['pyftsubset',str(f),'--output-file='+str(w),'--flavor=woff2','--text=Yashvi SharmaSoftware engineer exploring machine learning research0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz·—&.,:/()!↗'],check=True)
  return 'data:font/woff2;base64,'+base64.b64encode(w.read_bytes()).decode()
 except Exception as e: print('Font embedding skipped:',e); return None

def esc(x): return str(x).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\"','&quot;')
def svg(name,w,h,delay=0):
 face="" if not FONT else f"@font-face{{font-family:JetBrains;src:url('{FONT}') format('woff2')}}"
 anim="" if STATIC else f".in{{opacity:0;transform:translateY(10px);animation:up .7s ease {delay}s forwards}}@keyframes up{{to{{opacity:1;transform:translateY(0)}}}}"
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{name}</title><style>{face}text{{font-family:JetBrains,monospace}}.fg{{fill:{FG}}}.muted{{fill:{MUTED}}}.green{{fill:{GREEN}}}{anim}@media(prefers-reduced-motion:reduce){{.in{{animation:none!important;opacity:1!important;transform:none!important}}animate{{display:none!important}}}}</style><rect width="{w}" height="{h}" rx="16" fill="{BG}"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="15.5" fill="none" stroke="{LINE}"/>'''
def save(n,s): (OUT/n).write_text(s+'</svg>\n')

def render(d):
 OUT.mkdir(exist_ok=True); global FONT; FONT=font_uri()
 s=svg('Yashvi Sharma',900,210); s+=f'''<g class="in"><text x="32" y="38" class="muted" font-size="13" letter-spacing="3">// HELLO, WORLD</text><text x="32" y="98" class="fg" font-size="40">Yashvi Sharma</text><text x="34" y="137" class="muted" font-size="17">Software engineer exploring machine learning &amp; research.</text><circle cx="39" cy="175" r="5" class="green"/>'''
 if not STATIC:s+='<circle cx="39" cy="175" r="5" fill="none" stroke="#22C55E" stroke-width="2"><animate attributeName="r" values="5;10;5" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0;.7" dur="2.4s" repeatCount="indefinite"/></circle>'
 save('hero.svg',s+f'<text x="54" y="181" class="green" font-size="14">OPEN TO RESEARCH · ML · COLLABORATIONS</text><text x="868" y="38" text-anchor="end" class="muted" font-size="12">INDIA · {USER}</text></g>')
 for i,(label,detail,url) in enumerate(LINKS):
  s=svg(label,420,100,.2+i*.12)+f'<a xlink:href="{url}"><g class="in"><rect x="10" y="8" width="400" height="84" rx="13" fill="{PANEL}" stroke="{LINE}"/><text x="28" y="42" class="fg" font-size="14">{esc(label)}</text><text x="28" y="68" class="muted" font-size="12">{esc(detail)}</text><text x="386" y="55" text-anchor="end" class="green" font-size="18">↗</text></g></a>'
  save('link-'+('portfolio','research-agent','open-source')[i]+'.svg',s)
 days={x['date']:int(x['contributionCount']) for x in d.get('days',[])}; today=date.today(); active=sum(v>0 for v in days.values()); busy=max(days,key=days.get) if days and max(days.values()) else None
 cursor=today if days.get(today.isoformat(),0) else today-timedelta(days=1); streak=0
 while days.get(cursor.isoformat(),0):streak+=1;cursor-=timedelta(days=1)
 busiest=f'{date.fromisoformat(busy):%b %d} · {days[busy]}' if busy else '—'
 months=[]
 for off in range(11,-1,-1):
  a=today.year*12+today.month-1-off;y,m0=divmod(a,12);m=m0+1;months.append((calendar.month_abbr[m],sum(v for k,v in days.items() if k.startswith(f'{y:04d}-{m:02d}'))))
 s=svg('GitHub activity',900,250,.5)+'<g class="in"><text x="28" y="34" class="muted" font-size="12" letter-spacing="2">ACTIVITY / LAST 12 MONTHS</text>'
 stats=[('CONTRIBUTIONS',str(d.get('total_contributions',sum(days.values())))),('ACTIVE DAYS',str(active)),('CURRENT STREAK',f'{streak}d'),('BUSIEST DAY',busiest)]
 for i,(a,b) in enumerate(stats):x=28+i*215;s+=f'<text x="{x}" y="74" class="muted" font-size="11">{a}</text><text x="{x}" y="108" class="fg" font-size="22">{b}</text>'
 mx=max([v for _,v in months]or[1])or 1
 for i,(m,v) in enumerate(months):x=30+i*70;h=max(3,int(48*v/mx));s+=f'<rect x="{x}" y="218" width="38" height="{h}" rx="4" fill="{GREEN}"/><text x="{x+19}" y="239" text-anchor="middle" class="muted" font-size="10">{m}</text>'
 save('activity.svg',s+'</g>')
 for i,(slug,name,desc,stack,url) in enumerate(PROJECTS):
  s=svg(name,900,148,.7+i*.2)+f'<a xlink:href="{url}"><g class="in"><text x="28" y="32" class="muted" font-size="11" letter-spacing="2">FEATURED PROJECT / 0{i+1}</text><text x="28" y="72" class="fg" font-size="23">{esc(name)}</text><rect x="740" y="49" width="86" height="26" rx="13" fill="#102819"/><text x="783" y="67" text-anchor="middle" class="green" font-size="11">ACTIVE</text><text x="28" y="105" class="muted" font-size="13">{esc(desc)}</text><text x="28" y="130" class="muted" font-size="11">{esc(stack)}</text></g></a>'
  save('repo-'+slug+'.svg',s)
 s=svg('GitHub contribution graph',900,170,1.1)+'<g class="in"><text x="28" y="32" class="muted" font-size="12" letter-spacing="2">CONTRIBUTION MAP</text>'
 if d.get('days'):
  first=date.fromisoformat(d['days'][0]['date']); cells=[None]*((first.weekday()+1)%7)+d['days']
 else:cells=[None]*371
 mx=max([int(x.get('contributionCount',0)) for x in d.get('days',[])]or[1])or 1
 for i,x in enumerate(cells[:371]):
  n=int(x.get('contributionCount',0)) if x else 0; col='#202020' if not n else ('#14532D' if n<=mx*.25 else '#15803D' if n<=mx*.5 else '#16A34A' if n<=mx*.75 else GREEN)
  s+=f'<rect x="{28+(i//7)*16}" y="{48+(i%7)*16}" width="12" height="12" rx="3" fill="{col}"/>'
 s+=f'<text x="870" y="32" text-anchor="end" class="fg" font-size="12">{d.get("total_contributions",sum(days.values()))} contributions · last year</text></g>'
 save('contributions.svg',s)
 print('Rendered profile SVGs (STATIC='+str(int(STATIC))+')')

if __name__=='__main__':
 import sys
 if '--refresh-data' in sys.argv:refresh()
 d=json.loads(DATA.read_text()) if DATA.exists() else {'total_contributions':0,'days':[]}
 render(d)
