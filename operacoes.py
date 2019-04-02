#!bin/python
from flask import Flask,jsonify,abort
from flask import request


app = Flask(__name__)


'''
Primeiramente, rode esse arquivo no cmd. Ele deve subir um
servidor.

Acesse a pagina http://localhost:5000/primeira/

Se deu tudo certo, deveria ter aparecido uma página com a string 
"funções matemáticas".
'''


'''
O comando seguinte define uma função index, que retorna 
a string "funções matemáticas".

Acima dele, podemos ver um decorator de python.

Esse decorator está associando a página /primeira/ a essa função
Quando você carrega a página no navegador, essa função roda
'''

@app.route('/primeira/')
def index():
        print('mama mia')
        return "Funcoes matematicas!"
'''
Voce pode ver, no cmd, que a cada vez que voce carrega a página, a string
"mama mia" aparece (no cmd)
'''

'''
A próxima função nos ensina a ler um pedaço da URL que foi passada

Por exemplo, ao acessarmos 
http://localhost:5000/matematica/potencia_de_dois/5
a variavel "expoente" da função recebe o valor 5.
Por isso, recebemos  { "resposta": 32 }
ao acessar a página

A propósito: as funções do flask tem que retornar strings.
Assim, não podemos retornar o dicionario {'resposta':32}

Usamos a funcao jsonify para converter o dicionário de pythom
em uma string, respeitando o formato json.
'''
@app.route('/matematica/potencia_de_dois/<int:expoente>')
def potencia_de_dois(expoente):
        return jsonify({"resposta":(2**expoente)})

'''
A proxima função é um pouco melhor.
Ela bate com dois tipos de url diferente

Uma sem o expoente e uma com.

Se o expoente não foi mandado, ela consegue reclamar.
'''


@app.route('/matematica/potencia_de_dois_melhor/<int:expoente>')
def potencia_de_dois_melhor(expoente=None):
        return jsonify({"resposta":(2**expoente)})

@app.route('/matematica/potencia_de_dois_melhor/')
def potencia_de_dois_veio_sem_exp():
        return jsonify({"erro":"sem expoente"}), 400


''' Note que, quando o usuário cometeu um erro e nao mandou o
expoente, a funcao retornou 2 valores. O primeiro é a string
a ser mostrada na página. O segundo é um número, representado
o código de status http 400.

O codigo de status 400 representa erro de usuário
'''

'''
A proxima função recebe dois parametros na URL, na forma de
query strings. No caso, são dois números, a e b, que devem
ser somados

Ou seja,

http://localhost:5000/matematica/soma?b=13&a=12

Deverá retornar

{
    "soma": 25
}

Perceba que, no caso de uma query string, não foi necessário
escrever as posicoes dos parametros na url do decorator.

Os parametros simplesmente "apareceram" em um dicionario 
dentro da funcao: o dicionario request.args

'''

@app.route('/matematica/soma')
def soma_url():
  dici_dos_parametros = request.args
  #os parametros passados na URL vieram parar
  #na variavel acima
  if 'a' not in dici_dos_parametros:
      numero_a = None
  else:
      numero_a = dici_dos_parametros['a']
  if 'b' not in dici_dos_parametros:
      numero_b = None
  else:
      numero_b = dici_dos_parametros['b']
  if numero_a == None or numero_b == None:
    return jsonify({'erro':'variável faltando'}), 400
  try:
    dicionario = {"soma": (int(numero_a)+int(numero_b))}
    return jsonify(dicionario)
  except ValueError : #esse except vai acontecer
      #se numero_a ou numero_b nao forem
      #faceis de converter para inteiros.
      #por exemplo, se numero_a='banana'
      #Nesse caso, a excessao ValueError 
      #é lancada pela funcao int
    return jsonify({"erro":"variável não é INT"}), 400

'''
Podemos ver um pouco mais sobre query strings na URL abaixo:
https://en.wikipedia.org/wiki/Query_string
'''

'''
Outro método menos obvio de fazer a mesma coisa é
usando POST.

No GET acima, nós passamos duas váriaveis na URL

Agora, com o post, vamos passar essas mesmas duas variáveis
através de um arquivo json

Para a URL /matematica/soma, com o método POST,
queremos o seguinte:

Que ela receba um json no corpo (body) do request,
e esse json deve definir dois numeros (a e b)

Ela deve retornar um json {resposta: v} onde v=a+b

Se o json nao contiver as chaves a ou b, ela deve retornar
um erro 400 (request mal formado) e um texto de erro
'''

@app.route('/matematica/soma', methods=['POST'])
def soma():
  dicionario_do_json_enviado = request.json
  if 'a' not in dicionario_do_json_enviado:
      numero_a = None
  else:
      numero_a = dicionario_do_json_enviado['a']
  if 'b' not in dicionario_do_json_enviado:
      numero_b = None
  else:
      numero_b = dicionario_do_json_enviado['b']
  if numero_a == None or numero_b == None :
    return jsonify({'erro':'faltando uma variável'}), 400
  return jsonify({'resposta':numero_a+numero_b})


'''
Exercicio

Crie uma função olá que recebe uma string nome e devolve
"ola <nome>".

Ela deve "atender" na url /ola/<nome>
'''
@app.route("/ola/<string:nome>")
def ola(nome):
    return f"ola {nome}"

'''
Exercicio

Crie uma função ola2 que recebe duas strings pessoa1 e pessoa2 e devolve
"olá fulano e ciclano".

Ela deve "atender" na url /ola_upgrade?pessoa1=fulano,pessoa2=ciclano
Use as query strings, como no exemplo
'''
@app.route("/ola_upgrade")
def ola2():
    nomes_dic=request.args
    if 'pessoa1' not in nomes_dic:
      pessoa1 = None
    else:
      pessoa1 = nomes_dic['pessoa1']
    if 'pessoa2' not in nomes_dic:
      pessoa2 = None
    else:
      pessoa2 = nomes_dic['pessoa2']
    return f'ola {pessoa1} e {pessoa2}'


'''
Exercicio

Crie uma funcao ola3, que atende na url /ola_upgrade (também!)
mas agora via POST.

Ela deve receber a pessoa1 e a pessoa2 via json
'''
@app.route('/ola_upgrade',methods=['POST'])
def ola3():
    nomes_dic=request.json
    if 'pessoa1' not in nomes_dic:
      pessoa1 = None
    else:
      pessoa1 = nomes_dic['pessoa1']
    if 'pessoa2' not in nomes_dic:
      pessoa2 = None
    else:
      pessoa2 = nomes_dic['pessoa2']
    return f'ola {pessoa1} e {pessoa2}'


'''
Exercicio

Crie uma funcao ola4, que atende
na url /ola_com_dic?pessoa1=fulano&pessoa2=ciclano.

Ela tem duas diferenças com ola2:
    * A resposta deve ser um dicionario {'pessoa1': fulano, 'pessoa2':ciclano}
    * Se estiver faltando alguma pessoa, 
    a resposta deve ser um dicionario {'erro':'falta gente'} e o
    codigo de status deve ser 400 
'''
@app.route('/ola_com_dic')
def ola4():
    nomes_dic=request.args
    if 'pessoa1' not in nomes_dic:
      pessoa1 = None
    else:
      pessoa1 = nomes_dic['pessoa1']
    if 'pessoa2' not in nomes_dic:
      pessoa2 = None
    else:
      pessoa2 = nomes_dic['pessoa2']
    if pessoa1 == None or pessoa2 == None:
      dic_men = {"erro":"falta gente"}
      return jsonify(dic_men,),400
    else:
      dic_men = {'pessoa1':pessoa1,"pessoa2":pessoa2}
    return jsonify(dic_men)
'''
Exercicio

Crie uma funcao ola5, que atende
na url /ola_com_dic (também!) mas agora via POST

Ela tem duas diferenças com ola3:
    * A resposta deve ser um dicionario {'pessoa1': fulano, 'pessoa2':ciclano}
    * Se estiver faltando alguma pessoa, 
    a resposta deve ser um dicionario {'erro':'falta gente'} e o
    codigo de status deve ser 400 
'''
@app.route("/ola_com_dic",methods=['POST'])
def ola5():
    nomes_dic=request.json
    if 'pessoa1' not in nomes_dic:
      pessoa1 = None
    else:
      pessoa1 = nomes_dic['pessoa1']
    if 'pessoa2' not in nomes_dic:
      pessoa2 = None
    else:
      pessoa2 = nomes_dic['pessoa2']
    if pessoa1 == None or pessoa2 == None:
      dic_men = {"erro":"falta gente"}
      return jsonify(dic_men),400
    else:
      dic_men = {'pessoa1':pessoa1,"pessoa2":pessoa2}
    return jsonify(dic_men)

'''
A partir daqui nao tem mais nada pra fazer
'''
if __name__ == '__main__':
   app.run(debug=True,port=5000)
