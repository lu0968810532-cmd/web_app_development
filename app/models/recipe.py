from app.models import db
from datetime import datetime
import logging

# 設定 logging 以利捕捉錯誤
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        """
        新增一個標籤。
        :param name: 標籤名稱
        :return: 新增的 Tag 物件，失敗則回傳 None
        """
        try:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating Tag: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有標籤。
        :return: Tag 物件列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all Tags: {e}")
            return []

    @classmethod
    def get_by_id(cls, tag_id):
        """
        透過 ID 取得單一標籤。
        :param tag_id: 標籤 ID
        :return: Tag 物件或 None
        """
        try:
            return cls.query.get(tag_id)
        except Exception as e:
            logger.error(f"Error getting Tag by ID {tag_id}: {e}")
            return None

    @classmethod
    def update(cls, tag_id, name):
        """
        更新標籤名稱。
        :param tag_id: 標籤 ID
        :param name: 新的標籤名稱
        :return: 更新後的 Tag 物件，失敗則回傳 None
        """
        try:
            tag = cls.query.get(tag_id)
            if tag:
                tag.name = name
                db.session.commit()
                return tag
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating Tag {tag_id}: {e}")
            return None

    @classmethod
    def delete(cls, tag_id):
        """
        刪除標籤。
        :param tag_id: 標籤 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            tag = cls.query.get(tag_id)
            if tag:
                db.session.delete(tag)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting Tag {tag_id}: {e}")
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
        """
        新增一筆食譜。
        :param title: 食譜標題 (必填)
        :param ingredients: 食材清單
        :param steps: 烹飪步驟
        :param notes: 個人心得
        :param image_path: 圖片路徑
        :param is_favorite: 是否加入最愛
        :param tags: 關聯的 Tag 物件列表
        :return: 新增的 Recipe 物件，失敗則回傳 None
        """
        try:
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
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating Recipe: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有食譜，依時間倒序排列。
        :return: Recipe 物件列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting all Recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        透過 ID 取得單筆食譜。
        :param recipe_id: 食譜 ID
        :return: Recipe 物件或 None
        """
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            logger.error(f"Error getting Recipe by ID {recipe_id}: {e}")
            return None

    @classmethod
    def update(cls, recipe_id, **kwargs):
        """
        更新食譜資料。
        :param recipe_id: 食譜 ID
        :param kwargs: 要更新的欄位與值 (如 title="新標題", tags=[...])
        :return: 更新後的 Recipe 物件，失敗則回傳 None
        """
        try:
            recipe = cls.query.get(recipe_id)
            if recipe:
                for key, value in kwargs.items():
                    if key == 'tags':
                        recipe.tags = value
                    elif hasattr(recipe, key):
                        setattr(recipe, key, value)
                db.session.commit()
                return recipe
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating Recipe {recipe_id}: {e}")
            return None

    @classmethod
    def delete(cls, recipe_id):
        """
        刪除食譜。
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            recipe = cls.query.get(recipe_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting Recipe {recipe_id}: {e}")
            return False
