L, N, Q = map(int, input().split())
knight = [[0, 0, 0, 0, 0, 0] for _ in range(N + 1)]
command = []
dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
chess = [list(map(int, input().split())) for _ in range(L)]
occupy = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
temp_damage = [0 for _ in range(N + 1)]
for i in range(L):
    chess[i].insert(0, 0)
chess.insert(0, [0 for _ in range(L + 1)])
for i in range(1, N + 1):
    # x, y, x범위, y범위, 체력
    r, c, h, w, k = map(int, input().split())
    knight[i] = [r, c, h, w, k, 0]
for _ in range(Q):
    # d는 0, 1, 2, 3 중에 하나이며 각각 위쪽, 오른쪽, 아래쪽, 왼쪽 방향
    i, d = map(int, input().split())
    command.append([i, d])


def damage(idx):
    x_s, x_e, y_s, y_e = knight[idx][0], knight[idx][0] + knight[idx][2], knight[idx][1], knight[idx][1] + knight[idx][
        3]
    count = 0
    for j in range(y_s, y_e):
        for i in range(x_s, x_e):
            if chess[i][j] == 1:
                count += 1
    temp_damage[idx] = count


def pull(now, idx, direc):
    if knight[idx][0] == -1:
        return
    knight[idx][0], knight[idx][1] = knight[idx][0] + dx[direc], knight[idx][1] + dy[direc]
    if now == idx:
        return
    damage(idx)


def movable(now, i, direc, visited):
    nx, ny = knight[i][0] + dx[direc], knight[i][1] + dy[direc]
    x_s, x_e, y_s, y_e = nx, nx + knight[i][2], ny, ny + knight[i][3]
    for y in range(y_s, y_e):
        for x in range(x_s, x_e):
            if (not (0 < x <= L and 0 < y <= L) or chess[x][y] == 2) or \
                    (occupy[x][y] != i and occupy[x][y] != 0):  # 벽이나 기사
                if not (0 < x <= L and 0 < y <= L) or chess[x][y] == 2:
                    return False
                n_i = occupy[x][y]
                if not visited[n_i]:
                    visited[n_i] = True
                    if movable(now, n_i, direc, visited):
                        pull_list.append([now, n_i, direc])
                    else:
                        return False
    return True


def occupy_map():
    occupy = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
    for i in range(1, N + 1):
        if knight[i][0] == -1:
            continue
        x_s, x_e, y_s, y_e = knight[i][0], knight[i][0] + knight[i][2], knight[i][1], knight[i][1] + knight[i][3]
        for y in range(y_s, y_e):
            for x in range(x_s, x_e):
                occupy[x][y] = i
    return occupy


for i, d in command:
    temp_damage = [0 for _ in range(N + 1)]
    visited = [False for _ in range(N + 1)]
    pull_list = []
    if knight[i][0] == -1:
        continue
    occupy = occupy_map()
    if not movable(i, i, d, visited):
        continue
    else:
        knight[i][0], knight[i][1] = knight[i][0] + dx[d], knight[i][1] + dy[d]
        for i in pull_list:
            pull(i[0], i[1], i[2])
        for i in range(1, N + 1):
            knight[i][4] -= temp_damage[i]
            knight[i][5] += temp_damage[i]
            if knight[i][4] <= 0:
                knight[i][0] = -1

ans = 0
for k in knight:
    if k[0] != -1:
        ans += k[5]
print(ans)