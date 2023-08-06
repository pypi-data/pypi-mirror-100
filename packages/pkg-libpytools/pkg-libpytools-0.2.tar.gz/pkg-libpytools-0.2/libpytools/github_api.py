import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuário do github
    :param usuario: str com o nome do usuario
    :return: str com o link do avatar
    """

    url = f'https://api.github.com/users/{usuario}'
    resposta = requests.get(url)
    return resposta.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('gabrieldcpadilha'))
