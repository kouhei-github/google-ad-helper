from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from config.index import Base
from sqlalchemy.sql import func


# ArticleとTags間のMany-to-Manyリレーションのための関連テーブル
article_tags_table = Table(
'article_tags', Base.metadata,
Column('article_id', Integer, ForeignKey('articles.id')),
   Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    story = Column(Text)
    title = Column(String(100), unique=True)
    description = Column(String(200))
    dev_to_id = Column(Integer, unique=True)
    # tagsへのリレーション
    tags = relationship('Tag', secondary=article_tags_table, back_populates='articles')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    # articlesへのリレーション
    articles = relationship('Article', secondary=article_tags_table, back_populates='tags')
