from numpy import isin
import pandas as pd 
import os

f = os.path.join(os.path.dirname(__file__), 'data/full_data.xlsx')
df = pd.read_excel(f, sheet_name="mindong")

#make NaN into empty strings
df.fillna("", inplace=True)

#general fixes
#make commas into spaced slashes
df.replace(r"\,", " / ", inplace=True, regex=True)
#get rid of notes, parantheses, accidental 0s, and tone sandhi markers 
df.replace(r"\[.+\]|\(|\)|0|⁻", "", inplace=True, regex=True)
#fix aspiration
df.replace(r"([tsʃɕpk])[h']", r"\1ʰ", inplace=True, regex=True)
#fix E ᴇ
df.replace(r"E", "ᴇ", inplace=True, regex=True)



#the below is no longer true
#we can't use non-standard IPA so add diacritics for this and ɕ, ȵ, etc.
#I refuse to alter the chao tone letters. They can be kept as unkown maybe. He treats tones as modifiers which is unacceptable
#the alternative is to use rug l04 to get the distance or to find a way to jerry rig List's lingpy
#affricates need to be combined either with diacritic or fused


#akitani ningde tone 6 lengthening
#Akitani described these phonetically using the half long symbol
#this will cause issues comparing it to Norman's Ningde, so we'll use the full one
an = ["虎浿","咸村","九都"]
for site in an:
    df[site].replace(r"([iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ])([iu]?[^iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ]?[^iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ]?6)", r"\1ː\2", inplace=True, regex=True)

#phoneticize tones
f = os.path.join(os.path.dirname(__file__), 'data/phonetic_values.xlsx')
tvalues = pd.read_excel(f, sheet_name="mindong_tones")

for column in tvalues:
    if column != "tone":
        d = dict(zip(tvalues["tone"].map(str), tvalues[column]))
        df[column].replace(d, inplace=True, regex=True)

# #handle Akitani style lengthened tones. I am going to use the raised dash ⁻ to mark a doubled tone value in a 3 letter sequences
# df.replace(r"([¹²³⁴⁵])\1([¹²³⁴⁵])", r"\1⁻\2", inplace=True, regex=True)
# df.replace(r"([¹²³⁴⁵])([¹²³⁴⁵])\2", r"\1\2⁻", inplace=True, regex=True)

# #similarly, single targets will get a raised glottal stop ˀ marking that the tone is clipped
# df.replace(r"([^¹²³⁴⁵⁻])([¹²³⁴⁵])$", r"\1\2\2ˀ", inplace=True, regex=True)

#drop unnecessary rows
#水 extra 肥
df.drop(df[df.norman_head.isin(["水"])].index, inplace=True)
df.drop(df[df.akitani_lexidx.isin([433])].index, inplace=True)

#drop unnecessary columns
df.drop(["akitani_idx", "akitani_lexidx"], axis=1, inplace=True)

#rename columns
df.rename(columns={
    "虎浿" : "HP", 
    "咸村" : "XC", 
    "九都" : "JD",
    "八都" : "BD",	
    "泰順" : "TSh",
    "蒼南" : "CN", 
    "福鼎" : "FD",
    "白琳" : "BL", 
    "霞浦" : "XP",
    "長春" : "ChCh",
    "壽寧" : "ShN",	
    "斜灘" : "XT",
    "柘榮" : "ZhR",
    "富溪" : "FX",
    "穆陽" : "MY",
    "大橋" : "DQ",	
    "杉洋" : "ShY",
    "古田" : "GT",
    "平湖" : "PH",	
    "福州" : "FZh",
    "福清" : "FQ",	
    "赤溪" : "ChX",
    "柘洋" : "ZhY"
}, inplace=True)

#transpose
df.set_index("dm_idx", inplace=True)
df = df.T
print(df.head())

f = os.path.join(os.path.dirname(__file__), 'out/mindong_v1-4.txt')
df.to_csv(f, sep="\t", encoding="utf-8")

#TODO the remaining issue is what to do with the indel values
#for tones, maybe just tokenizing all the tone combos is an option
#dipthongs are more problematic