import const
from propub import ProPublica

pp = ProPublica(const.PROPUB_KEY)

bill = pp.get_bill("115", "hr5000")

print bill.title
