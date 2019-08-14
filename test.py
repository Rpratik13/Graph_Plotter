def quadraticDrawing(a, b, c):
    points = list()
    x = 0
    if b ** 2 - 4 * a * (c - x) >= 0:
        x1 = (-b + (b ** 2 - 4 * a * (c - x)) ** 0.5) / 2 * a
        x2 = (-b - (b ** 2 - 4 * a * (c - x)) ** 0.5) / 2 * a
        points.append([x1, x])
        points.append([x2, x])
    return points


print(quadraticDrawing(1, 0, 0))
