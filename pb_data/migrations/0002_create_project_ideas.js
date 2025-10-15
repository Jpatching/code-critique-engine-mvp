/// <reference path="../types.d.ts" />

migrate((db) => {
  const projectIdeas = new Collection({
    name:       "project_ideas",
    type:       "base",
    system:     false,
    schema: [
      { name: "title",             type: "text",   required: true,  unique: false, options: {} },
      { name: "description",       type: "text",   required: true,  unique: false, options: {} },
      { name: "purpose_statement", type: "text",   required: false, unique: false, options: {} },
      { name: "architecture_json", type: "json",   required: false, unique: false, options: {} },
      { name: "status",            type: "select", required: true,  unique: false,
        options: { values: ["draft","in_review","approved"] }
      }
    ],
    listRule:   null,
    viewRule:   null,
    createRule: null,
    updateRule: null,
    deleteRule: null,
    options:    {},
    indexes:    []
  });

  // import only this new collection
  return Dao(db).importCollections([ projectIdeas ], false);
}, (db) => {
  // rollback: drop it
  return Dao(db).deleteCollections([ "project_ideas" ]);
});