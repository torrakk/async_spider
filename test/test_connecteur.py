import pytest
import asyncio
from webcrawler.connecteur import Connect
from webcrawler.settings import *


# @pytest.mark.asyncio
def test_connecteur_get(event_loop):
    con = Connect(**{'action':'get','url':'http://www.loire-semene.fr', 'session':None})
    reponse = event_loop.run_until_complete(con.request())
    res = True if 'loire-semene' in reponse[1] else False
    assert res == True

# def test_connecteur_post(event_loop):
#     con = Connect(**{'action': 'post', 'url': 'http://www.loire-semene.fr', 'data': CODES,'session': None})
#     reponse = event_loop.run_until_complete(con.request())
#     res = True if 'loire-semene' in reponse[1] else False
#     assert res == True

# async def async_coro(loop=None):
#     await asyncio.sleep(0, loop=loop)
#     return 'ok'
#
# def test_event_loop_fixture(event_loop):
#     assert event_loop
#     ret =
#     assert ret == 'ok'