import json
import os
import random

PROXYCHAIN_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "proxychains_config.json"
)
PROXIES_LIST_PATH = os.path.join(os.path.dirname(__file__), "proxies_list.json")


def load_proxychain_config():
    if not os.path.exists(PROXYCHAIN_CONFIG_PATH):
        raise FileNotFoundError("proxychains_config.json não encontrado")
    try:
        with open(PROXYCHAIN_CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar proxychains_config.json: {e}")


def save_proxychain_config(config):
    try:
        with open(PROXYCHAIN_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar proxychains_config.json: {e}")


def load_proxies_list():
    if not os.path.exists(PROXIES_LIST_PATH):
        raise FileNotFoundError("proxies_list.json não encontrado")
    try:
        with open(PROXIES_LIST_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar proxies_list.json: {e}")


def save_proxies_list(proxies):
    try:
        with open(PROXIES_LIST_PATH, "w") as f:
            json.dump(proxies, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar proxies_list.json: {e}")


def generate_random_chain(length=3):
    proxies = load_proxies_list()
    if len(proxies) < length:
        raise ValueError("Não há proxies suficientes para gerar a cadeia")
    return random.sample(proxies, length)


def get_active_proxychain():
    config = load_proxychain_config()
    return config.get("chain", [])


def set_active_proxychain(chain):
    config = load_proxychain_config()
    config["chain"] = chain
    save_proxychain_config(config)


def test_proxychain(dest_host, dest_port):
    from .proxychains import ProxyChain  # Import local para evitar import circular

    chain = get_active_proxychain()
    pc = ProxyChain(chain)
    return pc.chain_connect(dest_host, dest_port)


def add_proxy(proxy):
    proxies = load_proxies_list()
    proxies.append(proxy)
    save_proxies_list(proxies)


def remove_proxy(index):
    proxies = load_proxies_list()
    if 0 <= index < len(proxies):
        proxies.pop(index)
        save_proxies_list(proxies)


def list_proxies():
    return load_proxies_list()


def list_chains():
    # Suporte a múltiplas cadeias salvas
    if not os.path.exists(PROXYCHAIN_CONFIG_PATH):
        return []
    with open(PROXYCHAIN_CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("chains", [data.get("chain", [])])


def save_chain(chain, name="default"):
    if os.path.exists(PROXYCHAIN_CONFIG_PATH):
        with open(PROXYCHAIN_CONFIG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}
    if "chains" not in data:
        data["chains"] = {}
    data["chains"][name] = chain
    save_proxychain_config(data)


def load_chain(name="default"):
    if not os.path.exists(PROXYCHAIN_CONFIG_PATH):
        return []
    with open(PROXYCHAIN_CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("chains", {}).get(name, [])


def test_all_chains(dest_host, dest_port):
    from .proxychains import ProxyChain  # Import local para evitar import circular

    results = {}
    chains = list_chains()
    for idx, chain in enumerate(chains):
        try:
            pc = ProxyChain(chain)
            sock = pc.chain_connect(dest_host, dest_port)
            results[f"chain_{idx}"] = "OK" if sock else "FAIL"
        except Exception as e:
            results[f"chain_{idx}"] = f"Erro: {e}"
    return results


def validate_chain(chain):
    errors = []
    for proxy in chain:
        if proxy.get("type") not in ["SOCKS5", "SOCKS4", "HTTP", "HTTPS"]:
            errors.append(f"Tipo inválido: {proxy.get('type')}")
        if not proxy.get("host") or not isinstance(proxy["host"], str):
            errors.append("Host inválido")
        if not proxy.get("port") or not (1 <= int(proxy["port"]) <= 65535):
            errors.append("Porta inválida")
    return errors


def reorder_chain(chain, new_order):
    return [chain[i] for i in new_order if 0 <= i < len(chain)]


def update_proxies_from_scraper(scraper_dir):
    proxies = []
    type_map = {
        "http.txt": "HTTP",
        "https.txt": "HTTPS",
        "socks4.txt": "SOCKS4",
        "socks5.txt": "SOCKS5",
    }
    for fname, ptype in type_map.items():
        path = os.path.join(scraper_dir, fname)
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if ":" in line:
                        host, port = line.split(":")
                        proxies.append({"type": ptype, "host": host, "port": int(port)})
    save_proxies_list(proxies)
    return proxies
