import math
import sqlite3
import json
from decimal import Decimal
from math import cos, sin, sqrt
import math
import numpy as np

sensor_type_fills = {"رادار": "radar",
                     "جمر": "jammer",
                     "آنتن": "antenna",
                     "انتن": "antenna",
                     "سنسور": "sensor",
                     "سنسورهای": "sensor",
                     "سنسورها": "sensor",
                     "رادارهای": "radar",
                     "رادارها": "radar",
                     "جمرهای": "jammer",
                     "جمرها": "jammer",
                     "آنتنهای": "antenna",
                     "آنتنها": "antenna",
                     "انتنهای": "antenna",
                     "انتنها": "antenna",
                     "رادارهایی": "radar",
                     "آنتنهایی": "antenna",
                     "انتنهایی": "antenna",
                     "جمرهایی": "jammer",
                     "سنسورهایی": "sensor"}

sensor_type = {"رادار": "radar",
               "جمر": "jammer",
               "آنتن": "antenna",
               "انتن": "antenna",
               "سنسور": "sensor"}

sensor_type_eng_to_per = {
    "radar": "رادار",
    "jammer": "جمر",
    "antenna": "آنتن",
    "sensor": "سنسور"
}

sensor_status = {"آفلاین": "0",
                 "آنلاین": "1",
                 "انلاین": "1",
                 "افلاین": "0"}

rank = {"سرهنگ": "sarhang",
        "سروان": "sarvan",
        "امیر": "amir"}

rank_fills = {
    "سرهنگ": "sarhang",
    "سروان": "sarvan",
    "امیر": "amir",
    "سرهنگهای": "sarhang",
    "سروانهای": "sarvan",
    "امیرهای": "amir"}

rank_eng_to_per = {
    "sarhang": "سرهنگ",
    "sarvan": "سروان",
    "amir": "امیر"
}

one_part_area = {"شمال": "north",
                 "جنوب": "south",
                 "شرق": "east",
                 "غرب": "west",
                 "مرکز": "center"}

two_part_area = {"شمال غربی": "north west",
                 "شمال شرقی": "north east",
                 "شمال میانه": "middle north",
                 "جنوب غربی": "west south",
                 "حنوب شرقی": "east south",
                 "جنوب میانه": "middle south",
                 "شرق میانه": "middle east",
                 "غرب میانه": "middle west"}

area = {
    "شمال غربی": "north west",
    "شمال شرقی": "north east",
    "شمال میانه": "middle north",
    "جنوب غربی": "west south",
    "حنوب شرقی": "east south",
    "جنوب میانه": "middle south",
    "شرق میانه": "middle east",
    "غرب میانه": "middle west",
    "شمال": "north",
    "جنوب": "south",
    "شرق": "east",
    "غرب": "west",
    "مرکز": "center"
}

parameter_fills = {
    "توان": "power",
    "فرکانس": "frequency",
    "آزیموت": "azimuth",
    "ازیموت": "azimuth",
    "توانی": "power",
    "فرکانسی": "frequency",
    "آزیموتی": "azimuth",
    "ازیموتی": "azimuth"
}

parameter = {
    "توان": "power",
    "فرکانس": "frequency",
    "آزیموت": "azimuth",
    "ازیموت": "azimuth"
}

parameter_eng_to_per = {
    "power": "توان",
    "frequency": "فرکانس",
    "azimuth": "آزیموت"
}

temp_staff_first_names = ["علی", "رضا", "حسن", "حسین", "امیر", "هادی", "مهدی", "محسن", "فرشید", "مجید",
                          "سعید", "ناصر", "نادر", "محمد", "سپهر", "عباس", "مصطفی", "جعفر", "مهرداد",
                          "مهران", "منصور", "میلاد"]
temp_staff_last_names = ["راد", "هاشمی", "نوشی", "فاضلی", "رحیمی", "صادقی", "صبوری", "افشاری", "محسنی",
                         "عدالت", "امیری", "حسینی", "حسنی", "منصوری", "ناصری", "نادری", "مرادی", "رضایی",
                         "حمیدی", "نوری"]

conn = sqlite3.connect('C4I_system.db')
print("database Opened successfully!")


def create_database_tables():
    print("database Opened successfully!")
    conn.execute(
        '''CREATE TABLE barracks
        (ID INTEGER primary key AUTOINCREMENT,
         name varchar not null unique,
         longitude double not null,
         latitude double not null,
         insider boolean not null,
         type varchar not null)
         ''')

    print("barracks table created successfully!")

    conn.execute(
        '''CREATE TABLE links
        (ID1 INT not null,
         ID2 INT not null,
         type varchar not null,
         online boolean not null,
         channel varchar not null,
         primary key (ID1, ID2),
         foreign key (ID1, ID2) references barracks(ID, ID)
         )
         ''')

    print("links table created successfully!")

    conn.execute(
        '''CREATE TABLE sub_barracks
        (ID INT not null,
         sub_ID INT not null,
         primary key (ID, sub_ID),
         foreign key (ID, sub_ID) references barracks(ID, ID)
         )
         ''')

    print("sub_barracks table created successfully!")

    conn.execute(
        '''CREATE TABLE staff
        (ID INTEGER primary key AUTOINCREMENT,
         barracks_ID INT not null,
         first_name varchar not null,
         last_name varchar not null,
         rank varchar not null,
         access_level varchar not null,
         active boolean not null,
         foreign key (barracks_ID) references barracks(ID)
         )
         ''')

    print("staff table created successfully!")

    conn.execute(
        '''CREATE TABLE sensors
        (ID INTEGER primary key AUTOINCREMENT,
         type varchar not null,
         parameters varchar not null,
         longitude double not null,
         latitude double not null,
         radius double not null,
         insider boolean not null,
         ip varchar not null,
         barracks_ID INT not null,
         link_type varchar not null,
         online boolean not null,
         foreign key (barracks_ID) references barracks(ID)
         )
         ''')

    print("sensors table created successfully!")


def add_barracks_to_db(name, longitude, latitude, insider, type):
    cursor = conn.cursor()
    cursor.execute("Insert INTO barracks (name, longitude, latitude, insider, type)\
            VALUES (?, ?, ?, ?, ?)", (name, longitude, latitude, insider, type))
    print("Barracks added to database successfully!")
    cursor.close()


def add_link_to_db(ID1, ID2, type, online, channel):
    cursor = conn.cursor()
    cursor.execute("Insert INTO links (ID1, ID2, type, online, channel)\
            VALUES (?, ?, ?, ?, ?)", (ID1, ID2, type, online, channel))
    print("Staff added to database successfully!")
    cursor.close()


def add_sub_barracks_to_db(ID, sub_ID):
    cursor = conn.cursor()
    cursor.execute("Insert INTO sub_barracks (ID, sub_ID)\
            VALUES (?, ?)", (ID, sub_ID))
    print("Sub_barracks added to database successfully!")
    cursor.close()


def add_staff_to_db(first_name, last_name, rank, barracks_ID, access_level, active):
    cursor = conn.cursor()
    cursor.execute("Insert INTO staff (first_name, last_name, rank, barracks_ID, access_level, active)\
            VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, rank, barracks_ID, access_level, active))
    print("Staff added to database successfully!")
    cursor.close()


def add_sensor_to_db(type, parameters, longitude, latitude, radius, insider, ip, barracks_ID, link_type, online):
    cursor = conn.cursor()
    cursor.execute("Insert INTO sensor (type, parameters, longitude, latitude, radius, insider, ip, barracks_ID, link_type, online)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (type, parameters, longitude, latitude, radius, insider, ip, barracks_ID, link_type, online))
    print("Staff added to database successfully!")
    cursor.close()


def create_ner_intent_json_file_with_persion_nervals():
    # train_list = []
    ner_intent_dict = {}
    # intent_dict = {}
    # ner_dict = {}
    for i in range(1, 51):
        for key in sensor_type:
            if sensor_type != "سنسور":
                # "چند سنسور از نوع رادار مربوط به پادگان 1 وجود دارد؟"
                text = "چند سنسور از نوع " + str(key) + " مربوط به پادگان " + str(i) + " وجود دارد؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"sensor_type_1": str(key),
                #              "barracks_name_1": str(i)},
                #    "query": {"intent": "get_sensor_count_based_on_sensor_type",
                #              "sensor_type_1": str(sensor_type[key]),
                #              "barracks_name_1": str(i)}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "O",
                        "O",
                        "O",
                        "O",
                        "B-sensor_type_1",
                        "O",
                        "O",
                        "O",
                        "B-barracks_name_1",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type_1": str(key),
                        "barracks_name_1": str(i)
                    },
                    "INTENTS": [
                        "get_sensor_count_based_on_sensor_type"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_sensor_count_based_on_sensor_type"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "O",
                #        "O",
                #        "O",
                #        "O",
                #        "B-sensor_type_1",
                #        "O",
                #        "O",
                #        "O",
                #        "B-barracks_name_1",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "sensor_type_1": str(key),
                #        "barracks_name_1": str(i)
                #    }
                # }
                # ner_dict[text] = ner

            # "آیپی سنسور 1 چیست؟"
            text = "آیپی " + str(key) + " " + str(i) + " چیست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_sensor_IP",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_sensor_IP"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensor_IP"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "ایپی سنسور 1 چیست؟"
            text = "ایپی " + str(key) + " " + str(i) + " چیست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_sensor_IP",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_sensor_IP"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensor_IP"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "مختصات جغرافیایی سنسور 1 چیست؟"
            text = "مختصات جغرافیایی " + str(key) + " " + str(i) + " چیست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_coordinates_of_sensor",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_coordinates_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_coordinates_of_sensor"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "مختصات سنسور 1 چیست؟"
            text = "مختصات " + str(key) + " " + str(i) + " چیست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_coordinates_of_sensor",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_coordinates_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            ## intent
            # intent = {"INTENTS": ["get_coordinates_of_sensor"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "پارامترهای مربوط به سنسور 1 دارای چه مقادیری هستند؟"
            text = "پارامترهای مربوط به " + str(key) + " " + str(i) + " دارای چه مقادیری هستند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_all_parameters_of_sensor",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_all_parameters_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_all_parameters_of_sensor"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "پارامتر های مربوط به سنسور 1 دارای چه مقادیری هستند؟"
            text = "پارامتر های مربوط به " + str(key) + " " + str(i) + " دارای چه مقادیری هستند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_all_parameters_of_sensor",
            #              "sensor_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "O",
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_all_parameters_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_all_parameters_of_sensor"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "O",
            #        "B-sensor_type_1",
            #        "B-sensor_name_1",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "سنسور های دشمن در پادگان 1 کدامند؟"
            text = str(key) + " های دشمن در پادگان " + str(i) + " کدامند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_enemy_sensors_based_on_barracks_id",
            #              "barracks_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "O",
                    "O",
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_enemy_sensors_based_on_barracks_id"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_enemy_sensors_based_on_barracks_id"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "O",
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "سنسورهای دشمن در پادگان 1 کدامند؟"
            text = str(key) + "های دشمن در پادگان " + str(i) + " کدامند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(i),
            #              "sensor_type_1": str(key)},
            #    "query": {"intent": "get_enemy_sensors_based_on_barracks_id",
            #              "barracks_name_1": str(i),
            #              "sensor_type_1": str(sensor_type[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "O",
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "sensor_type_1": str(key)
                },
                "INTENTS": [
                    "get_enemy_sensors_based_on_barracks_id"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_enemy_sensors_based_on_barracks_id"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "O",
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(i),
            #        "sensor_type_1": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            for key2 in parameter:
                # "رادار 1 با چه فرکانس ای کار میکند؟"
                text = str(key) + " " + str(i) + " با چه " + str(key2) + " ای کار میکند؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"sensor_name_1": str(i),
                #              "parameter": str(key2),
                #              "sensor_type_1": str(key)},
                #    "query": {"intent": "get_parameter_of_sensor_based_on_parameter_type",
                #              "sensor_name_1": str(i),
                #              "parameter": str(parameter[key2]),
                #              "sensor_type_1": str(sensor_type[key])}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "B-sensor_type_1",
                        "B-sensor_name_1",
                        "O",
                        "O",
                        "B-parameter",
                        "O",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type_1": str(key),
                        "sensor_name_1": str(i),
                        "parameter": str(key2)
                    },
                    "INTENTS": [
                        "get_parameter_of_sensor_based_on_parameter_type"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_parameter_of_sensor_based_on_parameter_type"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "B-sensor_type_1",
                #        "B-sensor_name_1",
                #        "O",
                #        "O",
                #        "B-parameter",
                #        "O",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "sensor_type": str(key),
                #        "sensor_name": str(i),
                #        "parameter": str(key2)
                #    }
                # }
                # ner_dict[text] = ner

                # "رادار 1 با چه فرکانسی کار میکند؟"
                text = str(key) + " " + str(i) + " با چه " + str(key2) + "ی کار میکند؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"sensor_name_1": str(i),
                #              "parameter": str(key2),
                #              "sensor_type_1": str(key)},
                #    "query": {"intent": "get_parameter_of_sensor_based_on_parameter_type",
                #              "sensor_name_1": str(i),
                #              "parameter": str(parameter[key2]),
                #              "sensor_type_1": str(sensor_type[key])}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "B-sensor_type_1",
                        "B-sensor_name_1",
                        "O",
                        "O",
                        "B-parameter",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type": str(key),
                        "sensor_name": str(i),
                        "parameter": str(key2)
                    },
                    "INTENTS": [
                        "get_parameter_of_sensor_based_on_parameter_type"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_parameter_of_sensor_based_on_parameter_type"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "B-sensor_type_1",
                #        "B-sensor_name_1",
                #        "O",
                #        "O",
                #        "B-parameter",
                #        "O",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "sensor_type": str(key),
                #        "sensor_name": str(i),
                #        "parameter": str(key2)
                #    }
                # }
                # ner_dict[text] = ner

            for key2 in sensor_status:
                # "چند سنسور آنلاین مربوط به پادگان 1 وجود دارد؟"
                text = "چند " + str(key) + " " + str(key2) + " مربوط به پادگان " + str(i) + " وجود دارد؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"sensor_type_1": str(key),
                #              "sensor_status_1": str(key2),
                #              "barracks_name_1": str(i)},
                #    "query": {"intent": "get_sensor_count_based_on_sensor_status",
                #              "sensor_type_1": str(sensor_type[key]),
                #              "sensor_status_1": str(sensor_status[key2]),
                #              "barracks_name_1": str(i)}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "O",
                        "B-sensor_type_1",
                        "B-sensor_status_1",
                        "O",
                        "O",
                        "O",
                        "B-barracks_name_1",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type_1": str(key),
                        "sensor_status_1": str(key2),
                        "barracks_name_1": str(i)
                    },
                    "INTENTS": [
                        "get_sensor_count_based_on_sensor_status"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_sensor_count_based_on_sensor_status"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "O",
                #        "B-sensor_type_1",
                #        "B-sensor_status_1",
                #        "O",
                #        "O",
                #        "O",
                #        "B-barracks_name_1",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "sensor_type_1": str(key),
                #        "sensor_status_1": str(key2),
                #        "barracks_name_1": str(i)
                #    }
                # }
                # ner_dict[text] = ner

        # "پادگان 1 از چه نوع است؟"
        text = "پادگان " + str(i) + " از چه نوع است؟ "
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(i)},
        #    "query": {"intent": "get_type_of_barracks",
        #              "barracks_name_1": str(i)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "B-barracks_name_1",
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(i)
            },
            "INTENTS": [
                "get_type_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_type_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "B-barracks_name_1",
        #        "O",
        #        "O",
        #        "O",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(i)
        #    }
        # }
        # ner_dict[text] = ner

        # "پادگان 1 مربوط به دشمن است یا خود؟"
        text = "پادگان " + str(i) + " مربوط به دشمن است یا خود؟ "
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(i)},
        #    "query": {"intent": "is_barracks_insider",
        #              "barracks_name_1": str(i)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "B-barracks_name_1",
                "O",
                "O",
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(i)
            },
            "INTENTS": [
                "is_barracks_insider"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["is_barracks_insider"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "B-barracks_name_1",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(i)
        #    }
        # }
        # ner_dict[text] = ner

        # "مختصات جغرافیایی پادگان 1 چیست؟"
        text = "مختصات جغرافیایی پادگان " + str(i) + " چیست؟ "
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(i)},
        #    "query": {"intent": "get_coordinates_of_barracks",
        #              "barracks_name_1": str(i)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "B-barracks_name_1",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(i)
            },
            "INTENTS": [
                "get_coordinates_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_coordinates_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "B-barracks_name_1",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(i)
        #    }
        # }
        # ner_dict[text] = ner

        # "مختصات پادگان 1 چیست؟"
        text = "مختصات پادگان " + str(i) + " چیست؟ "
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(i)},
        #    "query": {"intent": "get_coordinates_of_barracks",
        #              "barracks_name_1": str(i)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "B-barracks_name_1",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(i)
            },
            "INTENTS": [
                "get_coordinates_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_coordinates_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "B-barracks_name_1",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(i)
        #    }
        # }
        # ner_dict[text] = ner

        # "سنسور 1 از چه نوع است؟"
        text = "سنسور " + str(i) + " از چه نوع است؟ "
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"sensor_name_1": str(i)},
        #    "query": {"intent": "get_sensor_type",
        #              "sensor_name_1": str(i)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "B-sensor_name_1",
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
                "sensor_name_1": str(i)
            },
            "INTENTS": [
                "get_sensor_type"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_sensor_type"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "B-sensor_name_1",
        #        "O",
        #        "O",
        #        "O",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "sensor_name_1": str(i)
        #    }
        # }
        # ner_dict[text] = ner

        # "پادگان های دشمن کدامند؟"

    for key2 in one_part_area:
        for key in sensor_type:
            # "رادار های جنوب کشور چه وضعیتی دارند؟"
            text = str(key) + " های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(one_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "O",
                    "B-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "رادارهای جنوب کشور چه وضعیتی دارند؟"
            text = str(key) + "های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(one_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "B-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "رادارهای جنوب کشور چه وضعیتی دارند؟"
            text = str(key) + "ها " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(one_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "B-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

    for key2 in two_part_area:
        for key in sensor_type:
            # "رادار های جنوب شرقی کشور چه وضعیتی دارند؟"
            text = str(key) + " های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(two_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "O",
                    "B-area",
                    "I-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "I-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "رادارهای جنوب شرقی کشور چه وضعیتی دارند؟"
            text = str(key) + "های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(two_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "B-area",
                    "I-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "I-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "رادارهای جنوب شرقی کشور چه وضعیتی دارند؟"
            text = str(key) + "ها " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"sensor_type_1": str(key),
            #              "area": str(key2)},
            #    "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
            #              "sensor_type_1": str(sensor_type[key]),
            #              "area": str(two_part_area[key2])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-sensor_type_1",
                    "B-area",
                    "I-area",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "sensor_type_1": str(key),
                    "area": str(key2)
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-sensor_type_1",
            #        "O",
            #        "B-area",
            #        "I-area",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "sensor_type_1": str(key),
            #        "area": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

    for key in range(1, 11):
        for key2 in range(1, 21):
            for type1 in sensor_type:
                for type2 in sensor_type:
                    # "حوزه استحفاظی رادار 1 با حوزه استحفاظی آنتن 2 تداخل دارد؟"
                    text = "حوزه استحفاظی " + str(type1) + " " + str(key) + " با حوزه استحفاظی " + str(
                        type2) + " " + str(key2) + " تداخل دارد؟"
                    # train
                    # train_dict = {
                    #    "text": text,
                    #    "slots": {"sensor_name_1": str(key),
                    #              "sensor_name_2": str(key2),
                    #              "sensor_type_1": str(type1),
                    #              "sensor_type_2": str(type2)},
                    #    "query": {"intent": "check_if_two_sensors_interfere",
                    #              "sensor_type_1": str(sensor_type[type1]),
                    #              "sensor_type_2": str(sensor_type[type2]),
                    #              "sensor_name_1": str(key),
                    #              "sensor_name_2": str(key2)}
                    # }
                    # train_list.append(train_dict)
                    # ner_intent
                    ner_intent = {
                        "TEXT": text.split(),
                        "NERTAGS": [
                            "O",
                            "O",
                            "B-sensor_type_1",
                            "B-sensor_name_1",
                            "O",
                            "O",
                            "O",
                            "B-sensor_type_2",
                            "B-sensor_name_2",
                            "O",
                            "O"
                        ],
                        "NERVALS": {
                            "sensor_name_1": str(key),
                            "sensor_name_2": str(key2),
                            "sensor_type_1": str(type1),
                            "sensor_type_2": str(type2)
                        },
                        "INTENTS": [
                            "check_if_two_sensors_interfere"
                        ]
                    }
                    ner_intent_dict[text] = ner_intent
                    # intent
                    # intent = {"INTENTS": ["check_if_two_sensors_interfere"]}
                    # intent_dict[text] = intent
                    # ner
                    # ner = {
                    #    "TEXT": text.split(),
                    #    "NERTAGS": [
                    #        "O",
                    #        "O",
                    #        "B-sensor_type_1",
                    #        "B-sensor_name_1",
                    #        "O",
                    #        "O",
                    #        "O",
                    #        "B-sensor_type_2",
                    #        "B-sensor_name_2",
                    #        "O",
                    #        "O"
                    #    ],
                    #    "NERVALS": {
                    #        "sensor_name_1": str(key),
                    #        "sensor_name_2": str(key2),
                    #        "sensor_type_1": str(type1),
                    #        "sensor_type_2": str(type2)
                    #    }
                    # }
                    # ner_dict[text] = ner

    for key in sensor_type:
        # "حوزه استحفاظی چه رادار هایی با هم تداخل ندارند؟"
        text = "حوزه استحفاظی چه " + str(key) + " هایی با هم نداخل ندارند؟"
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"sensor_type_1": str(key)},
        #    "query": {"intent": "get_all_sensors_that_do_not_interfere_based_on_sensor_type",
        #              "sensor_type_1": str(sensor_type[key])}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "B-sensor_type_1",
                "O",
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
                "sensor_type_1": str(key)
            },
            "INTENTS": [
                "get_all_sensors_that_do_not_interfere_based_on_sensor_type"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_all_sensors_that_do_not_interfere_based_on_sensor_type"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "B-sensor_type_1",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "sensor_type_1": str(key)
        #    }
        # }
        # ner_dict[text] = ner

        # "حوزه استحفاظی چه رادارهایی با هم تداخل ندارند؟"
        text = "حوزه استحفاظی چه " + str(key) + "هایی با هم نداخل ندارند؟"
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"sensor_type_1": str(key)},
        #    "query": {"intent": "get_all_sensors_that_do_not_interfere_based_on_sensor_type",
        #              "sensor_type_1": str(sensor_type[key])}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "B-sensor_type_1",
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
                "sensor_type_1": str(key)
            },
            "INTENTS": [
                "get_all_sensors_that_do_not_interfere_based_on_sensor_type"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_all_sensors_that_do_not_interfere_based_on_sensor_type"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "B-sensor_type_1",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "sensor_type_1": str(key)
        #    }
        # }
        # ner_dict[text] = ner

    for key in rank:
        for i in range(1, 51):
            # "تعداد سرهنگ های پادگان 1 چند تاست؟"
            text = "تعداد " + str(key) + " های پادگان " + str(i) + " چندتاست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(i),
            #              "rank": str(key)},
            #    "query": {"intent": "get_count_of_barracks_staff_based_on_rank",
            #              "barracks_name_1": str(i),
            #              "rank": str(rank[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-rank",
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "rank": str(key)
                },
                "INTENTS": [
                    "get_count_of_barracks_staff_based_on_rank"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_count_of_barracks_staff_based_on_rank"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "B-rank",
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(i),
            #        "rank": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "تعداد سرهنگهای پادگان 1 چند تاست؟"
            text = "تعداد " + str(key) + "های پادگان " + str(i) + " چندتاست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(i),
            #              "rank": str(key)},
            #    "query": {"intent": "get_count_of_barracks_staff_based_on_rank",
            #              "barracks_name_1": str(i),
            #              "rank": str(rank[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-rank",
                    "O",
                    "B-barracks_name_1",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "rank": str(key)
                },
                "INTENTS": [
                    "get_count_of_barracks_staff_based_on_rank"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_count_of_barracks_staff_based_on_rank"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "B-rank",
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(i),
            #        "rank": str(key)
            #    }
            # }
            # ner_dict[text] = ner

        for ln in temp_staff_last_names:
            # "سرهنگ امیری در کدام پادگان حضور دارد؟"
            text = str(key) + " " + str(ln) + " در کدام پادگان حضور دارد؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"staff_name": str(ln),
            #              "rank": str(key)},
            #    "query": {"intent": "get_barracks_name_of_a_staff",
            #              "staff_name": str(ln),
            #              "rank": str(rank[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-rank",
                    "B-staff_name",
                    "O",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "staff_name": str(ln),
                    "rank": str(key)
                },
                "INTENTS": [
                    "get_barracks_name_of_a_staff"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_barracks_name_of_a_staff"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-rank",
            #        "B-staff_name",
            #        "O",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "staff_name": str(ln),
            #        "rank": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "سطح دسترسی سرهنگ امیری چیست؟"
            text = "سطح دسترسی " + str(key) + " " + str(ln) + " چیست؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"staff_name": str(ln),
            #              "rank": str(key)},
            #    "query": {"intent": "get_access_level_of_a_staff",
            #              "staff_name": str(ln),
            #              "rank": str(rank[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-rank",
                    "B-staff_name",
                    "O"
                ],
                "NERVALS": {
                    "staff_name": str(ln),
                    "rank": str(key)
                },
                "INTENTS": [
                    "get_access_level_of_a_staff"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_access_level_of_a_staff"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-rank",
            #        "B-staff_name",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "staff_name": str(ln),
            #        "rank": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            # "ُسرهنگ امیری فعال است یا بلاک؟"
            text = str(key) + " " + str(ln) + " فعال است یا بلاک؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"staff_name": str(ln),
            #              "rank": str(key)},
            #    "query": {"intent": "is_staff_active",
            #              "staff_name": str(ln),
            #              "rank": str(rank[key])}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "B-rank",
                    "B-staff_name",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "staff_name": str(ln),
                    "rank": str(key)
                },
                "INTENTS": [
                    "is_staff_active"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["is_staff_active"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "B-rank",
            #        "B-staff_name",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "staff_name": str(ln),
            #        "rank": str(key)
            #    }
            # }
            # ner_dict[text] = ner

            for fn in temp_staff_first_names:
                # "ُسرهنگ رضا امیری در کدام پادگان حضور دارد؟"
                text = str(key) + " " + str(ln) + " " + str(fn) + " در کدام پادگان حضور دارد؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"staff_name": str(fn) + " " + str(ln),
                #              "rank": str(key)},
                #    "query": {"intent": "get_barracks_name_of_a_staff",
                #              "staff_name": str(fn) + " " + str(ln),
                #              "rank": str(rank[key])}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "B-rank",
                        "B-staff_name",
                        "I-staff_name",
                        "O",
                        "O",
                        "O",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "staff_name": str(fn) + " " + str(ln),
                        "rank": str(key)
                    },
                    "INTENTS": [
                        "get_barracks_name_of_a_staff"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_barracks_name_of_a_staff"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "B-rank",
                #        "B-staff_name",
                #        "I-staff_name",
                #        "O",
                #        "O",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "staff_name": str(fn) + " " + str(ln),
                #        "rank": str(key)
                #    }
                # }
                # ner_dict[text] = ner

                # "سطح دسترسی سرهنگ رضا امیری چیست؟"
                text = "سطح دسترسی " + str(key) + " " + str(fn) + " " + str(ln) + " چیست؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"staff_name": str(fn) + " " + str(ln),
                #              "rank": str(key)},
                #    "query": {"intent": "get_access_level_of_a_staff",
                #              "staff_name": str(fn) + " " + str(ln),
                #              "rank": str(rank[key])}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "O",
                        "O",
                        "B-rank",
                        "B-staff_name",
                        "I-staff_name",
                        "O"
                    ],
                    "NERVALS": {
                        "staff_name": str(fn) + " " + str(ln),
                        "rank": str(key)
                    },
                    "INTENTS": [
                        "get_access_level_of_a_staff"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["get_access_level_of_a_staff"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "O",
                #        "O",
                #        "B-rank",
                #        "B-staff_name",
                #        "I-staff_name",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "staff_name": str(fn) + " " + str(ln),
                #        "rank": str(key)
                #    }
                # }
                # ner_dict[text] = ner

                # "سرهنگ رضا امیری فعال است یا بلاک؟"
                text = str(key) + " " + str(fn) + " " + str(ln) + " فعال است یا بلاک؟"
                # train
                # train_dict = {
                #    "text": text,
                #    "slots": {"staff_name": str(fn) + " " + str(ln),
                #              "rank": str(key)},
                #    "query": {"intent": "is_staff_active",
                #              "staff_name": str(fn) + " " + str(ln),
                #              "rank": str(rank[key])}
                # }
                # train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "B-rank",
                        "B-staff_name",
                        "I-staff_name",
                        "O",
                        "O",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "staff_name": str(fn) + " " + str(ln),
                        "rank": str(key)
                    },
                    "INTENTS": [
                        "is_staff_active"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                # intent = {"INTENTS": ["is_staff_active"]}
                # intent_dict[text] = intent
                ## ner
                # ner = {
                #    "TEXT": text.split(),
                #    "NERTAGS": [
                #        "B-rank",
                #        "B-staff_name",
                #        "I-staff_name",
                #        "O",
                #        "O",
                #        "O",
                #        "O"
                #    ],
                #    "NERVALS": {
                #        "staff_name": str(fn) + " " + str(ln),
                #        "rank": str(key)
                #    }
                # }
                # ner_dict[text] = ner
    for key in range(1, 11):
        for key2 in range(1, 21):
            # "ارتباط پادگان 1 با پادگان 2 از چه نوع است؟"
            text = "ارتباط پادگان " + str(key) + " با پادگان " + str(key2) + " از چه نوع است؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)},
            #    "query": {"intent": "get_type_of_two_barracks_link",
            #              "barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O",
                    "B-barracks_name_2",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(key),
                    "barracks_name_2": str(key2)
                },
                "INTENTS": [
                    "get_type_of_two_barracks_link"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_type_of_two_barracks_link"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O",
            #        "B-barracks_name_2",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(key),
            #        "barracks_name_2": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "ارتباط پادگان 1 با پادگان 2 آنلاین است یا آفلاین؟"
            text = "ارتباط پادگان " + str(key) + " با پادگان " + str(key2) + " آنلاین است یا آفلاین؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)},
            #    "query": {"intent": "get_status_of_two_barracks_link",
            #              "barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O",
                    "B-barracks_name_2",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(key),
                    "barracks_name_2": str(key2)
                },
                "INTENTS": [
                    "get_status_of_two_barracks_link"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_status_of_two_barracks_link"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O",
            #        "B-barracks_name_2",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(key),
            #        "barracks_name_2": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "ارتباط پادگان 1 با پادگان 2 آنلاین است یا آفلاین؟"
            text = "ارتباط پادگان " + str(key) + " با پادگان " + str(key2) + " انلاین است یا افلاین؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)},
            #    "query": {"intent": "get_status_of_two_barracks_link",
            #              "barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O",
                    "B-barracks_name_2",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(key),
                    "barracks_name_2": str(key2)
                },
                "INTENTS": [
                    "get_status_of_two_barracks_link"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_status_of_two_barracks_link"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O",
            #        "B-barracks_name_2",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(key),
            #        "barracks_name_2": str(key2)
            #    }
            # }
            # ner_dict[text] = ner

            # "ارتباط پادگان 1 با پادگان 2 روی چه کانالی میباشد؟"
            text = "ارتباط پادگان " + str(key) + " با پادگان " + str(key2) + " روی چه کانالی میباشد؟"
            # train
            # train_dict = {
            #    "text": text,
            #    "slots": {"barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)},
            #    "query": {"intent": "get_channel_of_two_barracks_link",
            #              "barracks_name_1": str(key),
            #              "barracks_name_2": str(key2)}
            # }
            # train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O",
                    "B-barracks_name_2",
                    "O",
                    "O",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(key),
                    "barracks_name_2": str(key2)
                },
                "INTENTS": [
                    "get_channel_of_two_barracks_link"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            # intent = {"INTENTS": ["get_channel_of_two_barracks_link"]}
            # intent_dict[text] = intent
            ## ner
            # ner = {
            #    "TEXT": text.split(),
            #    "NERTAGS": [
            #        "O",
            #        "O",
            #        "B-barracks_name_1",
            #        "O",
            #        "O",
            #        "B-barracks_name_2",
            #        "O",
            #        "O",
            #        "O",
            #        "O",
            #        "O"
            #    ],
            #    "NERVALS": {
            #        "barracks_name_1": str(key),
            #        "barracks_name_2": str(key2)
            #    }
            # }
            # ner_dict[text] = ner
    for key in range(1, 51):
        # "پادگان های زیر مجموعه پادگان 1 کدامند؟"
        text = "پادگان های زیرمجموعه پادگان " + str(key) + " کدامند؟"
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(key)},
        #    "query": {"intent": "get_sub_barracks_of_barracks",
        #              "barracks_name_1": str(key)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "O",
                "B-barracks_name_1",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(key)
            },
            "INTENTS": [
                "get_sub_barracks_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_sub_barracks_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "B-barracks_name_1",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(key)
        #    }
        # }
        # ner_dict[text] = ner

        # "پادگان های زیر مجموعه پادگان 1 کدامند؟"
        text = "پادگان های زیر مجموعه پادگان " + str(key) + " کدامند؟"
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(key)},
        #    "query": {"intent": "get_sub_barracks_of_barracks",
        #              "barracks_name_1": str(key)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "O",
                "O",
                "B-barracks_name_1",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(key)
            },
            "INTENTS": [
                "get_sub_barracks_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_sub_barracks_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "B-barracks_name_1",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(key)
        #    }
        # }
        # ner_dict[text] = ner

        # "پادگان های زیر مجموعه پادگان 1 کدامند؟"
        text = "پادگانهای زیرمجموعه پادگان " + str(key) + " کدامند؟"
        # train
        # train_dict = {
        #    "text": text,
        #    "slots": {"barracks_name_1": str(key)},
        #    "query": {"intent": "get_sub_barracks_of_barracks",
        #              "barracks_name_1": str(key)}
        # }
        # train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "B-barracks_name_1",
                "O"
            ],
            "NERVALS": {
                "barracks_name_1": str(key)
            },
            "INTENTS": [
                "get_sub_barracks_of_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        # intent = {"INTENTS": ["get_sub_barracks_of_barracks"]}
        # intent_dict[text] = intent
        ## ner
        # ner = {
        #    "TEXT": text.split(),
        #    "NERTAGS": [
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "O",
        #        "B-barracks_name_1",
        #        "O"
        #    ],
        #    "NERVALS": {
        #        "barracks_name_1": str(key)
        #    }
        # }
        # ner_dict[text] = ner

    print("number of training questions: " + str(len(ner_intent_dict)))
    with open('./ner_intent_files/ner_intent_persion_nervals.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)


# "چند سنسور از نوع # مربوط به پادگان # وجود دارد؟"
def get_sensor_count_based_on_sensor_type(sensor_type, barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select count(*) from sensors \
            where type=? and barracks_ID=?", (sensor_type_fills[str(sensor_type)], barracks_ID))
    rows = cursor.fetchall()
    if rows:
        output = str(rows[0][0]) + " سنسور از نوع " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " مربوط به پادگان " + str(
            barracks_ID) + " وجود دارد."
        print(output)
        cursor.close()
        return output
    else:
        output = "هیچ سنسوری از نوع " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " مربوط به پادگان " + str(
            barracks_ID) + " وجود ندارد."
        print(output)
        cursor.close()
        return output


# "چند سنسور # مربوط به پادگان # وجود دارد؟"
def get_sensor_count_based_on_sensor_status(sensor_type, sensor_status, barracks_ID):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select count(*) from sensors \
                   where online=? and barracks_ID=?", (sensor_status[str(sensor_status)], barracks_ID))
    else:
        cursor.execute("select count(*) from sensors \
                     where online=? and barracks_ID=? and type=?",
                       (sensor_status[str(sensor_status)], barracks_ID, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        output = str(rows[0][0]) + " " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) \
                 + " " + str(sensor_status) + " مربوط به پادگان " + str(
            barracks_ID) + " وجود دارد."
        print(output)
        cursor.close()
        return output
    else:
        output = "هیچ " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) \
                 + " " + str(sensor_status) + "ی مربوط به پادگان " + str(
            barracks_ID) + " وجود ندارد."
        print(output)
        cursor.close()
        return output


# "پادگان # از چه نوع است؟"
def get_type_of_barracks(barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select type from barracks \
                 where ID=?", (barracks_ID,))
    rows = cursor.fetchall()
    if rows:
        output = "پادگان " + str(barracks_ID) + "از نوع " + str(rows[0][0]) + " میباشد."
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با نوع پادگان " + str(barracks_ID) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "پادگان # مربوط به دشمن است یا خود؟"
def is_barracks_insider(barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select insider from barracks \
                 where ID=?", (barracks_ID,))
    rows = cursor.fetchall()
    if rows:
        if rows[0][0] == 1:
            output = "پادگان " + str(barracks_ID) + " خودی است."
            print(output)
            cursor.close()
            return output
        elif rows[0][0] == 0:
            output = "پادگان " + str(barracks_ID) + " مربوط به دشمن است."
            print(output)
            cursor.close()
            return output
    else:
        output = "داده ای در رابطه با خودی بودن یا نبودن پادگان " + str(barracks_ID) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "مختصات جغرافیایی پادگان # چیست؟"
def get_coordinates_of_barracks(barracks_id):
    cursor = conn.cursor()
    cursor.execute("select longitude, latitude from barracks \
                 where ID=?", (barracks_id,))
    rows = cursor.fetchall()
    if rows:
        output = "طول و عرض جغرافیایی مربوط به پادگان " + str(barracks_id) + " به ترتیب برابرند با: " + str(
            rows[0][0]) + ", " + str(rows[0][1])
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با مختصات جفرافیایی پادگان " + str(barracks_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "آیپی سنسور # چیست؟"
def get_sensor_IP(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select ip from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select ip from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        output = "آیپی " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
            sensor_id) + "، " + str(rows[0][0]) + " میباشد."
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با آیپی " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(sensor_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "سنسور # از چه نوع است؟"
def get_sensor_type(sensor_id):
    cursor = conn.cursor()
    cursor.execute("select type from sensors \
                 where ID=?", (sensor_id,))
    rows = cursor.fetchall()
    if rows:
        output = "سنسور " + str(sensor_id) + " از نوع " + str(rows[0][0]) + " است."
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با نوع سنسور " + str(sensor_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "مختصات جفرافیایی سنسور # چیست؟"
def get_coordinates_of_sensor(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select longitude, latitude from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select longitude, latitude from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        output = "طول و عرض جغرافیایی مربوط به " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
            sensor_id) + " به ترتیب برابرند با: " + str(rows[0][0]) + ", " + str(rows[0][1])
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با مختصات جفرافیایی " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(sensor_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "پارامترهای مربوط به سنسور # دارای چه مقادیری هستند؟"
def get_all_parameters_of_sensor(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select parameters from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select parameters from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        par_dict = json.loads(rows[0][0])
        output = "پارامترهای مربوط به " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
            sensor_id) + " دارای مقادیر زیر میباشند: \n"
        for par, val in par_dict:
            output = output + str(parameter_eng_to_per[par]) + ": " + str(val) + "\n"
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با پارامترهای مربوط به " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(sensor_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "سنسورهای دشمن در پادگان # کدامند؟"
def get_enemy_sensors_based_on_barracks_id(barracks_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select ID from sensors \
                     where barracks_ID=? and insider=0", (barracks_id,))
    else:
        cursor.execute("select ID from sensors \
                     where barracks_ID=? and type=? and insider=0", (barracks_id, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        output = str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " های دشمن در پادگان " + str(
            barracks_id) + " به شرح زیر میباشند: \n"
        for row in rows:
            output = output + str(row[0]) + "\n"
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " های دشمن در پادگان " + str(
            barracks_id) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "#های # کشور چه وضعیتی دارند؟"
def get_sensors_status_based_on_location_and_sensor_type(area, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        if area[str(area)] == "north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "north east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "north west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "middle north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "south east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "south west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "middle south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "middle east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "middle west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area[str(area)] == "center":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
    else:
        if area[str(area)] == "north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "north east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "north west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "middle north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "south east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "south west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "middle south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "middle east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "middle west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
        elif area[str(area)] == "center":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type_fills[str(sensor_type)],))
    rows = cursor.fetchall()
    if rows:
        output = "وضعیت " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " های " + str(
            area) + " کشور به شرح زیر میباشد: \n"
        for row in rows:
            if row[1] == 1:
                output = output + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
                    row[0]) + ": آنلاین" + "\n"
            elif row[1] == 0:
                output = output + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
                    row[0]) + ": آفلاین" + "\n"
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " های " + str(area) + " کشور یافت نشد."
        print(output)
        cursor.close()
        return output


# "سنسور # با چه #(پارامتر)ی کار میکند؟"
def get_parameter_of_sensor_based_on_parameter_type(sensor_id, parameter, sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select parameters from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select parameters from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type_fills[str(sensor_type)]))
    rows = cursor.fetchall()
    if rows:
        parameter_dict = json.loads(rows[0][0])
        output = parameter_eng_to_per[str(parameter_fills[str(parameter)])] + "مربوط به " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(
            sensor_id) + " برابر است با: " + str(parameter_dict[str(parameter)])
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با " + parameter_eng_to_per[str(parameter[str(parameter)])] + " مربوط به " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " " + str(sensor_id) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "حوزه استحفاظی سنسور # با حوزه استحفاظی سنسور # تداخل دارد؟"
def check_if_two_sensors_interfere(sensor_id_1, sensor_id_2, sensor_type_1, sensor_type_2):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type_1)] == "sensor":
        cursor.execute("select longitude, latitude, radius from sensors \
                             where ID=?", (sensor_id_1,))
        rows = cursor.fetchall()
        if rows:
            dict1 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            output = "داده ای در رابطه با حوزه استحفاظی " + str(
                sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_1)]]) + " " + str(sensor_id_1) + " یافت نشد."
            print(output)
            cursor.close()
            return output
    else:
        cursor.execute("select longitude, latitude, radius from sensors \
                             where ID=? and type=?", (sensor_id_1, sensor_type_fills[str(sensor_type_1)]))
        rows = cursor.fetchall()
        if rows:
            dict1 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            output = "داده ای در رابطه با حوزه استحفاظی " + str(
                sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_1)]]) + " " + str(sensor_id_1) + " یافت نشد."
            print(output)
            cursor.close()
            return output
    if sensor_type_fills[str(sensor_type_2)] == "sensor":
        cursor.execute("select longitude, latitude, radius from sensors \
                             where ID=?", (sensor_id_2,))
        rows = cursor.fetchall()
        if rows:
            dict2 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            output = "داده ای در رابطه با حوزه استحفاظی " + str(
                sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_2)]]) + " " + str(sensor_id_2) + " یافت نشد."
            print(output)
            cursor.close()
            return output
    else:
        cursor.execute("select longitude, latitude, radius from sensors \
                             where ID=? and type=?", (sensor_id_2, sensor_type_fills[str(sensor_type_2)]))
        rows = cursor.fetchall()
        if rows:
            dict2 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            output = "داده ای در رابطه با حوزه استحفاظی " + str(
                sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_2)]]) + " " + str(sensor_id_1) + " یافت نشد."
            print(output)
            cursor.close()
            return output
    cursor.close()
    if if_tow_circle_overlaps(dict1["longitude"], dict2["longitude"], dict1["latitude"], dict2["latitude"],
                              dict1["radius"], dict2["radius"]):
        output = "حوزه استحفاظی " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_1)]]) + " " + str(
            sensor_id_1) + " با حوزه استحفاظی " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_2)]]) + " " + str(sensor_id_2) + " تداخل دارد."
        print(output)
        cursor.close()
        return output
    else:
        output = "حوزه استحفاظی " + str(sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_1)]]) + " " + str(
            sensor_id_1) + " با حوزه استحفاظی " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type_2)]]) + " " + str(sensor_id_2) + " تداخل ندارد."
        print(output)
        cursor.close()
        return output


# "حوزه استحفاظی چه سنسورهایی با یکدیگر تداخل ندارد؟"
def get_all_sensors_that_do_not_interfere_based_on_sensor_type(sensor_type):
    cursor = conn.cursor()
    if sensor_type_fills[str(sensor_type)] == "sensor":
        cursor.execute("select * from sensors")
    else:
        cursor.execute("select * from sensors \
                     where type=?", (sensor_type_fills[str(sensor_type)],))
    rows = cursor.fetchall()
    if rows:
        rows2 = rows.copy()
        output = "حوزه استحفاظی جفت " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " های زیر با یکدیگر تداخل ندارند: \n"
        for i in rows:
            for j in rows2:
                if i[0] != j[0]:
                    if not if_tow_circle_overlaps(i[3], j[3], i[4], j[4], i[5], j[5]):
                        output = output + str(i) + ", " + str(j) + "\n"
    else:
        output = "داده ای در رابطه حوزه استحفاظی " + str(
            sensor_type_eng_to_per[sensor_type_fills[str(sensor_type)]]) + " هایی که با هم تداخل ندارند، یافت نشد. "
    print(output)
    cursor.close()
    return output


# "تعداد سرهنگ های پادگان # چندتاست؟"
def get_count_of_barracks_staff_based_on_rank(barracks_name, rank):
    cursor = conn.cursor()
    cursor.execute("select count(name) from staff \
                 where barracks_ID=? and rank=?", (barracks_name, rank_fills[str(rank)]))
    rows = cursor.fetchall()
    if rows:
        output = "تعداد " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " های پادگان " + str(
            barracks_name) + "برابر است با: " + str(rows[0][0])
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با تعداد " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " های پادگان " + str(
            barracks_name) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "ُسرهنگ # در کدام پادگان حضور دارد؟"
def get_barracks_name_of_a_staff(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select barracks_ID, first_name, last_name from staff \
                 where rank=?", (rank_fills[str(rank)],))
    rows = cursor.fetchall()
    if rows:
        output = str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(staff_name) + " در پادگان "
        for row in rows:
            if str(row[2]) == staff_name or str(row[1]) + " " + str(row[2]) == staff_name:
                output = output + str(row[0]) + " حضور دارد."
                print(output)
                cursor.close()
                return output
    else:
        output = "داده ای در رابطه با پادگان مربوط به " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(
            staff_name) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "سطح دسترسی سرهنگ # چیست؟"
def get_access_level_of_a_staff(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select access_level, first_name, last_name from staff \
                 where rank=?", (rank_fills[str(rank)],))
    rows = cursor.fetchall()
    if rows:
        output = "ُسطح دسترسی " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(staff_name) + " "
        for row in rows:
            if str(row[2]) == staff_name or str(row[1]) + " " + str(row[2]) == staff_name:
                output = output + str(row[0]) + " میباشد."
                print(output)
                cursor.close()
                return output
    else:
        output = "داده ای در رابطه با سطح دسترسی " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(
            staff_name) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "سرهنگ # فعال است یا بلاک؟"
def is_staff_active(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select active, first_name, last_name from staff \
                 where rank=?", (rank_fills[str(rank)],))
    rows = cursor.fetchall()
    if rows:
        output = str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(staff_name) + " "
        for row in rows:
            if str(row[2]) == staff_name or str(row[1]) + " " + str(row[2]) == staff_name:
                if row[0] == 0:
                    output = output + " بلاک میباشد."
                    print(output)
                    cursor.close()
                    return output
                elif row[0] == 1:
                    output = output + " فعال میباشد."
                    print(output)
                    cursor.close()
                    return output
    else:
        output = "داده ای در رابطه با فعال یا بلاک بودن " + str(rank_eng_to_per[rank_fills[str(rank)]]) + " " + str(
            staff_name) + "یافت نشد."
        print(output)
        cursor.close()
        return output


# "ارتباط پادگان # با پادگان # از چه نوع است؟"
def get_type_of_two_barracks_link(barracks_id_1, barracks_id_2):
    cursor = conn.cursor()
    cursor.execute("select type from links \
                 where (ID1=? and ID2=?) or (ID1=? and ID2=?)",
                   (barracks_id_1, barracks_id_2, barracks_id_2, barracks_id_1))
    rows = cursor.fetchall()
    if rows:
        output = "ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(barracks_id_2) + " از نوع " + str(
            rows[0][0]) + " میباشد."
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با نوع ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(
            barracks_id_2) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "ارتباط پادگان # با پادگان # آنلاین است یا آفلاین؟"
def get_status_of_two_barracks_link(barracks_id_1, barracks_id_2):
    cursor = conn.cursor()
    cursor.execute("select online from links \
                 where (ID1=? and ID2=?) or (ID1=? and ID2=?)",
                   (barracks_id_1, barracks_id_2, barracks_id_2, barracks_id_1))
    rows = cursor.fetchall()
    if rows:
        output = "ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(barracks_id_2) + " "
        if rows[0][0] == 0:
            output = output + "آفلاین میباشد."
            print(output)
            cursor.close()
            return output
        elif rows[0][0] == 1:
            output = output + "آنلاین میباشد."
            print(output)
            cursor.close()
            return output
    else:
        output = "داده ای در رابطه با آنلاین یا آفلاین بودن ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(
            barracks_id_2) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "ارتباط پادگان # با پادگان # روی چه کانالی میباشد؟"
def get_channel_of_two_barracks_link(barracks_id_1, barracks_id_2):
    cursor = conn.cursor()
    cursor.execute("select channel from links \
                 where (ID1=? and ID2=?) or (ID1=? and ID2=?)",
                   (barracks_id_1, barracks_id_2, barracks_id_2, barracks_id_1))
    rows = cursor.fetchall()
    if rows:
        output = "ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(barracks_id_2) + " روی کانال " + str(
            rows[0][0]) + " میباشد."
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با کانال ارتباط پادگان " + str(barracks_id_1) + " با پادگان " + str(
            barracks_id_2) + " یافت نشد."
        print(output)
        cursor.close()
        return output


# "پادگان های زیر مجموعه پادگان # کدامند؟"
def get_sub_barracks_of_barracks(barracks_id):
    cursor = conn.cursor()
    cursor.execute("select sub_ID from sub_barracks \
                 where ID=?", (barracks_id,))
    rows = cursor.fetchall()
    if rows:
        output = "پادگان های زیرمجموعه پادگان " + str(barracks_id) + " به شرح زیر میباشند: \n"
        for row in rows:
            output = output + str(row[0]) + "\n"
        print(output)
        cursor.close()
        return output
    else:
        output = "داده ای در رابطه با پادگان های زیرمجموعه پادگان " + str(barracks_id) + " یافت نشد."
        print(output)
        cursor.close()
        return output


def if_tow_circle_overlaps(longitude1, longitude2, latitude1, latitude2, radius1, radius2):
    '''
     1. Convert (lat, lon) to (x,y,z) geocentric coordinates.
     As usual, because we may choose units of measurement in which the earth has a unit radius
     '''
    x_p1 = Decimal(cos(math.radians(longitude1)) * cos(math.radians(latitude1)))  # x = cos(lon)*cos(lat)
    y_p1 = Decimal(sin(math.radians(longitude1)) * cos(math.radians(latitude1)))  # y = sin(lon)*cos(lat)
    z_p1 = Decimal(sin(math.radians(latitude1)))  # z = sin(lat)
    x1 = (x_p1, y_p1, z_p1)
    x_p2 = Decimal(cos(math.radians(longitude2)) * cos(math.radians(latitude2)))  # x = cos(lon)*cos(lat)
    y_p2 = Decimal(sin(math.radians(longitude2)) * cos(math.radians(latitude2)))  # y = sin(lon)*cos(lat)
    z_p2 = Decimal(sin(math.radians(latitude2)))  # z = sin(lat)
    x2 = (x_p2, y_p2, z_p2)
    '''
     2. Convert the radii r1 and r2 (which are measured along the sphere) to angles along the sphere.
     By definition, one nautical mile (NM) is 1/60 degree of arc (which is pi/180 * 1/60 = 0.0002908888 radians).
     '''
    r1 = Decimal(math.radians((radius1 / 1852) / 60))  # radius1/1852 converts meter to Nautical mile.
    r2 = Decimal(math.radians((radius2 / 1852) / 60))
    '''
     3. The geodesic circle of radius r1 around x1 is the intersection of the earth's surface with an Euclidean sphere
     of radius sin(r1) centered at cos(r1)*x1.
     4. The plane determined by the intersection of the sphere of radius sin(r1) around cos(r1)*x1 and the earth's surface
     is perpendicular to x1 and passes through the point cos(r1)x1, whence its equation is x.x1 = cos(r1)
     (the "." represents the usual dot product); likewise for the other plane. There will be a unique point x0 on the
     intersection of those two planes that is a linear combination of x1 and x2. Writing x0 = ax1 + b*x2 the two planar
     equations are;
        cos(r1) = x.x1 = (a*x1 + b*x2).x1 = a + b*(x2.x1)
        cos(r2) = x.x2 = (a*x1 + b*x2).x2 = a*(x1.x2) + b
     Using the fact that x2.x1 = x1.x2, which I shall write as q, the solution (if it exists) is given by
        a = (cos(r1) - cos(r2)*q) / (1 - q^2),
        b = (cos(r2) - cos(r1)*q) / (1 - q^2).
     '''
    q = Decimal(np.dot(x1, x2))
    if q ** 2 != 1:
        a = (Decimal(cos(r1)) - Decimal(cos(r2)) * q) / (1 - q ** 2)
        b = (Decimal(cos(r2)) - Decimal(cos(r1)) * q) / (1 - q ** 2)
        '''
         5. Now all other points on the line of intersection of the two planes differ from x0 by some multiple of a vector
         n which is mutually perpendicular to both planes. The cross product  n = x1~Cross~x2  does the job provided n is 
         nonzero: once again, this means that x1 and x2 are neither coincident nor diametrically opposite. (We need to 
         take care to compute the cross product with high precision, because it involves subtractions with a lot of
         cancellation when x1 and x2 are close to each other.)
         '''
        n = np.cross(x1, x2)
        '''
         6. Therefore, we seek up to two points of the form x0 + t*n which lie on the earth's surface: that is, their length
         equals 1. Equivalently, their squared length is 1:  
         1 = squared length = (x0 + t*n).(x0 + t*n) = x0.x0 + 2t*x0.n + t^2*n.n = x0.x0 + t^2*n.n
         '''
        x0_1 = [a * f for f in x1]
        x0_2 = [b * f for f in x2]
        x0 = [sum(f) for f in zip(x0_1, x0_2)]
        '''
           The term with x0.n disappears because x0 (being a linear combination of x1 and x2) is perpendicular to n.
           The two solutions easily are   t = sqrt((1 - x0.x0)/n.n)    and its negative. Once again high precision
           is called for, because when x1 and x2 are close, x0.x0 is very close to 1, leading to some loss of
           floating point precision.
         '''
        if (np.dot(x0, x0) <= 1) & (
                np.dot(n, n) != 0):  # This is to secure that (1 - np.dot(x0, x0)) / np.dot(n,n) > 0
            t = Decimal(sqrt((1 - np.dot(x0, x0)) / np.dot(n, n)))
            t1 = t
            t2 = -t
            i1 = x0 + t1 * n
            i2 = x0 + t2 * n
            '''
             7. Finally, we may convert these solutions back to (lat, lon) by converting geocentric (x,y,z) to geographic
             coordinates. For the longitude, use the generalized arctangent returning values in the range -180 to 180
             degrees (in computing applications, this function takes both x and y as arguments rather than just the
             ratio y/x; it is sometimes called "ATan2").
             '''
            i1_lat = math.degrees(math.asin(i1[2]))
            i1_lon = math.degrees(math.atan2(i1[1], i1[0]))
            ip1 = (i1_lat, i1_lon)
            i2_lat = math.degrees(math.asin(i2[2]))
            i2_lon = math.degrees(math.atan2(i2[1], i2[0]))
            ip2 = (i2_lat, i2_lon)
            return [ip1, ip2]
        elif np.dot(n, n) == 0:
            return "The centers of the circles can be neither the same point nor antipodal points."
        else:
            return "The circles do not intersect"
    else:
        return "The centers of the circles can be neither the same point nor antipodal points."


#create_ner_intent_json_file_with_persion_nervals()
#create_database_tables()
