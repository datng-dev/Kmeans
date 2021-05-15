import pygame
from random import randint
import math
from sklearn.cluster import KMeans

# function de tao chu cho button
def create_text_render(string, color, size):
    font = pygame.font.SysFont('sans', size)
    return font.render(string, True, color)

# function tinh khoang cach giua 2 diem
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

pygame.init() #Khoi tao

screen = pygame.display.set_mode((1200, 700)) #Khoi tao man hinh ngang, doc

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (224, 224, 235)
BLACK = (0, 0, 0)
BACKGROUND_PANEL = (31, 31, 46)
WHITE = (255, 255, 255)

# cluster color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

# Tao chu cho button
text_plus = create_text_render('+', WHITE, 40)
text_minus = create_text_render('-', WHITE, 40)
text_run = create_text_render('Run', WHITE, 40)
text_random = create_text_render('Random', WHITE, 40)
text_algorithm = create_text_render('Algorithm', WHITE, 40)
text_reset = create_text_render('Reset', WHITE, 40)

K = 0
points = []
clusters = []
labels = []

while running: #Luon chay neu running = true
    clock.tick(60) #set FPS: nhay bao nhieu lan trong 1s
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos() # Get position cua con chuot

    # Draw interface
    # Draw panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500)) # (50, 50) la toa do goc tren ben trai, (700, 500) la chieu ngang va doc cua hcn
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    # K button +
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(text_plus, (860, 50)) # Ve dau cong vao button

    # K button -
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    screen.blit(text_minus, (960, 50))

    # K value
    text_k = create_text_render('K = ' + str(K), BLACK, 40)
    screen.blit(text_k, (1050, 50))

    # Run button
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    screen.blit(text_run, (890, 150))

    # Random button
    pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
    screen.blit(text_random, (865, 250))

    # Algorithm button
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit(text_algorithm, (852, 450))

    # Reset button
    pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
    screen.blit(text_reset, (875, 550))

    # draw mouse position when mouse is in panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = create_text_render('(' + str(mouse_x - 50) + ', ' + str(mouse_y - 50) + ')', WHITE, 20) 
        screen.blit(text_mouse, (mouse_x +10, mouse_y))  

    # End draw interface

    

    for event in pygame.event.get(): # Cac nut bam vao
        if event.type == pygame.QUIT: # Neu event la nut tat
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # create point on panel
                if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                    labels = [] # khi tao diem moi thi xoa het label
                    point = [mouse_x - 50, mouse_y - 50]
                    points.append(point)

                # change + button
                if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                    if K < 9:
                        K += 1

                # change - button
                if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                    if K > 0:
                        K -= 1

                # run button
                if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                    labels = []
                    if clusters == []:
                        continue
                    # assign point to closet cluster
                    for p in points:
                        distances_to_cluster = [] # do dai cua array nay tuong ung voi so cluster va se reset khi nhay qua diem moi
                        for c in clusters: # tim gia tri nho nhat tu mot diem den cac cluseter
                            distances_to_cluster.append(distance(p, c))

                        min_distance = min(distances_to_cluster)
                        label = distances_to_cluster.index(min_distance) # xem gia tri nho nhat la tu diem den cluster nao
                        labels.append(label)

                    # update clusters
                    for i in range(K):
                        sum_x = 0
                        sum_y = 0
                        count = 0
                        for j in range(len(points)):
                            if labels[j] == i:
                                sum_x += points[j][0]
                                sum_y += points[j][1]
                                count += 1
                        if count != 0:
                            new_cluster = [sum_x/count, sum_y/count]
                            clusters[i] = new_cluster #update cluster  

                # random button
                if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                    labels = []
                    clusters = []
                    for i in range(K):
                        random_point = [randint(0,700), randint(0,500)]
                        clusters.append(random_point)

                # algorithm button
                if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                    kmeans = KMeans(n_clusters=K).fit(points) # huan luyen
                    #print(kmeans.cluster_centers_) # In ra diem trung tam sau khi thuat toan toi uu hoan toan
                    labels = kmeans.predict(points) # du doan, single prediction or batch prediction
                    clusters = kmeans.cluster_centers_

                # reset button
                if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                    points = []
                    clusters = []
                    K = 0

    # Draw point 
    for i in range(len(points)):
        pygame.draw.circle(screen, WHITE, (points[i][0]+50, points[i][1]+50), 6)

        if labels == []:
            pygame.draw.circle(screen, BLACK, (points[i][0]+50, points[i][1]+50), 5)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0]+50, points[i][1]+50), 5) # Ve lai mau cua diem tron sau khi run


    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (clusters[i][0]+50, clusters[i][1]+50), 10)

    # calculate and draw error
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])

    text_error = create_text_render('Error = ' + str(int(error)), BLACK, 40)
    screen.blit(text_error, (850, 350))

    pygame.display.flip() #De nhung cai do hoa ve o tren co hieu luc

pygame.quit() # xoa tat ca nhung cai ma python dang su dung sau khi thoat
