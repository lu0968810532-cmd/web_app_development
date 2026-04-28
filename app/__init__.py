import os
from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 資料庫設定 (SQLite)
    # 確保 instance 資料夾存在
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    db_path = os.path.join(instance_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 檔案上傳設定
    upload_path = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_path
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制 16MB
    
    # 初始化擴充套件
    db.init_app(app)
    
    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.recipe import recipe_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    
    # 初始化資料庫表格 (如果尚未建立)
    with app.app_context():
        db.create_all()
        
    return app
