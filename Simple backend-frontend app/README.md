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
1. Запускаем minikube

    ~~~
   minikube start --driver=virtualbox --no-vtx-check

2. Применяем наши конфигурации
   
    ~~~
   kubectl apply -f backend-deployment.yaml \
    kubectl apply -f backend-service.yaml \
    kubectl apply -f frontend-deployment.yaml \
    kubectl apply -f frontend-service.yaml

3. Дожидаемся пока все контейнеры будут иметь статус Running

    ~~~
   kubectl get pods

4. Получаем node-ip. (internal-ip из следующей команды)
   
    ~~~
   kubectl get nodes -o wide -n minikube
 
5. Обращаемся к фронтенду по адресу node-ip:30000 
   
    ~~~
   Invoke-WebRequest -Uri http://<node-ip>:30000 -Method POST 
                      -Headers @{ "Content-Type" = "application/json" }
                      -Body '{"message": "Hello backend!"}'

6. Получаем ответ и убеждаемся, что все корректно работает

    ~~~
   {"backend_response":{"response":"Backend recieved: Hello backend!"},
     "frontend_response":"Frontend successfully forwarded"}
    
## Удаление
Чтобы удалить все ресурсы: 

    kubectl delete -f backend-deployment.yaml
    kubectl delete -f backend-service.yaml
    kubectl delete -f frontend-deployment.yaml
    kubectl delete -f frontend-service.yaml

...или просто minikube delete если там больше ничего нет