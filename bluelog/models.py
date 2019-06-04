#!/usr/bin/env python
# -*- coding=utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    @property
    def password(self):
        raise AttributeError(u'该属性不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
#集合关系属性列表
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

#   针对哪一篇博客的评论
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#给这个属性赋值的时候，在另一侧也会自动给它赋值,标量关系属性
    post = db.relationship('Post', back_populates='comments')
    #建立自引用关系，一条评论有多个回复,这个id也可以说是回复的id
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    #remote_side 定义的一侧为 一,也就是评论
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    #对应的这一侧就是回复
    replies = db.relationship('Comment', back_populates='replied', cascade='all')

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))

