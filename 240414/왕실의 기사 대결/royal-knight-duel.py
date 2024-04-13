L, N, Q = map(int, input().split())
knight = [[0, 0, 0, 0, 0, 0] for _ in range(N + 1)]
command = []
dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
chess = [list(map(int, input().split())) for _ in range(L)]
occupy = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
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
    return count


def pull(idx, direc):
    if knight[idx][0] == -1:
        return
    nx, ny = knight[idx][0] + dx[direc], knight[idx][1] + dy[direc]
    knight[idx][0], knight[idx][1] = nx, ny
    dam = damage(idx)
    knight[idx][4] -= dam
    knight[idx][5] += dam
    if knight[idx][4] <= 0:
        knight[idx][0] = -1  # 죽음


def movable(idx, direc):
    nx, ny = knight[idx][0] + dx[direc], knight[idx][1] + dy[direc]
    x_s, x_e, y_s, y_e = nx, nx + knight[idx][2], ny, ny + knight[idx][3]
    for y in range(y_s, y_e):
        for x in range(x_s, x_e):
            if (occupy[x][y] != idx and occupy[x][y] != 0) or (
                    chess[x][y] == 2 or not (0 < x <= L and 0 < y <= L)):  # 기사나 벽
                if chess[x][y] == 2 or not (0 < x <= L and 0 < y <= L):
                    return False
                i = occupy[x][y]
                nx_x, nx_e, ny_s, ny_e = x_s, x_e, y_s, y_e = knight[i][0], knight[i][0] + knight[i][2], knight[i][1], \
                                                              knight[i][1] + knight[i][3]
                if occupy[x][y] != idx and occupy[x][y] != 0:
                    if movable(i, direc):
                        pull(i, direc)
                    else:
                        return False
    else:
        return True


def occupy_map():
    for i in range(1, N + 1):
        if knight[i][0] == -1:
            continue
        x_s, x_e, y_s, y_e = knight[i][0], knight[i][0] + knight[i][2], knight[i][1], knight[i][1] + knight[i][3]
        for y in range(y_s, y_e):
            for x in range(x_s, x_e):
                occupy[x][y] = i


for i, d in command:
    occupy_map()
    if knight[i][0] == -1:
        continue
    if not movable(i, d):
        continue
    else:
        knight[i][0], knight[i][1] = knight[i][0] + dx[d], knight[i][1] + dy[d]
        pull(i, d)
ans = 0
for k in knight:
    if k[0] != -1:
        ans += k[4]
print(ans)