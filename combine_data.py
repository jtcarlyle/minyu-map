import pandas as pd

def cleanup(df):
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

def convert_tvalues(data, tvalues):
    for column in tvalues:
        if column != "tone":
            d = dict(zip(tvalues["tone"].map(str), tvalues[column]))
            if column in data.columns:
                data[column].replace(d, inplace=True, regex=True)

tone_value_change = {
    '1' : '¹',
    '2' : '²',
    '3' : '³',
    '4' : '⁴',
    '5' : '⁵',
    '6' : '⁶',
    '7' : '⁷',
    '8' : '⁸',
    '9' : '⁹',
    '0' : '⁰' 
}
#flip it here because I am lazy
tone_dict = {v:k for k,v in tone_value_change.items()}

# get the mindong data
funing = pd.read_csv('data/akitani-funing.tsv', sep='\t', encoding='utf-8')
gutian = pd.read_csv('./data/akitani-gutian.tsv', sep='\t', encoding='utf-8')
ningde = pd.read_csv('./data/akitani-ningde.tsv', sep='\t', encoding='utf-8')

an = ["hupei","xiancun","jiudu"]
for site in an:
    ningde[site].replace(r"([iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ])([iu]?[^iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ]?[^iyɪʏʊueøəoɛœʌɔaɐᴇɵɿ]?6)", r"\1ː\2", inplace=True, regex=True)

zhenan = pd.read_csv('./data/akitani-zhenan.tsv', sep='\t', encoding='utf-8')
norman_md = pd.read_csv('./data/norman-mindong.tsv', sep='\t', encoding='utf-8')

# merge it
mindong = [funing, gutian, ningde, zhenan, norman_md]
for df in mindong:
    df.dropna(inplace=True, subset=['id'])
    df.set_index('id', inplace=True)
    # print(df[df.index.duplicated(keep=False)])
    df = df[~df.index.duplicated(keep='first')]
mindong = pd.concat(mindong, axis=1)

#index as integer
mindong.index = mindong.index.astype(int)

#get rid of zheyang in Norman's data since it is a duplicate
#and get rid of other all other unnecessary columns
mindong.drop(columns=['zheyang', 'zitou', 'akitani_zi', 'akitani_ci', 'notes', 'note', 'akitani_idx','akitani_id', 'akitani_lexidx'], inplace=True)
cleanup(mindong)
mindong_tvalues = pd.read_csv('./data/mindong-tvalues.tsv', sep='\t', encoding='utf-8')
convert_tvalues(mindong, mindong_tvalues)

#get the kwok minnan data
kwok = pd.read_csv('./data/kwok-data.tsv', sep='\t', encoding='utf-8')

#get the tone classes as non-superscripts
kwok.replace(tone_dict, regex=True, inplace=True)
#drop psm and the other junk columns
kwok.drop(columns=['PSM', 'leizhou', 'gloss', 'kwok_id', 'zi'], inplace=True)
kwok.dropna(inplace=True, subset=['id'])
kwok.set_index('id', inplace=True)
kwok.index = kwok.index.astype(int)
cleanup(kwok)
kwok_values = pd.read_csv('./data/kwok-psm-tvalues.tsv', sep='\t', encoding='utf-8')
convert_tvalues(kwok, kwok_values)

#next up is akitani minbei data
a_mb_zi = pd.read_csv('./data/akitani-minbei-zi.tsv', sep='\t', encoding='utf-8')

#get the tone classes as non-superscripts
a_mb_zi.replace(tone_dict, regex=True, inplace=True)
#drop the junk columns
a_mb_zi.drop(columns=['akitani_zi_id', 'zitou', 'en_gloss', 'notes'], inplace=True)
a_mb_zi.dropna(inplace=True, subset=['id'])
a_mb_zi.set_index('id', inplace=True)
a_mb_zi.index = a_mb_zi.index.astype(int)
cleanup(a_mb_zi)
a_mb_values = pd.read_csv('./data/akitani-minbei-tvalues.tsv', sep='\t', encoding='utf-8')
convert_tvalues(a_mb_zi, a_mb_values)

a_mb_ci = pd.read_csv('./data/akitani-minbei-ci.tsv', sep='\t', encoding='utf-8')
a_mb_ci.drop(columns=['akitani_ci_id', 'zitou', 'en_gloss', 'notes'], inplace=True)
a_mb_ci.dropna(inplace=True, subset=['id'])
a_mb_ci.set_index('id', inplace=True)
a_mb_ci.index = a_mb_ci.index.astype(int)

a_mb = pd.concat([a_mb_zi, a_mb_ci])
a_mb = a_mb[~a_mb.index.duplicated(keep='first')]

#shengzhi mindong
md_shengzhi = pd.read_csv('./data/md_shengzhi.tsv', sep='\t', encoding='utf-8', index_col=0, header=None).T
md_shengzhi.drop(columns=['zitou'], inplace=True)
md_shengzhi.dropna(inplace=True, subset=['id'])
md_shengzhi.set_index('id', inplace=True)
md_shengzhi.index = md_shengzhi.index.astype(int)
cleanup(md_shengzhi)
md_shengzhi_tvalues = pd.read_csv('./data/md_shengzhi_tvalues.tsv', sep='\t', encoding='utf-8')
convert_tvalues(md_shengzhi, md_shengzhi_tvalues)

#then put in the XXT data ~14 dialects and norman's data
xn_mbplus = pd.read_csv('./data/xxt_norman_minbei_nmore.tsv', sep='\t', encoding='utf-8')#discard fu'an since it isn't IPA
xn_mn = pd.read_csv('./data/xxt_norman_minnan.tsv', sep='\t', encoding='utf-8')
xn_mzw = pd.read_csv('./data/xxt_norman_minzhongw.tsv', sep='\t', encoding='utf-8')

# merge it
xxt = [xn_mbplus, xn_mn, xn_mzw]
for df in xxt:
    df.dropna(inplace=True, subset=['id'])
    df.set_index('id', inplace=True)
    # print(df[df.index.duplicated(keep=False)])
    df = df[~df.index.duplicated(keep='first')]
xxt = pd.concat(xxt, axis=1)

#index as integer
xxt.index = xxt.index.astype(int)

#get rid of zheyang in Norman's data since it is a duplicate
#and get rid of other all other unnecessary columns 
xxt.drop(columns=["fu'an", "shaowu_xxt", "zi"], inplace=True)
cleanup(xxt)
norman_tvalues = pd.read_csv('./data/norman-other-tvalues.tsv', sep='\t', encoding='utf-8')
convert_tvalues(xxt, norman_tvalues)

#shengzhi minnan

#then we gotta figure out what to salvage from li rulong

#put it all together
# print(mindong[mindong.index.duplicated(keep=False)])
# print(kwok[kwok.index.duplicated(keep=False)])
# print(a_mb[a_mb.index.duplicated(keep=False)])
full = pd.concat([mindong, kwok, a_mb, md_shengzhi, xxt], axis=1)
full = full.T
full.to_csv('./data/full_data.csv', encoding='utf-8')

