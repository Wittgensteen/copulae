import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from copulae.special.special_func import *


@pytest.mark.parametrize('n, k, exp', [
    ('A', 'B', None),
    (5, 3, 26),
    (14, 3, 198410786),
    (3, 3, 0),
    (15, 0, 1)
])
def test_eulerian(n, k, exp):
    if isinstance(n, str) or isinstance(k, str):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            eulerian(n, k)
    else:
        assert eulerian(n, k) == exp


@pytest.mark.parametrize('n, exp', [
    (0, 1),
    (5, [1, 26, 66, 26, 1]),
    (10, [1, 1013, 47840, 455192, 1310354, 1310354, 455192, 47840, 1013, 1]),
    (12, [1, 4083, 478271, 10187685, 66318474, 162512286, 162512286, 66318474, 10187685, 478271, 4083, 1])
])
def test_eulerian_all(n, exp):
    assert_almost_equal(eulerian_all(n), exp)


@pytest.mark.parametrize('value, exp', [
    (2.5, -0.08565048),
    ([5.6, 1.4], [-0.003704718, -0.283154954])
])
def test_log1mexp(value, exp):
    assert_almost_equal(log1mexp(value), exp)


@pytest.mark.parametrize('value, exp', [
    (2.5, 2.57888973429255),
    ([5.6, 1.4], [5.60369104342695, 1.62041740991845])
])
def test_log1mexp(value, exp):
    assert_almost_equal(log1pexp(value), exp)


@pytest.mark.parametrize('z, s, log, dp, exp', [
    (np.arange(-4, 0.1, 0.4), -7, False, 6,
     [-0.5126656000003, -0.573610269987928, -0.606087738137387, -0.579693804311355, -0.446840155547746,
      -0.145404663923222, 0.363288070892882, 0.937598521985122, 0.878245290738864, -0.493319717367522, 0]),
    (np.arange(0, 4.1, 0.4), -7, False, 3,
     [0, 10142.9492455418, 819890420.000001, 4127873429.99997, 2116512.53772291, 94586, 14605.1307824849,
      3990.40387466444, 1504.3276293274, 695.371444040548, 369.475994513025]),
    (np.arange(0.1, 1, 0.1), -11, True, 4,
     [7.49391587403553, 11.7916877939206, 15.2747867369797, 18.5513667073359, 21.9004628928554, 25.5630317509794,
      29.8734730437786, 35.5015876869881, 44.5067157736232]),
    (np.arange(0.1, 1, 0.1), 1, True, 4,
     [-2.25036732731245, -1.49993998675952, -1.03093043315872, -0.671726992092122, -0.366512920581664,
      -0.0874215717907552, 0.185626758862366, 0.475884995327111, 0.834032445247956]),
    (0.5, 2, False, 6, 0.5822405),  # special case
])
@pytest.mark.parametrize('method', ['default', 'neg-eulerian'])
def test_poly_log(z, s, method, log, exp, dp):
    if s == 2 and method != 'default':
        return
    assert_almost_equal(poly_log(z, s, method=method, log=log), exp, dp)


@pytest.mark.parametrize('coef, x, exp', [
    ([0.5, 4, 3, -1.5], 0.4, 2.484),
    ([0.3, -0.9, 5], [-0.5, 1.2], (2, 6.42)),
    (50, -5, 50)
])
def test_polyn_eval(coef, x, exp):
    assert_almost_equal(polyn_eval(coef, x), exp)


@pytest.mark.parametrize('n, k, exp', [
    (5, 3, 35),
    (8, 4, 6769),
    (8, 5, -1960),
    (7, 2, -1764),
    (2, 0, 0)
])
def test_stirling_first(n, k, exp):
    assert stirling_first(n, k) == exp


@pytest.mark.parametrize('n, exp', [
    (7, [720, -1764, 1624, -735, 175, -21, 1]),
    (8, [-5040, 13068, -13132, 6769, -1960, 322, -28, 1])
])
def test_stirling_first_all(n, exp):
    assert stirling_first_all(n) == exp


@pytest.mark.parametrize('n, k, exp', [
    (5, 3, 25),
    (8, 4, 1701),
    (8, 5, 1050),
    (6, 5, 15),
    (2, 0, 0)
])
def test_stirling_second(n, k, exp):
    assert stirling_second(n, k) == exp


@pytest.mark.parametrize('n, exp', [
    (7, [1, 63, 301, 350, 140, 21, 1]),
    (8, [1, 127, 966, 1701, 1050, 266, 28, 1])
])
def test_stirling_second_all(n, exp):
    assert_almost_equal(stirling_second_all(n), exp)


# noinspection PyTypeChecker
@pytest.mark.parametrize('n, k', [
    ([1, 2, 3], [4, 5, 6])
])
def test_stirling_raises_type_error(n, k):
    match = '`k` and `n` must both be integers'
    with pytest.raises(TypeError, match=match):
        stirling_first(n, k)
    with pytest.raises(TypeError, match=match):
        stirling_second(n, k)


@pytest.mark.parametrize('n, k', [
    (4, 6),
    (4, -1)
])
def test_stirling_raises_value_error(n, k):
    match = r'`k` must be in the range of \[0, `n`\]'
    with pytest.raises(AssertionError, match=match):
        stirling_first(n, k)

    with pytest.raises(AssertionError, match=match):
        stirling_second(n, k)
