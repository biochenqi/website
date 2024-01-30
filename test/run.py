from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_paginate import Pagination, get_page_parameter
import matplotlib.pyplot as plt
import numpy as np
import os,sys,re,json
import pandas as pd
from math import ceil
from flask_babel import Babel
from functools import reduce

app = Flask(__name__)
app.debug=True
# app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
babel = Babel(app)

def excel_deal(file):
    df = pd.read_excel(file,sheet_name='所有结果')  # 读取文件
    ####先设定好有哪些是固定的类型
    class_list=['IVW','MR Egger','Weighted median','Weighted.mode','simple.mode','MR Raps']
    # 列表包含了你想要选择的所有列名
    selected_columns = ['outcome', 'exposure', 'N','FDR','Het_Q_pval','Pleio_pval']
    dict_all = {}
    col_num = len(df.columns)
    # 对于每一个类，选择该类的列以及其后面的5列
    for column in class_list:
        # 获取当前类名的索引位置
        index = df.columns.get_loc(column)
        # 选择该类的列以及其后面的5列并生成新的pd.dataframe, list_column为selected_columns 在df矩阵中对应的列
        list_column = [0,1,2,8,29,30]
        dfs = df.iloc[:,list_column+[i for i in range(index,index+5 if index+5 <=col_num else col_num)]]
        #更改head并重新生成dfs
        head = selected_columns + dfs.iloc[0,len(list_column):].to_list()
        dfs = dfs.iloc[1:,:]
        dfs.columns = head
        dict_all[column] = dfs
    list_outcome = dfs['outcome'].unique().tolist()
    # list_outcome.insert(0,'all')
    return dict_all,list_outcome

# 将文件内容读入 pandas DataFrame
infos,list_outcome = excel_deal('bin/test.xls')

@app.route('/index',methods=['GET', 'POST'])
def index():
    query_type,valuex="",""
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        valuex = request.form.get('valuex')
    else:
        pass
    text = request.args.get('text', default=None, type=str)
    df = pd.read_csv('bin/%s.xls'%text,sep='\t')  # 读取文件
    df.columns = df.columns.str.replace(' ', '_')  # 替换列名中的空格为下划线
    df = df[df[query_type]==valuex] if query_type and valuex else df
    data = df.to_dict(orient='records')  # 转换为字典列表
    return render_template('test1.html', data=data)  # 渲染模板，传递数据


@app.route('/test1',methods=['GET', 'POST'])
def analysis_workflow():
    query_type,valuex="",""
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        valuex = request.form.get('valuex')
    else:
        pass
    print('#####################')
    print(query_type,valuex)
    print('#####################')
    df = pd.read_csv('bin/MR_info.xls',sep='\t')  # 读取文件
    df.columns = df.columns.str.replace(' ', '_')  # 替换列名中的空格为下划线
    df = df[df[query_type]==valuex] if query_type and valuex else df
    data = df.to_dict(orient='records')  # 转换为字典列表
    return render_template('test1.html', data=data)  # 渲染模板，传递数据


#此处直接读取所有的数据用来展示表格
@app.route('/test2',methods=['GET', 'POST'])
def test2():
    query_type,valuex,text,query_class="","","",'all'
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        valuex = request.form.get('valuex')
        query_class = request.form.get('query_class')
    elif request.method == 'GET':
        text = request.args.get('text', default=None, type=str)
    print('#####################')
    print(query_type,valuex)
    print(text)
    print('#####################')
    df = infos['IVW'] if not text else infos[text]
    # df = df[df[query_type]==valuex] if query_type and valuex else df
    df = df[df[query_type]==query_class] if query_class!='all' else df
    return render_template('test2.html', classes=list(infos.keys()),data=df.to_dict(orient='records') ,list_outcome=list_outcome)  # 渲染模板，传递数据

@app.route('/test',methods=['GET', 'POST'])
def test():
    query_type,query_class,filter_range, filters="",'',"",""
    action = request.form.get('action')
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        query_class = request.form.get('query_class')
        filters = request.form.get('filter')
        if filters:
            a = filters.split(';')
            # filter_range = {i.split(':')[0]:[float(j) for j in i.split(':')[1].split('|')] for i in a}
            filter_range = {i.split(':')[0]:[float(j) if ('>' not in j) and ('<' not in j) else j for j in i.split(':')[1].split('|')] for i in a}
    elif request.method == 'GET':
        # text = request.args.get('text', default=None, type=str)
        pass
    print('#####################')
    print(query_type,query_class,action,filter_range)
    print('#####################')
    if action=='reset':
        query_type,query_class,filter_range, filters="",'',"",""
    df = infos['IVW'] if query_class=="" else infos[query_class]
    df = df[df['outcome']==query_type] if query_type else df
    thead = df.columns.to_list()
    ##用于过滤搜索
    if filter_range:
        # conditions = [(df[key]>=value[0])&(df[key]<=value[1]) for key,value in filter_range.items()]
        conditions = [(df[key]>=value[0])&(df[key]<=value[1])  if len(value)==2 else compare(df,key,value[0]) for key,value in filter_range.items()]
        final_condition = reduce(lambda x, y: x & y, conditions)
        df =  df[final_condition]
    return render_template('test.html', 
    classes=list(infos.keys()),
    thead = thead, #表头信息
    data=df.to_dict(orient='records') , #包含了表格的所有信息
    list_outcome=list_outcome,
    query_class=query_class, #查询统计学方法
    query_type=query_type, #查询疾病类型
    filter_condition=filters #查询过滤条件
    )  # 渲染模板，传递数据

def compare(df,key,value):
    #只考虑小于或者大于的情况，不考虑小于等于或者大于等于的情况
    if '=' in value:
        num  = float(value[2:])
        if '>' in value:
            return (df[key]>=num)
        elif '<' in value:
            return (df[key]<=num)
    else:
        num = float(value[1:])
        if '>' in value:
            print(df)
            return (df[key]>num)
        elif '<' in value:
            return (df[key]<num)

#此处用来生成browse网页
@app.route('/browse')
def browse():
    text='all'
    if request.method == 'GET':
        text = request.args.get('text', default='all', type=str)

    df_browser = pd.read_excel('bin/demo.xlsx',sheet_name="Browse页面",skiprows=1)
    classes = df_browser['Measurement'].unique().tolist()
    df_browser.columns = df_browser.columns.str.replace(' ', '_')  # 替换列名中的空格为下划线
    df_browser = df_browser[df_browser['Measurement']==text] if text!='all' else df_browser #按照需要提取对应的Measurement
    print(df_browser,text)
    return render_template('browse.html', classes=classes,data=df_browser.to_dict(orient='records'))  # 渲染模板，传递数据

def demo_deal(file,sheet):
    df = pd.read_excel('bin/demo.xlsx',sheet_name=sheet,skiprows=2)
    list_cols = [i for i in df.columns if 'Unnamed:' not in i]
    list_cols_sta= df.iloc[0,:].values[4:]
    return df.iloc[1:,:],list_cols,list_cols_sta

#此处用来生成MR analylsis网页
@app.route('/MR_ana',methods=['GET', 'POST'])
def MR_ana():
    text='all'
    IDP, Disease, mr_ana_class = "", "", ""
    action = request.form.get('action')
    if request.method == 'POST':
        IDP = request.form.get('IDP')
        # IDP = IDP if IDP!='all' else ""
        Disease = request.form.get('Disease')
        mr_ana_class = request.form.get('mr_ana_class')
    elif request.method == 'GET':
        # text = request.args.get('text', default='all', type=str)
        pass
    if action=='reset':
        IDP, Disease, mr_ana_class = "", "", ""
    print('###################')
    print(IDP, Disease, mr_ana_class)
    print('##################')

    #用来提取数据信息
    if mr_ana_class=="Reverse":
        df,list_cols,list_cols_sta = demo_deal('bin/demo.xlsx','HOME页面2')
        df = df[df.iloc[:,1] == IDP] if IDP else df
        df = df[df.iloc[:,0] == Disease] if Disease else df
        idp = df.iloc[:,1].unique().tolist()
        disease = df.iloc[:,0].unique().tolist()
    else:
        df,list_cols,list_cols_sta = demo_deal('bin/demo.xlsx','HOME页面')
        df = df[df.iloc[:,0] == IDP] if IDP else df
        df = df[df.iloc[:,2] == Disease] if Disease else df
        idp = df.iloc[:,0].unique().tolist()
        disease = df.iloc[:,2].unique().tolist()

    return render_template('MR_ana.html', 
    heads=list_cols, #第一行头
    heads_ana = list_cols_sta , #第二行头
    list_idp = idp , #idp选择
    list_disease = disease, #disease选择
    idp_fir = IDP, #设定IDP第一个选项
    disease_fir = Disease, #设定disease的第一个选项
    mr_ana_fir = mr_ana_class, #设定mr_ana的第一个选项
    data=df.to_dict(orient='records'))  # 渲染模板，传递数据

#绘制图像 柱状图用于显示forward 和 reverse得 各个疾病得IDP数量
@app.route('/draw_pic')
def draw_pic():
    df_Reverse,list_cols,list_cols_sta = demo_deal('bin/demo.xlsx','HOME页面2')
    df_forward,list_cols,list_cols_sta = demo_deal('bin/demo.xlsx','HOME页面')
    dis_forward = df_forward.iloc[:,2].value_counts()[df_forward.iloc[:,2].unique().tolist()].to_dict()
    dis_Reverse = df_Reverse.iloc[:,0].value_counts()[df_Reverse.iloc[:,0].unique().tolist()].to_dict()
    name = list(dis_forward.keys())
    for_val =list(dis_forward.values())
    rev_val = [dis_Reverse[i] for i in name]
    print(dis_forward)
    print(dis_Reverse)
    return render_template('draw_pic.html',
    forward_names = name,
    forward_vals = for_val,
    reverse_names = name,
    reverse_vals = rev_val)

#用于测试绘制图像
@app.route('/test_pic')
def test_pic():
    # return render_template('test_draw.html')
    return render_template('test_draw.html',
    forward_names = json.dumps(['SCZ', 'AN', 'BD', 'ASD', 'OCD', 'TS', 'MDD', 'PTSD', 'ADHD', 'ANX']),
    forward_vals = json.dumps([95, 100, 44, 92, 24, 33, 59, 35, 52, 23]),
    reverse_names = json.dumps(['SCZ', 'AN', 'BD', 'ASD', 'OCD', 'TS', 'MDD', 'PTSD', 'ADHD', 'ANX']),
    reverse_vals = json.dumps([95, 100, 44, 92, 24, 33, 59, 35, 52, 23]))


##用于展示
@app.route('/home')
def home():
    # return render_template('work_test.html')
    return "hello world"

# @app.route('/home')
# def home():
#     df = pd.read_table('bin/stats.xls')
#     # json_records = df.to_json(orient ='records')
#     return render_template('home.html',disease=df['Disease'].to_list(),ldsc=df['LDSC'].to_list())

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)