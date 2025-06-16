from gui.kill_switch import enable_kill_switch, disable_kill_switch


def test_enable_disable_kill_switch():
    # Apenas testa se as funções executam sem erro (mock real seria necessário para efeito prático)
    enable_kill_switch()
    disable_kill_switch()
