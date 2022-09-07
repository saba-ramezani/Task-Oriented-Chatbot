import math
import sqlite3
import json
from decimal import Decimal
from math import cos, sin, sqrt
import math
import numpy as np

sensor_type = {"رادار": "radar",
               "جمر": "jammer",
               "آنتن": "antenna",
               "سنسور": "sensor"}

sensor_status = {"آفلاین": "0",
                 "آنلاین": "1"}

rank = {"سرهنگ": "sarhang",
        "سروان": "sarvan",
        "امیر": "amir"}

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

parameter = {
    "توان": "power",
    "فرکانس": "frequency",
    "آزیموت": "azimuth"
}

temp_staff_first_names = ["علی", "رضا", "حسن", "حسین", "امیر", "هادی", "مهدی", "محسن", "فرشید", "مجید",
                          "سعید", "ناصر", "نادر", "محمد", "سپهر", "عباس", "مصطفی", "جعفر", "مهرداد",
                          "مهران", "منصور", "میلاد"]
temp_staff_last_names = ["راد", "هاشمی", "نوشی", "فاضلی", "رحیمی", "صادقی", "صبوری", "افشاری", "محسنی",
                         "عدالت", "امیری", "حسینی", "حسنی", "منصوری", "ناصری", "نادری", "مرادی", "رضایی",
                         "حمیدی", "نوری"]

conn = sqlite3.connect('test.db')
print("database Opened successfully!")


# "چند سنسور از نوع # مربوط به پادگان # وجود دارد؟"
def get_sensor_count_based_on_sensor_type(sensor_type, barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select count(*) from sensors \
            where type=? and barracks_ID=?", (sensor_type, barracks_ID))
    rows = cursor.fetchall()
    if rows:
        print(str(rows[0][0]))
    else:
        print("None")
    cursor.close()


# "چند سنسور # مربوط به پادگان # وجود دارد؟"
def get_sensor_count_based_on_sensor_status(sensor_type, sensor_status, barracks_ID):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select count(*) from sensors \
                   where online=? and barracks_ID=?", (sensor_status, barracks_ID))
    else:
        cursor.execute("select count(*) from sensors \
                     where online=? and barracks_ID=? and type=?", (sensor_status, barracks_ID, sensor_type))
    rows = cursor.fetchall()
    if rows:
        print(str(rows[0][0]))
    else:
        print("None")
    cursor.close()


# "پادگان # از چه نوع است؟"
def get_type_of_barracks(barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select type from barracks \
                 where ID=?", (barracks_ID,))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("This barracks doesnt exist!")
    cursor.close()


# "پادگان # مربوط به دشمن است یا خود؟"
def is_barracks_insider(barracks_ID):
    cursor = conn.cursor()
    cursor.execute("select insider from barracks \
                 where ID=?", (barracks_ID,))
    rows = cursor.fetchall()
    if rows:
        if rows[0][0] == 1:
            print("Barracks " + str(barracks_ID) + " is insider!")
        elif rows[0][0] == 0:
            print("Barracks " + str(barracks_ID) + " is not insider!")
    else:
        print("This barracks doesnt exist!")
    cursor.close()


# "مختصات جغرافیایی پادگان # چیست؟"
def get_coordinates_of_barracks(barracks_id):
    cursor = conn.cursor()
    cursor.execute("select longitude, latitude from barracks \
                 where ID=?", (barracks_id,))
    rows = cursor.fetchall()
    if rows:
        print("longitude= " + str(rows[0][0]) + " , latitude= " + str(rows[0][1]))
    else:
        print("There is no barracks with this name")
    cursor.close()


# "آیپی سنسور # چیست؟"
def get_sensor_IP(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select ip from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select ip from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("This sensor does not exist!")
    cursor.close()


# "سنسور # از چه نوع است؟"
def get_sensor_type(sensor_id):
    cursor = conn.cursor()
    cursor.execute("select type from sensors \
                 where ID=?", (sensor_id,))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("This sensor doesnt exist!")
    cursor.close()


# "مختصات جفرافیایی سنسور # چیست؟"
def get_coordinates_of_sensor(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select longitude, latitude from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select longitude, latitude from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("This sensor doesnt exist!")
    cursor.close()


# "پارامترهای مربوط به سنسور # دارای چه مقادیری هستند؟"
def get_all_parameters_of_sensor(sensor_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select parameters from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select parameters from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("This sensor doesnt exist!")
    cursor.close()


# "پادگان های دشمن کدامند؟"
def get_enemy_barracks():
    cursor = conn.cursor()
    cursor.execute("select ID from barracks \
                 where insider=0")
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    else:
        print("There is no enemy barracks")
    cursor.close()


# "سنسورهای دشمن در پادگان # کدامند؟"
def get_enemy_sensors_based_on_barracks_id(barracks_id, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select ID from sensors \
                     where barracks_ID=? and insider=0", (barracks_id,))
    else:
        cursor.execute("select ID from sensors \
                     where barracks_ID=? and type=? and insider=0", (barracks_id, sensor_type))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Nothing found! ")
    cursor.close()


# "#های # کشور چه وضعیتی دارند؟"
def get_sensors_status_based_on_location_and_sensor_type(area, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        if area == "north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "north east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "north west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "middle north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "south east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "south west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "middle south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "middle east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "middle west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
        elif area == "center":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1")
    else:
        if area == "north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "north east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "north west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "middle north":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "south east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "south west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "middle south":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "middle east":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "middle west":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
        elif area == "center":
            cursor.execute("select ID,online from sensors \
                         where longitude > 1 and latitude > 1 and type=?", (sensor_type,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Nothing found")
    cursor.close()


# "سنسور # با چه #(پارامتر)ی کار میکند؟"
def get_parameter_of_sensor_based_on_parameter_type(sensor_id, parameter, sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select parameters from sensors \
                     where ID=?", (sensor_id,))
    else:
        cursor.execute("select parameters from sensors \
                     where ID=? and type=?", (sensor_id, sensor_type))
    cursor.execute("select parameters from sensors \
                 where ID=? and", (sensor_id,))
    rows = cursor.fetchall()
    if rows:
        parameter_dict = json.loads(rows[0][0])
        print(parameter_dict[str(parameter)])
    else:
        print("This sensor doesnt exist!")
    cursor.close()


# "حوزه استحفاظی سنسور # با حوزه استحفاظی سنسور # تداخل دارد؟"
def check_if_two_sensors_interfere(sensor_id_1, sensor_id_2, sensor_type_1, sensor_type_2):
    cursor = conn.cursor()
    if sensor_type_1 == "sensor" and sensor_type_2 == "sensor":
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
            print("This sensor doesnt exist!")
            return
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
            print("This sensor doesnt exist!")
            return
    else:
        cursor.execute("select longitude, latitude, radius from sensors \
                     where ID=? and type=?", (sensor_id_1, sensor_type_1))
        rows = cursor.fetchall()
        if rows:
            dict1 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            print("This sensor doesnt exist!")
            return
        cursor.execute("select longitude, latitude, radius from sensors \
                     where ID=? and type=?", (sensor_id_2, sensor_type_2))
        rows = cursor.fetchall()
        if rows:
            dict2 = {
                "longitude": rows[0][0],
                "latitude": rows[0][1],
                "radius": rows[0][2]
            }
        else:
            print("This sensor doesnt exist!")
            return
    cursor.close()
    if if_tow_circle_overlaps(dict1["longitude"], dict2["longitude"], dict1["latitude"], dict2["latitude"],
                              dict1["radius"], dict2["radius"]):
        print("Yes!")
        return 1
    else:
        print("No!")
        return 0


# "حوزه استحفاظی چه سنسورهایی با یکدیگر تداخل ندارد؟"
def get_all_sensors_that_do_not_interfere_based_on_sensor_type(sensor_type):
    cursor = conn.cursor()
    if sensor_type == "sensor":
        cursor.execute("select * from sensors")
    else:
        cursor.execute("select * from sensors \
                     where type=?", (sensor_type,))
    rows = cursor.fetchall()
    if rows:
        rows2 = rows.copy()
        for i in rows:
            for j in rows2:
                if i[0] != j[0]:
                    if not if_tow_circle_overlaps(i[3], j[3], i[4], j[4], i[5], j[5]):
                        print(i)
                        print("and")
                        print(j)
                        print("********")
    else:
        print("Nothing found!")
    cursor.close()


# "تعداد سرهنگ های پادگان # چندتاست؟"
def get_count_of_barracks_staff_based_on_rank(barracks_name, rank):
    cursor = conn.cursor()
    cursor.execute("select count(name) from staff \
                 where barracks_ID=? and rank=?", (barracks_name, rank))
    rows = cursor.fetchall()
    if rows:
        print(rows[0][0])
    cursor.close()


# "ُسرهنگ # در کدام پادگان حضور دارد؟"
def get_barracks_name_of_a_staff(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select barracks_ID, first_name, last_name from staff \
                 where rank=?", (rank, ))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            if row[2] == staff_name:
                print(row[0])
                return
            elif str(row[1]) + " " + str(row[2]) == staff_name:
                print(row[0])
                return
    print(rank + " " + staff_name + " does not exist!")
    cursor.close()


# "سطح دسترسی سرهنگ # چیست؟"
def get_access_level_of_a_staff(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select access_level, first_name, last_name from staff \
                 where rank=?", (rank, ))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            if row[2] == staff_name:
                print(row[0])
                return
            elif str(row[1]) + " " + str(row[2]) == staff_name:
                print(row[0])
                return
    print(rank + " " + staff_name + " does not exist!")
    cursor.close()


# "سرهنگ # فعال است یا بلاک؟"
def is_staff_active(staff_name, rank):
    cursor = conn.cursor()
    cursor.execute("select active from staff \
                 where name=? and rank=?", (staff_name, rank))
    rows = cursor.fetchall()
    if rows:
        if rows[0][0] == 1:
            print(rank + " " + staff_name + " is active!")
        elif rows[0][0] == 0:
            print(rank + " " + staff_name + " is blocked!")
    else:
        print(rank + " " + staff_name + " does not exist!")
    cursor.close()


def create_json_files_part_one():
    train_list = []
    ner_intent_dict = {}
    intent_dict = {}
    ner_dict = {}
    for i in range(1, 101):
        for key in sensor_type:
            if sensor_type != "سنسور":
                # "چند سنسور از نوع رادار مربوط به پادگان 1 وجود دارد؟"
                text = "چند سنسور از نوع " + str(key) + " مربوط به پادگان " + str(i) + " وجود دارد؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"sensor_type_1": str(key),
                              "barracks_name_1": str(i)},
                    "query": {"intent": "get_sensor_count_based_on_sensor_type",
                              "sensor_type_1": str(sensor_type[key]),
                              "barracks_name_1": str(i)}
                }
                train_list.append(train_dict)
                # ner_intent
                ner_intent = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "O",
                        "O",
                        "O",
                        "O",
                        "B-sensor_type-1",
                        "O",
                        "O",
                        "O",
                        "B-barracks_name_1",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type_1": str(sensor_type[key]),
                        "barracks_name_1": str(i)
                    },
                    "INTENTS": [
                        "get_sensor_count_based_on_sensor_type"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["get_sensor_count_based_on_sensor_type"]}
                intent_dict[text] = intent
                # ner
                ner = {
                    "TEXT": text.split(),
                    "NERTAGS": [
                        "O",
                        "O",
                        "O",
                        "O",
                        "B-sensor_type-1",
                        "O",
                        "O",
                        "O",
                        "B-barracks_name_1",
                        "O",
                        "O"
                    ],
                    "NERVALS": {
                        "sensor_type_1": str(sensor_type[key]),
                        "barracks_name_1": str(i)
                    }
                }
                ner_dict[text] = ner

            # "آیپی سنسور 1 چیست؟"
            text = "آیپی " + str(key) + " " + str(i) + " چیست؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"sensor_name_1": str(i),
                          "sensor_type_1": str(key)},
                "query": {"intent": "get_sensor_IP",
                          "sensor_name_1": str(i),
                          "sensor_type_1": str(sensor_type[key])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key])
                },
                "INTENTS": [
                    "get_sensor_IP"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_sensor_IP"]}
            intent_dict[text] = intent
            # ner
            ner = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-sensor_type_1",
                    "B-sensor_name_1",
                    "O"
                ],
                "NERVALS": {
                    "sensor_name_1": str(i),
                    "sensor_type_1": str(sensor_type[key])
                }
            }
            ner_dict[text] = ner

            # "مختصات جغرافیایی سنسور 1 چیست؟"
            text = "مختصات جغرافیایی " + str(key) + " " + str(i) + " چیست؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"sensor_name_1": str(i),
                          "sensor_type_1": str(key)},
                "query": {"intent": "get_coordinates_of_sensor",
                          "sensor_name_1": str(i),
                          "sensor_type_1": str(sensor_type[key])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key])
                },
                "INTENTS": [
                    "get_coordinates_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_coordinates_of_sensor"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "sensor_type_1": str(sensor_type[key])
                }
            }
            ner_dict[text] = ner

            # "پارامترهای مربوط به سنسور 1 دارای چه مقادیری هستند؟"
            text = "پارامترهای مربوط به " + str(key) + " " + str(i) + " دارای چه مقادیری هستند؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"sensor_name_1": str(i),
                          "sensor_type_1": str(key)},
                "query": {"intent": "get_all_parameters_of_sensor",
                          "sensor_name_1": str(i),
                          "sensor_type_1": str(sensor_type[key])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key])
                },
                "INTENTS": [
                    "get_all_parameters_of_sensor"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_all_parameters_of_sensor"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "sensor_type_1": str(sensor_type[key])
                }
            }
            ner_dict[text] = ner

            # "سنسورهای دشمن در پادگان 1 کدامند؟"
            text = str(key) + " های دشمن در پادگان " + str(i) + " کدامند؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"barracks_name_1": str(i),
                          "sensor_type_1": str(key)},
                "query": {"intent": "get_enemy_sensors_based_on_barracks_id",
                          "barracks_name_1": str(i),
                          "sensor_type_1": str(sensor_type[key])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key])
                },
                "INTENTS": [
                    "get_enemy_sensors_based_on_barracks_id"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_enemy_sensors_based_on_barracks_id"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "sensor_type_1": str(sensor_type[key])
                }
            }
            ner_dict[text] = ner

            for key2 in parameter:
                # "رادار 1 با چه فرکانسی کار می کند؟"
                text = str(key) + " " + str(i) + " با چه " + str(key2) + " ای کار می کند؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"sensor_name_1": str(i),
                              "parameter": str(key2),
                              "sensor_type_1": str(key)},
                    "query": {"intent": "get_parameter_of_sensor_based_on_parameter_type",
                              "sensor_name_1": str(i),
                              "parameter": str(parameter[key2]),
                              "sensor_type_1": str(sensor_type[key])}
                }
                train_list.append(train_dict)
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
                        "sensor_type": str(sensor_type[key]),
                        "sensor_name": str(i),
                        "parameter": str(parameter[key2])
                    },
                    "INTENTS": [
                        "get_parameter_of_sensor_based_on_parameter_type"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["get_parameter_of_sensor_based_on_parameter_type"]}
                intent_dict[text] = intent
                # ner
                ner = {
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
                        "sensor_type": str(sensor_type[key]),
                        "sensor_name": str(i),
                        "parameter": str(parameter[key2])
                    }
                }
                ner_dict[text] = ner

            for key2 in sensor_status:
                # "چند سنسور آنلاین مربوط به پادگان 1 وجود دارد؟"
                text = "چند " + str(key) + " " + str(key2) + " مربوط به پادگان " + str(i) + " وجود دارد؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"sensor_type_1": str(key),
                              "sensor_status_1": str(key2),
                              "barracks_name_1": str(i)},
                    "query": {"intent": "get_sensor_count_based_on_sensor_status",
                              "sensor_type_1": str(sensor_type[key]),
                              "sensor_status_1": str(sensor_status[key2]),
                              "barracks_name_1": str(i)}
                }
                train_list.append(train_dict)
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
                        "sensor_type_1": str(sensor_type[key]),
                        "sensor_status_1": str(sensor_status[key2]),
                        "barracks_name_1": str(i)
                    },
                    "INTENTS": [
                        "get_sensor_count_based_on_sensor_status"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["get_sensor_count_based_on_sensor_status"]}
                intent_dict[text] = intent
                # ner
                ner = {
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
                        "sensor_type_1": str(sensor_type[key]),
                        "sensor_status_1": str(sensor_status[key2]),
                        "barracks_name_1": str(i)
                    }
                }
                ner_dict[text] = ner

        # "پادگان 1 از چه نوع است؟"
        text = "پادگان " + str(i) + " از چه نوع است؟ "
        # train
        train_dict = {
            "text": text,
            "slots": {"barracks_name_1": str(i)},
            "query": {"intent": "get_type_of_barracks",
                      "barracks_name_1": str(i)}
        }
        train_list.append(train_dict)
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
        intent = {"INTENTS": ["get_type_of_barracks"]}
        intent_dict[text] = intent
        # ner
        ner = {
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
            }
        }
        ner_dict[text] = ner

        # "پادگان 1 مربوط به دشمن است یا خود؟"
        text = "پادگان " + str(i) + " مربوط به دشمن است یا خود؟ "
        # train
        train_dict = {
            "text": text,
            "slots": {"barracks_name_1": str(i)},
            "query": {"intent": "is_barracks_insider",
                      "barracks_name_1": str(i)}
        }
        train_list.append(train_dict)
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
        intent = {"INTENTS": ["is_barracks_insider"]}
        intent_dict[text] = intent
        # ner
        ner = {
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
            }
        }
        ner_dict[text] = ner

        # "مختصات جغرافیایی پادگان 1 چیست؟"
        text = "مختصات جغرافیایی پادگان " + str(i) + " چیست؟ "
        # train
        train_dict = {
            "text": text,
            "slots": {"barracks_name_1": str(i)},
            "query": {"intent": "get_coordinates_of_barracks",
                      "barracks_name_1": str(i)}
        }
        train_list.append(train_dict)
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
        intent = {"INTENTS": ["get_coordinates_of_barracks"]}
        intent_dict[text] = intent
        # ner
        ner = {
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
            }
        }
        ner_dict[text] = ner

        # "سنسور 1 از چه نوع است؟"
        text = "سنسور " + str(i) + " از چه نوع است؟ "
        # train
        train_dict = {
            "text": text,
            "slots": {"sensor_name_1": str(i)},
            "query": {"intent": "get_sensor_type",
                      "sensor_name_1": str(i)}
        }
        train_list.append(train_dict)
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
        intent = {"INTENTS": ["get_sensor_type"]}
        intent_dict[text] = intent
        # ner
        ner = {
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
            }
        }
        ner_dict[text] = ner

        # "پادگان های دشمن کدامند؟"
        text = "پادگان های دشمن کدامند؟ "
        # train
        train_dict = {
            "text": text,
            "slots": {},
            "query": {"intent": "get_enemy_barracks"}
        }
        train_list.append(train_dict)
        # ner_intent
        ner_intent = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
            },
            "INTENTS": [
                "get_enemy_barracks"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        intent = {"INTENTS": ["get_enemy_barracks"]}
        intent_dict[text] = intent
        # ner
        ner = {
            "TEXT": text.split(),
            "NERTAGS": [
                "O",
                "O",
                "O",
                "O"
            ],
            "NERVALS": {
            }
        }
        ner_dict[text] = ner

    print("part 1 train_list size: " + str(len(train_list)))
    with open('./trainset_files/trainset_part1.json', 'w', encoding='utf8') as json_file:
        json.dump(train_list, json_file, indent=6, ensure_ascii=False)
    print("part 1 ner_intent_dict size: " + str(len(train_list)))
    with open('./ner_intent_files/ner_intent_part1.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 1 intent_dict size: " + str(len(train_list)))
    with open('./intent_files/intent_part1.json', 'w', encoding='utf8') as json_file:
        json.dump(intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 1 ner_dict size: " + str(len(train_list)))
    with open('./ner_files/ner_part1.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_dict, json_file, indent=6, ensure_ascii=False)


def create_json_files_part_two():
    train_list = []
    ner_intent_dict = {}
    intent_dict = {}
    ner_dict = {}
    for key2 in one_part_area:
        for key in sensor_type:
            # "رادارهای جنوب کشور چه وضعیتی دارند؟"
            text = str(key) + " های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"sensor_type_1": str(key),
                          "area": str(key2)},
                "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
                          "sensor_type_1": str(sensor_type[key]),
                          "area": str(one_part_area[key2])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key]),
                    "area": str(one_part_area[key2])
                },
                "INTENTS": [
                    "get_enemy_sensors_based_on_barracks_id"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "sensor_type_1": str(sensor_type[key]),
                    "area": str(one_part_area[key2])
                }
            }
            ner_dict[text] = ner

    for key2 in two_part_area:
        for key in sensor_type:
            # "رادارهای جنوب شرقی کشور چه وضعیتی دارند؟"
            text = str(key) + " های " + str(key2) + " کشور چه وضعیتی دارند؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"sensor_type_1": str(key),
                          "area": str(key2)},
                "query": {"intent": "get_sensors_status_based_on_location_and_sensor_type",
                          "sensor_type_1": str(sensor_type[key]),
                          "area": str(two_part_area[key2])}
            }
            train_list.append(train_dict)
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
                    "sensor_type_1": str(sensor_type[key]),
                    "area": str(two_part_area[key2])
                },
                "INTENTS": [
                    "get_sensors_status_based_on_location_and_sensor_type"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_sensors_status_based_on_location_and_sensor_type"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "sensor_type_1": str(sensor_type[key]),
                    "area": str(two_part_area[key2])
                }
            }
            ner_dict[text] = ner

    print("part 2 train_list size: " + str(len(train_list)))
    with open('./trainset_files/trainset_part2.json', 'w', encoding='utf8') as json_file:
        json.dump(train_list, json_file, indent=6, ensure_ascii=False)
    print("part 2 ner_intent_dict size: " + str(len(train_list)))
    with open('./ner_intent_files/ner_intent_part2.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 2 intent_dict size: " + str(len(train_list)))
    with open('./intent_files/intent_part2.json', 'w', encoding='utf8') as json_file:
        json.dump(intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 2 ner_dict size: " + str(len(train_list)))
    with open('./ner_files/ner_part2.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_dict, json_file, indent=6, ensure_ascii=False)


def create_json_files_part_three():
    train_list = []
    ner_intent_dict = {}
    intent_dict = {}
    ner_dict = {}
    for key in range(1, 51):
        for key2 in range(1, 101):
            for type1 in sensor_type:
                for type2 in sensor_type:
                    # "حوزه استحفاظی رادار 1 با حوزه استحفاظی آنتن 2 تداخل دارد؟"
                    text = "حوزه استحفاظی " + str(type1) + " " + str(key) + " با حوزه استحفاظی " + str(
                        type2) + " " + str(key2) + " تداخل دارد؟"
                    # train
                    train_dict = {
                        "text": text,
                        "slots": {"sensor_name_1": str(key),
                                  "sensor_name_2": str(key2),
                                  "sensor_type_1": str(type1),
                                  "sensor_type_2": str(type2)},
                        "query": {"intent": "check_if_two_sensors_interfere",
                                  "sensor_type_1": str(sensor_type[type1]),
                                  "sensor_type_2": str(sensor_type[type2]),
                                  "sensor_name_1": str(key),
                                  "sensor_name_2": str(key2)}
                    }
                    train_list.append(train_dict)
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
                            "sensor_type_1": str(sensor_type[type1]),
                            "sensor_type_2": str(sensor_type[type2])
                        },
                        "INTENTS": [
                            "check_if_two_sensors_interfere"
                        ]
                    }
                    ner_intent_dict[text] = ner_intent
                    # intent
                    intent = {"INTENTS": ["check_if_two_sensors_interfere"]}
                    intent_dict[text] = intent
                    # ner
                    ner = {
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
                            "sensor_type_1": str(sensor_type[type1]),
                            "sensor_type_2": str(sensor_type[type2])
                        }
                    }
                    ner_dict[text] = ner

    print("part 3 train_list size: " + str(len(train_list)))
    with open('./trainset_files/trainset_part3.json', 'w', encoding='utf8') as json_file:
        json.dump(train_list, json_file, indent=6, ensure_ascii=False)
    print("part 3 ner_intent_dict size: " + str(len(train_list)))
    with open('./ner_intent_files/ner_intent_part3.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 3 ner_intent_dict size: " + str(len(train_list)))
    with open('./intent_files/intent_part3.json', 'w', encoding='utf8') as json_file:
        json.dump(intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 3 ner_dict size: " + str(len(train_list)))
    with open('./ner_files/ner_part3.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_dict, json_file, indent=6, ensure_ascii=False)


def create_json_files_part_four():
    train_list = []
    ner_intent_dict = {}
    intent_dict = {}
    ner_dict = {}
    for key in range(51, 101):
        for key2 in range(1, 101):
            for type1 in sensor_type:
                for type2 in sensor_type:
                    # "حوزه استحفاظی رادار 1 با حوزه استحفاظی آنتن 2 تداخل دارد؟"
                    text = "حوزه استحفاظی " + str(type1) + " " + str(key) + " با حوزه استحفاظی " + str(
                        type2) + " " + str(key2) + " تداخل دارد؟"
                    # train
                    train_dict = {
                        "text": text,
                        "slots": {"sensor_name_1": str(key),
                                  "sensor_name_2": str(key2),
                                  "sensor_type_1": str(type1),
                                  "sensor_type_2": str(type2)},
                        "query": {"intent": "check_if_two_sensors_interfere",
                                  "sensor_type_1": str(sensor_type[type1]),
                                  "sensor_type_2": str(sensor_type[type2]),
                                  "sensor_name_1": str(key),
                                  "sensor_name_2": str(key2)}
                    }
                    train_list.append(train_dict)
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
                            "sensor_type_1": str(sensor_type[type1]),
                            "sensor_type_2": str(sensor_type[type2])
                        },
                        "INTENTS": [
                            "check_if_two_sensors_interfere"
                        ]
                    }
                    ner_intent_dict[text] = ner_intent
                    # intent
                    intent = {"INTENTS": ["check_if_two_sensors_interfere"]}
                    intent_dict[text] = intent
                    # ner
                    ner = {
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
                            "sensor_type_1": str(sensor_type[type1]),
                            "sensor_type_2": str(sensor_type[type2])
                        }
                    }
                    ner_dict[text] = ner

    print("part 4 train_list size: " + str(len(train_list)))
    with open('./trainset_files/trainset_part4.json', 'w', encoding='utf8') as json_file:
        json.dump(train_list, json_file, indent=6, ensure_ascii=False)
    print("part 4 ner_intent_dict size: " + str(len(train_list)))
    with open('./ner_intent_files/ner_intent_part4.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 4 intent_dict size: " + str(len(train_list)))
    with open('./intent_files/intent_part4.json', 'w', encoding='utf8') as json_file:
        json.dump(intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 4 ner_dict size: " + str(len(train_list)))
    with open('./ner_files/ner_part4.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_dict, json_file, indent=6, ensure_ascii=False)


def create_json_files_part_five():
    train_list = []
    ner_intent_dict = {}
    intent_dict = {}
    ner_dict = {}
    for key in sensor_type:
        # "حوزه استحفاظی چه رادارهایی با هم تداخل ندارند؟"
        text = "حوزه استحفاظی چه " + str(key) + " هایی با هم نداخل ندارند؟"
        # train
        train_dict = {
            "text": text,
            "slots": {"sensor_type_1": str(key)},
            "query": {"intent": "get_all_sensors_that_do_not_interfere_based_on_sensor_type",
                      "sensor_type_1": str(sensor_type[key])}
        }
        train_list.append(train_dict)
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
                "sensor_type_1": str(sensor_type[key])
            },
            "INTENTS": [
                "get_all_sensors_that_do_not_interfere_based_on_sensor_type"
            ]
        }
        ner_intent_dict[text] = ner_intent
        # intent
        intent = {"INTENTS": ["get_all_sensors_that_do_not_interfere_based_on_sensor_type"]}
        intent_dict[text] = intent
        # ner
        ner = {
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
                "sensor_type_1": str(sensor_type[key])
            }
        }
        ner_dict[text] = ner

    for key in rank:
        for i in range(1, 101):
            # "تعداد سرهنگ های پادگان 1 چند تاست؟"
            text = "تعداد " + str(key) + " های پادگان " + str(i) + "چندتاست؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"barracks_name_1": str(i),
                          "rank": str(key)},
                "query": {"intent": "get_count_of_barracks_staff_based_on_rank",
                          "barracks_name_1": str(i),
                          "rank": str(rank[key])}
            }
            train_list.append(train_dict)
            # ner_intent
            ner_intent = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-rank",
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "rank": str(rank[key])
                },
                "INTENTS": [
                    "get_count_of_barracks_staff_based_on_rank"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_count_of_barracks_staff_based_on_rank"]}
            intent_dict[text] = intent
            # ner
            ner = {
                "TEXT": text.split(),
                "NERTAGS": [
                    "O",
                    "B-rank",
                    "O",
                    "O",
                    "B-barracks_name_1",
                    "O",
                    "O"
                ],
                "NERVALS": {
                    "barracks_name_1": str(i),
                    "rank": str(rank[key])
                }
            }
            ner_dict[text] = ner

        for ln in temp_staff_last_names:
            # "سرهنگ امیری در کدام پادگان حضور دارد؟"
            text = str(key) + " " + str(ln) + " در کدام پادگان حضور دارد؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"staff_name": str(ln),
                          "rank": str(key)},
                "query": {"intent": "get_barracks_name_of_a_staff",
                          "staff_name": str(ln),
                          "rank": str(rank[key])}
            }
            train_list.append(train_dict)
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
                    "rank": str(rank[key])
                },
                "INTENTS": [
                    "get_barracks_name_of_a_staff"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_barracks_name_of_a_staff"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "rank": str(rank[key])
                }
            }
            ner_dict[text] = ner

            # "سطح دسترسی سرهنگ امیری چیست؟"
            text = "سطح دسترسی " + str(key) + " " + str(ln) + " چیست؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"staff_name": str(ln),
                          "rank": str(key)},
                "query": {"intent": "get_access_level_of_a_staff",
                          "staff_name": str(ln),
                          "rank": str(rank[key])}
            }
            train_list.append(train_dict)
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
                    "rank": str(rank[key])
                },
                "INTENTS": [
                    "get_access_level_of_a_staff"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["get_access_level_of_a_staff"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "rank": str(rank[key])
                }
            }
            ner_dict[text] = ner

            # "ُسرهنگ امیری فعال است یا بلاک؟"
            text = str(key) + " " + str(ln) + " فعال است یا بلاک؟"
            # train
            train_dict = {
                "text": text,
                "slots": {"staff_name": str(ln),
                          "rank": str(key)},
                "query": {"intent": "is_staff_active",
                          "staff_name": str(ln),
                          "rank": str(rank[key])}
            }
            train_list.append(train_dict)
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
                    "rank": str(rank[key])
                },
                "INTENTS": [
                    "is_staff_active"
                ]
            }
            ner_intent_dict[text] = ner_intent
            # intent
            intent = {"INTENTS": ["is_staff_active"]}
            intent_dict[text] = intent
            # ner
            ner = {
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
                    "rank": str(rank[key])
                }
            }
            ner_dict[text] = ner

            for fn in temp_staff_first_names:
                # "ُسرهنگ رضا امیری در کدام پادگان حضور دارد؟"
                text = str(key) + " " + str(ln) + " " + str(fn) + " در کدام پادگان حضور دارد؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"staff_name": str(fn) + " " + str(ln),
                              "rank": str(key)},
                    "query": {"intent": "get_barracks_name_of_a_staff",
                              "staff_name": str(fn) + " " + str(ln),
                              "rank": str(rank[key])}
                }
                train_list.append(train_dict)
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
                        "rank": str(rank[key])
                    },
                    "INTENTS": [
                        "get_barracks_name_of_a_staff"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["get_barracks_name_of_a_staff"]}
                intent_dict[text] = intent
                # ner
                ner = {
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
                        "rank": str(rank[key])
                    }
                }
                ner_dict[text] = ner

                # "سطح دسترسی سرهنگ رضا امیری چیست؟"
                text = "سطح دسترسی " + str(key) + " " + str(fn) + " " + str(ln) + " چیست؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"staff_name": str(fn) + " " + str(ln),
                              "rank": str(key)},
                    "query": {"intent": "get_access_level_of_a_staff",
                              "staff_name": str(fn) + " " + str(ln),
                              "rank": str(rank[key])}
                }
                train_list.append(train_dict)
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
                        "rank": str(rank[key])
                    },
                    "INTENTS": [
                        "get_access_level_of_a_staff"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["get_access_level_of_a_staff"]}
                intent_dict[text] = intent
                # ner
                ner = {
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
                        "rank": str(rank[key])
                    }
                }
                ner_dict[text] = ner

                # "سرهنگ رضا امیری فعال است یا بلاک؟"
                text = str(key) + " " + str(fn) + " " + str(ln) + " فعال است یا بلاک؟"
                # train
                train_dict = {
                    "text": text,
                    "slots": {"staff_name": str(fn) + " " + str(ln),
                              "rank": str(key)},
                    "query": {"intent": "is_staff_active",
                              "staff_name": str(fn) + " " + str(ln),
                              "rank": str(rank[key])}
                }
                train_list.append(train_dict)
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
                        "rank": str(rank[key])
                    },
                    "INTENTS": [
                        "is_staff_active"
                    ]
                }
                ner_intent_dict[text] = ner_intent
                # intent
                intent = {"INTENTS": ["is_staff_active"]}
                intent_dict[text] = intent
                # ner
                ner = {
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
                        "rank": str(rank[key])
                    }
                }
                ner_dict[text] = ner

    print("part 5 train_list size: " + str(len(train_list)))
    with open('./trainset_files/trainset_part5.json', 'w', encoding='utf8') as json_file:
        json.dump(train_list, json_file, indent=6, ensure_ascii=False)
    print("part 5 ner_intent_dict size: " + str(len(train_list)))
    with open('./ner_intent_files/ner_intent_part5.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 5 ner_intent_dict size: " + str(len(train_list)))
    with open('./intent_files/intent_part5.json', 'w', encoding='utf8') as json_file:
        json.dump(intent_dict, json_file, indent=6, ensure_ascii=False)
    print("part 5 ner_dict size: " + str(len(train_list)))
    with open('./ner_files/ner_part5.json', 'w', encoding='utf8') as json_file:
        json.dump(ner_dict, json_file, indent=6, ensure_ascii=False)


def create_all_json_files():
    create_json_files_part_one()
    create_json_files_part_two()
    create_json_files_part_three()
    create_json_files_part_four()
    create_json_files_part_five()


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


# create_all_json_files()
# cursor = conn.execute('select * from links')
# names = list(map(lambda x: x[0], cursor.description))
# conn.close()
# print(names)

