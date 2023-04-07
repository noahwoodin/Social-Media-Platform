db = new Mongo().getDB("SocialMedia")

db.createCollection('Users')
db.createCollection('Posts')
db.createCollection('Comments')
db.createCollection('Likes')
db.createCollection('Notifications')
db.createCollection('UserActivity')
