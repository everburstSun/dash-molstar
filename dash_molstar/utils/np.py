def named_params(name, params=None):
    """
    Generate `NamedParams` for parameters

    Parameters
    ----------
    `name` — str
        Parameter name
    `params` — any
        Parameters

    Returns
    -------
    `dict`
        NamedParams
    """
    return {'name': name, 'params': params}