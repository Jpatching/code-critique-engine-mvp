/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "projects_collection",
    "created": "2025-10-15 12:00:00.000Z",
    "updated": "2025-10-15 12:00:00.000Z",
    "name": "projects",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "project_name",
        "name": "name",
        "type": "text",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "min": 1,
          "max": 200,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "project_description",
        "name": "description",
        "type": "text",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": 2000,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "project_stack",
        "name": "stack",
        "type": "json",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 1000000
        }
      },
      {
        "system": false,
        "id": "architecture_type",
        "name": "architecture_type",
        "type": "select",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSelect": 1,
          "values": [
            "monolith",
            "microservices",
            "serverless",
            "modular_monolith",
            "other"
          ]
        }
      },
      {
        "system": false,
        "id": "code_style",
        "name": "code_style",
        "type": "json",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 500000
        }
      },
      {
        "system": false,
        "id": "user_id",
        "name": "user_id",
        "type": "relation",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "collectionId": "users",
          "cascadeDelete": true,
          "minSelect": null,
          "maxSelect": 1,
          "displayFields": ["email"]
        }
      }
    ],
    "indexes": [
      "CREATE INDEX idx_projects_user ON projects (user_id)"
    ],
    "listRule": "@request.auth.id = user_id",
    "viewRule": "@request.auth.id = user_id",
    "createRule": "@request.auth.id != \"\"",
    "updateRule": "@request.auth.id = user_id",
    "deleteRule": "@request.auth.id = user_id",
    "options": {}
  });

  return db.createCollection(collection);
}, (db) => {
  const collection = db.findCollectionByNameOrId("projects_collection");
  return db.deleteCollection(collection);
});
