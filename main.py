visibility_matrix = [ 0,-1,-1],\
                    [ 0,-1,-1],\
                    [ 0, 0,-1],\
                    [-1,-1, 0],\
                    [-1, 0, 0],\
                    [ 0, 0, 0],\
                    [ 0, 0, 0],\
                    [-1, 0,-1],\
                    [-1, 0,-1],\
                    [-1, 0, 0],\
                    [-1,-1, 0],\
                    [-1, 0, 0],\
                    [-1,-1, 0]


communication_matrix =  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],\
                        [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],\
                        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],\
                        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],\
                        [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],\
                        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],\
                        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],\
                        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],\
                        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],\
                        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],\
                        [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],\
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]


def assign(visibility_mtx):
    print("===========================================================================================================")
    sensor = get_sensor(visibility_mtx)

    if sensor is False:
        print("-> Tracking system completely solved")
        return True
    else:
        for target in range(len(visibility_mtx[0])):
            visibility_mtx[sensor[0] - 1][sensor[1]] = 1
            print("target", sensor[1] + 1, "is on progress!")
            print("Solving...")
            result = check_if_valid(visibility_mtx)
            if result:
                print("target", sensor[1] + 1, "matched!")
                print("Current state is :", visibility_mtx)
                r = assign(visibility_mtx)
                if r:
                    return True
            if result == 1:
                continue
            if result == 2:
                visibility_mtx[sensor[0] - 1][sensor[1]] = 0
                print("Current state is :", visibility_mtx)


row1 = 0
column1 = 0


def get_sensor(matrix):
    global row1
    global column1

    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if matrix[row][column] == 1:
                break
            if matrix[row][column] == 0:
                print(f'Sensor {row + 1} selected!')
                row1 = row
                column1 = column
                return row + 1, column
    return False


def check_if_valid(matrix):
    rule_1 = has_connection_with_other_sensors(matrix)
    rule_2 = is_idol(matrix)
    if rule_1 and rule_2:
        return True
    if not rule_1 and rule_2:
        return 1
    if rule_1 and not rule_2:
        return 2


def has_connection_with_other_sensors(matrix):
    counter = 0
    sens = []

    for column in range(len(matrix[0])):
        for row in range(len(matrix)):
            if matrix[row][column] == 1:
                counter += 1
                sens.append(row)

        if counter <= 1:
            return True
        counter = 0

    if communication_matrix[sens[-1]][sens[-2]] == 0:
        return True
    else:
        matrix[row1][column1] = -2
        print("-> Sensor has no useful connection, Backtracking")
        return False


def is_idol(matrix):
    counter = 0
    for row in range(len(matrix)):
        # print("Matrix ", matrix[row])
        for column in range(len(matrix[0])):
            if matrix[row][column] == 1:
                counter += 1
                # print(counter)
        if counter > 1:
            print("-> Sensor is not idle, Backtracking !")
            return False
        else:
            counter = 0
    return True


assign(visibility_matrix)
