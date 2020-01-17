## Cloud function to handle start/stop VM

Usage

```
# start VM associated to a token
curl http://<func_url>/startvm?token=<token>

# stop VM associated to a token
curl http://<func_url>/stopvm?token=<token>
```

### Local development

```

# get a service account credential json file from GCP
# place it in the current directory and name it service-account.json
# let API library know to use it as credential
# this step is not required when deployed into GCP

export GOOGLE_APPLICATION_CREDENTIALS=service-account.json

python3 -m venv
source venv/bin/activate
pip install -r requirements-dev.txt

# test using http trigger
functions-framework --target vm_action

# just run without functions framework
python main.py


```

### Deploy into GCP

```
gcloud functions deploy vm_action --runtime python37 --trigger-http

```
