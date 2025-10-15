/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "analyses_collection",
    "created": "2025-10-15 12:00:00.000Z",
    "updated": "2025-10-15 12:00:00.000Z",
    "name": "analyses",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "analysis_user_id",
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
      },
      {
        "system": false,
        "id": "analysis_project_id",
        "name": "project_id",
        "type": "relation",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "collectionId": "projects_collection",
          "cascadeDelete": true,
          "minSelect": null,
          "maxSelect": 1,
          "displayFields": ["name"]
        }
      },
      {
        "system": false,
        "id": "analysis_prompt",
        "name": "prompt",
        "type": "text",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "min": 1,
          "max": 10000,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "analysis_code",
        "name": "code",
        "type": "text",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "min": 1,
          "max": 100000,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "analysis_scores",
        "name": "scores",
        "type": "json",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 10000
        }
      },
      {
        "system": false,
        "id": "analysis_reports",
        "name": "reports",
        "type": "json",
        "required": true,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 500000
        }
      },
      {
        "system": false,
        "id": "refactored_code",
        "name": "refactored_code",
        "type": "text",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": 100000,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "roadmap",
        "name": "roadmap",
        "type": "json",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 50000
        }
      }
    ],
    "indexes": [
      "CREATE INDEX idx_analyses_user ON analyses (user_id)",
      "CREATE INDEX idx_analyses_project ON analyses (project_id)",
      "CREATE INDEX idx_analyses_created ON analyses (created)"
    ],
    "listRule": "@request.auth.id = user_id",
    "viewRule": "@request.auth.id = user_id",
    "createRule": "@request.auth.id != \"\"",
    "updateRule": null,
    "deleteRule": "@request.auth.id = user_id",
    "options": {}
  });

  return db.createCollection(collection);
}, (db) => {
  const collection = db.findCollectionByNameOrId("analyses_collection");
  return db.deleteCollection(collection);
});
