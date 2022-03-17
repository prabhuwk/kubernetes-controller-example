# kubernetes controller example

This example show how to implement a kuberentes controller.

Prerequisites: 

1. Install kind kubernetes cluster
```shell
$ brew install kind 
$ kind create cluster
```
2. Install jq
```shell
$ brew install jq
```
3. Install whitebox-controller
```shell
$ curl -L -O https://github.com/summerwind/whitebox-controller/releases/latest/download/whitebox-controller-darwin-amd64.tar.gz
$ tar zxvf whitebox-controller-darwin-amd64.tar.gz
$ mv whitebox-controller /usr/local/bin/
$ mv whitebox-gen /usr/local/bin/
```

Steps: 
1. Create configuration file [config.yaml]  
   It defines which resources you want to watch for the changes and which commands you want to execute when changes are made.
2. Create custom resource definition    
   ```shell
   $ kubectl apply -f crds.yaml 
   customresourcedefinition.apiextensions.k8s.io/greetings.example.io created
   $ kubectl get crds 
   NAME                   CREATED AT
   greetings.example.io   2022-03-17T12:48:21Z
   ```
3. Create custom resource  
   ```shell
   $  kubectl apply -f morning_greetings.yaml
   greeting.example.io/morning created
   $ kubectl get greeting
   NAME    AGE
   morning   5s
   ```
4. Create reconciler to add status [reconciler.py]  
   Add execute permission to reconciler file.
   ```shell
   $ chmod +x reconciler.py
   ```
5. Run whitebox controller and you can see that it has added status.phase field
   ```shell
   $ whitebox-controller
   ```
   
   output:
   ```shell
   {"level":"info","ts":1647541449.290396,"logger":"controller-runtime.metrics","msg":"metrics server is starting to listen","addr":":8080"}
   {"level":"info","ts":1647541449.290741,"logger":"controller-runtime.controller","msg":"Starting EventSource","controller":"greeting-controller","source":"kind source: example.io/v1alpha1, Kind=Greeting"}
   {"level":"info","ts":1647541449.290855,"logger":"controller-runtime.controller","msg":"Starting EventSource","controller":"greeting-controller","source":"channel source: 0xc0000ba960"}
   {"level":"info","ts":1647541449.29104,"logger":"controller-runtime.manager","msg":"starting metrics server","path":"/metrics"}
   {"level":"info","ts":1647541449.392531,"logger":"controller-runtime.controller","msg":"Starting Controller","controller":"greeting-controller"}
   {"level":"info","ts":1647541449.492862,"logger":"controller-runtime.controller","msg":"Starting workers","controller":"greeting-controller","worker count":1}
   {"level":"info","ts":1647541449.494785,"logger":"reconciler","msg":"Reconcile a resource","namespace":"default","name":"morning"}
   {"level":"info","ts":1647541449.5125089,"logger":"handler","msg":"Sending state","state":"{\"object\":{\"apiVersion\":\"example.io/v1alpha1\",\"kind\":\"Greeting\",\"metadata\":{\"annotations\":{\"kubectl.kubernetes.io/last-applied-configuration\":\"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"},\"creationTimestamp\":\"2022-03-17T17:45:06Z\",\"generation\":1,\"managedFields\":[{\"apiVersion\":\"example.io/v1alpha1\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kubectl.kubernetes.io/last-applied-configuration\":{}}},\"f:spec\":{\".\":{},\"f:message\":{}}},\"manager\":\"kubectl-client-side-apply\",\"operation\":\"Update\",\"time\":\"2022-03-17T17:45:06Z\"}],\"name\":\"morning\",\"namespace\":\"default\",\"resourceVersion\":\"35616\",\"uid\":\"74dbfd80-4519-41b0-b945-e7715fff1339\"},\"spec\":{\"message\":\"Good Morning\"}}}"}
   {"level":"info","ts":1647541449.620322,"logger":"handler","msg":"Received new state","state":"{\"object\": {\"apiVersion\": \"example.io/v1alpha1\", \"kind\": \"Greeting\", \"metadata\": {\"annotations\": {\"kubectl.kubernetes.io/last-applied-configuration\": \"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"}, \"creationTimestamp\": \"2022-03-17T17:45:06Z\", \"generation\": 1, \"managedFields\": [{\"apiVersion\": \"example.io/v1alpha1\", \"fieldsType\": \"FieldsV1\", \"fieldsV1\": {\"f:metadata\": {\"f:annotations\": {\".\": {}, \"f:kubectl.kubernetes.io/last-applied-configuration\": {}}}, \"f:spec\": {\".\": {}, \"f:message\": {}}}, \"manager\": \"kubectl-client-side-apply\", \"operation\": \"Update\", \"time\": \"2022-03-17T17:45:06Z\"}], \"name\": \"morning\", \"namespace\": \"default\", \"resourceVersion\": \"35616\", \"uid\": \"74dbfd80-4519-41b0-b945-e7715fff1339\"}, \"spec\": {\"message\": \"Good Morning\"}, \"status\": {\"phase\": \"completed\"}}}","code":0}
   {"level":"info","ts":1647541449.620617,"logger":"reconciler","msg":"Updating resource","kind":"Greeting","namespace":"default","name":"morning"}
   ```