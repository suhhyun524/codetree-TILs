from collections import deque

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
tower = []
tower_turn = [[0 for _ in range(M)] for _ in range(N)]
dp = [[-1 for _ in range(M)] for _ in range(N)]
visited_dp = [[False for _ in range(M)] for _ in range(N)]


def bfs(sx, sy, ex, ey):
    route = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    dist = [[int(1e9) for _ in range(M)] for _ in range(N)]
    q = deque([(sx, sy, 0)])
    dist[sx][sy] = 0
    while q:
        x, y, d = q.popleft()
        for dx, dy in zip((0, 1, 0, -1), (1, 0, -1, 0)):
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= N:
                nx = N - abs(nx)
            if ny < 0 or ny >= M:
                ny = M - abs(ny)
            if arr[nx][ny] > 0 and dist[nx][ny] > d + 1:
                dist[nx][ny] = d + 1
                route[nx][ny] = [x, y]
                q.append((nx, ny, d + 1))
    return route


def laser_attack(sx, sy, ex, ey):
    route_map = bfs(sx, sy, ex, ey)
    r = []
    if route_map[ex][ey] != [-1, -1]:
        now = route_map[ex][ey]
        r.append([ex, ey])
        while now != [sx, sy]:
            r.append(now)
            now = route_map[now[0]][now[1]]
    if r:
        for x, y in r:
            if x == ex and y == ey:
                arr[x][y] -= arr[sx][sy]
            else:
                arr[x][y] -= (arr[sx][sy] // 2)
        return True
    return False


def find_tower():
    global tower
    tower = []
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0:
                tower.append([i, j, arr[i][j], tower_turn[i][j]])


def shell_attack(sx, sy, ex, ey):
    power = arr[sx][sy]
    for i in range(ex - 1, ex + 2):
        for j in range(ey - 1, ey + 2):
            if i < 0 or i >= N:
                i = N - abs(i)
            if j < 0 or j >= M:
                j = M - abs(j)
            if sx == i and sy == j:
                continue
            if ex == i and ey == j:
                arr[i][j] -= power
            else:
                arr[i][j] -= (power // 2)


def update_tower(tower, sx, sy, ex, ey):
    for t in tower:
        x, y = t[0], t[1]
        if (x == sx and y == sy) or (x == ex and y == ey):
            continue
        if t[2] == arr[x][y]:
            arr[x][y] += 1


for k in range(1, K + 1):
    visited = [[False for _ in range(M)] for _ in range(N)]
    # 가장 약한 포탑(공격자) 찾고 공격력, 공격 시점 업데이트
    find_tower()
    if len(tower) == 1:
        print(tower[0][2])
        exit(0)
    tower.sort(key=lambda x: (x[2], -tower_turn[x[0]][x[1]], -(x[0] + x[1]), -x[1]))  # 공격력, 최근 공격, 행과 열 합, 열 순 정렬
    weak = tower[0]
    arr[weak[0]][weak[1]] += N + M
    tower[0][2] += N + M
    tower_turn[weak[0]][weak[1]] = k
    # 가장 강한 포탑 찾기
    tower.sort(key=lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[1]))
    strong = tower[-1]
    if [strong[0], strong[1]] == [weak[0], weak[1]]:
        strong = tower[-2]
    if not laser_attack(weak[0], weak[1], strong[0], strong[1]):
        shell_attack(weak[0], weak[1], strong[0], strong[1])
    update_tower(tower, weak[0], weak[1], strong[0], strong[1])
ans = 0
for i in range(N):
    for j in range(M):
        ans = max(arr[i][j], ans)
print(ans)