import requests






import unittest

class TestStringMethods(unittest.TestCase):


    def test_000_operacoes_ola1(self):
        r = requests.get('http://localhost:5000/ola/marcio')
        self.assertEqual(r.text,'ola marcio')
        r = requests.get('http://localhost:5000/ola/mario')
        self.assertEqual(r.text,'ola mario')
    
    def test_001_operacoes_ola2(self):
        r = requests.get('http://localhost:5000/ola_upgrade?pessoa1=marcio&pessoa2=alvaro')
        self.assertEqual(r.text,'ola marcio e alvaro')
        r = requests.get('http://localhost:5000/ola_upgrade?pessoa2=alvaro&pessoa1=marcio')
        self.assertEqual(r.text,'ola marcio e alvaro')
        r = requests.get('http://localhost:5000/ola_upgrade?pessoa2=robin&pessoa1=batman')
        self.assertEqual(r.text,'ola batman e robin')

    def test_002_operacoes_ola3(self):
        r = requests.post('http://localhost:5000/ola_upgrade', json={'pessoa1':'batman','pessoa2':'robin'})
        self.assertEqual(r.text,'ola batman e robin')
        r = requests.post('http://localhost:5000/ola_upgrade', json={'pessoa1':'tonico','pessoa2':'tinoco'})
        self.assertEqual(r.text,'ola tonico e tinoco')
    
    def test_003_operacoes_ola_com_dic(self):
        r = requests.get('http://localhost:5000/ola_com_dic?pessoa1=barney&pessoa2=fred')
        self.assertEqual(r.json()['pessoa1'],'barney')
        self.assertEqual(r.json()['pessoa2'],'fred')
        r = requests.get('http://localhost:5000/ola_com_dic?pessoa2=ron&pessoa1=harry')
        self.assertEqual(r.json()['pessoa1'],'harry')
        self.assertEqual(r.json()['pessoa2'],'ron')
    
    def test_004_operacoes_ola_com_dic(self):
        r = requests.get('http://localhost:5000/ola_com_dic?pessoa1=barney')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'falta gente')
        r = requests.get('http://localhost:5000/ola_com_dic?pessoa2=barney')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'falta gente')

    
    def test_005_operacoes_ola_com_dic(self):
        r = requests.post('http://localhost:5000/ola_com_dic',
            json={'pessoa1':'barney','pessoa2':'fred'})
        self.assertEqual(r.json()['pessoa1'],'barney')
        self.assertEqual(r.json()['pessoa2'],'fred')
        r = requests.post('http://localhost:5000/ola_com_dic',
            json={'pessoa1':'harry','pessoa2':'ron'})
        self.assertEqual(r.json()['pessoa1'],'harry')
        self.assertEqual(r.json()['pessoa2'],'ron')
    
    def test_006_operacoes_ola_com_dic(self):
        r = requests.post('http://localhost:5000/ola_com_dic',
            json={'pessoa2':'fred'})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'falta gente')
        r = requests.post('http://localhost:5000/ola_com_dic',
            json={'pessoa1':'harry'})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'falta gente')

    def test_101_aquecimento_consulta(self):
        self.assertEqual(consulta('tt0076759','lucio')['comment'],'achei legal')
        self.assertEqual(consulta('tt0076759','marcos')['comment'],'gostei')
        self.assertEqual(consulta('tt0076759','maria'),'nao encontrado')

    def test_102_aquecimento_adiciona(self):
        self.assertEqual(consulta('1212','maria'),'nao encontrado')
        adiciona('1212','maria','filme otimo')
        self.assertEqual(consulta('1212','maria')['comment'],'filme otimo')
    
    def test_103_aquecimento_adiciona(self):
        adiciona('1212','maria','filme otimo')
        self.assertEqual(consulta('1212','maria')['comment'],'filme otimo')
        antes = len(reviews_aquecimento)
        adiciona('1212','maria','mudei de ideia')
        self.assertEqual(consulta('1212','maria')['comment'],'mudei de ideia')
        adiciona('1212','maria','quer saber? bom mesmo')
        self.assertEqual(consulta('1212','maria')['comment'],'quer saber? bom mesmo')
        depois = len(reviews_aquecimento)
        self.assertEqual(antes,depois)



    def test_203_pega_review(self):
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt0076759/marcos')
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertTrue('gostei' in r.json()['comment'])
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt0076759/lucio')
        self.assertEqual(r.json(),{'user_id':'lucio','comment':'achei legal'})
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt1211837/lucio')
        self.assertEqual(r.json(),{'user_id':'lucio','comment':'estranho'})
    
    def test_204_pega_review_com_erro(self):
        r = requests.get('http://localhost:5001/socialfilm/reviews/outro/gato')
        self.assertEqual(r.json(),{'erro':'comentario nao encontrado'})
        self.assertEqual(r.status_code,404)

    def test_205_adiciona_review(self):
        r = requests.put('http://localhost:5001/socialfilm/reviews/tt1211837/marcos',
                json={'comment':'esquisito mesmo'})
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertEqual(r.json()['comment'],'esquisito mesmo')
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt1211837/marcos')
        self.assertEqual(r.json(),{'user_id':'marcos','comment':'esquisito mesmo'})
        r = requests.put('http://localhost:5001/socialfilm/reviews/tt0087332/marcos',
                json={'comment':'curiosa mistura de fantasmas e empreendedorismo'})
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertEqual(r.json()['comment'],'curiosa mistura de fantasmas e empreendedorismo')
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt0087332/marcos')
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertEqual(r.json()['comment'],'curiosa mistura de fantasmas e empreendedorismo')


    def test_206_muda_review(self):
        antes = self.total_reviews()
        r = requests.put('http://localhost:5001/socialfilm/reviews/tt0087332/marcos',
                json={'comment':'mudei de ideia. Nao gosto de fantasmas'})
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertEqual(r.json()['comment'],'mudei de ideia. Nao gosto de fantasmas')
        r = requests.get('http://localhost:5001/socialfilm/reviews/tt0087332/marcos')
        self.assertEqual(r.json()['user_id'],'marcos')
        self.assertEqual(r.json()['comment'],'mudei de ideia. Nao gosto de fantasmas')
        depois = self.total_reviews()
        self.assertEqual(antes,depois)

    def test_207_filme_invalido(self):
        r = requests.put('http://localhost:5001/socialfilm/reviews/jamesbond/marcos',
                json={'comment':'mudei de ideia. Nao gosto de fantasmas'})
        self.assertEqual(r.json()['error'],'filme nao encontrado')
        self.assertEqual(r.status_code,404)

    def test_208_all_films(self):
        r = requests.get('http://localhost:5001/socialfilm/reviews/all_films/marcos')
        lista_respostas = r.json()
        self.assertTrue(len(lista_respostas) >= 2)
        achei_dr_strange = False
        for review in r.json():
            if review['film_id'] == 'tt1211837':
                achei_dr_strange = True
        if not achei_dr_strange:
            self.fail('a lista de reviews do marcos nao contem o filme dr strange')
    
    def test_209_all_films_nome(self):
        r = requests.get('http://localhost:5001/socialfilm/reviews/all_films/marcos')
        lista_respostas = r.json()
        achei_dr_strange = False
        achei_star_wars = False
        for review in r.json():
            if 'film_name' not in review:
                self.fail('achei um filme sem nome!')
            if 'trange' in review['film_name']: 
                achei_dr_strange = True
            if 'ars' in review['film_name']:
                achei_star_wars = True
        if not achei_dr_strange:
            self.fail('a lista de reviews do marcos nao contem o nome do dr strange')
        if not achei_star_wars:
            self.fail('a lista de reviews do marcos nao contem o nome do star wars')

    def test_210_all_films_nao_deve_alterar_a_review(self):
        r = requests.get('http://localhost:5001/socialfilm/all')
        lista_reviews = r.json()['reviews']
        for review in lista_reviews:
            if 'film_name' in review:
                self.fail('voce alterou as reviews do servidor, colocando nome')

    def test_211_estrelas(self):
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759/marcos')
        self.assertEqual(int(r.json()['stars']),4)
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759/lucio')
        self.assertEqual(int(r.json()['stars']),5)
        r = requests.get('http://localhost:5001/socialfilm/stars/tt1211837/lucio')
        self.assertEqual(int(r.json()['stars']),2)
        self.assertEqual(r.status_code,200) #codigo normal, que ocorre
        #se voce simplesmente nao fizer nada
    
    def test_212_estrelas_filme_inexistente(self):
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759nao/marcos')
        self.assertTrue('error' in r.json())
        self.assertEqual(r.json()['error'],'filme nao encontrado')
        r = requests.get('http://localhost:5001/socialfilm/stars/tt00076759/marcos')
        self.assertTrue('error' in r.json())
        self.assertEqual(r.json()['error'],'filme nao encontrado')
        self.assertEqual(r.status_code,404)

    def test_213_estrelas_review_nao_encontrada(self):
        r = requests.get('http://localhost:5001/socialfilm/stars/tt1211837/marcos')
        self.assertTrue('error' in r.json())
        self.assertEqual(r.json()['error'],'review nao encontrada')
        self.assertEqual(r.status_code,404)

    def test_214_novas_estrelas(self):
        r = requests.put('http://localhost:5001/socialfilm/stars/tt0119177/marcos',
                json={'stars':3})
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0119177/marcos')
        self.assertEqual(r.json()['stars'],3)
        contagem = self.total_stars()
        r = requests.put('http://localhost:5001/socialfilm/stars/tt0119177/marcos',
                json={'stars':4})
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0119177/marcos')
        self.assertEqual(r.json()['stars'],4)
        cont_depois = self.total_stars()
        self.assertEqual(contagem,cont_depois)

    def test_215_average_stars(self):
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759/average')
        self.assertTrue(4.4 < r.json()['average_stars'] < 4.6)
        r = requests.put('http://localhost:5001/socialfilm/stars/tt0076759/marcos',
                json={'stars':1})
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759/average')
        self.assertTrue(2.9 < r.json()['average_stars'] < 3.1)
        r = requests.put('http://localhost:5001/socialfilm/stars/tt0076759/marcos',
                json={'stars':4})
        r = requests.get('http://localhost:5001/socialfilm/stars/tt0076759/average')
        self.assertTrue(4.4 < r.json()['average_stars'] < 4.6)





    

    def total_reviews(self):
        r = requests.get('http://localhost:5001/socialfilm/all')
        return len(r.json()['reviews'])
    
    def total_stars(self):
        r = requests.get('http://localhost:5001/socialfilm/all')
        return len(r.json()['notas'])


    

    

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()
