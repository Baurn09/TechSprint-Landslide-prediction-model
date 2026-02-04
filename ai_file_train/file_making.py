import json
import re

raw = """[93.335972, 27.241524], { date: '06-06-2021', name: 'Leporiang Landslide' }
[95.274842, 28.122053], { date: '13-08-2021', name: 'Sirki Waterfall Landslide' }
[95.181389, 28.153611], { date: '27-06-2021', name: 'Rotlung Landslide' }
[94.748649, 28.849609], { date: '13-08-2021', name: 'Tuting Yingkiong_landslide' }
[94.721322, 27.784222], { date: '13-08-2021', name: 'Likabali Basar landslide' }
[94.842537, 28.936253], { date: '17-06-2021', name: 'Pekong Landslide' }
[94.467809, 27.965813], { date: '08-07-2021', name: 'Tode landslide' }
[93.622322, 27.095983], { date: '31-05-2021', name: 'IG Park Landslide' }
[92.43801, 27.326763], { date: '05-06-2021', name: 'BCT Road Landslide' }
[92.479767, 27.208119], { date: '25-05-2021', name: 'Nechipu_Saddle_landslide' }
[95.603611, 26.911944], { date: '22-06-2021', name: 'Kuthong Landslide' }
[95.235101, 28.214774], { date: '30-06-2021', name: 'Pasighat_Yingkiong_Landslide' }
[94.71335, 27.796145], { date: '30-06-2021', name: 'Garu Landslide' }
[92.303984, 27.186597], { date: '28-04-2021', name: 'Membachur Garbow landslide' }
[94.9963, 28.233722], { date: '27-06-2021', name: 'Sangam bridge_collapse' }
[94.073954, 27.794025], { date: '09-09-2021', name: 'Raga landslide' }
[92.566072, 27.104442], { date: '20-09-2021', name: '20 landslides BCT road' }
[91.694636, 26.162784], { date: '18-06-2021', name: 'Water works_colony_landslide' }
[93.110996, 26.574761], { date: '25-08-2021', name: 'Burapahar Landslide' }
[91.690161, 26.170251], { date: '20-10-2021', name: 'Pandu landslide' }
[91.810523, 26.154238], { date: '06-08-2021', name: 'Borabari landslide' }
[93.820138, 25.217562], { date: '06-06-2021', name: 'Tujang Waichong_landslide' }
[93.509375, 24.503658], { date: '20-08-2021', name: 'S_kholep_landslide' }
[93.677995, 25.158298], { date: '24-06-2021', name: 'Tamel landslide' }
[93.857702, 25.241119], { date: '02-08-2021', name: 'Lamlenkon landslide' }
[93.56119, 24.826041], { date: '16-08-2021', name: 'Awang khul landslide' }
[93.677995, 25.158298], { date: '07-06-2021', name: 'Tamei2 landslide' }
[94.160246, 24.319566], { date: '26-07-2021', name: 'Chahmol landslide' }
[93.440246, 24.818353], { date: '19-07-2021', name: 'Thingou landslide' }
[94.358421, 25.091769], { date: '16-06-2021', name: 'Mini Secretariat landiside' }
[93.332535, 24.767366], { date: '19-07-2021', name: 'Sibilong temple landslide' }
[93.915829, 24.005219], { date: '09-10-2021', name: 'Khulmulen-Sajik landslide' }
[91.86466, 25.585545], { date: '24-02-2021', name: 'Sonapani landslide' }
[90.214668, 25.499358], { date: '30-06-2021', name: 'Tura dalu stretch' }
[92.362063, 25.081742], { date: '02-08-2021', name: 'Kuliang landslide' }
[90.831915, 25.202693], { date: '30-06-2021', name: 'Malikona_Village_landslide' }
[92.761693, 22.130154], { date: '26-08-2021', name: 'Zochachhuah landslide' }
[92.816565, 22.805047], { date: '19-07-2021', name: 'Bualtei landslide' }
[92.741738, 23.74192], { date: '11-06-2021', name: 'Thuampui landslide' }
[92.859428, 23.689863], { date: '09-10-2021', name: 'Thingsulthliah landslide' }
[93.805655, 25.793499], { date: '02-02-2021', name: 'TL Park landslide' }
[94.254627, 26.092899], { date: '06-08-2021', name: 'Lower Etsuchuka Colony landslide' }
[93.806, 25.772599], { date: '17-02-2021', name: 'TL Park 2 landslide' }
[94.767115, 26.046657], { date: '20-07-2021', name: 'Wangshu_PwD Road_landslide' }
[94.438812, 25.657788], { date: '12-07-2021', name: 'Losami Phek landslide' }
[94.254289, 26.096249], { date: '06-08-2021', name: 'Police Point landslide' }
[94.246956, 26.091211], { date: '06-08-2021', name: 'Airfield colony landslide' }
[94.221938, 26.208542], { date: '05-08-2021', name: 'Sanis Doyarig_landslide' }
[93.940678, 25.766187], { date: '10-05-2021', name: 'Piphema landslide' }
[94.863047, 25.7623], { date: '17-08-2021', name: 'Pungro-Mimi landslide' }
[94.686755, 25.603106], { date: '14-07-2021', name: 'Phek landslide' }
[94.409427, 25.659725], { date: '31-07-2021', name: 'Pfutsero-Khomi-Phek landslide' }
[94.402948, 25.723469], { date: '31-07-2021', name: 'Pfutsero-Lanye Landslide' }
[95.061502, 26.250081], { date: '08-11-2021', name: 'Wensoi Landslide' }
[94.939423, 26.232589], { date: '09-09-2021', name: 'Chedang Saddle Landslide' }
[88.614992, 27.250224], { date: '24-08-2021', name: 'Samsing Shanti Turn Landslide' }
[88.152087, 27.1624], { date: '24-08-2021', name: 'Muneew Tareybhir Landslide' }
[88.45744, 27.090965], { date: '29-07-2021', name: 'Melli Secondary School Landslide' }
[88.456816, 27.090724], { date: '30-07-2021', name: 'Melli Bazaar Landslide' }
[88.531935, 27.142902], { date: '30-07-2021', name: 'Mamkhola Landslide' }
[88.466754, 27.10871], { date: '30-07-2021', name: 'Melli 2 Landslide' }
[88.325929, 27.111336], { date: '30-07-2021', name: 'Melli Jorethang_landslide' }
[88.609439, 27.32459], { date: '20-10-2021', name: 'Pani House Landslide' }
[88.464695, 27.09117], { date: '18-06-2021', name: 'Bhalukhola landslide' }
[88.728341, 27.376583], { date: '25-03-2021', name: 'Kyonsola waterfall landslide' }
[88.597286, 27.255462], { date: '08-08-2021', name: 'Basilakha landslide' }
[88.487805, 27.366542], { date: '31-07-2021', name: 'Seley Ward landslide' }
[88.441413, 26.939387], { date: '31-07-2021', name: 'Seti Jhora Landslide' }
[88.280411, 27.146369], { date: '30-07-2021', name: 'Sisney Landslide' }
[88.307456, 27.221268], { date: '27-08-2021', name: 'Jorethang-Legship Landslide' }
[88.61023, 27.326815], { date: '01-06-2021', name: 'Seesa Golai Landslide' }
[88.608275, 27.343272], { date: '09-06-2021', name: 'Tashi Namgyal Secondary School Landslide' }
[88.158235, 27.276428], { date: '29-08-2021', name: 'Bongten-Changay Landslide' }
[91.480725, 23.2463], { date: '26-08-2021', name: 'Sarsima Landiside' }
[91.494288, 23.228158], { date: '26-08-2021', name: 'Jharjhari landslide' }
[92.3835, 25.300713], { date: '2022-04-13', name: 'Byndihati-Umtyra_Road_Creep' }
[92.386284, 25.299032], { date: '2022-04-13', name: 'Byndihati-Umtyra_1' } 
[92.38648, 25.298933], { date: '2022-04-13', name: 'Byndihati-Umtyra_2' } 
[92.386894, 25.29857], { date: '2022-04-13', name: 'Byndihati-Umtyra_3' } 
[92.386955, 25.29842], { date: '2022-04-13', name: 'Byndihati-Umtyra_4' } 
[92.386986, 25.298416], { date: '2022-04-13', name: 'Byndihati-Umtyra_5' } 
[92.386986, 25.298306], { date: '2022-04-13', name: 'Byndihati-Umtyra_6' } 
[92.38725, 25.297895], { date: '2022-04-13', name: 'Byndihati-Umtyra_7' } 
[92.38736, 25.297684], { date: '2022-04-13', name: 'Byndihati-Umtyra_8' } 
[92.38735, 25.297401], { date: '2022-04-13', name: 'Byndihati-Umtyra_9' } 
[92.38551, 25.259485], { date: '2022-04-13', name: 'Nongsning_12' } 
[92.3757, 25.242348], { date: '2022-04-13', name: 'Shiehruphi_1' } 
[92.37896, 25.220339], { date: '2022-04-13', name: 'Thangskai_1' } 
[92.36781, 25.150444], { date: '2022-04-13', name: 'Umlaper_tea_stall_1' } 
[92.37676, 25.147703], { date: '2022-04-13', name: 'Tongseng1' } 
[92.373055, 25.143984], { date: '2022-04-13', name: 'Tongseng2' } 
[92.37366, 25.1438], { date: '2022-04-13', name: 'Tongseng3' } 
[92.37443, 25.144033], { date: '2022-04-13', name: 'Tongseng4' } 
[92.379005, 25.14076], { date: '2022-04-13', name: 'HP_petrol_pump_tongseng_1' } 
[92.37903, 25.140772], { date: '2022-04-13', name: 'HP_petrol_pump_tongseng_2' } 
[92.37898, 25.140808], { date: '2022-04-13', name: 'HP_petrol_pump_tongseng_3' } 
[92.388245, 25.129538], { date: '2022-04-13', name: '3km_before_sonapur_1' } 
[92.38578, 25.12547], { date: '2022-04-13', name: 'Before_Sonapur2' } 
[92.37368, 25.113762], { date: '2022-04-13', name: 'Before_Sonapur3' } 
[92.410835, 25.045042], { date: '2022-04-13', name: 'Donsakul 1' } 
[92.43025, 25.044744], { date: '2022-04-13', name: 'Ratacherra 1' } 
[90.060165, 25.389677], { date: '2022-06-09', name: 'Jebalgre_landslide' } 
[89.951546, 25.507116], { date: '2022-06-09', name: 'Betasingh_landslide' } 
[92.37444, 25.18166], { date: '2020-06-16', name: 'Lumshnong_landslide' } 
[91.57084, 25.44632], { date: '2022-06-16', name: 'Laitlarem landslide' } 
[92.02121, 25.206291], { date: '2022-06-17', name: 'Darrang_landslide' } 
[90.03326, 25.459652], { date: '2022-06-17', name: 'Bolsalgre_landslide' } 
[90.68374, 25.351841], { date: '2022-06-17', name: 'Siju_landslide' } 
[93.6878, 27.112083], { date: '2022-06-19', name: 'Sood_landslide' } 
[93.62141, 27.095318], { date: '2022-05-16', name: 'Punjabi_dhabha_landslide' } 
[93.61592, 27.079184], { date: '2022-05-16', name: 'Ganga_Jully_basti_road' } 
[93.650566, 27.107346], { date: '2022-06-19', name: 'Modirijo landslide' } 
[93.27676, 27.856197], { date: '2022-04-19', name: 'Sulung_tapin_landslide' } 
[93.6709, 24.80265], { date: '2022-06-30', name: 'Tupul_yard_landslide' } 
[92.84086, 22.690073], { date: '2022-06-19', name: 'Tawipui_road' } 
[88.695972, 27.830094], { date: '2022-08-31', name: 'Poom_landslide' } 
[88.395556, 27.296944], { date: '2022-11-04', name: 'Yangang Landslide' }
[95.7776,28.2333]), {date:'2023-02-24', name:'Roing Anini'}
[94.86047758,28.78213823]), {date:'2023-03-24', name:'Tuting Landslide'}
[94.77570872,28.79895656]), {date:'2023-05-05', name:'Mossing Landslide'}
[93.43502779,27.89451833]), {date:'2023-05-06', name:'Kurung 1'}
[93.42410335,27.8964705]), {date:'2023-05-06', name:'Kurung 2'}
[92.610166,27.026924]), {date:'2023-06-12', name:'Tippi Landslide'}
[93.828636,27.095932]), {date:'2023-06-23', name:'Karsingsa Landslide'}
[93.671454,27.101535]), {date:'2023-06-23', name:'Puroik Landslide'}
[92.525162,27.10699]), {date:'2023-06-23', name:'Sessa Landslide'}
[94.930641,28.233721]), {date:'2023-06-23', name:'Pangin Landslide'}
[95.282822,28.095267]), {date:'2023-07-16', name:'Pangin Landslide'}
[94.144356,28.235584]), {date:'2023-07-28', name:'Taliha Landslide'}
[95.269295,28.14251]), {date:'2023-07-28', name:'NH 13, Pangin Landslide'}
[94.697075,27.717104]), {date:'2023-08-18', name:'Siji Landslide'}
[92.547048,27.204944]), {date:'2023-08-27', name:'Nag Mandir Landslide'}
[92.38797,27.203191]), {date:'2023-08-27', name:'Rupa Landslide'}
[92.136539,27.057521]), {date:'2023-08-27', name:'Dengzi Landslide'}
[92.218027,27.09638]), {date:'2023-08-27', name:'Tenzin Landslide'}
[94.258982,27.552115]), {date:'2023-10-27', name:'Subansiri Landslide'}
[93.76566,25.529813]), {date:'2023-07-10', name:'Iron Bridge Landslide'}
[94.85535,25.994082]), {date:'2023-07-16', name:'Kiphire Landslide'}
[94.047805,25.709988]), {date:'2023-07-17', name:'Meriema Landslide'}
[94.784753,25.876143]), {date:'2023-08-09', name:'Kiphire Town Landslide'}
[94.906812,25.708869]), {date:'2023-08-25', name:'Mimi Landslide'}
[94.51346,26.653847]), {date:'2023-08-27', name:'Noklangsangba Landslide'}
[93.797729,25.798326]), {date:'2023-07-04', name:'Pakala Pahar Landslide'}
[95.080945,26.106224]), {date:'2023-07-09', name:'Choklangan Landslide'}
[95.020282,26.197297]), {date:'2023-07-09', name:'Wonthai Landslide'}
[95.015413,26.199008]), {date:'2023-07-09', name:'Ehoukeh King Landslide'}
[93.204533,23.491709]), {date:'2023-01-26', name:'Hermon Veng Landslide'}
[92.714248,23.745055]), {date:'2023-06-16', name:'Hunthar Landslide'}
[92.71425,23.74506]), {date:'2023-07-04', name:'Hunthar Landslide'}
[92.708782,23.742421]), {date:'2023-07-27', name:'Vaivakawn Landslide'}
[92.889308,22.518533]), {date:'2023-08-08', name:'Lawngtlai Landslide'}
[92.760969,22.880829]), {date:'2023-08-08', name:'Lunglei Landslide'}
[92.713846,23.745833]), {date:'2023-08-09', name:'Hunthar Landslide'}
[92.91265,23.233976]), {date:'2023-09-11', name:'Keitum Landslide'}
[91.876558,25.371447]), {date:'2023-04-14', name:'Rngain Landslide'}
[90.202987,25.515019]), {date:'2023-05-06', name:'Tura Civil Hospital Landslide'}
[92.36018,25.105844]), {date:'2023-05-27', name:'Sonapur Tunnel Landslide'}
[92.360242,25.105931]), {date:'2023-04-05', name:'Sonapur Tunnel Landslide'}
[92.360245,25.105937]), {date:'2023-06-10', name:'Sonapur Tunnel Landslide'}
[92.360255,25.10594]), {date:'2023-06-14', name:'Sonapur Tunnel Landslide'}
[91.902608,25.309601]), {date:'2023-06-11', name:'Pynursla Landslide'}
[92.360259,25.105945]), {date:'2023-06-15', name:'Sonapur Tunnel Landslide'}
[91.876551,25.371452]), {date:'2023-06-14', name:'Rngain Landslide'}
[91.366042,25.275153]), {date:'2023-06-17', name:'Dommawlein Landslide'}
[91.57097,25.446165]), {date:'2023-06-17', name:'Laitlarem Landslide'}
[92.020892,25.205927]), {date:'2023-06-17', name:'Darrang Landslide'}
[92.3603,25.10595]), {date:'2023-06-19', name:'Sonapur Tunnel Landslide'}
[90.181776,25.521879]), {date:'2023-06-22', name:'PA Sangma Stadium Landslide'}
[91.948666,25.687251]), {date:'2023-06-22', name:'Umiam View Point Landslide'}
[92.361278,25.105701]), {date:'2023-06-23', name:'Sonapur Tunnel Landslide'}
[92.36114,25.106073]), {date:'2023-07-03', name:'Sonapur Tunnel Landslide'}
[92.360407,25.106083]), {date:'2023-08-04', name:'Sonapur Tunnel Landslide'}
[92.36123,25.106699]), {date:'2023-08-10', name:'Sonapur Tunnel Landslide'}
[92.360287,25.105957]), {date:'2023-08-26', name:'Sonapur Tunnel Landslide'}
[91.615265,25.88385]), {date:'2023-09-26', name:'Patharkhmah Landslide'}
[92.180176,25.390614]), {date:'2023-10-08', name:'Pynthorlangtein Landslide'}
[93.550414,24.820487]), {date:'2023-08-16', name:'Awangkhul Landslide'}
[93.477731,24.826582]), {date:'2023-08-16', name:'Khongsang Landslide'}
[93.55041,24.820481]), {date:'2023-08-20', name:'Awangkhul Landslide'}
[94.25992713,27.55468158]), {date:'2023-04-03', name:'Subansiri Lower Hydroelectric Project'}
[91.719487,26.123803]), {date:'2023-06-17', name:'Dhirenpara Landslide'}
[91.43331,25.894901]), {date:'2023-06-29', name:'Joramhuria-Khokhapara Road Landslide'}
[93.038339,24.795353]), {date:'2023-08-21', name:'Lalpani Landslide'}
[91.76544,26.19676]), {date:'2023-10-06', name:'Kharguli Landslide'}
[91.793724,26.187105]), {date:'2023-10-06', name:'Bamunimaidam Landslide'}
[91.798065,26.152334]), {date:'2023-10-07', name:'Lechubagan Landslide'}
[91.75701,26.141897]), {date:'2023-10-07', name:'Kahilipara Landslide'}
[88.52320007,27.39235464]), {date:'2023-03-26', name:'Sokpay Landslide'}
[88.657305,27.613235]), {date:'2023-05-19', name:'Chungthang Landslide'}
[88.64646,27.603889]), {date:'2023-06-16', name:'Chungthang 2 Landslide'}
[88.250366,27.26933]), {date:'2023-06-18', name:'Kalej Khola Landslide'}
[88.136778,27.254354]), {date:'2023-06-18', name:'Dentam Landslide'}
[88.103311,27.142583]), {date:'2023-06-18', name:'Lower Okhrey Landslide'}
[88.500328,27.535576]), {date:'2023-07-12', name:'Lingzya Busty Landslide'}
[88.390868,27.299226]), {date:'2023-07-14', name:'Rafung Khola Landslide'}
[88.728199,27.378152]), {date:'2023-07-14', name:'9th Mile Landslide'}
[88.649425,27.565792]), {date:'2023-07-14', name:'Theng Landslide'}
[88.55059,27.259994]), {date:'2023-08-04', name:'32 No. Landslide'}
[88.550684,27.259936]), {date:'2023-08-24',name:'32 No. Landslide'}
[88.08848,27.278215]), {date:'2023-08-25', name:'Lingzing Landslide'}
[88.18362,27.912811]), {date:'2023-10-04', name:'Lhonak Landslide'}
[91.62872,23.837263]), {date:'2023-03-31', name:'Teliamura Landslide'}
[95.777581,28.233285], {date:'2024-04-24', name:'Hunli-Anini'}
[93.542196,27.78598], {date:'2024-05-16', name:'Pach Nallah'}
[94.910333,28.748529], {date:'2024-06-15', name:'Bomdo'}
[93.783419,27.121869], {date:'2024-06-18', name:'Karsingsa'}
[93.62708,27.099654], {date:'2024-06-23', name:'Itanagar'}
[95.746747,27.141177], {date:'2024-06-16', name:'Rangfra'}
[92.605617,27.03649], {date:'2024-06-26', name:'Tippi'}
[94.711676,27.923784], {date:'2024-06-25', name:'Siji'}
[94.883203,28.226541], {date:'2024-06-29', name:'Tarak'}
[93.6327,27.07383], {date:'2024-06-29', name:'Jullang'}
[94.361341,28.519848], {date:'2024-06-29', name:'Tatu'}
[96.374843,27.886843], {date:'2024-06-29', name:'Demwe'}
[96.565515,28.06798], {date:'2024-06-29', name:'Hayuliang'}
[92.958741,27.30978], {date:'2024-06-30', name:'Bana'}
[94.964479,28.676866], {date:'2024-06-30', name:'Jengging'}
[95.092954,28.142213], {date:'2024-06-29', name:'Babuk'}
[93.605705,27.090926], {date:'2024-07-01', name:'DivisionIV'}
[93.430041,27.895164], {date:'2024-06-30', name:'Rengchi'}
[93.591888,27.089317], {date:'2024-07-01', name:'Baat'}
[94.98636,28.233305], {date:'2024-07-04', name:'Pangin'}
[95.093074,28.142494], {date:'2024-07-06', name:'Babuk2'}
[93.783633,27.121839], {date:'2024-07-05', name:'Karsingsa'}
[94.316142,28.697524], {date:'2024-07-05', name:'ShiYomi'}
[96.439961,28.047143], {date:'2024-07-05', name:'Mompani'}
[93.636163,27.72775], {date:'2024-07-05', name:'Palin'}
[92.792901,27.307091], {date:'2024-07-14', name:'Palizi'}
[93.621829,27.031002], {date:'2024-07-22', name:'Holongi'}
[91.857654,27.611051], {date:'2024-09-07', name:'Bramadungchung'}
[92.562963,27.203922], {date:'2024-10-04', name:'Kaspi'}
[92.891914,25.109872], {date:'2024-05-01', name:'Jatinga'}
[92.76249,25.019471], {date:'2024-05-03', name:'Damcherra'}
[95.738226,27.282038], {date:'2024-05-26', name:'Tikok'}
[94.263033,27.532524], {date:'2024-05-27', name:'Subansiri'}
[91.747639,26.144954], {date:'2024-05-29', name:'KrishnaNagar'}
[91.71827,26.125215], {date:'2024-06-03', name:'Katahbari'}
[91.698208,26.160366], {date:'2024-06-03', name:'GramyaNagar'}
[93.116465,25.179895], {date:'2024-05-30', name:'Mahur'}
[93.01028,25.202045], {date:'2024-05-30', name:'Lungkhok'}
[93.020431,25.1934], {date:'2024-05-30', name:'Bethel'}
[91.775725,26.190964], {date:'2024-05-30', name:'RudraNagar'}
[92.523786,24.787043], {date:'2024-06-19', name:'Bendargool'}
[91.846223,26.111529], {date:'2024-07-04', name:'8thMile'}
[91.829241,26.179508], {date:'2024-07-12', name:'Bonda'}
[92.747317,25.006926], {date:'2024-08-10', name:'Damchera2'}
[94.27133,24.67507], {date:'2024-05-27', name:'Kasom'}
[93.7777,24.78167], {date:'2024-05-28', name:'Imphal'}
[93.97409,25.26763], {date:'2024-05-28', name:'Senapati'}
[94.21625,24.95445], {date:'2024-07-02', name:'MongkotChepu'}
[94.34178,25.06391], {date:'2024-07-03', name:'Kazipphung'}
[93.96529,25.13191], {date:'2024-07-04', name:'Kangpokpi'}
[93.49901,24.98131], {date:'2024-07-29', name:'Dimthanlong'}
[93.79057,24.7764], {date:'2024-07-29', name:'Sinam'}
[93.43601,24.76632], {date:'2024-07-29', name:'Rengpang'}
[93.46316,24.75121], {date:'2024-07-29', name:'Taodaijang'}
[93.83401,24.53455], {date:'2024-08-01', name:'Thanga1'}
[93.81729,24.52563], {date:'2024-08-01', name:'Thanga2'}
[93.81477,24.5226], {date:'2024-08-01', name:'ThangaNgaram'}
[93.919,24.73502], {date:'2024-08-01', name:'Oinam'}
[93.82001,24.52711], {date:'2024-08-01', name:'Heisnam'}
[93.13879,24.75096], {date:'2024-08-06', name:'Jiribam'}
[93.42788,24.75648], {date:'2024-08-07', name:'Nungba'}
[93.26164,24.72047], {date:'2024-08-07', name:'Kaimai'}
[94.35854,25.092], {date:'2024-08-12', name:'Hamleikhong'}
[93.73187,24.78893], {date:'2024-08-18', name:'KSinam2'}
[93.55647,24.81961], {date:'2024-08-18', name:'Awangkhul'}
[93.5706,24.83803], {date:'2024-10-01', name:'AwangkhulRangkhung'}
[92.36018,25.105844], {date:'2024-02-03', name:'SonapurTunnel1'}
[92.358006,25.102667], {date:'2024-04-30', name:'SonapurTunnel2'}
[91.856166,25.569287], {date:'2024-05-16', name:'ThirdMile'}
[91.856614,25.568237], {date:'2024-05-16', name:'Borma'}
[91.873806,25.568556], {date:'2024-05-17', name:'ShillongAssembly'}
[92.360977,25.106205], {date:'2024-05-27', name:'SonapurTunnel3'}
[91.614595,25.363389], {date:'2024-05-28', name:'Weilong'}
[91.893134,25.62836], {date:'2024-05-28', name:'Mawlai'}
[91.902597,25.625808], {date:'2024-05-28', name:'Mawkynroh'}
[91.751767,25.453314], {date:'2024-05-28', name:'Mawphland'}
[91.871489,25.567062], {date:'2024-05-28', name:'Rilbong'}
[91.881821,25.560962], {date:'2024-05-28', name:'Lumparing'}
[91.3896869,25.39192932], {date:'2024-05-28', name:'13KM'}
[91.748951,25.271534], {date:'2024-05-30', name:'Nongpriang'}
[92.368435,25.15457], {date:'2024-05-30', name:'Lumshnong1'}
[92.38607,25.162582], {date:'2024-06-15', name:'Lumshnong2'}
[91.866635,25.568354], {date:'2024-06-15', name:'Lummawbah'}
[91.433141,25.52819], {date:'2024-06-17', name:'Markasa'}
[91.874287,25.82781], {date:'2024-06-14', name:'RiPalei'}
[91.875187,25.800588], {date:'2024-06-14', name:'Umsamlem'}
[91.899853,25.679203], {date:'2024-06-14', name:'Umiam1'}
[91.466408,25.368971], {date:'2024-06-15', name:'Mawkyrwat'}
[91.236212,25.225818], {date:'2024-06-15', name:'Ranikor'}
[91.828582,25.518951], {date:'2024-06-19', name:'Pomlum'}
[92.220332,25.152774], {date:'2024-06-17', name:'Karkhana'}
[91.700373,25.510164], {date:'2024-06-28', name:'Sohiong'}
[91.903928,25.669593], {date:'2024-06-30', name:'Umiam2'}
[91.898077,25.653138], {date:'2024-07-01', name:'UmiamDam'}
[91.900697,25.682492], {date:'2024-06-30', name:'Umbang1'}
[91.897497,25.676048], {date:'2024-06-30', name:'NEPA'}
[91.898378,25.675099], {date:'2024-06-30', name:'Umiam3'}
[91.902376,25.686237], {date:'2024-06-30', name:'Umbang2'}
[91.903145,25.686801], {date:'2024-06-30', name:'Umbang3'}
[91.906341,25.692127], {date:'2024-06-30', name:'Sumer'}
[91.899541,25.67939], {date:'2024-06-30', name:'Umbang4'}
[91.271797,25.529008], {date:'2024-07-02', name:'Tiehsaw'}
[91.514339,25.466183], {date:'2024-07-02', name:'Pariong'}
[90.647418,25.193381], {date:'2024-07-04', name:'Baghmara1'}
[90.633676,25.210055], {date:'2024-07-04', name:'Baghmara2'}
[91.898983,25.649229], {date:'2024-07-02', name:'Umiam4'}
[91.898692,25.650726], {date:'2024-07-02', name:'Umiam5'}
[91.893994,25.651025], {date:'2024-07-02', name:'UmiamView'}
[91.889399,25.641388], {date:'2024-07-02', name:'Mawlai2'}
[91.889427,25.640973], {date:'2024-07-02', name:'Mawlai3'}
[92.362414,25.08048], {date:'2024-07-12', name:'Kuliang1'}
[90.193856,25.724652], {date:'2024-07-13', name:'Dadenggre'}
[91.875303,25.809077], {date:'2024-07-14', name:'Pahamrinai'}
[91.874717,25.781194], {date:'2024-07-06', name:'Umran'}
[91.869058,26.029622], {date:'2024-07-18', name:'Maupur'}
[92.362358,25.080525], {date:'2024-08-06', name:'Kuliang2'}
[92.361029,25.106369], {date:'2024-08-06', name:'SonapurTunnel4'}
[92.362247,25.080525], {date:'2024-08-12', name:'Kuliang3'}
[92.362123,25.080525], {date:'2024-08-17', name:'Kuliang4'}
[91.865183,25.951567], {date:'2024-09-06', name:'Shangbangla'}
[92.362183,25.080516], {date:'2024-09-30', name:'Kuliang5'}
[90.237665,25.267236], {date:'2024-10-04', name:'Koinadubi'}
[90.424197,25.236002], {date:'2024-10-05', name:'Attesia'}
[90.257292,25.599743], {date:'2024-06-15', name:'Rongram'}
[90.420247,25.556716], {date:'2024-06-15', name:'Mangrure1'}
[90.420122,25.556503], {date:'2024-06-15', name:'Mangrure2'}
[90.420051,25.556389], {date:'2024-06-15', name:'Mangrure3'}
[90.412596,25.549989], {date:'2024-06-15', name:'Simsang1'}
[90.412686,25.55002], {date:'2024-06-15', name:'Simsang2'}
[90.408643,25.549016], {date:'2024-06-15', name:'Simsang3'}
[90.385679,25.547884], {date:'2024-06-15', name:'Durakalakgre'}
[90.351459,25.561542], {date:'2024-06-15', name:'Matchurigre1'}
[90.351379,25.561887], {date:'2024-06-15', name:'Matchurigre2'}
[90.351379,25.561884], {date:'2024-06-15', name:'Matchurigre3'}
[90.349382,25.561705], {date:'2024-06-15', name:'Matchurigre4'}
[90.341414,25.557146], {date:'2024-06-15', name:'Matchurigre5'}
[90.341198,25.55621], {date:'2024-06-15', name:'Matchurigre6'}
[90.340616,25.555088], {date:'2024-06-15', name:'Matchurigre7'}
[90.236012,25.556378], {date:'2024-06-15', name:'Chasingre'}
[90.230769,25.545538], {date:'2024-06-15', name:'Rongkon'}
[90.204561,25.308286], {date:'2024-06-15', name:'Rengsipara1'}
[90.204644,25.308134], {date:'2024-06-15', name:'Rengsipara2'}
[90.220672,25.496547], {date:'2024-06-15', name:'Bolpuchring1'}
[90.221742,25.496702], {date:'2024-06-15', name:'Bolpuchring2'}
[90.222287,25.496123], {date:'2024-06-15', name:'Bolpuchring3'}
[90.223143,25.47651], {date:'2024-06-15', name:'Derengre'}
[90.220833,25.470969], {date:'2024-06-15', name:'Dinasagre1'}
[90.220708,25.469956], {date:'2024-06-15', name:'Dinasagre2'}
[90.223057,25.399736], {date:'2024-06-15', name:'Rongbretgre1'}
[90.226635,25.396902], {date:'2024-06-15', name:'Rongbretgre2'}
[90.22618,25.395992], {date:'2024-06-15', name:'Rongbretgre3'}
[90.225665,25.39366], {date:'2024-06-15', name:'Rongbretgre4'}
[90.222252,25.355696], {date:'2024-06-15', name:'Santogre1'}
[90.222034,25.355738], {date:'2024-06-15', name:'Santogre2'}
[90.203781,25.338717], {date:'2024-06-15', name:'Kherapara1'}
[90.205449,25.324709], {date:'2024-06-15', name:'Kherapara2'}
[90.205134,25.324395], {date:'2024-06-15', name:'Kherapara3'}
[90.205068,25.324305], {date:'2024-06-15', name:'Kherapara4'}
[90.200065,25.314873], {date:'2024-06-15', name:'Dopogre1'}
[90.200072,25.314952], {date:'2024-06-15', name:'Dopogre2'}
[92.71768,23.68059], {date:'2024-05-28', name:'Hlimen'}
[92.71425,23.74506], {date:'2024-05-28', name:'Hunthar'}
[92.7266,23.71769], {date:'2024-05-28', name:'Salem'}
[92.72635,23.62224], {date:'2024-05-28', name:'Falkawn'}
[92.68159,23.45122], {date:'2024-05-28', name:'Lungsei'}
[92.70656,23.55912], {date:'2024-05-28', name:'Aibawk'}
[92.27094,23.75095], {date:'2024-06-11', name:'Khantlang'}
[92.73935,23.75524], {date:'2024-07-02', name:'Zuangtui'}
[92.72946,23.75565], {date:'2024-07-02', name:'Bawngkawn'}
[92.7463,23.73397], {date:'2024-07-02', name:'Zemabawk'}
[92.73362,23.76229], {date:'2024-07-02', name:'Durtlang'}
[92.64393,23.99435], {date:'2024-08-28', name:'Kawnpui'}
[94.521634,26.006772], {date:'2024-07-01', name:'ZunhebotoDIET'}
[94.841673,26.185832], {date:'2024-07-03', name:'KWongthu'}
[94.746775,26.090935], {date:'2024-07-05', name:'Chessore'}
[94.12725,25.607096], {date:'2024-07-12', name:'SecaKhel'}
[94.531077,26.015899], {date:'2024-07-07', name:'Alahuto'}
[94.255575,26.107402], {date:'2024-07-15', name:'Wokha'}
[94.25861,26.09928], {date:'2024-07-22', name:'Tchuyiro'}
[94.246652,26.2956], {date:'2024-07-22', name:'Lakhuti'}
[94.103026,25.680683], {date:'2024-07-26', name:'Pezielietsie'}
[94.18373,25.671317], {date:'2024-08-04', name:'Dzuu'}
[94.930126,25.699199], {date:'2024-08-12', name:'Lophukhong'}
[94.034266,25.724445], {date:'2024-08-14', name:'Zubza'}
[94.04216,25.670326], {date:'2024-08-23', name:'Khonoma'}
[94.254992,26.098734], {date:'2024-08-26', name:'Etsuchuka'}
[94.537726,26.249363], {date:'2024-08-29', name:'Longsa'}
[94.586325,26.302047], {date:'2024-08-26', name:'Mokokchung'}
[93.913722,25.773953], {date:'2024-09-03', name:'Pherima'}
[94.068528,25.710966], {date:'2024-09-09', name:'KMCDump1'}
[94.068536,25.710898], {date:'2024-10-04', name:'KMCDump2'}
[88.61161,27.24534], {date:'2024-05-17', name:'PakyongDC'}
[88.67311,27.62714], {date:'2024-06-01', name:'Matim'}
[88.61639,27.37194], {date:'2024-06-01', name:'Tashi'}
[88.41938,27.29403], {date:'2024-06-10', name:'Majua'}
[88.53445,27.50028], {date:'2024-06-13', name:'Mangan1'}
[88.50579,27.23553], {date:'2024-06-11', name:'Shantinagar'}
[88.60993,27.32167], {date:'2024-06-11', name:'PaniHouse'}
[88.54756,27.86372], {date:'2024-06-11', name:'Zeema'}
[88.55658,27.50669], {date:'2024-06-13', name:'Pakshep'}
[88.52691,27.5086], {date:'2024-06-13', name:'Sangkalang'}
[88.60395,27.32468], {date:'2024-06-28', name:'Lingding'}
[88.32418,27.35164], {date:'2024-07-12', name:'Makha'}
[88.5491,27.82149], {date:'2024-07-21', name:'MunsiThang'}
[88.65081,27.56807], {date:'2024-07-22', name:'Toong'}
[88.45966,27.25169], {date:'2024-08-20', name:'Balutar'}
[88.59367,27.23968], {date:'2024-08-29', name:'PakyongAirport'}
[88.52716,27.47775], {date:'2024-09-30', name:'RangRang'}
[88.49725,27.37807], {date:'2024-09-30', name:'LowerTintek'}
[88.09037,27.17605], {date:'2024-09-30', name:'RibdiBhareng'}
[91.705846,23.878866], {date:'2024-06-15', name:'Mungiakami'}
[91.516866,23.167876], {date:'2024-08-19', name:'Debipur'}
[91.634953,23.839927], {date:'2024-08-19', name:'Teliamura'}
[91.908101,24.109649], {date:'2024-08-19', name:'Saikar'}
[91.524158,23.312969], {date:'2024-08-22', name:'Gardang'}
[91.755621,23.423169], {date:'2024-08-22', name:'NutanBazar'}
[25.67923, 91.89988], { date: '30-05-2025', name: 'Umiam Landslide 7' }
[25.68672, 91.9034],  { date: '30-05-2025', name: 'Umbang Landslide' }
[25.68624, 91.90282], { date: '30-05-2025', name: 'Umbang Landslide 2' }
[25.69024, 91.90534], { date: '30-05-2025', name: 'Sumer Landslide 1' }
[25.75852, 91.87999], { date: '30-05-2025', name: 'Umsamlem Landslide' }
[25.82308, 91.87242], { date: '30-05-2025', name: 'Kwinain Landslide' }
[25.81488, 91.87571], { date: '30-05-2025', name: 'Umnget Landslide' }
[25.92683, 91.87521], { date: '30-05-2025', name: 'Umling Landslide' }
[25.92723, 91.87506], { date: '30-05-2025', name: 'Umling Landslide 2' }
[25.95857, 91.86467], { date: '30-05-2025', name: 'Umling Landslide 3' }
[25.9571,  91.86125], { date: '30-05-2025', name: 'Umling Landslide 4' }
[26.01556, 91.86894], { date: '30-05-2025', name: 'Byrnihat Landslide' }
[26.0169,  91.86662], { date: '30-05-2025', name: 'Byrnihat Landslide 2' }
[26.02992, 91.86895], { date: '30-05-2025', name: '17 Mile Landslide' }
[26.03532, 91.86799], { date: '30-05-2025', name: 'Byrnihat Landslide 3' }
[26.03628, 91.86832], { date: '30-05-2025', name: 'Byrnihat Landslide 4' }
[26.08904, 91.87737], { date: '30-05-2025', name: 'Ampher Landslide' }
[26.09923, 91.87597], { date: '30-05-2025', name: 'Jorabat Landslide' }
[25.70906, 91.89498], { date: '30-05-2025', name: 'Umsning Landslide' }
[25.70907, 91.895],   { date: '30-05-2025', name: 'Umsning Landslide 2' }
[25.6792,  91.89967], { date: '30-05-2025', name: 'Umiam Landslide 8' }
[25.67051, 91.90494], { date: '30-05-2025', name: 'Umiam Landslide 9' }
[25.66272, 91.90127], { date: '30-05-2025', name: 'Umiam Landslide 10' }
[25.66073, 91.9014],  { date: '30-05-2025', name: 'Umiam Landslide 11' }
[25.65293, 91.89804], { date: '30-05-2025', name: 'Umiam Landslide 12' }
[25.62575, 91.89703], { date: '30-05-2025', name: 'ISBT Bypass Landslide 1' }
[25.6248,  91.91046], { date: '30-05-2025', name: 'ISBT Bypass Landslide 2' }
[25.62053, 91.90989], { date: '30-05-2025', name: 'ISBT Bypass Landslide 3' }
[25.49086, 91.82135], { date: '30-05-2025', name: 'Mylliem Landslide 2' }
[25.48787, 91.81959], { date: '30-05-2025', name: 'Mylliem Landslide 3' }
[25.48715, 91.81948], { date: '30-05-2025', name: 'Mylliem Landslide 4' }
[25.4868,  91.81987], { date: '30-05-2025', name: 'Mylliem Landslide 5' }
[25.47565, 91.81801], { date: '30-05-2025', name: 'Mylliem Landslide 6' }
[25.47174, 91.81621], { date: '31-05-2025', name: 'Mylliem Landslide 7' }
[25.47133, 91.81608], { date: '30-05-2025', name: 'Mylliem Landslide 8' }
[25.46944, 91.81748], { date: '30-05-2025', name: 'Mylliem Landslide 9' }
[25.46891, 91.8184],  { date: '30-05-2025', name: 'Mylliem Landslide 10' }
[25.46687, 91.81902], { date: '31-05-2025', name: 'Mylliem Landslide 11' }
[25.46591, 91.82085], { date: '31-05-2025', name: 'Mylliem Landslide 12' }
[25.46593, 91.82263], { date: '30-05-2025', name: 'Mylliem Landslide 13' }
[25.46529, 91.82496], { date: '31-05-2025', name: 'Umtyngar Landslide' }
[25.46555, 91.82614], { date: '30-05-2025', name: 'Umtyngar Landslide 2' }
[25.46443, 91.82775], { date: '31-05-2025', name: 'Umtyngar Landslide 3' }
[25.46194, 91.82976], { date: '31-05-2025', name: 'Laitkroh Landslide' }
[25.46117, 91.83177], { date: '31-05-2025', name: 'Laitkroh Landslide 2' }
[25.44031, 91.84712], { date: '30-05-2025', name: 'Laitkroh Landslide 3' }
[25.43961, 91.8491],  { date: '30-05-2025', name: 'Laitkroh Landslide 4' }
[25.43813, 91.85107], { date: '30-05-2025', name: 'Laitkroh Landslide 5' }
[25.43763, 91.85282], { date: '31-05-2025', name: 'Lum Thnagding Landslide' }
[25.43763, 91.85432], { date: '30-05-2025', name: 'Lum Thnagding Landslide 2' }
[25.43707, 91.8561],  { date: '30-05-2025', name: 'Lum Thnagding Landslide 3' }
[25.437,   91.85824], { date: '30-05-2025', name: 'Lum Thnagding Landslide 4' }
[25.43398, 91.86066], { date: '31-05-2025', name: 'Wah Bnoh Landslide' }
[25.43231, 91.86152], { date: '31-05-2025', name: 'Wah Bnoh Landslide 2' }
[25.43141, 91.86274], { date: '31-05-2025', name: 'Wah Bnoh Landslide 3' }
[25.42705, 91.86312], { date: '30-05-2025', name: 'Wah Bnoh Landslide 4' }
[25.4229,  91.86607], { date: '31-05-2025', name: 'Wah Bnoh Landslide 5' }
[25.42221, 91.86785], { date: '31-05-2025', name: 'Wah Bnoh Landslide 6' }
[25.42162, 91.86807], { date: '31-05-2025', name: 'Pomlum Landslide' }
[25.42881, 91.86459], { date: '30-05-2025', name: 'Pomlum Landslide 2' }
[25.41838, 91.86815], { date: '31-05-2025', name: 'Pomlum Landslide 3' }
[25.41072, 91.87425], { date: '30-05-2025', name: 'Pomlum Landslide 4' }
[25.40375, 91.87281], { date: '31-05-2025', name: 'Mawkejam Landslide' }
[25.39732, 91.87258], { date: '31-05-2025', name: 'Mawkejam Landslide 2' }
[25.39072, 91.87185], { date: '31-05-2025', name: 'Mawkejam Landslide 3' }
[25.3852,  91.87428], { date: '31-05-2025', name: 'Mawkejam Landslide 4' }
[25.38303, 91.87442], { date: '31-05-2025', name: 'Rgnain Landslide' }
[25.38257, 91.87439], { date: '30-05-2025', name: 'Rgnain Landslide 2' }
[25.37975, 91.87347], { date: '31-05-2025', name: 'Rgnain Landslide 3' }
[25.37642, 91.87452], { date: '31-05-2025', name: 'Rgnain Landslide 4' }
[25.36093, 91.88129], { date: '30-05-2025', name: 'Kyntiew Masi Landslide' }
[25.3604,  91.88673], { date: '30-05-2025', name: 'Kyntiew Masi Landslide 2' }
[25.35567, 91.89466], { date: '31-05-2025', name: 'Langkyrdem Landslide' }
[25.34457, 91.8906],  { date: '30-05-2025', name: 'Langkyrdem Landslide 2' }
[93.826,27.104], {date:'2020-09-17', name:'Bandardewa NH15'}
[93.74347,27.134693], {date:'2020-07-10', name:'Tigdo Landslide'}
[93.698,27.107], {date:'2020-07-10', name:'Modrijo'}
[93.61283,27.081306], {date:'2020-06-25', name:'Donyi Colony'}
[94.522,26.326], {date:'2020-08-15', name:'Alongmen Ward Mokochung'}
[94.487,26.166], {date:'2020-08-14', name:'Akuluto Town'}
[94.519,26.01], {date:'2020-08-17', name:'DC Hill West Colony'}
[94.441,25.873], {date:'2020-07-08', name:'Xuivi Kilomi Stretch'}
[94.098,25.689], {date:'2020-07-11', name:'High School Area Kohima'}
[94.106,25.662], {date:'2020-10-04', name:'Lower PWD Kohima'}
[94.091,25.664], {date:'2020-08-19', name:'Paramedical Colony Kohima'}
[94.387,25.498], {date:'2020-08-20', name:'Laii Village'}
[94.142,25.396], {date:'2020-06-02', name:'Imphal-Jiribam Landslide-1d'}
[94.06528,25.355955], {date:'2020-10-23', name:'Khongnem-Thana'}
[93.911,25.236], {date:'2020-07-06', name:'Twilang Landslide'}
[93.985,24.925], {date:'2020-07-21', name:'K Sinam Village NH37'}
[93.986,24.748], {date:'2020-08-11', name:'Khenjonglang Landslide'}
[94.222,24.318], {date:'2020-08-20', name:'Khongkhang'}
[93.382774,23.692778], {date:'2020-08-01', name:'Zotlang-1'}
[93.19319,23.523083], {date:'2020-10-03', name:'Khazawl1'}
[92.7973,23.350964], {date:'2020-07-10', name:'Sailam_1'}
[92.891945,23.533611], {date:'2020-08-04', name:'Electric_veng3'}
[92.97425,23.612047], {date:'2020-05-28', name:'Mualpheng_1'}
[92.967,23.6625], {date:'2020-10-02', name:'Rulchawm1'}
[92.88556,23.673332], {date:'2020-07-10', name:'Phullen5'}
[92.72628,23.562675], {date:'2020-07-11', name:'Melriat_1'}
[93.05194,23.84111], {date:'2020-10-13', name:'Phullen3'}
[93.0475,23.855618], {date:'2020-08-17', name:'Phullen2'}
[92.75766,23.730278], {date:'2020-02-02', name:'Zemabawk_2'}
[92.760025,23.731928], {date:'2020-10-06', name:'Zembawk_1'}
[92.731186,23.721556], {date:'2020-09-22', name:'Bawngkawn_1'}
[92.728676,23.720222], {date:'2020-07-04', name:'Bawngkawn_2'}
[92.71698,23.720278], {date:'2020-06-10', name:'Khatla_1'}
[92.6981,23.720156], {date:'2020-06-05', name:'Maubawk_1'}
[92.70033,23.72324], {date:'2020-09-27', name:'Maubawk_2'}
[92.723,23.746222], {date:'2020-06-15', name:'Ramhlun_1'}
[92.72158,23.740454], {date:'2020-10-01', name:'Venglai_1'}
[92.71415,23.73952], {date:'2020-10-02', name:'Vaivakawn_1'}
[92.708725,23.739746], {date:'2020-07-17', name:'Vaivakawn_2'}
[92.695946,23.751072], {date:'2020-08-13', name:'Maubawk_3'}
[92.492226,23.916945], {date:'2020-07-11', name:'Mamit2'}
[92.49111,23.92], {date:'2020-06-10', name:'Mamit1'}
[92.49028,23.924168], {date:'2020-06-11', name:'Mamit3'}
[92.49,23.94861], {date:'2020-05-29', name:'Mamit5'}
[92.39056,23.912779], {date:'2020-06-11', name:'Mamit4'}
[92.67528,24.231943], {date:'2020-10-21', name:'Tumpui_veng1'}
[92.74167,24.455], {date:'2020-05-25', name:'Variengte_IOC_veng1'}
[92.98905,24.646982], {date:'2020-06-08', name:'SDMA_AS_2020_SONAI2'}
[92.903854,24.721872], {date:'2020-06-04', name:'SDMA_AS_2020_SONAI5'}
[92.82317,24.727879], {date:'2020-06-08', name:'SDMA_AS_2020_SONAI4'}
[92.646805,24.703638], {date:'2020-06-02', name:'SDMA_AS_2020_Mohanpur Grant Slide 1'}
[92.64739,24.731167], {date:'2020-06-02', name:'SDMA_AS_2020_Mohanpur Grant Slide 3'}
[92.55505,24.79489], {date:'2020-06-02', name:'SDMA_AS_2020_Chandipur Grant Slide'}
[92.45372,24.780027], {date:'2020-06-02', name:'SDMA_AS_2020_Karimpur Slide 2'}
[92.45564,24.783806], {date:'2020-06-02', name:'SDMA_AS_2020_Karimpur Slide 1'}
[93.07306,24.920973], {date:'2020-06-02', name:'SDMA_AS_2020_Kanakpur Slide'}
[93.2457,24.8172], {date:'2020-06-02', name:'Imphal-Jiribam Landslide-1c'}
[93.284,24.774], {date:'2020-06-02', name:'Imphal-Jiribam Landslide-1a'}
[93.43889,24.775278], {date:'2020-05-27', name:'Imphal-Jiribam Landslide-2'}
[93.696,24.792], {date:'2020-08-28', name:'Kotlen'}
[93.814735,25.770794], {date:'2020-09-19', name:'Patkai Bridge Kukidolong Stretch'}
[93.805565,25.793833], {date:'2020-09-12', name:'Patkai Bridge Kukidolong Stretch'}
[93.80233,25.796417], {date:'2020-09-07', name:'Patkai Bridge Kukidolong Stretch'}
[88.424,27.565], {date:'2020-05-26', name:'Myong Kyong 12th Mile Slide'}
[88.509,27.52], {date:'2020-06-27', name:'Uphill Panang Landslide'}
[88.50451,27.505192], {date:'2020-06-27', name:'Barfok-Lingdok GPU'}
[88.528,27.506], {date:'2020-06-27', name:'Mangan-Sangkhalang Road'}
[88.535,27.502], {date:'2020-06-29', name:'Mangang-Chungtohong Road'}
[88.48735,27.456923], {date:'2020-06-27', name:'Hee Gyanthang'}
[88.61,27.453], {date:'2020-06-25', name:'North_Sikkim_cutoff_event_2'}
[88.62566,27.39839], {date:'2020-05-24', name:'Satala Landslide'}
[88.62358,27.398666], {date:'2020-05-24', name:'Dhare Landslide'}
[88.546,27.411], {date:'2020-06-25', name:'North_Sikkim_cutoff_event_1'}
[88.505,27.384], {date:'2020-06-25', name:'North_Sikkim_cutoff_event_3'}
[88.47566,27.389505], {date:'2020-06-27', name:'Lum Village'}
[88.429,27.39], {date:'2020-06-01', name:'Sokpay_landslide'}
[88.59,27.286], {date:'2020-09-08', name:'20 Mile Bardun'}
[88.553,27.261], {date:'2020-09-08', name:'Gangtok_Rangpo_landslides'}
[88.546,27.256], {date:'2020-09-08', name:'Gai Dhara Landslide'}
[88.459,27.251], {date:'2020-06-27', name:'Tessta V NHPC Landslide'}
[88.421,27.257], {date:'2020-06-08', name:'Thakka Road mudslide'}
[88.311,27.163], {date:'2020-08-06', name:'Jorengthang Landslide'}
[88.2034,27.2206], {date:'2020-10-02', name:'Boom Tafel'}
[88.219,27.286], {date:'2020-05-24', name:'Lingchom Landslide'}
[88.232,27.357], {date:'2020-06-28', name:'Landslide near Fambrong Falls'}
[89.98556,25.589167], {date:'2020-09-17', name:'L325'}
[89.97,25.581388], {date:'2020-09-17', name:'L328'}
[90.005554,25.577778], {date:'2020-09-17', name:'L326'}
[89.99917,25.574167], {date:'2020-09-17', name:'L324'}
[89.992775,25.567778], {date:'2020-09-17', name:'L323'}
[89.98194,25.559723], {date:'2020-09-17', name:'L327'}
[89.937225,25.5525], {date:'2020-09-17', name:'L332'}
[89.93222,25.544167], {date:'2020-09-17', name:'L329'}
[89.943054,25.501389], {date:'2020-09-17', name:'L330'}
[89.953,25.471905], {date:'2020-07-08', name:'L321'}
[89.5919,25.275], {date:'2020-08-09', name:'L322'}
[90.5069,25.26278], {date:'2020-07-13', name:'L335'}
[90.81416,25.551666], {date:'2020-07-13', name:'L339'}
[90.57521,25.582556], {date:'2020-09-06', name:'Khera Songsak'}
[90.57833,25.592367], {date:'2020-07-12', name:'Rongap Songgitcham'}
[90.394,25.726], {date:'2020-07-24', name:'Tura Highway landslide'}
[91.055,25.676], {date:'2020-07-14', name:'Mawshynrut C and D block'}
[91.16778,25.624443], {date:'2020-09-24', name:'L338'}
[91.178055,25.6], {date:'2020-06-27', name:'L340'}
[91.262,25.528], {date:'2020-07-11', name:'Nongstoin Tura By-pass'}
[91.272,25.523], {date:'2020-07-14', name:'Nongstoin Block CandRD'}
[25.54161, 92.01250], { date: '2015-2016', name: 'Debris slide along NH-44 (TS 83 C/2)' }
[25.53961, 92.00156], { date: '2015-2016', name: 'Rock slide along NH-44 (TS 83 C/2)' }
[25.56933, 92.20214], { date: '2015-2016', name: 'Earth slide along Nongbah Road (TS 83 C/2)' }
[25.43011, 92.18217], { date: '2015-2016', name: 'Rock slide along NH-40 (TS 83 C/3)' }
[25.49047, 92.06931], { date: '2015-2016', name: 'Debris slide on downslope of road (TS 83 C/3)' }
[25.40019, 92.01573], { date: '2015-2016', name: 'Natural rock slide by toe erosion (TS 83 C/3)' }
[25.65839, 93.11808], { date: 'May-2015', name: 'Shallow translational debris slide along NH-54, ~2 km SE of Langlao Disa (LS-1)' }
[25.61092, 93.09178], { date: '2015', name: 'Shallow translational debris slide along NH-54, ~1.5 km W of Purana Dibolong (LS-4)' }
[25.67153, 93.11522], { date: '05-07-2015', name: 'Slope cut failure (topple) along NH-54, ~1 km E of Langlao Disa (LS-5)' }
[25.64897, 93.12083], { date: '2015', name: 'Shallow translational debris slide along NH-54, ~3 km N of Hatikhali (LS-6)' }
[25.50669, 93.10536], { date: '2015', name: 'Shallow translational debris slide along NH-54, near Langting (LS-7)' }
[25.81756, 93.10886], { date: '15-11-2015', name: 'Rock fall along NH-54, ~2 km SW of Arlongapai (LS-8)' }
[25.72561, 93.13075], { date: '15-08-2015', name: 'Shallow translational debris slide at Manderdisa–Daolapur 3 (LS-9)' }
[25.72486, 93.13108], { date: '15-08-2015', name: 'Shallow translational debris slide at Manderdisa–Daolapur 3 (LS-10)' }
[25.97253, 91.85939], { date: '2015-2016', name: 'Umling Debris slide (reactivated)' }
[91.75978,26.262201], {date:'2020-06-27', name:'SDMA North Guwahati – Dirgheswari 3'}
[91.76268,26.254368], {date:'2020-06-27', name:'SDMA North Guwahati – Dirgheswari 2'}
[91.765,26.196], {date:'2020-06-28', name:'Kharguli, Guwahati'}
[91.69352,26.214209], {date:'2020-06-26', name:'Gauripur, North Guwahati'}
[91.689445,26.210833], {date:'2020-06-25', name:'Amingaon, Guwahati'}
[91.756,26.146], {date:'2020-06-26', name:'Kahilipara, Guwahati'}
[91.863,26.102], {date:'2020-07-12', name:'Jorabat – 12th Mile'}
[91.889,25.746], {date:'2020-10-24', name:'NH-06, Umsning'}
[91.893,25.65], {date:'2020-09-24', name:'Ryndang Briew, Umiam'}
[91.88272,25.62], {date:'2020-05-21', name:'Mawiong Umjapung'}
[91.884,25.581], {date:'2020-07-12', name:'Police Reserve, Shillong'}
[91.88,25.561], {date:'2020-09-25', name:'Dhobi Ghat, Laban'}
[91.86076,25.5573], {date:'2020-09-26', name:'L267'}
[91.84,25.56], {date:'2020-06-27', name:'L264'}
[91.8409,25.563], {date:'2020-09-24', name:'L266'}
[91.845,25.566], {date:'2020-06-27', name:'L263'}
[91.817,25.5097], {date:'2020-06-27', name:'L279'}
[91.8062,25.5035], {date:'2020-05-21', name:'L284'}
[91.805,25.49052], {date:'2020-06-27', name:'L270'}
[91.81946,25.496], {date:'2020-06-27', name:'L268'}
[91.81968,25.49393], {date:'2020-07-11', name:'L271'}
[91.8215,25.4895], {date:'2020-06-27', name:'L275'}
[91.82072,25.48429], {date:'2020-06-27', name:'L269'}
[91.813225,25.470934], {date:'2020-05-24', name:'L234'}
[91.82667,25.460016], {date:'2020-05-27', name:'L177'}
[91.8357,25.4617], {date:'2020-06-27', name:'L283'}
[91.84,25.448], {date:'2020-07-11', name:'Laitlyngkot–Pomlum'}
[91.74595,25.4717], {date:'2020-09-25', name:'L261'}
[91.8468,25.351], {date:'2020-05-26', name:'L259'}
[91.786,25.4], {date:'2020-05-29', name:'Mawkdok–Khadarshnong Rd'}
[91.766815,25.393795], {date:'2020-06-27', name:'L218'}
[91.75563,25.380148], {date:'2020-05-27', name:'L191'}
[91.767845,25.355244], {date:'2020-06-24', name:'L195'}
[91.76776,25.34702], {date:'2020-06-27', name:'L222'}
[91.76536,25.347097], {date:'2020-08-30', name:'L211'}
[91.79079,25.33172], {date:'2020-06-27', name:'L227'}
[91.79825,25.323166], {date:'2020-06-24', name:'L205'}
[91.803795,25.326237], {date:'2020-06-27', name:'L231'}
[91.93597,25.3946], {date:'2020-05-26', name:'L18'}
[91.94392,25.380934], {date:'2020-05-27', name:'L32'}
[91.981186,25.37435], {date:'2020-06-27', name:'L39'}
[91.9854,25.378433], {date:'2020-07-10', name:'L43'}
[91.98962,25.385916], {date:'2020-06-26', name:'L34'}
[91.98842,25.38875], {date:'2020-05-26', name:'L2'}
[91.99098,25.392033], {date:'2020-05-26', name:'L10'}
[92.0077,25.3451], {date:'2020-05-23', name:'Mawlat'}
[92.05989,25.590668], {date:'2020-09-27', name:'Thangshalai, Diengpasoh'}
[92.18784,25.453518], {date:'2020-05-26', name:'Shillong–Agartala Rd'}
[92.201385,25.447416], {date:'2020-05-26', name:'Salaroh'}
[92.19558,25.441778], {date:'2020-05-26', name:'Iawmusiang Landslide II'}
[92.19447,25.442333], {date:'2020-05-26', name:'Iawmusiang Landslide I'}
"""

features = []

pattern = re.compile(
    r'\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]\)?\s*,\s*\{\s*date\s*:\s*\'([^\']+)\'\s*,\s*name\s*:\s*\'([^\']+)\'\s*\}',
    re.IGNORECASE
)


for lon, lat, date, name in pattern.findall(raw):
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(lon), float(lat)]
        },
        "properties": {
            "date": date,
            "name": name
        }
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("new_500_pts_landslides.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print("DONE. Total points:", len(features))
