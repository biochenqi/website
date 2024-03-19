from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_paginate import Pagination, get_page_parameter, get_page_args
import matplotlib.pyplot as plt
import numpy as np
import os,sys,re,json
import pandas as pd
from math import ceil
from flask_babel import Babel
from functools import reduce
import ast
from flask_caching import Cache

app = Flask(__name__)
app.debug=True
# app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
babel = Babel(app)

##首先获取所有数据文件进行读取，后续就不用再加载数据
class Config:
    def __init__(self):
        self.bin_dir='bin/real_info/'
        # self.neurological_Forward_df, self.neurological_Forward_all = excel_read('%s/Forward/neurological disoders.xlsx'%self.bin_dir)
        # self.neurological_Reverse_df, self.neurological_Reverse_all = excel_read('%s/Reverse/neurological disoders.xlsx'%self.bin_dir)
        # self.neuro_oncological_Forward_df, self.neuro_oncological_Forward_all = excel_read('%s/Forward/neuro-oncological disoders.xlsx'%self.bin_dir)
        # self.neuro_oncological_Reverse_df, self.neuro_oncological_Reverse_all = excel_read('%s/Reverse/neuro-oncological disoders.xlsx'%self.bin_dir)
        # self.psychiatric_Forward_df, self.psychiatric_Forward_all = excel_read('%s/Forward/psychiatric disoders.xlsx'%self.bin_dir)
        # self.psychiatric_Reverse_df, self.psychiatric_Reverse_all = excel_read('%s/Reverse/psychiatric disoders.xlsx'%self.bin_dir)

        self.dict_all = {'Reverse':{'neurological disoders':self.excel_read('%s/Reverse/neurological disoders.xlsx'%self.bin_dir),
                                    'neuro-oncological disoders':self.excel_read('%s/Reverse/neuro-oncological disoders.xlsx'%self.bin_dir),
                                    'psychiatric disoders':self.excel_read('%s/Reverse/psychiatric disoders.xlsx'%self.bin_dir)},
                        'Forward':{'neurological disoders':self.excel_read('%s/Forward/neurological disoders.xlsx'%self.bin_dir),
                                    'neuro-oncological disoders':self.excel_read('%s/Forward/neuro-oncological disoders.xlsx'%self.bin_dir),
                                    'psychiatric disoders':self.excel_read('%s/Forward/psychiatric disoders.xlsx'%self.bin_dir)}}
    
    def excel_read(self,file):
        df = pd.read_excel(file,sheet_name='所有结果',skiprows=1)
        # df = df.loc[:,['IDP Name','IDP ID','Tissue/Region','IDP Subtype','Unnamed: 10','Disorder']]
        list_head = df.loc[:,['IDP Name','IDP ID','Tissue/Region','IDP Subtype','Disorder']]
        return list_head,df

config = Config()

@cache.memoize(timeout=None)
def excel_read(file):
    df = pd.read_excel(file,sheet_name='所有结果',skiprows=1)
    list_head = df.loc[:,['IDP Name','IDP ID','Tissue/Region','IDP Subtype','Disorder']]
    return list_head,df

def data_extract(df_fo,df_re,arg):
    #meta 信息
    print('################################')
    print(arg)
    print(df_fo)
    print(df_re)
    print('################################')
    dict_result = {}
    df_fo = df_fo[(df_fo['IDP ID']==arg['IDP ID']) & (df_fo['Disorder']==arg['Disorder'])]
    df_re = df_re[(df_re['IDP ID']==arg['IDP ID']) & (df_re['Disorder']==arg['Disorder'])]

    list_head = ['IVW','MR Egger','Weighted median','Weighted.mode','simple.mode']
    
    dict_result['meta'] = [arg['IDP ID'],arg['Disorder'],int(df_fo['Unnamed: 10'].values[0]),int(df_re['Unnamed: 10'].values[0]),arg['IDP Name']]
    #GC Forward和Reverse得一致
    dict_result['GC'] = [arg['IDP ID']] + df_fo.iloc[:,6:10].values[0].tolist()
    #result
    df_fo  = df_fo.iloc[:,11:-8].values[0].tolist()
    dict_result['Forward']  = []
    df_re  = df_re.iloc[:,11:-8].values[0].tolist()
    dict_result['Reverse']  = []
    count = 0
    for i in list_head:
        dict_result['Forward'].append([i]+df_fo[count:count+5])
        dict_result['Reverse'].append([i]+df_re[count:count+5])
        count += 5
    return dict_result

@app.route('/MR_result')
def MR_result():
    file = session.get('file')
    arg = request.args.get('arg')
    arg = ast.literal_eval(arg)
    # arg = {'IDP Name': 'MD in the right cingulum cingulate gyrus part', 'IDP ID': '1636', 'Tissue/Region': 'Limbic system fibers', 'IDP Subtype': 'WM tract MD', 'Unnamed: 10': 20.0, 'Disorder': 'ALZ'}
    dict_all = config.dict_all
    df_fo = dict_all['Forward'][file][1]
    df_re = dict_all['Reverse'][file][1]
    dict_result = data_extract(df_fo,df_re,arg)
    
    # return render_template('MR_result.html')
    return render_template('MR_result.html',info = dict_result)

@app.route('/MRlist',methods=['GET'])
def MRlist():
    page = request.args.get('page', type=int, default=1)  #默认第几页得页数

    file = request.args.get('file',default=None, type=None)
    Disorder = request.args.get('Disorder',default=None, type=None)
    idp_subtype = request.args.get('idp_subtype',default=None, type=None)
    idp_id = request.args.get('idp_id',default=None, type=None)
    types = request.args.get('types',default=None, type=None)
    return 'hello world'
    print('################################################################')
    print(file,idp_subtype,Disorder,types)
    print('################################################################')
    if file:
        # df,all_df = excel_read('bin/real_info/%s/%s.xlsx'%(types,file))
        df,all_df = config.dict_all[types][file]
        if idp_subtype != 'All':
            df = df[df['IDP Subtype'] == idp_subtype]
        if Disorder != 'All':
            df = df[df['Disorder'] == Disorder]
        if idp_id:
            df = df[df['IDP ID'] == idp_id]
        session['file'] = file
    else:
        # df,all_df = excel_read('bin/real_info/Forward/neurological disoders.xlsx')
        df,all_df = config.dict_all['Forward']['neurological disoders']
        session['file'] = 'neurological disoders'
    

    total_num = df.shape[0]
    limit = 200  # 每页显示的行数
    start = (page - 1) * limit
    end = page * limit if total_num > page * limit else total_num
    paginate = Pagination(page=page, total=total_num)
    df = df.iloc[start:end,:]
    return render_template('MRlist.html',
    data=df.to_dict(orient='records'),
    paginate=paginate,
    num=total_num)


@app.route('/MR_ana', methods=['GET','POST'])
def MR_ana():
    if request.method == 'POST':
        file_name = request.form.get('mr_ana_class')
        Disorder = request.form.get('Disease')
        idp_subtype = request.form.get('Subtype')
        idp_id = request.form.get('IDP')
        types = request.form.get('types')
        return 'hello world'
        return redirect(url_for('MRlist', 
        file = file_name, 
        Disorder=Disorder,
        idp_subtype=idp_subtype,
        idp_id=idp_id,
        types=types))

    dict_disoders = {'neurological disoders':['All','ALZ', 'LBD', 'PD', 'MS', 'MG', 'ALS', 'PM', 'EDS', 'FTD', 'HERATAXIA', 'NMO', 'HMSN', 'MD', 'Migraine', 'MM'],
                'neuro-oncological disoders':['All','all_glioma', 'GBM', 'non_GBM', 'Pituitary', 'Meningioma'],
                'psychiatric disoders':['All','SCZ', 'ED', 'ADHD', 'BIPall', 'MDD', 'ASD ', 'CDG', 'SUDalc', 'SUDcud', 'PTSD', 'ANX', 'TS', 'OCD']}
    # dict_idp_subtype = {'neurological disorders':['All','WM tract MD', 'WM tract ICVF', 'WM tract OD', 'WM tract FA', 'cortical grey-white contrast', 'WM tract ISOVF', 'WM tract MO', 'regional and tissue intensity', 'regional and tissue volume', 'cortical area', 'cortical thickness'],
    #                     'neuro-oncological disoders':['WM tract MD', 'WM tract ICVF', 'WM tract FA', 'cortical grey-white contrast', 'WM tract ISOVF', 'regional and tissue intensity', 'WM tract MO', 'cortical area', 'regional and tissue volume', 'cortical thickness', 'WM tract OD']}
    ###目前来看，三种类型不分Reverse还是Forward，subtype都是一样的
    list_idp = ['All','WM tract MD', 'WM tract ICVF', 'WM tract OD', 'WM tract FA', 'cortical grey-white contrast', 'WM tract ISOVF', 'WM tract MO', 'regional and tissue intensity', 'regional and tissue volume', 'cortical area', 'cortical thickness']
    df = pd.read_table('bin/bar.csv')
    list_bar = df.values.tolist()
    # list_bar.insert(0,['疾病',  'LDSC'  ,  '正向MR',  '反向MR'])
    return render_template('MR_ana_web.html',
                            data1 = json.dumps(dict_disoders), 
                            list_dis = dict_disoders['neurological disoders'],
                            list_idp = list_idp,
                            list_bar = json.dumps(list_bar))

##用于展示
@app.route('/home')
def home():
    # return render_template('work_test.html')
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)