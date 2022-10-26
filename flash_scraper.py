import requests
import pandas as pd
import os
from tqdm import tqdm

## Website Address
address = "dagobah.net"
## Output Folder
outfolder = "/dagobah/"

r = requests.get(f"http://web.archive.org/cdx/search/cdx?url={address}*")
with open("temp_url_list.csv", 'wb') as f:
  f.write(r.content)

df = pd.read_csv("temp_url_list.csv",delimiter=" ",encoding  = "latin1",header = None)
df1 =  df[(df[2].str.endswith(".swf")) & (df[4] != "404") & (df[3] == "application/x-shockwave-flash")]
df2 = df1.sort_values([0,1],ascending=False).drop_duplicates([2],keep="first")
dflist = df2[1].tolist()

for enum,a in enumerate(tqdm(df2[2])):
    dl_url = "https://web.archive.org/web/"+str(dflist[enum])+"if_/"+a
    outpath = outfolder+a.split(f"{address}/")[-1]
    checkpath = "/".join(outpath.split("/")[0:-1])
    if not os.path.exists(checkpath):
      os.makedirs(checkpath)   
    if os.path.exists(outpath):
      continue
    r = requests.get(dl_url)
    if r.status_code == 200:
      try:
        with open(outpath, 'wb') as f:
          f.write(r.content)
      except:
        print("invalid link: "+dl_url)
