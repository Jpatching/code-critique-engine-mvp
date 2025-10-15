/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("oq1fwbcmfbkzfz7")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "uwmr5fxa",
    "name": "status",
    "type": "select",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "maxSelect": 1,
      "values": [
        "draft",
        "in_review",
        "approved"
      ]
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("oq1fwbcmfbkzfz7")

  // remove
  collection.schema.removeField("uwmr5fxa")

  return dao.saveCollection(collection)
})
