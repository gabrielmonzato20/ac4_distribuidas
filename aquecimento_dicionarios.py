reviews_aquecimento = [
    {
        'film_id': 'tt0076759',
        'user_id': 'marcos',
        'comment': 'gostei'
    },
    {
        'film_id': 'tt0076759',
        'user_id': 'lucio',
        'comment': 'achei legal'
    },
    {
        'film_id': 'tt1211837',
        'user_id': 'lucio',
        'comment': 'estranho'
    }
]

'''
A proxima atividade vai ter tudo a ver com essa
estrutura acima.

A idéia é que ela representa uma lista
de avaliacoes que os usuarios fizeram,
dando sua opiniao sobre alguns filmes.

Cada avaliacao está representada
como um dicionario com 3 chaves
'''

'''
primeiramente, façamos uma funcao
consulta que, dados o film_id e o user_id
devolve o dicionario da avaliacao
'''
def consulta(film_id,user_id):
    for dicio in reviews_aquecimento:
        if dicio ['filme_id'] == filme_id and dicio ['user_id'] == user_id:
            return dicio['comment']

'''
Agora, façamos uma funcao que adiciona uma nova avaliacao
'''
def adiciona(film_id,user_id,comment):
    for dicio in reviews_aquecimento:
        if dicio ['filme_id'] == filme_id and dicio ['user_id'] == user_id:
            if(dicio['comment']):
                dicio['comment'] = comment
            else:
                dicio = {'filme_id':filme_id,'user_id':user_id,'comment':comment}
                reviews_aquecimento.append(dicio.copy())
                dicio.clear()
def exemplo():
    print(oi)

'''
Agora, façamos um upgrade na adiciona:
    se o usuario ja avaliou esse filme,
    ao inves de adicionar uma nova avaliacao,
    mudamos a avaliacao existente.
'''
