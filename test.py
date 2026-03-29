from firebase_db import db

db.collection("test").add({
    "msg": "funcionando!"
})

print("OK")