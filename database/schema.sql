CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    ingredients TEXT,
    steps TEXT,
    notes TEXT,
    image_path VARCHAR(255),
    is_favorite BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipe_tag (
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES tags (id) ON DELETE CASCADE
);
