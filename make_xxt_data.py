import pandas as pd

minyu = pd.read_csv("./xxt/min.tsv", sep="\t", encoding="utf-8") #load min dialects
dialects = {
    "南安(溪美鎮)" : "nan'an",
    "漳浦" : "zhangpu",
    "澄海" : "chenghai",
    "仙游(城關話)" : "xianyou",
    "莆田" : "putian",
    "建陽(潭城鎮城關話)" : "jianyang",
    "松溪" : "songxi",
    "沙縣(城關話)" : "shaxian",
    "明溪(城關話)" : "mingxi",
    "三明(三元話)" : "sanyuan",
    "將樂(城關話)" : "jiangle",
    "晉江(青陽鎮)" : "jinjiang"
}
minyu = minyu[minyu.dialect.isin(dialects.keys())]
minyu["dialect"] = minyu.dialect.replace(dialects, regex=False)

ganyu = pd.read_csv("./xxt/gan.tsv", sep="\t", encoding="utf-8") #load "gan" dialects
dialects = {
    "建寧城關話" : "jianning",
    "泰寧城關話" : "taining",
    "邵武" : "shaowu"
} 
ganyu = ganyu[ganyu.dialect.isin(dialects.keys())]
ganyu["dialect"] = ganyu.dialect.replace(dialects, regex=False)

df = pd.concat([minyu, ganyu]) #combine
index = pd.read_csv("index.tsv", sep="\t", encoding="utf-8") #load index
df = df[df.zi.isin(index.zitou)] #get only the characters we want


#fix tone values
df["tone_value"] = df["tone_value"].astype(str)
df["tone_value"] = df["tone_value"].str.replace(r"(\d).0", r"\1", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"1", r"¹", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"2", r"²", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"3", r"³", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"4", r"⁴", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"5", r"⁵", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r", ", r"/", regex=True)
df["tone_value"] = df["tone_value"].str.replace(r"0|O|nan", r"", regex=True)

#fix initials
df["initial"] = df["initial"].astype(str)
df["initial"] = df["initial"].str.replace(r"(\d).0", r"\1", regex=True)
df["initial"] = df["initial"].str.replace(r"0|O|nan", r"", regex=True)
df["initial"] = df["initial"].str.replace(r", ", r"/", regex=True)

#fix finals
df["final"] = df["final"].str.replace(r"E", r"ᴇ", regex=True)
df["final"] = df["final"].str.replace(r"A", r"ᴀ", regex=True)
df["final"] = df["final"].str.replace(r"Y", r"ʏ", regex=True)
df["final"] = df["final"].str.replace(r"I", r"ɪ", regex=True)
df["final"] = df["final"].str.replace(r"U", r"ʊ", regex=True)
df["final"] = df["final"].str.replace(r"ɣ", r"ɤ", regex=True)
df["final"] = df["final"].str.replace(r", ", r"/", regex=True)
df["final"] = df["final"].str.replace(r"0|O|nan", r"", regex=True)

#fix tone classes, probably involves making sure loan tone names have sheng after
df["tone_class"] = df["tone_class"].str.replace(r", ", r"/", regex=True)

df["ipa"] = df["initial"] + "," + df["final"] + "," + df["tone_value"]

def infer_duoyin(s):
    """
    try to infer the multiple character readings from
    XXT's asinine chopping up of initial, finals, and tones

    Assumptions:
    1) usually, the order of the initial, final, and tones in / separated
    sublists is the same
    2) we infer the least amount of possible readings by only making as many readings
    as the maximum amount of / separated segments
    3) if a segment has less than the maximum amount of readings, its final element in the / 
    separated string is copied and used in all further concatenations

    each s is a string where initial, final and tone are separated by , and mutiple XXT readings
    are separated by /
    """
    s = str(s)
    l = s.split(',')
    if len(l) < 3:
        l.extend([''] * (3 - len(l)))
    l = [s.split('/') for s in l]
    n = max([len(sublist) for sublist in l])
    for sublist in l:
        sublist.extend([sublist[-1]] * (n - len(sublist)))
    ret = []
    for i,f,t in zip(l[0], l[1], l[2]):
        ret.append(str(i) + str(f) + str(t))
    return ret

df["ipa"] = df["ipa"].apply(infer_duoyin)
df = df.explode("ipa")

df.drop_duplicates(subset=["zi", "dialect", "ipa"], inplace=True) #get rid of duplicates
df = df[["dialect", "zi", "ipa"]] #keep just the rows we want
df = pd.pivot_table(df, index=["zi"], columns=["dialect"], values="ipa", aggfunc=lambda x: '/'.join(x), fill_value="")#make the df wide
df = df.reset_index()
index = index.rename(columns={"zitou":"zi"})
df = pd.merge(df, index[["zi", "id"]], on="zi", how="left") #pull the id numbers
df = df[["id", "zi", "nan'an", "jinjiang", "zhangpu", "chenghai", "xianyou", "putian", "jianyang", "songxi", "mingxi", "sanyuan", "shaxian", "jiangle", "taining", "jianning", "shaowu"]]#reorder the dialects by group for easy checking
df.to_csv("./data/xxt.tsv", sep="\t", encoding="utf-8", index=False)
 