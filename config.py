class Config():
    SECRET_KEY = 'ItsaGreatMoringin$%@#$%^SDFkl345SDFY'
    MONGODB_SETTINGS = {
    'db': 'fooddrive',
    'host': 'mongodb://fooddrive:ByS4d8dgUJgLM04z@dnc1-shard-00-00-khc8c.gcp.mongodb.net:27017,dnc1-shard-00-01-khc8c.gcp.mongodb.net:27017,dnc1-shard-00-02-khc8c.gcp.mongodb.net:27017/test?ssl=true&replicaSet=DNC1-shard-0&authSource=admin&retryWrites=true&w=majority',
    }
## Example Connection STring: mongodb+srv://<username>:<password>@dnc1-khc8c.gcp.mongodb.net/test?retryWrites=true&w=majority
## You may have to remove +srv in the URL 