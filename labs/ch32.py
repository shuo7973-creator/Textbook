"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
firms=[{'name':'甲','book':100,'market':200,'ni':15,'avg_equity':100},
       {'name':'乙','book':80,'market':80,'ni':6,'avg_equity':80}]
for f in firms:
    f['bm']=f['book']/f['market']; f['roe']=f['ni']/f['avg_equity']
assert firms[0]['bm']==.5 and firms[1]['bm']==1
assert isclose(firms[0]['roe'],.15) and isclose(firms[1]['roe'],.075)
accrual=(20-8)/100; investment=120/100-1
assert isclose(accrual,.12) and isclose(investment,.20)
print({'企业':firms,'应计率':accrual,'资产增长':investment})
