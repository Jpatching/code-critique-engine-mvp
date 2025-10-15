/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("oq1fwbcmfbkzfz7")

  // remove
  collection.schema.removeField("48acz34j")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ff1mrf7e",
    "name": "architecture_json",
    "type": "json",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "maxSize": 10000
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("oq1fwbcmfbkzfz7")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "48acz34j",
    "name": "status",
    "type": "select",
    "required": true,
    "presentable": false,
    "unique": false,
    "options": {
      "maxSelect": 0,
      "values": [
        "draft",
        "in_review",
        "approved"
      ]
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ff1mrf7e",
    "name": "architecture_json",
    "type": "json",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "maxSize": 0
    }
  }))

  return dao.saveCollection(collection)
})
