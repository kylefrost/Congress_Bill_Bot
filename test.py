# -*- coding: utf-8 -*-

import const
import utils
from propub import ProPublica

pp = ProPublica(const.PROPUB_KEY)

for action in pp.get_bill('115','hr38').actions:
    print action.date
