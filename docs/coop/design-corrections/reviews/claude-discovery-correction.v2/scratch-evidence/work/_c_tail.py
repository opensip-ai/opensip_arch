args.out.write_text(json.dumps({"standing":"CLAUDE reference controls for the XA-02 / CR-25 correction; synthetic trusted observations; NOT product qualification","source":str(args.source),"controls":rows,"passed":sum(1 for r in rows if r["holds"]),"failed":[r["control"] for r in rows if not r["holds"]]}, indent=2)+chr(10))
print("controls", sum(1 for r in rows if r["holds"]), "of", len(rows))
sys.exit(0 if all(r["holds"] for r in rows) else 1)
