# Kubernetes Backend-Frontend App Deployment

## Описание
Проект представляет систему из фронтенда и бэкенда:
- Frontend принимает входящие запросы от клиента, пересылает их в Backend, получает ответ и возвращает клиенту.
- Backend обрабатывает запросы и отвечает.

## Для работы требуются:
- Docker
- Minikube
- kubectl
- *VirtualBox (см. примечание)

## Примечание:

Работа выполнялась и была проверена на Windows 11. \
В ходе выполнения работы выяснилось, что если запускать minikube на vm-driver docker, то nodeport по нужному адресу недоступен. \
Поэтому пришлось переделывать на VirtualBox и тогда все заработало \
Еще при запуске minikube пришлось прописывать опцию --no-vtx-check т.к. он жаловался на то что виртуализация недоступна, хотя на самом деле она доступна.

## Шаги для запуска
1. Сборка докер образов

   Вообще докер-образы собраны и залиты на мой DockerHub, но их можно собрать вручную
   ~~~
   docker build -t <your_repo>/my_backend:latest .\backend\
   docker build -t <your_repo>/my_frontend:latest .\frontend\
   ~~~
   После чего надо залить их на DockerHub
   ~~~
   docker push <your_repo>/my_backend:latest
   docker push <your_repo>/my_frontend:latest
   ~~~
   И сменить параметр image в deployment файлах:
   ~~~
   image: <your_repo>/my_backend:latest в backend-deployment.yaml
   image: <your_repo>/my_frontend:latest в frontend-deployment.yaml

2. Запускаем minikube

    ~~~
   minikube start --driver=virtualbox --no-vtx-check

3. Применяем наши конфигурации
   
    ~~~
   kubectl apply -f backend-deployment.yaml \
    kubectl apply -f backend-service.yaml \
    kubectl apply -f frontend-deployment.yaml \
    kubectl apply -f frontend-service.yaml

4. Дожидаемся пока все поды будут иметь статус Running

    ~~~
   kubectl get pods

5. Получаем node-ip. (internal-ip из следующей команды)
   
    ~~~
   kubectl get nodes -o wide -n minikube
 
6. Обращаемся к фронтенду по адресу node-ip:30000 
   
    ~~~
   Invoke-WebRequest -Uri http://<node-ip>:30000 -Method POST 
                      -Headers @{ "Content-Type" = "application/json" }
                      -Body '{"message": "Hello backend!"}'

7. Получаем ответ и убеждаемся, что все корректно работает

    ~~~
   {"backend_response":{"response":"Backend recieved: Hello backend!"},
     "frontend_response":"Frontend successfully forwarded"}
   ~~~
   Мы видим, что фронтенд получил наше сообщение, переслал его в бекенд, \
   а тот его получил, и отправил ответ.
    
## Удаление
Чтобы удалить все ресурсы: 

    kubectl delete -f backend-deployment.yaml
    kubectl delete -f backend-service.yaml
    kubectl delete -f frontend-deployment.yaml
    kubectl delete -f frontend-service.yaml

...или просто minikube delete если там больше ничего нет