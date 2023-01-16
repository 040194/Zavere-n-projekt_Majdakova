import mysql.connector
from mysql.connector import connect, Error




def load_all_sensors():
    """
        Funkcia nacita vsetky existujuce senzory a ich najposlednejsie hodnoty
        Vracia list of JSON elements
    """


    HOST="localhost"
    USER="db"
    PWD="pass"
    DATABASE="project"


    all_sensors=[]
    # print(type(all_sensors))

    try:
        # skusam sa pripojit do DB
        my_db = connect(host=HOST, user=USER, password=PWD, database=DATABASE) 
        cursor = my_db.cursor()

        query = """
            select rooms.room_id, sensors.sensor_id, sensor_type, sensor_value, sensor_unit, MAX(time_stamp) 
            from rooms inner join sensors on sensors.sensor_id = rooms.sensor_id 
            group by room_id, sensor_type;
                """
        cursor.execute(query)
        available_sensors = cursor.fetchall()

        # prejdem vsetkymi vysledkami 'available_sensors' z DB 
        # a spravim z kazdeho JSON 'sensor' (=dictionary)
        # a hotovy element pridam do tuple 'all_sensors'
        for single_sensor in available_sensors:
            # print(single_sensor)    # test print
            sensor = {
                "room_id": single_sensor[0],
                "sensor_id": single_sensor[1],
                "sensor_type": single_sensor[2],
                "sensor_value": single_sensor[3], 
                "sensor_unit": single_sensor[4], 
                "latest_datetime": single_sensor[5]
            }
            #print(sensor)           # test print
            #print(type(sensor))
            
            all_sensors.append(sensor)

        # slusne uzavriem spojenie do DB
        cursor.close()

        return all_sensors


    except Error as e:
        print(e)
    


def store_sensor_data(sensor_id, room, type, value):


    HOST="localhost"
    USER="db"
    PWD="pass"
    DATABASE="project"



    last_id = None
    try:
        # skusam sa pripojit do DB
        tuple_sensor = (sensor_id, type, value)
        my_db = connect(host=HOST, user=USER, password=PWD, database=DATABASE)
        cursor = my_db.cursor()
        cursor.execute ("""INSERT INTO sensors (sensor_id, sensor_type, sensor_value) VALUES (%s, %s, %s);""",
	tuple_sensor)
        cursor.execute("""COMMIT;""")
        last_id = cursor.lastrowid
        cursor.close()
    except Error as e:
        print(e)

    return last_id


def get_room_data(room_id):

    # expecting no sensors for the room
    room_sensors = []


    HOST="localhost"
    USER="db"
    PWD="pass"
    DATABASE="project"


    # joining all sensors for particular room_id
    query = f"""
        select rooms.room_id, sensors.sensor_id, sensor_type, sensor_value, MAX(time_stamp) 
        from rooms inner join sensors on sensors.sensor_id = rooms.sensor_id
        where rooms.room_id = '{room_id}'
        group by room_id, sensor_type;
        """

    try:
        # skusam sa pripojit do DB
        my_db = connect(host=HOST, user=USER, password=PWD, database=DATABASE) 
        cursor = my_db.cursor()

        cursor.execute(query)
        available_sensors = cursor.fetchall()

        for single_sensor in available_sensors:
            sensor = {
                "room_id": single_sensor[0],
                "sensor_id": single_sensor[1],
                "sensor_type": single_sensor[2],
                "sensor_value": single_sensor[3],
                "latest_datetime": single_sensor[4]
            }
           # print(type(sensor))

            room_sensors.append(sensor)

        # slusne uzavriem spojenie do DB
        cursor.close()

    except Error as e:
        print(e)

    return room_sensors


if __name__ == "__main__":

   print()
