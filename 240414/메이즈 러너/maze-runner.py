N, M, K = map(int, input().split())
miro = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    miro[i].insert(0, -1)
miro.insert(0, [-1 for _ in range(N + 1)])
man = [list(map(int, input().split())) for _ in range(M)]
door = list(map(int, input().split()))
step = 0


# 왼쪽 상단에 가까운 정사각형 우선
def find_square():  # 왼쪽 위 좌표, 변 길이 반환
    l = 2 * N + 1
    square_set = []
    for i in range(len(man)):
        if man[i][0] == -1:
            continue
        tl = max(abs(man[i][0] - door[0]) + 1, abs(man[i][1] - door[1]) + 1)
        if tl <= l:
            if tl < l:
                square_set = []
            x, y, l = 0, 0, tl
            if door[0] == man[i][0]:
                x, y = door[0] - tl + 1, min(door[1], man[i][1])
                while x <= 0:
                    x += 1
            elif door[1] == man[i][1]:
                x, y = min(door[0], man[i][0]), door[1] - tl + 1
                while y <= 0:
                    y += 1
            else:
                if abs(man[i][0] - door[0]) > abs(man[i][1] - door[1]):  # x좌표 기준 l 길이 결정
                    x, y = min(door[0], man[i][0]), max(door[1], man[i][1]) - tl + 1
                    while y <= 0:
                        y += 1
                elif abs(man[i][0] - door[0]) < abs(man[i][1] - door[1]):
                    x, y = max(door[0], man[i][0]) - tl + 1, min(door[1], man[i][1])
                    while x <= 0:
                        x += 1
                else:
                    x, y = min(door[0], man[i][0]), min(door[1], man[i][1])
            square_set.append([x, y, tl])
    return sorted(square_set)[0]


def find_direction(x, y):
    global step
    dist = abs(door[0] - x) + abs(door[1] - y)
    nx, ny = x, y
    for dx, dy in zip((0, 0, -1, 1), (-1, 1, 0, 0)):  # 상하 우선
        tx, ty = x + dx, y + dy
        if 0 < tx <= N and 0 < ty <= N:
            if miro[tx][ty] > 0:
                continue
            d = abs(door[0] - tx) + abs(door[1] - ty)
            if d <= dist:
                dist = d
                nx, ny = tx, ty
    if nx != x or ny != y:  # 움직였다면
        step += 1
    return nx, ny


def rotate(x, y, l):
    new_man, new_door = [], []
    temp = [[0 for _ in range(l)] for _ in range(l)]
    for i in range(l):
        for j in range(l):
            if miro[i + x][j + y] > 0:  # 벽 파괴
                miro[i + x][j + y] -= 1
            if door == [i + x, j + y]:
                new_door = [j + x, l - i - 1 + y]
            else:
                for m in range(len(man)):
                    if man[m] == [i + x, j + y]:
                        man[m] = [-1, -1]
                        new_man.append([j + x, l - i - 1 + y])
            temp[j][l - i - 1] = miro[i + x][j + y]
    for i in range(x, x + l):
        for j in range(y, y + l):
            miro[i][j] = temp[i - x][j - y]
    man.extend(new_man)
    door[0], door[1] = new_door[0], new_door[1]
    return


for _ in range(K):
    for i in range(len(man)):
        if man[i][0] == -1:
            continue
        man[i] = list(find_direction(man[i][0], man[i][1]))
        if man[i] == door:
            man[i] = [-1, -1]
    if sum(x[0] for x in man) == -1 * len(man):
        print(step)
        print(*door)
        exit(0)
    sx, sy, l = find_square()
    rotate(sx, sy, l)
    try:
        for i in range(len(man)):
            if man[i] == [-1, -1]:
                man.pop(i)
    except IndexError:
        pass
print(step)
print(*door)