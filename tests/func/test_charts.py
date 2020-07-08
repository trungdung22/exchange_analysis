import pytest
import tests.testdata as testdata
import json


@pytest.mark.parametrize(
    'pair_name',
    [(
        'BUSD-BD1_IDRTB-178'
    )]
)
def test_pair_list(app, client, pair_name):
    url = '/api/pairs'
    rv = client.post(url, data=dict(pair_name=pair_name))
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'result' in data['data']
    result = data['data']['result']
    assert result['name'] == pair_name


@pytest.mark.parametrize(
    'pair_id,start,end',
    [(
        testdata.PAIR_OBJECT_ID_1,
        '2020-07-02',
        '2020-07-03',
    )]
)
def test_spread_datas(app, client, pair_id, start, end):
    data = {
        'start': start,
        'end': end
    }
    url = '/api/order-spread/' + str(pair_id)
    rv = client.get(url, query_string=data)
    data = rv.get_json()
    assert rv.status_code == 200
    assert 'results' in data['data']
    results = data['data']['results']
    assert len(results) > 0


@pytest.mark.parametrize(
    'pair_id',
    [(
        testdata.PAIR_OBJECT_ID_1,
    )]
)
def test_pair_list(app, client, pair_id):
    url = '/api/pairs'
    rv = client.get(url)
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'results' in data['data']
    results = data['data']['results']
    assert len(results) > 0