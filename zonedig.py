#!/usr/bin/env python
# coding: utf-8

import sys      #argv を取得するため
import re       #正規表現モジュール
import commands #dig コマンド用
import string   #文字列操作用
import time     #unixtimeの使用
import os.path  #ディレクトリの操作

zoneinfofile = '/var/log/named/slave/zoneinfo' #zoneinfo ファイルの場所
#zoneinfofile = 'zoneinfo' #テストファイル
tmpfile = '/tmp/zonedig_tmp_' + str(int(time.time()))
summaryfile = '/tmp/zonedig_summary_' + str(int(time.time()))
#一時ファイルの設定 zonedig_temp_<UNIXTIME>
#tmpfile = 'zonedig_tmp_' + str(int(time.time())) #テストファイル

if not os.path.isfile(zoneinfofile):
#zoneinfofile があるかのチェックなければプログラム終了
    print 'ファイルがありません\n'
    quit() #プログラム終了

f = open(zoneinfofile) #ファイルオープン
for line in f: #1行ずつ読み込む
    line = line.strip()
    zone = 'dig +norec @localhost %s NS' % (line)
    #dig コマンドの作成
    #zone = '/usr/bin/dig {0}'.format(line)  #テストコマンド
    dig = commands.getoutput(zone) #dig コマンドの実行
    t = open(tmpfile, 'a') #dig 結果を出力するファイルを開く
    t.write(dig) #dig の結果を出力

t.close() #ファイルクローズ
f.close() #ファイルクローズ

summary_list = [] #結果を挿入するリストを作成

t = open(tmpfile) #dig の結果を加工するためファイルオープン
for line in t: #ファイルの内容を一行ずつ読み出し
    read = re.sub('^\;.+', '', line)
    #先頭が ; の行を空白行に置換
    if read != '\n':
    #空白行か判定し、空白行ならリストに追加しない
        summary_list.append(read)

summary_list.sort() #リスト内をソート

summary = "" #結果を挿入する変数
for b in summary_list:
    summary += b

f = open(summaryfile, 'a')
 #最終結果を書き込むファイルをオープン
f.write(summary)

f.close() #ファイルクローズ
t.close() #ファイルクローズ

