import json, pathlib, urllib.request, urllib.parse, time, datetime
root=pathlib.Path("olive-oil-monitor/data")
root.mkdir(parents=True,exist_ok=True)
ok=0
for country in (152,32,858,604):
 for year in range(2022,datetime.date.today().year+1):
  for hs in ("150920","150930","150940","150990"):
   params=dict(reporterCode=country,period=year,cmdCode=hs,flowCode="X",partner2Code=0,customsCode="C00",motCode=0,maxRecords=500)
   url="https://comtradeapi.un.org/public/v1/preview/C/A/HS?"+urllib.parse.urlencode(params)
   try:
    with urllib.request.urlopen(url,timeout=45) as response: j=json.load(response)
    rows=j.get("data")
    if not isinstance(rows,list) or len(rows)>=500 or (j.get("count") or 0)>=500: raise ValueError("invalid or truncated")
    if not rows: continue
    j["retrievedAt"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    j["source"]=url
    (root/f"A-{country}-{year}-{hs}.json").write_text(json.dumps(j,ensure_ascii=False),encoding="utf-8")
    ok+=1
   except Exception as e: print(country,year,hs,str(e),flush=True)
   finally: time.sleep(2)
if not ok: raise SystemExit("No valid datasets retrieved")
print("Datasets retrieved:",ok)
