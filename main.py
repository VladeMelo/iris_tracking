import numpy as np
import cv2
import mediapipe as mp
import math

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]
LEFT_IRIS = [474,475, 476, 477]
LEFT_EYE_LEFT_MOST_LANDMARK = [362] # ponto mais a esquerda do olho esquerdo
LEFT_EYE_RIGHT_MOST_LANDMARK = [263]  # ponto mais a direita do olho esquerdo

RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246] 
RIGHT_IRIS = [469, 470, 471, 472]
RIGHT_EYE_LEFT_MOST_LANDMARK = [33] # ponto mais a esquerda do olho direito
RIGHT_EYE_RIGHT_MOST_LANDMARK = [133] # ponto mais a direita do olho direito

def get_distance(p1, p2):
    x1, y1 = np.ravel(p1)
    x2, y2 = np.ravel(p2)

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_iris_position(iris_center, left_point, right_point):
    distance_center_left = get_distance(iris_center, left_point)
    distance_left_right = get_distance(left_point, right_point)

    ratio = distance_center_left / distance_left_right

    iris_position = ''

    if ratio < 0.42:
        iris_position = 'left'
    elif ratio > 0.58:
        iris_position = 'right'
    else:
        iris_position = 'center'

    return iris_position

mp_face_mesh = mp.solutions.face_mesh

video_capture = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    refine_landmarks=True, # para detectar os pontos na malha facial respectivos da iris
) as face_mesh:
    while True:
        ret, img = video_capture.read()

        if not ret:
            break
        
        img = cv2.flip(img, 1) # inverte o img horizontalmente, para ficar que nem um espelho

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_height, img_width = rgb_img.shape[:2]

        results = face_mesh.process(rgb_img) # processa o img para detectar os pontos na malha facial 

        if not results.multi_face_landmarks:
            continue
        
        mesh_points = np.array([np.multiply([face_landmark.x, face_landmark.y], [img_width, img_height]).astype(int) for face_landmark in results.multi_face_landmarks[0].landmark])

        (left_iris_x, left_iris_y), radius_left_iris = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
        (right_iris_x, right_iris_y), radius_right_iris = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])

        center_left_iris = (int(left_iris_x), int(left_iris_y))
        center_right_iris = (int(right_iris_x), int(right_iris_y))

        cv2.circle(img, center_left_iris, int(radius_left_iris), (0, 255, 0), 1, cv2.LINE_AA)
        cv2.circle(img, center_right_iris, int(radius_right_iris), (0, 255, 0), 1, cv2.LINE_AA)

        left_iris_position = get_iris_position(center_left_iris, mesh_points[LEFT_EYE_LEFT_MOST_LANDMARK], mesh_points[LEFT_EYE_RIGHT_MOST_LANDMARK]) # basta pegar apenas a posição de uma iris

        cv2.putText(img, 'Iris Position: {}'.format(left_iris_position), (30, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow('Imagem', img)

        if cv2.waitKey(1) == ord('q'): # a cada 1 milissegundo fica no aguardo de receber a letra 'q' para ser finalizada a sessão
            break
    
video_capture.release()
cv2.destroyAllWindows()