from argh import arg

@arg("-c", "--config", help="Mead Make Config file")
def make_mead(config="sso.cfg"):
    """
    Create Make Mead configuration
    :param config: Make Mead config name
    :return:
    """
    return config
