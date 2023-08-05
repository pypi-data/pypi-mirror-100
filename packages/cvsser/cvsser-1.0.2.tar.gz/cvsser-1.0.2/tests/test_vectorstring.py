# -*- coding: utf-8 -*-

"""Tests for cvsser"""

import cvsser

sample = "CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C"

def test_sample():
    assert cvsser.VectorString(sample).av == 'L'
