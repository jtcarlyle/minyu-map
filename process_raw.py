import pandas as pd
import os

sample_zi = [
    "枝","鼻","鯉","眉","臍","肥","水","書",
    # "簰",
    "雞","飛","苧","浮",
    # "牛",
    "手","樹",
    # "菇",
    "烏","五","墓","廚","雨","戍","刀","毛",
    # "笆",
    # "耙",
    "馬","斜",
    # "蔗",
    "畫","沙","我","大","帶",
    # "蛇",
    "騎",
    "外",
    "短",
    "坐",
    "條",
    "鉤",
    "頭",
    "草",
    "雷",
    "貓",
    "早",
    "笑",
    "熊",
    "十",
    # "箴",
    "鐮",
    "染",
    "簪",
    "暗",
    "三",
    "擔",
    "鴨",
    "翼",
    "煙",
    "面",
    "七",
    "日",
    "冰",
    "蠅",
    "直",
    "板",
    # "賊",
    "根",
    "乞",
    "肩",
    # "反",
    "八",
    # "扼",
    "年",
    "鐵",
    "舌",
    "血",
    "船",
    # "出",
    "掘",
    "骨",
    "滑",
    "酸",
    "卵",
    # "飯",
    # "脫",
    # "磚",
    "月",
    "肝",
    "傘",
    "殺",
    "泉",
    "懶",
    "滿",
    "半",
    "夢",
    "目",
    "龍",
    "種",
    "竹",
    "叔",
    "肉",
    # "蜂",
    "蔥",
    "銅",
    "膿",
    "重",
    "腹",
    "角",
    "六",
    "腸",
    "兩",
    "索",
    "擇",
    "落",
    "羊",
    "上",
    "石",
    # "箬",
    "青",
    "平",
    "井",
    "白",
    "名",
    "鼎",
    "赤",
    "黃",
    "圓"
]

#TODO handle the dialect points XXT mislabeled as Gan later
#includes Shaowu, Jianning, and Taining

#TODO possibly expand the southern Min region to include Zhangzhou, Zhangpu, Longyan, etc.
dialect_points = {
    #Norman CM Data
    #-------EM
    "福安" : "FA",
    #Muyang
    "寧德" : "ND",
    #Fuzhou 1
    "福州" : "FZh",
    "福清" : "FQ",
    #Yongchun
    #-------SM
    #Amoy 1
    "廈門" : "AM",
    #Zhangping
    #Chaoyang
    "揭陽(榕城話)" : "RCh",
    #-------NM
    "崇安(崇城鎮城關話)" : "ChA",
    "建甌" : "JO",
    #Jianyang 1
    "建陽(潭城鎮城關話)" : "JY",
    #Shufang
    "石陂" : "ShB",
    #Dianqian
    #-------CM
    #Yongchun
    #-------WM
    #Shaowu (XXT Gan)
    #Heping
    #Gaotang
    #End Norman CDC

    #-------EM
    #-------SM
    "莆田" : "PT", #'Puxian group
    "仙游(城關話)" : "XY", #Puxian group
    "大田(前路話)" : "DT",
    "南安(溪美鎮)" : "NA",
    "晉江(青陽鎮)" : "JJ",
    "漳州" : "ZhZh",
    "漳浦" : "ZhP",
    "潮州(府城話)": "ChZh",
    #-------NM
    "松溪": "SX",
    #-------CM
    "三明(三元話)" : "SY",
    "沙縣(城關話)" : "ShX",
    "明溪(城關話)" : "MX",
    #-------WM
    "將樂(城關話)" : "JL",
}

#the tone classes are a huge nasty mess because people have no goddamn sense
#I am just going to use values for now
tone_class_dict = {
    "陽平甲" : "2",
    "陽平乙" : "9",
    "第九調" : "9",
    "陽平5" : "2",
    "陰平" : "1", 
    "陽平" : "2",
    "陰上" : "3",
    "陽上" : "4",
    "陰去" : "5",
    "陽去" : "6",
    "陰入" : "7",
    "陽入" : "8",
    "入聲" : "7",
    "揚入" : "8",
    "平聲" : "1",
    "上聲" : "3",
    "去聲" : "5",
    "平" : "1",
    "上" : "3",
    "去" : "5",
    "入" : "7",
}

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

f = os.path.join(os.path.dirname(__file__), 'min_list_final.xlsx')
df = pd.read_excel(f)
df["initial"] = df.initial.replace("0", "")
df["tone_class"] = df.tone_class.replace(tone_class_dict, regex=True)
df["IPA"] = df.initial.map(str) + df.final.map(str) + df.tone_class.map(str)
df = df[df.graph.isin(sample_zi)]
df = df[df.dialect.isin(dialect_points.keys())]
df = df[["dialect", "graph", "IPA"]]
df = pd.pivot_table(df, index='dialect', columns='graph', values='IPA', fill_value="", aggfunc=','.join)
df = df[sample_zi]
f = os.path.join(os.path.dirname(__file__), 'min_data_raw.xlsx')
df.to_excel(f)
