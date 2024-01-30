import json
import os

__all__ = ['get_env']


def get_env():
    envd = {
        "SK": "h(*rz5uu+%h((iv2)pggx5aw_s^)m-k7q3x46uz=vdg!%vj3%5",
        "AH": ["127.0.0.1", "localhost"],
        "DDU": "",
        "DDP": "",
        "MR": "",
        "EHU": "",
        "EHP": "",
    }
    try:
        envf = os.path.join(os.environ['HOME'], '.sysucc_settings')
    except Exception as e:
        print(e)
        return envd
    if not os.path.isfile(envf):
        return envd
    with open(envf, 'r') as fp:
        d = json.load(fp)
        for k in d.keys():
            try:
                envd[k] = d[k]
            except KeyError:
                print('error key <%s> in %s' % (k, envf))
                raise KeyError
    return envd
