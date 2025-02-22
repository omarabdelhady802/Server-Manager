from app import db


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)

    app_name = db.Column(db.String(250), nullable=False)

    app_port = db.Column(db.Integer, nullable=False)

    app_root_dir = db.Column(db.String(500), nullable=False)

    main_file_name = db.Column(db.String(100), nullable=False)

    start_app_bat_pth = db.Column(db.String(500), nullable=False)

    home_page_route = db.Column(db.String(500), nullable=True)

    app_description = db.Column(db.String(500), nullable=True)

    photo_path = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f'{self.app_name}  {self.app_description} '
