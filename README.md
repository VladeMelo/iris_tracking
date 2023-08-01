<h1 align="center">Iris Tracking<h1>

![EyeAnnotation](https://github.com/VladeMelo/iris_tracking/assets/63476377/ce25132b-77f0-4459-bc61-6a535e1ca21b)

## 1. Objetivo

Conseguir verificar a direção na qual a pessoa esteja olhando.

## 2. Captação dos Landmarks Faciais

- A partir da biblioteca MediaPipe, há a possibilidade de captura de toda a malha facial e seus respectivos Landmarks
  - https://github.com/google/mediapipe/blob/a908d668c730da128dfa8d9f6bd25d519d006692/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
- As coordenadas X e Y chegam normalizadas, então trata-se os dados para a sua forma real

## 3. Seleção dos Landmarks da Íris e do Olho

- Os Landmarks correspondentes a cada íris são:
  - Esquerda: 474,475, 476 e 477
  - Direita: 469, 470, 471 e 472
- Os Landmarks correspondentes a cada olho são:
  - Esquerda: 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384 e 398
  - Direita: 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 e 246
- Utiliza a função minEnclosingCircle() da biblioteca OpenCV para calcular as coordenadas do centro da íris a partir dos seus respectivos Landmarks

## 4. Verificação da direção da íris

- Escolhe um dos olhos
- Calcula a distância do ponto mais extremo a esquerda do olho até o ponto mais extremo a direita do olho
  - Ex.: Se fosse o olho esquerdo seria 362 e 263
- Calcula a distância do centro da íris até um dos pontos mais extremos do olho
- Divide a distância do centro da íris até um dos extremos pela distância do extremo esquerdo até o extremo direito do olho em questão
- A partir dessa divisão obtemos o ratio que será usado para distinguir se há pessoa está olhando para a esquerda, direta ou para o centro

## Próximos Passos / Em Andamento

- Acompanhar para onde a pessoa está olhando na tela do computador/celular
- Integrar o modelo com uma aplicação Web
