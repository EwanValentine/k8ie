# K8ie

## Template parser for managing Kubernetes deployments easier

## Getting started

1. Install `$ curl -O https://raw.githubusercontent.com/EwanValentine/k8ie/master/install.sh && sh ./install.sh`

2. Create a template file, such as `deployment.tmpl`. Define your Kubernetes config, you may include a service and a deployment within the same file. For example...

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{name}}
spec:
  selector:
    app: {{name}}
  ports:
    - port: {{port}}
      targetPort: {{target_port}}
  type: LoadBalancer

---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: {{name}}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{name}}
  template:
    metadata:
      labels:
        app: {{name}}
      name: {{name}}
    spec:
      containers:
      - image: nginx
        imagePullPolicy: IfNotPresent
        name: {{container_name}}
        env:
          - name: PORT
            value: "{{port}}"
        ports:
          - containerPort: {{container_port or '8080'}}
```

3. Now define a `service.yaml` file:

```yaml
name: "svc"
port: "80"
target_port: "80"

staging:
    name: "my-staging-service"
    container_name: "my-staging-service-container"

production:
    name: "my-service"
    container_name: "my-serivce-container"
```

Keys in the route of your `service.yaml` will be overwritten by items within your environment specific fields on render. So if you use --env=staging, keys defined under `staging` will override items with the same name within the document root.

4. Run your deployment `$ k8ie deploy deployment.tmpl --env=staging`.

If deployments or services already exist, they will be updated instead.
