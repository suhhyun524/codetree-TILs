N, M, P, C, D = map(int, input().split())
R = list(map(int, input().split()))
santa = [[0, 0, 0, 0] for _ in range(P + 1)]
score = [0 for _ in range(P + 1)]
for _ in range(P):
    num, x, y = map(int, input().split())
    santa[num] = [num, x, y, -1]
santa.pop(0)


def find_direction(x, y, R):  # 상우하좌
    direction = [0, 0]
    dist = (R[0] - x) ** 2 + (R[1] - y) ** 2
    for nx, ny in zip((x - 1, x, x + 1, x), (y, y + 1, y, y - 1)):  # 상우하좌
        d = (R[0] - nx) ** 2 + (R[1] - ny) ** 2
        if d < dist:
            for s in santa:
                if s[1] == nx and s[2] == ny:
                    break
            else:
                dist = d
                direction = [nx - x, ny - y]
        if d == dist:
            if direction[0] != -1:
                if nx - x == -1:
                    direction = [nx - x, ny - y]
                elif nx - x == 0 and ny - y == 1:
                    direction = [nx - x, ny - y]
                elif direction[1] != 1 and nx - x == 1 and ny - y == 0:
                    direction = [nx - x, ny - y]
    return direction


def interaction(n, x, y, direc):
    for i in range(len(santa)):
        if santa[i][0] != -1 and santa[i][0] != n and santa[i][1] == x and santa[i][2] == y:
            santa[i][1] += direc[0]
            santa[i][2] += direc[1]
            # 게임판 밖 확인
            if not 0 < santa[i][1] <= N or not 0 < santa[i][2] <= N:
                santa[i] = [-1, -1, -1, True]
            else:
                interaction(santa[i][0], santa[i][1], santa[i][2], direc)
                return True
    else:
        return False


def crush(num, x, y, direc, t):
    if num == 0:  # 루돌프 이동
        for i in range(len(santa)):
            if santa[i][0] == -1:
                continue
            n, sx, sy = santa[i][0], santa[i][1], santa[i][2]
            if sx == x and sy == y:
                santa[i][3] = t + 1
                score[n] += C
                # 산타 이동
                santa[i][1] += C * direc[0]
                santa[i][2] += C * direc[1]
                # 게임판 밖 확인
                if not 0 < santa[i][1] <= N or not 0 < santa[i][2] <= N:
                    santa[i] = [-1, -1, -1, True]  # 산타 방출
                # 상호작용 확인
                else:
                    interaction(n, santa[i][1], santa[i][2], direc)
    else:
        if x == R[0] and y == R[1]:
            for i in range(len(santa)):
                if santa[i][0] == -1:
                    continue
                if santa[i][0] == num:
                    santa[i][3] = t + 1
                    score[num] += D
                    # 산타 이동
                    santa[i][1] -= direc[0] * D
                    santa[i][2] -= direc[1] * D
                    # 게임판 밖 확인
                    if not 0 < santa[i][1] <= N or not 0 < santa[i][2] <= N:
                        santa[i] = [-1, -1, -1, True]  # 산타 방출
                    # 상호작용 확인
                    else:
                        interaction(santa[i][0], santa[i][1], santa[i][2], [-direc[0], -direc[1]])
                    break


def move_r(R, t):
    x, y = R[0], R[1]
    target_santa = [0, 0]
    direction = [0, 0]
    dist = int(1e9)
    # 타겟 산타 결정
    for n, sx, sy, state in santa:
        if n == -1:
            continue
        d = abs(x - sx) ** 2 + abs(y - sy) ** 2
        if d < dist:
            dist = d
            target_santa[0], target_santa[1] = sx, sy
        elif d == dist:
            if target_santa[0] < sx or target_santa[0] == sx and target_santa[1] < sy:
                target_santa[0], target_santa[1] = sx, sy
    # 움직일 방향 결정
    if x < target_santa[0]:
        direction[0] = 1
    elif x == target_santa[0]:
        direction[0] = 0
    else:
        direction[0] = -1
    if y < target_santa[1]:
        direction[1] = 1
    elif y == target_santa[1]:
        direction[1] = 0
    else:
        direction[1] = -1
    # 루돌프 이동
    R[0] += direction[0]
    R[1] += direction[1]
    # 충돌탐지
    crush(0, R[0], R[1], direction, t)


def move_s(santa, t):
    for i in range(len(santa)):
        if santa[i][0] == -1:
            continue
        n, sx, sy, state = santa[i][0], santa[i][1], santa[i][2], santa[i][3]
        if state >= t:
            continue
        else:
            # 움직일 방향 결정
            direction = find_direction(sx, sy, R)
            santa[i][1] += direction[0]
            santa[i][2] += direction[1]
            crush(n, santa[i][1], santa[i][2], direction, t)


for t in range(M):
    move_r(R, t)
    move_s(santa, t)
    if sum(x[0] for x in santa) == -1 * P:
        for i in range(1, P + 1):
            print(score[i], end=" ")
        exit(0)
    for i in range(len(santa)):
        if santa[i][0] == -1:
            continue
        score[santa[i][0]] += 1
for i in range(1, P + 1):
    print(score[i], end=" ")