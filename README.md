# kubernetes controller example

This example show how to implement a greeting-controller.  

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
   
5. Run controller and you can see that it has added status.phase field

   ```shell
   $ kubectl get greetings.example.io morning -o json | jq .status
   null
   ```

   ```shell
   $ whitebox-controller
   ```

   ```shell
   $ kubectl get greetings.example.io morning -o json | jq .status
   {
   "phase": "completed"
   }
   ```   

   controller logs:
   ```shell
   {"level":"info","ts":1647599154.1495922,"logger":"controller-runtime.controller","msg":"Starting Controller","controller":"greeting-controller"}
   {"level":"info","ts":1647599154.250489,"logger":"controller-runtime.controller","msg":"Starting workers","controller":"greeting-controller","worker count":1}
   {"level":"info","ts":1647599171.508439,"logger":"reconciler","msg":"Reconcile a resource","namespace":"default","name":"morning"}
   {"level":"info","ts":1647599171.5310478,"logger":"handler","msg":"Sending state","state":"{\"object\":{\"apiVersion\":\"example.io/v1alpha1\",\"kind\":\"Greeting\",\"metadata\":{\"annotations\":{\"kubectl.kubernetes.io/last-applied-configuration\":\"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"},\"creationTimestamp\":\"2022-03-18T10:26:11Z\",\"generation\":1,\"managedFields\":[{\"apiVersion\":\"example.io/v1alpha1\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kubectl.kubernetes.io/last-applied-configuration\":{}}},\"f:spec\":{\".\":{},\"f:message\":{}}},\"manager\":\"kubectl-client-side-apply\",\"operation\":\"Update\",\"time\":\"2022-03-18T10:26:11Z\"}],\"name\":\"morning\",\"namespace\":\"default\",\"resourceVersion\":\"54083\",\"uid\":\"eb46abe6-b10e-4edb-9bd1-0985b91d2bbe\"},\"spec\":{\"message\":\"Good Morning\"}}}"}
   {"level":"info","ts":1647599171.6952262,"logger":"handler","msg":"Received new state","state":"{\"object\": {\"apiVersion\": \"example.io/v1alpha1\", \"kind\": \"Greeting\", \"metadata\": {\"annotations\": {\"kubectl.kubernetes.io/last-applied-configuration\": \"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"}, \"creationTimestamp\": \"2022-03-18T10:26:11Z\", \"generation\": 1, \"managedFields\": [{\"apiVersion\": \"example.io/v1alpha1\", \"fieldsType\": \"FieldsV1\", \"fieldsV1\": {\"f:metadata\": {\"f:annotations\": {\".\": {}, \"f:kubectl.kubernetes.io/last-applied-configuration\": {}}}, \"f:spec\": {\".\": {}, \"f:message\": {}}}, \"manager\": \"kubectl-client-side-apply\", \"operation\": \"Update\", \"time\": \"2022-03-18T10:26:11Z\"}], \"name\": \"morning\", \"namespace\": \"default\", \"resourceVersion\": \"54083\", \"uid\": \"eb46abe6-b10e-4edb-9bd1-0985b91d2bbe\"}, \"spec\": {\"message\": \"Good Morning\"}, \"status\": {\"phase\": \"completed\"}}}","code":0}
   {"level":"info","ts":1647599171.695947,"logger":"reconciler","msg":"Updating resource","kind":"Greeting","namespace":"default","name":"morning"}
   {"level":"info","ts":1647599171.707314,"logger":"reconciler","msg":"Reconcile a resource","namespace":"default","name":"morning"}
   {"level":"info","ts":1647599171.7135098,"logger":"handler","msg":"Sending state","state":"{\"object\":{\"apiVersion\":\"example.io/v1alpha1\",\"kind\":\"Greeting\",\"metadata\":{\"annotations\":{\"kubectl.kubernetes.io/last-applied-configuration\":\"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"},\"creationTimestamp\":\"2022-03-18T10:26:11Z\",\"generation\":2,\"managedFields\":[{\"apiVersion\":\"example.io/v1alpha1\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kubectl.kubernetes.io/last-applied-configuration\":{}}},\"f:spec\":{\".\":{},\"f:message\":{}}},\"manager\":\"kubectl-client-side-apply\",\"operation\":\"Update\",\"time\":\"2022-03-18T10:26:11Z\"},{\"apiVersion\":\"example.io/v1alpha1\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:status\":{\".\":{},\"f:phase\":{}}},\"manager\":\"whitebox-controller\",\"operation\":\"Update\",\"time\":\"2022-03-18T10:26:11Z\"}],\"name\":\"morning\",\"namespace\":\"default\",\"resourceVersion\":\"54084\",\"uid\":\"eb46abe6-b10e-4edb-9bd1-0985b91d2bbe\"},\"spec\":{\"message\":\"Good Morning\"},\"status\":{\"phase\":\"completed\"}}}"}
   {"level":"info","ts":1647599171.789533,"logger":"handler","msg":"Received new state","state":"{\"object\": {\"apiVersion\": \"example.io/v1alpha1\", \"kind\": \"Greeting\", \"metadata\": {\"annotations\": {\"kubectl.kubernetes.io/last-applied-configuration\": \"{\\\"apiVersion\\\":\\\"example.io/v1alpha1\\\",\\\"kind\\\":\\\"Greeting\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"morning\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"message\\\":\\\"Good Morning\\\"}}\\n\"}, \"creationTimestamp\": \"2022-03-18T10:26:11Z\", \"generation\": 2, \"managedFields\": [{\"apiVersion\": \"example.io/v1alpha1\", \"fieldsType\": \"FieldsV1\", \"fieldsV1\": {\"f:metadata\": {\"f:annotations\": {\".\": {}, \"f:kubectl.kubernetes.io/last-applied-configuration\": {}}}, \"f:spec\": {\".\": {}, \"f:message\": {}}}, \"manager\": \"kubectl-client-side-apply\", \"operation\": \"Update\", \"time\": \"2022-03-18T10:26:11Z\"}, {\"apiVersion\": \"example.io/v1alpha1\", \"fieldsType\": \"FieldsV1\", \"fieldsV1\": {\"f:status\": {\".\": {}, \"f:phase\": {}}}, \"manager\": \"whitebox-controller\", \"operation\": \"Update\", \"time\": \"2022-03-18T10:26:11Z\"}], \"name\": \"morning\", \"namespace\": \"default\", \"resourceVersion\": \"54084\", \"uid\": \"eb46abe6-b10e-4edb-9bd1-0985b91d2bbe\"}, \"spec\": {\"message\": \"Good Morning\"}, \"status\": {\"phase\": \"completed\"}}}","code":0}
   ```
