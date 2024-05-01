import requests
import json
import config

import vk_api

token = config.token
version = config.version

URLS = ['mnemotec', '194465324', '1911009', 'mnemotehnika', '155325550', 'mnemonicaru', '82573315', 'mnemonics_timurio',
        'mnemocon', 'eidetikaodessa', 'skorochtenieodessa', 'mnemokurs', 'vector_rosta_ufa', '124018766', 'clubmnemonica',
        'kseniya_demeshova', 'homosuperior', '28696425', 'thebestmemory', 'mnemotechnica', '99126194',
        'smemory', 'genius_center', 'mnemo_nsk', 'trening_memory', 'mnemologovo', 'mnemonika_kz', 'mnemo_tech',
        '11700346', 'mnemonikum', '111766289', 'silaym', 'thebestmemory', '104102294', 'mnemonika1', 'mnemotechniques',
        'makushina_school', '14713718', 'rhetoric_and_mnemonics', 'english_mnemo', 'mnemoscoro', '75460421', 'frmnemo',
        'patanga', '81772733', '53778081', 'mnemo4english', 'skorochteniye', 'mipt_mnemoclub', 'ssuiq', 'iqintellect',
        '93104664', 'big_memory_lesson', 'advancemind', 'memorymanipulation', 'snz_supermozg', 'razvitiepamyati', 'brain_sc',
        'shkolaskorochteniya', 'iq007chaikovskii', 'megamozg_mm', 'scorochtenie', 'clever_akademia', 'cit74', 'razvitie_pamyati',
        'skorochtenie_kursy', 'intellectus174', 'fastread_spb', 'kmechteru', 'mnemoschool', 'flashumor', 'schoolofmemory',
        'adv_mem', 'superbrainy', '128876643', 'pamyat_skorochtenie_saratov', 'razvitie_intellekta74', 'dudin_education_2',
        'megainten', 'memorydevelopment', 'skorochtenie_izhevsk', 'pranadpua', 'mnemonikaenglish', 'i_mnemo_teach', '142598078',
        '23632217', '49870008', 'razfitie', 'ankiru', 'den_babushkin', 'mentalathlete', 'easyils', '193077360', 'slovari_club',
        '15499827', '179029096', 'easy_deutsch', 'megamozg3', '49267282', '128114003', 'uptosmart', '73464386', 'advance100slov',
        'brainhot', 'pomnuvse', 'sinxron', 'center_um_nvkz', 'dudin_education_3', 'dudin_education_4', 'dudin_education_5',
        'dudin_education_6'
        ]

URLSLOCKED = [-184635596, -54460646, -184293420, -185587893, -185053703, -32198230, -192258292,
              -181470560, -29775651, -197695107, -198405809, -198189010, -129964912, -200647938,
              -96512274, -186619220, -192188560, -21297088]


def IDs_Members(URLS, version, token):
    pdpset = set()
    for j in range(len(URLS)):
        response = requests.get('https://api.vk.com/method/groups.getMembers',
                                params={
                                    'group_id': URLS[j],
                                    'access_token': token,
                                    'v': version
                                }
                                )
        pdp = []
        data = json.loads(response.text)
        count = data['response']['count']
        offset = 0
        for i in range((count // 1000) + 1):
            response = requests.get('https://api.vk.com/method/groups.getMembers',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'group_id': URLS[j],
                                        'offset': offset
                                    }
                                    )
            data = json.loads(response.text)
            items = data['response']['items']
            pdp.extend(items)
            offset += 1000
        pdpset.update(pdp)
    pdpset = list(pdpset)
    pdpset = sorted(pdpset)
    return pdpset

def IDs_by_likes_and_comms(URLSLOCKED, version, token):
    IDs = []
    for j in range(len(URLSLOCKED)):
        response_count_posts = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'owner_id': URLSLOCKED[j],
                                    'access_token': token,
                                    'v': version
                                }
                                )
        count_posts = json.loads(response_count_posts.text)['response']['count']
        offset = 0
        pst = []
        for i in range((count_posts//100) + 1):
            response_posts = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'owner_id': URLSLOCKED[j],
                                        'access_token': token,
                                        'v': version,
                                        'count': 100,
                                        'offset': offset
                                    }
                                    )
            posts = json.loads(response_posts.text)['response']['items']
            pst.extend(posts)
            offset += 100
        IDs_posts = []
        for k in range(len(pst)):
            IDs_posts.append(pst[k]['id'])

        # на этом этапе есть список с id всех постов конкретного канала.
        # внутри этого канала, цикля все посты, циклим все лайки, добавляем id пользователей в IDs

        for y in range(len(IDs_posts)):         #перебираем посты
            response_count_likes = requests.get('https://api.vk.com/method/likes.getList',
                                                params={
                                                    'owner_id': URLSLOCKED[j],
                                                    'access_token': token,
                                                    'v': version,
                                                    'type': 'post',
                                                    'item_id': IDs_posts[y]
                                                }
                                                )
            count_likes = json.loads(response_count_likes.text)['response']['count']
            offset = 0
            for q in range((count_likes//1000) + 1):            #перебираем лайки конкретного поста
                response_likes = requests.get('https://api.vk.com/method/likes.getList',
                                                    params={
                                                        'owner_id': URLSLOCKED[j],
                                                        'access_token': token,
                                                        'v': version,
                                                        'type': 'post',
                                                        'item_id': IDs_posts[y],
                                                        'count': 1000,
                                                        'offset': offset
                                                    }
                                                    )
                likes = json.loads(response_likes.text)['response']['items']
                IDs.extend(likes)
                offset += 1000

            response_count_comms = requests.get('https://api.vk.com/method/wall.getComments',
                                          params={
                                              'owner_id': URLSLOCKED[j],
                                              'access_token': token,
                                              'v': version,
                                              'post_id': IDs_posts[y]
                                          }
                                          )
            count_comms = json.loads(response_count_comms.text)['response']['count']
            offset = 0
            commsITEMS = []
            for q in range((count_comms//100) + 1):            #перебираем комментарии конкретного поста
                response_comms = requests.get('https://api.vk.com/method/wall.getComments',
                                                    params={
                                                        'owner_id': URLSLOCKED[j],
                                                        'access_token': token,
                                                        'v': version,
                                                        'post_id': IDs_posts[y],
                                                        'count': 100,
                                                        'offset': offset
                                                    }
                                                    )
                comms = json.loads(response_comms.text)['response']['items']
                commsITEMS.extend(comms)
                offset += 100
            try:
                for w in range(len(commsITEMS)):
                    IDs.append(commsITEMS[w]['from_id'])
            except KeyError:
                pass

    IDs = sorted(list(set(IDs)))
    return IDs


list_IDs.copy(IDs_Members(URLS, version, token))
list_IDs.extend(IDs_by_likes_and_comms(URLSLOCKED, version, token))

list_IDs = sorted(list(set(list_IDs)))




