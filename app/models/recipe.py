from app.models import db
from datetime import datetime

# 多對多關聯表：食譜與標籤
recipe_tag = db.Table('recipe_tag',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    @classmethod
    def create(cls, name):
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, tag_id):
        return cls.query.get(tag_id)

    @classmethod
    def update(cls, tag_id, name):
        tag = cls.query.get(tag_id)
        if tag:
            tag.name = name
            db.session.commit()
        return tag

    @classmethod
    def delete(cls, tag_id):
        tag = cls.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return True
        return False

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 建立與 Tag 的多對多關係
    tags = db.relationship('Tag', secondary=recipe_tag, lazy='subquery',
        backref=db.backref('recipes', lazy=True))

    @classmethod
    def create(cls, title, ingredients=None, steps=None, notes=None, image_path=None, is_favorite=False, tags=None):
        recipe = cls(
            title=title,
            ingredients=ingredients,
            steps=steps,
            notes=notes,
            image_path=image_path,
            is_favorite=is_favorite
        )
        if tags:
            recipe.tags.extend(tags)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    @classmethod
    def update(cls, recipe_id, **kwargs):
        recipe = cls.query.get(recipe_id)
        if recipe:
            for key, value in kwargs.items():
                if key == 'tags':
                    recipe.tags = value
                elif hasattr(recipe, key):
                    setattr(recipe, key, value)
            db.session.commit()
        return recipe

    @classmethod
    def delete(cls, recipe_id):
        recipe = cls.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return True
        return False
