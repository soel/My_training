#!/usr/bin/env python
# coding: utf-8

import re #正規表現モジュール
import sys # argv を取得するため
import string #文字列操作用

argvs = sys.argv #コマンドライン引数を格納したリストの取得
argc = len(argvs) #引数の個数の取得

if argc != 2: #引数が正しいか確認　2だと正しい
    print 'ファイル名を指定してください\n'
    quit() #プログラムの終了
else:
    f = open(argvs[1]) #ファイルオープン
   
    sum_mail = [] #リストの作成   
    for line in f.readlines(): #1行ずつ読み込む

        mail = re.findall("([\w\.-]+@[\w\.-]+)", line)
        #メールの正規表現により抽出
        num = re.search("[0-9]{6}", line)
        #6桁のID番号の抽出
        set_mail = set(mail)
        #重複の排除


        list_mail = [] #リストの作成
        for va_mail in set_mail: #セット型の展開
            list_mail += [va_mail] #リスト型へ変換し代入
        list_mail.reverse() #読み取った順番になっているのでもとに戻す
        #sum_mail += [num.group(0) + ',' +  string.join(list_mail, ';')] 
        sum_mail.append(num.group(0) + ',' +  string.join(list_mail, ';'))
        #ID+メールアドレスの結合をリスト型で追加
        #print sum_mail #デバックプリント

    f.close() #ファイル閉じる

    sum_mail.sort() #内容をソートして順番をID順にする
    #print sum_mail #デバックプリント
    
    f = open('custmail.txt', 'w') #custmail.txt として出力
    for write_mail in sum_mail: #リスト型 sum_mail を展開
        f.write(write_mail+'\n') #展開したデータを書き込む

    f.close()
