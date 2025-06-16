from tests.mocks.mock_network import MockNetwork


def test_network_stats():
    net = MockNetwork()
    stats = net.get_network_stats()
    assert stats["up"] == 100
    assert stats["down"] == 200


def test_vpn_status():
    net = MockNetwork()
    assert net.get_vpn_status() == "active"
    assert net.get_tor_status() == "inactive"
    assert net.get_proxy_status() == "active"
