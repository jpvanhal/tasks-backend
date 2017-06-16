export function up(schema) {
  return schema
    .createTable('tasks', table => {
      table.increments().primary();

      table.text('name').notNullable();
      table.boolean('is_completed').notNullable().defaultTo(false);
      table.timestamps();

      table.index('created_at');
      table.index('updated_at');
    });
}

export function down(schema) {
  return schema.dropTable('tasks');
}
