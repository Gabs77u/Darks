class MockNetwork:
    def get_network_stats(self):
        return {"up": 100, "down": 200}

    def get_connections(self):
        return ["conn1", "conn2"]

    def get_vpn_status(self):
        return "active"

    def get_tor_status(self):
        return "inactive"

    def get_proxy_status(self):
        return "active"
