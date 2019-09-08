from server import db, login_manager


class Book(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String(60))
    book_name = db.Column(db.String(60))
    code = db.Column(db.String(60))
    edition = db.Column(db.String(60))
    author = db.Column(db.String(128))
    score = db.Column(db.Integer, db.ForeignKey('departments.id'))


class User(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    age = db.Column(db.String(60), db.ForeignKey('book.id'))
    email = db.Column(db.String(60), db.ForeignKey('book.id'))
    account = db.Column(db.String(60))
    password = db.Column(db.String(60))
    rank = db.Column(db.String(60))


class Review(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(60))
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    book_id = db.Column(db.String(60), db.ForeignKey('book.id'))
    review_detail_id = db.Column(db.String(60))


class ReviewDetail(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'review_detail'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(3000))
    #hoan thanh: done; dang doc: reading; chua doc: unread
    category = db.Column(db.String(60))


class Library(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    book_id = db.Column(db.String(60), db.ForeignKey('book.id'))
    mode = db.Column(db.String(60))


class Question(db.Model):
    """
    Create an Employee table
    """
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    book_id = db.Column(db.String(60), db.ForeignKey('book.id'))