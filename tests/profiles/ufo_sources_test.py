import os

import defcon
import pytest

from fontbakery.checkrunner import (DEBUG, ERROR, FAIL, INFO, PASS, SKIP, WARN)

check_statuses = (ERROR, FAIL, SKIP, PASS, WARN, INFO, DEBUG)


@pytest.fixture
def empty_ufo_font(tmpdir):
    ufo = defcon.Font()
    ufo_path = str(tmpdir.join("empty_font.ufo"))
    ufo.save(ufo_path)
    return (ufo, ufo_path)


def test_check_ufolint(empty_ufo_font):
    from fontbakery.profiles.ufo_sources import (
        com_daltonmaag_check_ufolint as check)
    _, ufo_path = empty_ufo_font

    print('Test PASS with empty UFO.')
    c = list(check(ufo_path))
    status, _ = c[-1]
    assert status == PASS

    print('Test FAIL with maimed UFO.')
    os.remove(os.path.join(ufo_path, "metainfo.plist"))
    c = list(check(ufo_path))
    status, message = c[-1]
    assert status == FAIL
    assert type(message) == str


def test_check_required_fields(empty_ufo_font):
    from fontbakery.profiles.ufo_sources import (
        com_daltonmaag_check_required_fields as check)
    ufo, _ = empty_ufo_font

    print('Test FAIL with empty UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == FAIL

    ufo.info.unitsPerEm = 1000
    ufo.info.ascender = 800
    ufo.info.descender = -200
    ufo.info.xHeight = 500
    ufo.info.capHeight = 700
    ufo.info.familyName = "Test"

    print('Test PASS with almost empty UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == PASS


def test_check_recommended_fields(empty_ufo_font):
    from fontbakery.profiles.ufo_sources import (
        com_daltonmaag_check_recommended_fields as check)
    ufo, _ = empty_ufo_font

    print('Test WARN with empty UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == WARN

    ufo.info.postscriptUnderlineThickness = 1000
    ufo.info.postscriptUnderlinePosition = 800
    ufo.info.versionMajor = -200
    ufo.info.versionMinor = 500
    ufo.info.styleName = "700"
    ufo.info.copyright = "Test"
    ufo.info.openTypeOS2Panose = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    print('Test PASS with almost empty UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == PASS


def test_check_unnecessary_fields(empty_ufo_font):
    from fontbakery.profiles.ufo_sources import (
        com_daltonmaag_check_unnecessary_fields as check)
    ufo, _ = empty_ufo_font

    print('Test PASS with empty UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == PASS

    ufo.info.openTypeNameUniqueID = "aaa"
    ufo.info.openTypeNameVersion = "1.000"
    ufo.info.postscriptUniqueID = -1
    ufo.info.year = 2018

    print('Test WARN with unnecessary fields in UFO.')
    c = list(check(ufo))
    status, _ = c[-1]
    assert status == WARN
