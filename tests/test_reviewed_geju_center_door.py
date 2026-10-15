"""Explicit center-door exclusion and exact historical-profile regression."""
import json
from pathlib import Path

import pytest
from kintaiyi import api, reviewed_geju

OLD = json.loads((Path(__file__).parent/'fixtures/reviewed_geju_v1_response_hashes.json').read_text(encoding='utf-8'))
PROFILE = 'maintainer_reviewed_geju_20261015_v1_1'

@pytest.mark.parametrize('board', OLD, ids=lambda b:b['board_id'])
def test_original_144_public_responses_remain_byte_identical(board):
    result = api.calculate('patterns.reviewed_minute_v1', **board['inputs'])
    assert result['content_hash'] == board['content_hash']

@pytest.mark.parametrize('board', OLD, ids=lambda b:b['board_id'])
def test_new_profile_all_144_complete_including_center_door_na(board):
    values={**board['inputs'],'source_profile':PROFILE}
    result=api.calculate('patterns.reviewed_minute_v1',**values)
    assert result['complete'] is True
    assert result['source_profile']==PROFILE
    for context,role in (('HOME','home_general'),('AWAY','away_general')):
        r=result['readiness'][context]
        if values[role]==5:
            assert r['not_applicable'] is True
            assert r['ready'] is None and r['missing_reason'] is None
            assert r['door']['status']=='NOT_APPLICABLE_CENTER'
            assert 'palace_to_door' not in r['door']
        else:
            assert r.get('not_applicable') is not True

@pytest.mark.parametrize('context,role,call', [('HOME','home_general','host_door_readiness'),('AWAY','away_general','guest_door_readiness')])
def test_center_context_never_calls_eight_door_function(monkeypatch,context,role,call):
    values={**OLD[0]['inputs'],'source_profile':PROFILE,role:5}
    monkeypatch.setattr(reviewed_geju,call,lambda *args,**kwargs:pytest.fail('Center must not invoke a door overlay'))
    result=api.calculate('patterns.reviewed_minute_v1',**values)
    assert result['readiness'][context]['not_applicable'] is True
    assert result['events'] and result['positions'][role]['palace']==5


def test_taiyi_center_is_still_a_chart_bug():
    with pytest.raises(ValueError,match='chart bug'):
        api.calculate('patterns.reviewed_minute_v1',**{**OLD[0]['inputs'],'source_profile':PROFILE,'taiyi':5})
