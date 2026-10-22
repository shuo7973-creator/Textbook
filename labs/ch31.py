"""本章独立离线实验：全部输入为假设数据。"""

from datetime import datetime
from math import isclose
rows=[('2025-04-20T18:00:00',100),('2025-08-01T18:00:00',95)]
def asof(cutoff):
    available=[(datetime.fromisoformat(t),v) for t,v in rows if datetime.fromisoformat(t)<=cutoff]
    return max(available)[1] if available else None
assert asof(datetime(2025,4,20,15)) is None
assert asof(datetime(2025,6,1))==100
assert asof(datetime(2025,9,1))==95
r=(10.5+.2-10)/10
assert isclose(r,.07)
print({'六月可用值':asof(datetime(2025,6,1)),'总收益':r})
