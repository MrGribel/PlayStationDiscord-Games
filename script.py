import sys, os, requests, re, json, urllib.request, urllib.error, hashlib, hmac, traceback, logging, shutil
from pytablewriter import MarkdownTableWriter

# key for tdmb link generation (from ps3, ps4)
tmdb_key = bytearray.fromhex('F5DE66D2680E255B2DF79E74F890EBF349262F618BCAE2A9ACCDEE5156CE8DF2CDF2D48C71173CDC2594465B87405D197CF1AED3B7E9671EEB56CA6753C2E6B0')

title_ids = [
    'CUSA07022_00', # Fortnite
    'CUSA05042_00', # Destiny 2
    'CUSA11100_00', # Black Ops 4
    'CUSA03522_00', # Modern Warfare Remastered
    'CUSA02290_00', # Black Ops 3
    'CUSA00803_00', # Advanced Warfare
    'CUSA08724_00', # Battlefield V
    'CUSA00110_00', # Battlefield 4
    'CUSA00900_00', # Bloodborne
    'CUSA02429_00', # Battlefield 1
    'CUSA01760_00', # Dark Souls 2 SOFTS
    'CUSA00359_00', # Until Dawn
    'CUSA05218_00', # For Honor
    'CUSA04220_00', # Sniper Elite 4
    'CUSA02344_00', # Uncharted: Nathan Drake Collection
    'CUSA03617_00', # Mafia III
    'CUSA04013_00', # Titanfall 2
    'CUSA02377_00', # Assasins Creed: Syndicate
    'CUSA03041_00', # Red Dead Redemption 2
    'CUSA10237_00', # Horizon Complete
    'CUSA02299_00', # Spider-Man
    'CUSA01163_00', # Rocket League
    'CUSA01401_00', # Borderlands Handsome Collection
    'CUSA03506_00', # GTA SA
    'CUSA07408_00', # God Of War
    'CUSA00527_00', # Witcher 3
    'CUSA00419_00', # GTA V
    'CUSA08344_00', # Detroit Become Human
    'CUSA00113_00', # NFS Rivals
    'CUSA02557_00', # Fallout 4
    'CUSA03946_00', # Dying Light Enhanced
    'CUSA02085_00', # DOOM
    'CUSA00079_00', # Injustice
    'CUSA12540_00', # Apex Legends
    'CUSA11600_00', # FIFA 19
    'CUSA07399_00', # Crash Trilogy
    'CUSA01800_00', # Rainbow Six Siege
    'CUSA00967_00', # Mortal Kombat X
    'CUSA10608_00', # Conan Exiles
    'CUSA00341_00', # Uncharted 4
    'CUSA01623_00', # God of War III Remastered
    'CUSA00552_00', # The Last Of US Remastered
    'CUSA00223_00', # Infamous Second Son
    'CUSA00496_00', # Far Cry 4
    'CUSA00625_00', # Battlefield Hardline
    'CUSA01493_00', # Just Cause 3
    'CUSA02976_00', # HITMAN
    'CUSA00325_00', # Outlast
    'CUSA06623_00', # Outlast 2
    'CUSA02337_00', # Resident Evil 0
    'CUSA00220_00', # Dragon Age Inquisiton
    'CUSA00107_00', # Tomb Raider Definitive
    'CUSA01047_00', # Ratchet & Clank
    'CUSA01799_00', # Deus Ex: Mankind Divided
    'CUSA12476_00', # NBA 2K19
    'CUSA02703_00', # Mad Max
    'CUSA01140_00', # Metal Gear Solid V
    'CUSA05794_00', # Rise of Tomb Raider
    'CUSA08966_00', # Days Gone
    'CUSA05855_00', # AC Origins
    'CUSA09311_00', # AC Odyssey
    'CUSA07671_00', # Wipeout Omega Collection
    'CUSA05347_00', # Darksiders Remastered
    'CUSA02420_00', # Darksiders 2 
    'CUSA08880_00', # Darksiders 3
    'CUSA01671_00', # Devil May Cry 4 SE
    'CUSA08216_00', # Devil May Cry 5
    'CUSA03333_00', # SOMA
    'CUSA02533_00', # Heavy Rain
    'CUSA03220_00', # GT Sport
    'CUSA07713_00', # Monster Hunter World
    'CUSA05877_00', # Persona 5
    'CUSA00191_00', # Killzone Shadow Fall
    'CUSA07113_00', # Nioh
    'CUSA00785_00', # The Order 1886
    'CUSA03507_00', # Bully
    'CUSA03508_00', # GTA III
    'CUSA03509_00', # GTA Vice City
    'CUSA11518_00', # Mortal Kombat 11
    'CUSA12047_00', # Sekiro Shadows Die Twice
    'CUSA03388_00', # Dark Souls 3
    'CUSA08155_00', # Dark Souls 3 Fire Fades
    'CUSA08692_00', # Dark Souls Remastered
    'CUSA13917_00', # Far Cry New Dawn
    'CUSA03352_00', # Far Cry Primal
    'CUSA05904_00', # Far Cry 5
    'CUSA00021_00', # Watch Dogs
    'CUSA04459_00', # Watch Dogs 2
    'CUSA00744_00', # Minecraft
    'CUSA01068_00', # Resident Evil HD   
    'CUSA04885_00', # Resident Evil 4
    'CUSA04437_00', # Resident Evil 5
    'CUSA03856_00', # Resident Evil 6
    'CUSA03962_00', # Resident Evil 7
    'CUSA02845_00', # Super Meat Bot
    'CUSA01037_00', # Surgeon Simulator
    'CUSA03979_00', # Bioshock Colleciton
    'CUSA00623_00', # Metro 2033
    'CUSA00624_00', # Metro Last Light
    'CUSA11408_00', # Metro Exodus
    'CUSA13529_00', # Subnautica
    'CUSA00203_00', # The Evil Within
    'CUSA06166_00', # The Evil Within 2
    'CUSA01940_00', # Shadows of Mordor GOTY
    'CUSA04439_00', # Shadows of War
    'CUSA01810_00', # Tom Clancy’s The Division
    'CUSA12639_00', # Tom Clancy’s The Division 2
    'CUSA02902_00', # Tom Clancy’s Ghost Recon Wildlands
    'CUSA00314_00', # Wolfenstein The New Order
    'CUSA07384_00', # Wolfenstein II: The New Colossus
    'CUSA07385_00', # Dragon's Dogma: Dark Arisen
    'CUSA05882_00', # Amnesia Collection
    'CUSA05333_00', # Skyrim
    'CUSA10938_00', # Shadow Of The Tomb Raider
    'CUSA05008_00', # Assassin Creed Ezio Collection
    'CUSA14081_00', # PUBG
    'CUSA10158_00', # AC Rogue Remastered

]

urls = [
    # Top 50 Games
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-TOPGAMES?size=200&bucket=games&start=0&gameContentType=games&platform=ps4",
    # PS+ Games
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-PSPLUSFREEGAMES?size=30&bucket=games&start=0&platform=ps4",
    # Top 50 digital only games
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-TOPPSNGAMES?size=50&bucket=games&start=0&platform=ps4",
    # 10 newest free games
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-GAMESFREETOPLAY?sort=release_date&direction=desc&size=10&bucket=games&start=0&platform=ps4",
    # Newest games this month
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-NEWTHISMONTH?game_content_type=games&size=100&bucket=games&start=0&platform=ps4",
    # Coming soon
    #"https://store.playstation.com/valkyrie-api/en/US/19/container/STORE-MSF77008-PS3PSNPREORDERS?gameContentType=games&gameType=ps4_full_games%2Cpsn_games&releaseDate=coming_soon%2Clast_30_days&platform=ps4"
]

image_dir = 'ps4'

def create_url(title_id):
    hash = hmac.new(tmdb_key, bytes(title_id, 'utf-8'), hashlib.sha1)
    return f'https://tmdb.np.dl.playstation.net/tmdb2/{title_id}_{hash.hexdigest().upper()}/{title_id}.json'


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    discord_title_ids = []

    done = {"ps4": []}
    table_writer = None

    if os.path.isfile('README.template'):
        table_writer = MarkdownTableWriter()
        table_writer.headers = ["Icon", "Title"]
        table_writer.value_matrix = []
    else:
         print('missing README.template. wont update README.md file.')

    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    for url in urls:
        print(f'--- {url} ---')
        content = requests.get(url).json()

        for item in content['included']:
            info = item['attributes']
            
            if 'thumbnail-url-base' not in info:
                continue

            if 'game' not in str(info['game-content-type']).lower():
                continue

            print(info['name'])

            rating = info['star-rating']
            if not rating['total']:
                print('\tno ratings')
                continue

            if rating['total'] < 10 or rating['score'] < 4:
                print('\tfailed rating check')
                continue

            match = re.search(r'([A-Z]{4}[0-9]{5}_00)', info['default-sku-id'])

            if not match:
                print('\tfailed regex check')
                continue
            
            title_id = match.group(1)

            if title_id not in title_ids:
                title_ids.append(title_id)
                print('\tadded to list')
            else:
                print('\talready added')

    # added all the titleIds... now get their images
    for title_id in title_ids:
        url = create_url(title_id)
        content = requests.get(url)

        if content.status_code != 200:
            print('skipping', title_id)
            continue

        content = content.json()
        
        game_name = content['names'][0]['name']
        
        print(game_name)

        if not content['icons'] or len(content['icons']) == 0:
            print('\tno icons')
            continue

        game_icon = None

        for icon in content['icons']:
            if icon['type'] == '512x512':
                game_icon = icon['icon']
                break
        
        if game_icon == None:
            print('\tno 512x512 icon')
            continue

        done["ps4"].append({
            "name": game_name,
            "titleId": title_id
        })

        discord_title_ids.append(title_id.lower())

        if not os.path.exists(image_dir):
            os.mkdir(image_dir)

        icon_file = f'{image_dir}/{title_id}.png'

        if table_writer != None:
            table_writer.value_matrix.append([
                f'<img src="{icon_file}?raw=true" width="100" height="100">',
                game_name
            ])

        if os.path.exists(icon_file):
            print('\ticon file exists')
            continue

        urllib.request.urlretrieve(game_icon, icon_file)
        
        print('\tsaved')
    
    if table_writer != None:
        with open("README.template", "rt") as template:
            with open('README.md', 'wt', encoding='utf-8') as readme:
                for line in template:
                    readme.write(line.replace('!!games!!', table_writer.dumps()))
    
    with open('games.json', 'w') as games_file:
       json.dump(done, games_file)
