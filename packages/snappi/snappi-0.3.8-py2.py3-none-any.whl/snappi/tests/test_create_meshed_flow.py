import pytest


def test_create_meshed_flow(api):
    """Demonstrates a fully meshed configuration
    """
    config = api.config()

    for i in range(1, 33):
        config.ports.port(name='Port %s' % i, location='localhost/%s' % i)
        device = config.devices.device(name='Device %s' % i)[-1]
        device.ethernet.name = 'Eth %s' % i
        device.ethernet.ipv4.name = 'Ipv4 %s' % i

    flow = config.flows.flow(name='Fully Meshed Flow')[0]
    for tx in config.devices:
        for rx in config.devices:
            if tx.name != rx.name:
                flow.tx_rx.device.maps.map(tx_name=tx.name, rx_name=rx.name)
    flow.size.fixed = 128
    flow.rate.pps = 1000
    flow.duration.fixed_packets.packets = 10000
    flow.packet.ethernet().vlan().ipv4().tcp()

    print(config)


if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])
