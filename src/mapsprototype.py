# coding: utf-8
import requests, json
import time
from scrapping import acessoqedu
from scrapping import checarsistemaensino

def pesquisaportexto(query, api_key):
    query = query.replace(' ', '+')
    url = '''
https://maps.googleapis.com/maps/api/place/textsearch/json?
key=%s&
query=%s
''' % (api_key, query)
    url = url.replace('\n', '')
    print("Acessando o endereço: " + url)

    r = requests.get(url)
    x = r.json()
    y = x["results"]
    print("Query Pesquisada:" + query + '\n')
    next_page = x["next_page_token"] if "next_page_token" in x else ""
    print("Escolas encontradas: " + str(len(y))+'\n')
    return y, next_page

def pesquisadetalhada(school_json,api_key):
    # realizamos uma pesquisa detalhada para cada elemento encontrado na pesquisa por texto
    url_details = ''' 
https://maps.googleapis.com/maps/api/place/details/json?
placeid=%s&
key=%s
''' % (school_json['place_id'], api_key)
    url_details = url_details.replace('\n', '')
    r_details = requests.get(url_details)
    x = r_details.json()
    z = x['result']
    return z

def inserirnovaescola(driver,data, school_json,api_key,PATH):
    print("\n\nInserindo nova escola:")
    # chamamos a pesquisa detalhada e inserimos as informações que precisamos da escola lá dentro
    z = pesquisadetalhada(school_json,api_key)
    #print(z)

    data['place_id'] = school_json['place_id'] if 'place_id' in school_json else ''
    data['name'] = school_json['name'] if 'name' in school_json else ''
    data['formatted_address'] = school_json['formatted_address'] if 'formatted_address' in school_json else ''
    data['website'] = z['website'] if 'website' in z else ''
    data['formatted_phone_number'] = z['formatted_phone_number'] if 'formatted_phone_number' in z else ''
    inep, cidade, qedu_url = acessoqedu(driver,data['name'],data['formatted_address'].split(",")[2].split("-")[0])
    data['Inep'] = inep
    data['city'] = cidade
    data['qedu_url'] = qedu_url
    data['Sistema de Ensino'], data['Escola é Bilíngue?'], data['Comunidade que a escola pertence'], driver = checarsistemaensino(driver,data['website'],PATH)
    return data, driver

def pesquisanextpage(next_page,api_key):
    time.sleep(2)
    url = '''
https://maps.googleapis.com/maps/api/place/textsearch/json?
pagetoken=%s&key=%s
''' % (next_page, api_key)
    url = url.replace('\n', '')
    print("Acessando o endereço: " + url)
    r = requests.get(url)
    x = r.json()
    y = x["results"]
    next_page = x["next_page_token"] if "next_page_token" in x else ""
    print("Escolas encontradas: " + str(len(y)) + '\n')
    return y, next_page






# Exemplo de Output do Search Text
# Referências:
# API do Google:
# https://developers.google.com/maps/documentation/places/web-service/search?hl=en

# Artigos / projetos:
# https://www.geeksforgeeks.org/python-get-set-places-according-search-query-using-google-places-api/
# https://github.com/Pithikos/Geoexplorer
# https://github.com/Pithikos/Geoexplorer
# https://github.com/drobnikj/crawler-google-places

# Exemplo de output:
# {
#    "html_attributions" : [],
#    "next_page_token" : "ATtYBwLBOxxpxNbWLAZC66WhLGiMX2eZ9qXRDNJMQa3TOGsja_aKoPeNjiCf7ycUJhuYsiEx0ouH2BqXmuiKGDELIWW3im9EKBxnViHcEJojzW0I7ZgC2HEmY7QqvfUEOma9YvLXxuSrkqKFwE_2G3th85FwNC5TMRPWO7NlOQefbu6wi9qjWp0FXNo_21Ld5EyO7XNn8gTowGRr-gLlGE_YFMi5vVLXbqPE9roW92r1rUtZrbMj9KORUNnPBKG4pljW2oTqJIfXWgrEXCsxs_WWq5iq5nbE4NTGT1MK9y9VHBoUzn6sukdM70U_xaniPT0HbxcIeRAOdTFTFdQ-KbzVmfp4D8YhC0HbPaGU3wPhftBKvTq0Ymi5bjn-wIXWqRcQsySxIKebACwqRKSqyqdrYZz4",
#    "results" : [
#       {
#          "business_status" : "CLOSED_TEMPORARILY",
#          "formatted_address" : "R. Umari - Mucuripe, Fortaleza - CE, 60175-280, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7261335,
#                "lng" : -38.48379540000001
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.724787620107278,
#                   "lng" : -38.48238587010728
#                },
#                "southwest" : {
#                   "lat" : -3.727487279892721,
#                   "lng" : -38.48508552989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "School High School Dragon Sea",
#          "permanently_closed" : true,
#          "photos" : [
#             {
#                "height" : 691,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/107895280021622558621\"\u003eDRAG├âO DO MAR\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwIRnsP6aqBrf---R9EamO2k53nB-E5CQIjBFF4HK4oEPbOs_2jpNQ8RR5xWVUqEf_tb87pvJRB_jo9j7EyxPkMfhVg_W74Kq0xKLsKu0hdcn_ek10NHEKhufce9KbaqyDrcWc1zaO3MFiLK0BMwlKZFl0qBMpw8PByBvLSqBU--fVhk",
#                "width" : 771
#             }
#          ],
#          "place_id" : "ChIJP_qTwNhHxwcRzOLD_KKZ99A",
#          "plus_code" : {
#             "compound_code" : "7GF8+GF Mucuripe, Fortaleza - State of Cear├í",
#             "global_code" : "69837GF8+GF"
#          },
#          "rating" : 4.3,
#          "reference" : "ChIJP_qTwNhHxwcRzOLD_KKZ99A",
#          "types" : [ "secondary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 7
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. Ildefonso Albano, 1030 - Meireles, Fortaleza - CE, 60115-000, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7300076,
#                "lng" : -38.5123553
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.728683420107278,
#                   "lng" : -38.51092187010727
#                },
#                "southwest" : {
#                   "lat" : -3.731383079892722,
#                   "lng" : -38.51362152989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Col├®gio Darwin",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 1349,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/103616554554828175966\"\u003eLuuh Felix\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwLEKE3IJQdlV8hlxVkALqGikszTAKZitN2A_1PmxgSGhSuqjUf69JnMrLxTtcvjad62cLBKVK-MIkeMW_UwIxo3MIRnEUjnz8oI2EjDbhMgunqSiXnrE-UNLsyyZz70HRNftDnve1yH40ucRAhopPwztmnTIpAzATd5yQEXM_i4C35I",
#                "width" : 2024
#             }
#          ],
#          "place_id" : "ChIJ8TJyk1tIxwcROPVduQGnzBk",
#          "plus_code" : {
#             "compound_code" : "7F9Q+X3 Meireles, Fortaleza - State of Cear├í",
#             "global_code" : "69837F9Q+X3"
#          },
#          "rating" : 4.1,
#          "reference" : "ChIJ8TJyk1tIxwcROPVduQGnzBk",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 46
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. dos Expedicion├írios, 3910 - Jardim Am├®rica, Fortaleza - CE, 60410-446, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7525385,
#                "lng" : -38.5375821
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.751206220107278,
#                   "lng" : -38.53617582010728
#                },
#                "southwest" : {
#                   "lat" : -3.753905879892722,
#                   "lng" : -38.53887547989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "M.S. Filgueiras Lima",
#          "photos" : [
#             {
#                "height" : 1960,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/116290423132396535425\"\u003eGl├íumer Fernandes\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwKno4-KNc4ScDVCer0BLzfTUyPAVWctT0UFvp4uIWeZLzayLWRXOQl42mRjzzCzrfUhA051JbAk8yu9WUjSBluUbxH0gFl2fPv76RxEMSeNW3I6ejIM2-txZ3inw0SoLxlWBI-yb2ZTCbGIObOlLpPTRttH6pjwfXesmO-93Q6pXpbh",
#                "width" : 4032
#             }
#          ],
#          "place_id" : "ChIJS81xtTxJxwcRuG1wve5PGbs",
#          "plus_code" : {
#             "compound_code" : "6FW6+XX Jardim Am├®rica, Fortaleza - State of Cear├í",
#             "global_code" : "69836FW6+XX"
#          },
#          "rating" : 4.1,
#          "reference" : "ChIJS81xtTxJxwcRuG1wve5PGbs",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 41
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. In├ício Moreira, 133 - Messejana, Fortaleza - CE, 60871-585, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.835045499999999,
#                "lng" : -38.4912035
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.833707770107278,
#                   "lng" : -38.49002862010728
#                },
#                "southwest" : {
#                   "lat" : -3.836407429892722,
#                   "lng" : -38.49272827989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Col├®gio Paiva Andrade",
#          "photos" : [
#             {
#                "height" : 346,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/115783744268462735182\"\u003eCamila Taumaturgo\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwL5tKRk0QzGj_TdGhlYtcmkgtKqIEb_hGK9iwNEoZJp97W34jgDaAk-nBkZvXBPnpHoHjaqzxaWMc7czuJTI_xgfheOSVBNK1cxdzGQFZhrcWNltNKHTdgG9hu6D_znDFX_pW6mp8orz3ZzqEsqfjQI6A6uCQfq2xxX3LmEEuq1mZPw",
#                "width" : 518
#             }
#          ],
#          "place_id" : "ChIJN7ZdD_tPxwcRb6D-wppCnRs",
#          "plus_code" : {
#             "compound_code" : "5G75+XG Messejana, Fortaleza - State of Cear├í",
#             "global_code" : "69835G75+XG"
#          },
#          "rating" : 4.4,
#          "reference" : "ChIJN7ZdD_tPxwcRb6D-wppCnRs",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 63
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Rua Dom Sebasti├úo Leme, 819 - F├ítima, Fortaleza - CE, 60050-220, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7489757,
#                "lng" : -38.525645
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.747636020107278,
#                   "lng" : -38.52435917010727
#                },
#                "southwest" : {
#                   "lat" : -3.750335679892722,
#                   "lng" : -38.52705882989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Vila",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 2448,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/116293520912391108758\"\u003ekurtis fran├ºois Bastos\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwLsTzAQ67S1h_pP1g61MeFfqUS3RPw0g-puKX2qGGerxNHN_6abr_aRvxBHkT3hw2CXVvanMQZDet0H-tQBQuUjAh9CzoSwCaabgPvD7jAhDkYp8Oz2UTi42vq2b8EiDSt3fsoaGKGSUCqi40RjHFL2IatHFHRcxZ7YdDGmd7ElyuDR",
#                "width" : 3264
#             }
#          ],
#          "place_id" : "ChIJuzHPN-BIxwcRqcHpB1L6Z3k",
#          "plus_code" : {
#             "compound_code" : "7F2F+CP Fatima, Fortaleza - State of Cear├í",
#             "global_code" : "69837F2F+CP"
#          },
#          "rating" : 4.1,
#          "reference" : "ChIJuzHPN-BIxwcRqcHpB1L6Z3k",
#          "types" : [ "school", "primary_school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 25
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Senador Virg├¡lio T├ívora, 2000 - Aldeota, Fortaleza - CE, 60170-078, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.743888,
#                "lng" : -38.4962526
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.742643720107278,
#                   "lng" : -38.49454517010727
#                },
#                "southwest" : {
#                   "lat" : -3.745343379892722,
#                   "lng" : -38.49724482989271
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "College Saint Cecilia",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 683,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/105246715315021800170\"\u003eCol├®gio Santa Cec├¡lia\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwKYVWcC5x2-XrhXnkxbLRMqj6d2Pg7L70btUkvC-uQPC-DgHnn0rgEH8g6o9xf_NNyWnnZ7tHkpfzlDwWLZEMgoByuz65fT487WE18glA_2cWTe32IRwiYIKP2RouJjKjYYtv6fRKwCwgPqA_hoKEx1NCwrSLfJryqCEaNqC0fmQR7N",
#                "width" : 1024
#             }
#          ],
#          "place_id" : "ChIJrVHTAJBIxwcR_e0i66_aMw8",
#          "plus_code" : {
#             "compound_code" : "7G43+CF Aldeota, Fortaleza - State of Cear├í",
#             "global_code" : "69837G43+CF"
#          },
#          "rating" : 4.5,
#          "reference" : "ChIJrVHTAJBIxwcR_e0i66_aMw8",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 97
#       },
#       {
#          "business_status" : "CLOSED_TEMPORARILY",
#          "formatted_address" : "R. Estado do Rio, 955 - Panamericano, Fortaleza - CE, 60440-145, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.759179399999999,
#                "lng" : -38.5709947
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.757754970107278,
#                   "lng" : -38.56976057010728
#                },
#                "southwest" : {
#                   "lat" : -3.760454629892722,
#                   "lng" : -38.57246022989273
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "EEFM Joaquim Alves",
#          "permanently_closed" : true,
#          "photos" : [
#             {
#                "height" : 960,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/106050295699973313492\"\u003eFranklins Torres\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwIiAI4WZq4IJ-Z5AlQ96NTyXAY4u3C_muA5PeFxb5k6aiSGGcaWTaTcFgtuOie-Pp1offwfoB-ave6YRJIXdSbSFMlRgbJoKzCpxS7hPFZlEwQtdLnMEvzQxHpb-knIfh3DKD86SjAQjbORdo9f1XH_B4ovWVtvOsMFlA2CzQk3IKC0",
#                "width" : 1280
#             }
#          ],
#          "place_id" : "ChIJMVheDP1LxwcRbztQb8-BIU4",
#          "plus_code" : {
#             "compound_code" : "6CRH+8J Panamericano, Fortaleza - State of Cear├í",
#             "global_code" : "69836CRH+8J"
#          },
#          "rating" : 3.9,
#          "reference" : "ChIJMVheDP1LxwcRbztQb8-BIU4",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 21
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. Rafael Tobias, 2861 - Lagoa Sapiranga (Coit├®), Fortaleza - CE, 60830-105, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.8066004,
#                "lng" : -38.4712573
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.805254320107279,
#                   "lng" : -38.46996192010728
#                },
#                "southwest" : {
#                   "lat" : -3.807953979892722,
#                   "lng" : -38.47266157989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Canadense de Fortaleza",
#          "place_id" : "ChIJEeTuLXFFxwcR3ok3aczjVAs",
#          "plus_code" : {
#             "compound_code" : "5GVH+9F Lagoa Sapiranga (Coit├®), Fortaleza - State of Cear├í",
#             "global_code" : "69835GVH+9F"
#          },
#          "rating" : 4.3,
#          "reference" : "ChIJEeTuLXFFxwcR3ok3aczjVAs",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 3
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Jo├úo Pessoa, 4279 - Damas, Fortaleza - CE, 60425-813, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.751101999999999,
#                "lng" : -38.54749839999999
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.749554720107278,
#                   "lng" : -38.54636632010727
#                },
#                "southwest" : {
#                   "lat" : -3.752254379892722,
#                   "lng" : -38.54906597989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Col├®gio Juvenal de Carvalho",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 3096,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/115076423935414083036\"\u003eO incr├¡vel mundo de R├┤la\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwJTyYhd_I2HD1UcdeFHRcmrxYQ7AWNNrQb5ST_Ja1Z-3ZtTQ6y1afp52vfiZ7DB7TsB119L2JoMdWQKZue47uyNLHcTVAgCMEnXLdrKf07gHJQJjXBKdoInKNU4BeYh9ve2hYIrvdUIpwE3U5PubOWDVJ6u8jMWSvUPVVWqQdTJvJTf",
#                "width" : 4128
#             }
#          ],
#          "place_id" : "ChIJ78zGd0BJxwcRHcKIQJ1Qo6I",
#          "plus_code" : {
#             "compound_code" : "6FX3+H2 Damas, Fortaleza - State of Cear├í",
#             "global_code" : "69836FX3+H2"
#          },
#          "rating" : 4.3,
#          "reference" : "ChIJ78zGd0BJxwcRHcKIQJ1Qo6I",
#          "types" : [ "secondary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 72
#       },
#       {
#          "business_status" : "CLOSED_TEMPORARILY",
#          "formatted_address" : "Rua Dr. Joaquim Bento, 590 - Messejana, Fortaleza - CE, 60840-200, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.828501299999999,
#                "lng" : -38.4863502
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.827041420107278,
#                   "lng" : -38.48499762010727
#                },
#                "southwest" : {
#                   "lat" : -3.829741079892722,
#                   "lng" : -38.48769727989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Municipal Josefa Barros De Alencar",
#          "permanently_closed" : true,
#          "place_id" : "ChIJI5LGjPhPxwcRGkxBkTaEStk",
#          "plus_code" : {
#             "compound_code" : "5GC7+HF Messejana, Fortaleza - State of Cear├í",
#             "global_code" : "69835GC7+HF"
#          },
#          "rating" : 3.7,
#          "reference" : "ChIJI5LGjPhPxwcRGkxBkTaEStk",
#          "types" : [ "primary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 15
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Duque de Caxias, 1452 - Centro, Fortaleza - CE, 60034-111, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7292878,
#                "lng" : -38.5371768
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.727986470107278,
#                   "lng" : -38.53584242010728
#                },
#                "southwest" : {
#                   "lat" : -3.730686129892721,
#                   "lng" : -38.53854207989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Col├®gio Tiradentes: Ensino Infantil e Fundamental, Matr├¡culas Abertas Centro, Fortaleza CE",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 810,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/112119610302872744735\"\u003eA Google User\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwKGxvF0dr82k_yqG7OHC4GoZMNirdcrx9ZhjZ7ZKM0NyQTbNLcouNufLAls8P2anNvlxTwdi-eSE5T-ZiOdp9sWCjKTxOTor5vfIO_r7VtMPU3LrIxyjMWrggADd0YE4Zo_esrGMkEpTIYVUP8DEoKayiwuKeEvq6hTXpKmOcxht14b",
#                "width" : 1080
#             }
#          ],
#          "place_id" : "ChIJG2vTUK9JxwcRiW6xr_VpC5Y",
#          "plus_code" : {
#             "compound_code" : "7FC7+74 Centro, Fortaleza - State of Cear├í",
#             "global_code" : "69837FC7+74"
#          },
#          "rating" : 4.5,
#          "reference" : "ChIJG2vTUK9JxwcRiW6xr_VpC5Y",
#          "types" : [ "primary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 26
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. P├┤rto Velho, 401 - Jo├úo XXIII, Fortaleza - CE, 60525-571, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7688159,
#                "lng" : -38.5853757
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.767300320107278,
#                   "lng" : -38.58407452010728
#                },
#                "southwest" : {
#                   "lat" : -3.769999979892722,
#                   "lng" : -38.58677417989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "EGF - Escola Grande Fortaleza",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 3024,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/116251906564735782460\"\u003eA Google User\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwKcIcQgcvAX7wQK6j4qMqEYSqEDZnWcSZH2lB0F8n0gIbQvrZKMHRHbkJLyyY-cY0H_TYUhqvMKuCpNQmo-uOd5eEZ9r65DmazeEoQt72bim1k986aFGBtPmauiFlKDayF2U4ZVNNo3RbwS52ZpPWIioTTTiQnf_MQd_AIU4f12DAqv",
#                "width" : 4032
#             }
#          ],
#          "place_id" : "ChIJ7aVSoQ5MxwcRVLooszGzoWg",
#          "plus_code" : {
#             "compound_code" : "6CJ7+FR Jo├úo XXIII, Fortaleza - State of Cear├í",
#             "global_code" : "69836CJ7+FR"
#          },
#          "rating" : 4.8,
#          "reference" : "ChIJ7aVSoQ5MxwcRVLooszGzoWg",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 25
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Santos Dumont, 5572 - Coc├│, Fortaleza - CE, 60191-151, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7418174,
#                "lng" : -38.4822408
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.740293620107278,
#                   "lng" : -38.48083972010728
#                },
#                "southwest" : {
#                   "lat" : -3.742993279892722,
#                   "lng" : -38.48353937989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Col├®gio Integral",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 3456,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/106820629623115674388\"\u003eMovile Maia\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwLrHFXNLnhlF2pTFtIBE8mQj5_HSSOyHgBj8rl0VOWtE0hd3YojLjLFCmHuzCRIGo24lrl4G9RFAHhLO60mk3C3t0lruRlE8lzNI6gFKZ9INDGOA8onTEBOrO72h4q3ZTwzM_UTni_IWj-VBoX1_UWhz6OqMaFcYonQoTLrCaVIAU0k",
#                "width" : 4608
#             }
#          ],
#          "place_id" : "ChIJ1UXLdSlGxwcR8OvyGVAPciM",
#          "plus_code" : {
#             "compound_code" : "7G59+74 Coc├│, Fortaleza - State of Cear├í",
#             "global_code" : "69837G59+74"
#          },
#          "rating" : 3.5,
#          "reference" : "ChIJ1UXLdSlGxwcR8OvyGVAPciM",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 42
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Santos Dumont, 55 - Centro, Fortaleza - CE, 60150-160, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7279868,
#                "lng" : -38.5226677
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.726789920107278,
#                   "lng" : -38.52137107010728
#                },
#                "southwest" : {
#                   "lat" : -3.729489579892722,
#                   "lng" : -38.52407072989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "College of the Imaculada Concei├º├úo",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 2248,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/114108538938307162118\"\u003epedro-jn nascimento\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwJT_nEBceSP3u4VEbEDxJPYWe-gdxXBWVaUgF332TkIg93vgAee6frPR6klvsg4Mo7Ebi04irdh6KIpyfrfEST4_CvIeuxFHBZNSHcGEGBgAzbC9t_Jy8kGr0iR0gzpKpAN1gV3PjJLi2bAZBInRhM4fTOZmTOpz1H68JED8M90OTEt",
#                "width" : 4000
#             }
#          ],
#          "place_id" : "ChIJ73a1SVJIxwcRmo86Ozrk1Zw",
#          "plus_code" : {
#             "compound_code" : "7FCG+RW Centro, Fortaleza - State of Cear├í",
#             "global_code" : "69837FCG+RW"
#          },
#          "rating" : 4.2,
#          "reference" : "ChIJ73a1SVJIxwcRmo86Ozrk1Zw",
#          "types" : [ "secondary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 66
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. da Assun├º├úo, 1668 - Jos├® Bonifacio, Fortaleza - CE, 60712-020, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7440035,
#                "lng" : -38.531986
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.742675170107278,
#                   "lng" : -38.53056922010727
#                },
#                "southwest" : {
#                   "lat" : -3.745374829892722,
#                   "lng" : -38.53326887989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Sonho Infantil | Educa├º├úo Infantil | Ensino Fundamental | Col├®gio Particular Infantil |",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 810,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/101556111218085904136\"\u003eA Google User\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwK-5wP0Lm7ySRFmV4tluTvA6C71Cif3prDX6PvDsqdY-iLP20gW4wngIVaVChel0aY9_gXXBkPJsPFR0NsnJE7r-GFLVEswwEYUpukGedgog18d-j8xu2wkEGSUqtFwpXOvxeGwN0l4TISO91Ulmb4FWS2ommQTmAryQha2PMuMhVOa",
#                "width" : 1240
#             }
#          ],
#          "place_id" : "ChIJ2aoohxxJxwcRYE3htYdGcgE",
#          "plus_code" : {
#             "compound_code" : "7F49+96 Jos├® Bonifacio, Fortaleza - State of Cear├í",
#             "global_code" : "69837F49+96"
#          },
#          "rating" : 4.5,
#          "reference" : "ChIJ2aoohxxJxwcRYE3htYdGcgE",
#          "types" : [ "primary_school", "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 14
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Bernardo Manuel, 9970A - Dend├¬, Fortaleza - CE, 60761-282, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.8054262,
#                "lng" : -38.5536712
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.804093870107278,
#                   "lng" : -38.55226057010728
#                },
#                "southwest" : {
#                   "lat" : -3.806793529892722,
#                   "lng" : -38.55496022989273
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Municipal De Tempo Integral E Educa├º├úo Bil├¡ngue Francisco Suderland Bastos Mota",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 655,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/114279883057873342429\"\u003eA Google User\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwLpOUEHFrI6rZCYqlbn34i8R_qceiiGuz8vhogfAtqzMXe5P_yyG-LjoAFTwE48CZ6ZMo2hSA3Fvjj0T5ndmkqDp4OlZdx2Dwa05bcGSFv6yl4YU9GFMhdJOmPDuBp3dt9w-ukCVDPa_Dv7fws0wC-VQXjTUVyzE39IepZB7We6qEXz",
#                "width" : 720
#             }
#          ],
#          "place_id" : "ChIJAf3LcZ5PxwcR6g6CQwZKUjE",
#          "plus_code" : {
#             "compound_code" : "5CVW+RG Dend├¬, Fortaleza - State of Cear├í",
#             "global_code" : "69835CVW+RG"
#          },
#          "rating" : 4,
#          "reference" : "ChIJAf3LcZ5PxwcR6g6CQwZKUjE",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 1
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "R. Ant├┤nio Augusto, 1300 - Aldeota, Fortaleza - CE, 60110-370, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.7322894,
#                "lng" : -38.5141518
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.730950520107278,
#                   "lng" : -38.51276857010728
#                },
#                "southwest" : {
#                   "lat" : -3.733650179892722,
#                   "lng" : -38.51546822989273
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Instituto Educacional Girassol",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 3096,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/116703382539092836932\"\u003eJosemir Mendes\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwIV0GWhnrQylsJ6UA4t-zMdmeVkbI_zwaod3UjDh3CoCcYQU0R__IxENxAbtOoTmYG2e0cl40J0qWJSEOnl5a30uBJ005g9FhSFyPysb7XxRhimHJB05WWmprhn63Qjoo8XWnQWCkEoSFpB0LWkxd2X6LnIRinAn7I6_jpLHJ3BpSRy",
#                "width" : 4128
#             }
#          ],
#          "place_id" : "ChIJP-rXoFlIxwcRDpmHpmp8Z3Y",
#          "plus_code" : {
#             "compound_code" : "7F9P+38 Aldeota, Fortaleza - State of Cear├í",
#             "global_code" : "69837F9P+38"
#          },
#          "rating" : 4.1,
#          "reference" : "ChIJP-rXoFlIxwcRDpmHpmp8Z3Y",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 18
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Santos Dumont, 485 - Aldeota, Fortaleza - CE, 60150-160, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.72902,
#                "lng" : -38.51776100000001
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.728135570107278,
#                   "lng" : -38.51656242010728
#                },
#                "southwest" : {
#                   "lat" : -3.730835229892722,
#                   "lng" : -38.51926207989273
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Military College of Fortaleza - CMF",
#          "photos" : [
#             {
#                "height" : 612,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/107674632961764855856\"\u003eIan Vitor\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwIQbDFlKbz8IQ85VF83Ur0jfeL8HEgX-PsK4RO45DcaCaF5BlQWdFLRTHKXE_DDgXWZEr5p0E0AaDAZyhN04N-nlovI4Jr-WbBVc-qDmhVvxHbavwajey02IOgeIiO68ogH6RPkI6B2zqDzrB4EGYEAhDBeHXrr72hkzYWbkyS9Dku7",
#                "width" : 816
#             }
#          ],
#          "place_id" : "ChIJN46duFBIxwcRcCV1Ce13EG4",
#          "plus_code" : {
#             "compound_code" : "7FCJ+9V Aldeota, Fortaleza - State of Cear├í",
#             "global_code" : "69837FCJ+9V"
#          },
#          "rating" : 4.7,
#          "reference" : "ChIJN46duFBIxwcRcCV1Ce13EG4",
#          "types" : [
#             "primary_school",
#             "secondary_school",
#             "school",
#             "point_of_interest",
#             "establishment"
#          ],
#          "user_ratings_total" : 194
#       },
#       {
#          "business_status" : "CLOSED_TEMPORARILY",
#          "formatted_address" : "Rua Monsenhor Salazar, 1480 - S├úo Jo├úo do Tauape, Fortaleza - CE, 60130-731, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.75561,
#                "lng" : -38.50609
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.754151720107278,
#                   "lng" : -38.50474832010728
#                },
#                "southwest" : {
#                   "lat" : -3.756851379892722,
#                   "lng" : -38.50744797989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Escola Municipal De Tempo Integral Professora Antonieta Cals",
#          "permanently_closed" : true,
#          "photos" : [
#             {
#                "height" : 2448,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/105561076205554969667\"\u003eHander Hans\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwJQ99tjJhTy7uzFWgmI28saFfA21UW0cS7Fs8fFRlGU1OxDo_2TQ8mM87Sg8PGHBhMmf2ke7biRpp0uWu7oDOmIONG4hclYEj1xespvIFk-YP4qp17MgrH91QcsfWgGRHSBD2ZT6cRRWhJ2liypP3IK2Xu0FbIZK9JrWJRdu1GdC2yJ",
#                "width" : 3264
#             }
#          ],
#          "place_id" : "ChIJbwxWysBIxwcRQwC1_hVmEzo",
#          "plus_code" : {
#             "compound_code" : "6FVV+QH S├úo Jo├úo do Tauape, Fortaleza - State of Cear├í",
#             "global_code" : "69836FVV+QH"
#          },
#          "rating" : 3.7,
#          "reference" : "ChIJbwxWysBIxwcRQwC1_hVmEzo",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 10
#       },
#       {
#          "business_status" : "OPERATIONAL",
#          "formatted_address" : "Av. Ant├┤nio Sales, 116 - Joaquim T├ívora (Fortaleza), Fortaleza - CE, 60135-101, Brazil",
#          "geometry" : {
#             "location" : {
#                "lat" : -3.739878,
#                "lng" : -38.520846
#             },
#             "viewport" : {
#                "northeast" : {
#                   "lat" : -3.738442420107278,
#                   "lng" : -38.51946767010728
#                },
#                "southwest" : {
#                   "lat" : -3.741142079892722,
#                   "lng" : -38.52216732989272
#                }
#             }
#          },
#          "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png",
#          "name" : "Salesian Don Bosco College",
#          "opening_hours" : {
#             "open_now" : true
#          },
#          "photos" : [
#             {
#                "height" : 1280,
#                "html_attributions" : [
#                   "\u003ca href=\"https://maps.google.com/maps/contrib/107417504250221912233\"\u003eA Google User\u003c/a\u003e"
#                ],
#                "photo_reference" : "ATtYBwKOvQ-HUeqpgLmO1Ug3fBAy-vf8SZQqorpDGKsPHozr6kUMOcvYEFuNg0BHqRgVUbeggmRdpMbhDpw7-hiDYQZuTLUCBaUbvW6rxX_HjzNSalhnUScAcZj_pvzsPQFoeSmqX1U2WCl7Jc7LkZPhfVXvJbSNhWd07ZpACiOIk60Noro",
#                "width" : 1920
#             }
#          ],
#          "place_id" : "ChIJX4w3k_tIxwcRrwAPg_1lViY",
#          "plus_code" : {
#             "compound_code" : "7F6H+2M Joaquim T├ívora (Fortaleza), Fortaleza - State of Cear├í",
#             "global_code" : "69837F6H+2M"
#          },
#          "rating" : 4.1,
#          "reference" : "ChIJX4w3k_tIxwcRrwAPg_1lViY",
#          "types" : [ "school", "point_of_interest", "establishment" ],
#          "user_ratings_total" : 17
#       }
#    ],
#    "status" : "OK"
# }