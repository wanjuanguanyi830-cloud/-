from kintaiyi.junshi_zhanlue import junshi_zhanlue


def test_c8_defaults_to_strict_volume5_source_profile():
    data = junshi_zhanlue(home_cal=17, away_cal=13)
    assert data["source_profile"] == "volume5_strict"
    assert data["cross_volume_merge"] is False
    assert data["source_variants"] == []


def test_each_c8_layer_exposes_source_scope():
    data = junshi_zhanlue(home_cal=17, away_cal=13)
    layers = data["layers"]
    assert layers["eight_divinations"]["source_scope"] == "canonical_eight_divinations"
    assert layers["three_doors_five_generals"]["source_scope"] == "volume5_military"
    assert layers["host_guest_movement"]["source_rule"] == "明主客以分先后动静之术"
    assert layers["commanders"]["source_rule"] == "明内外将帅贤否之术"
