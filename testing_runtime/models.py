from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Unicode, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table
import ganymede.settings
import os

Base = declarative_base()

jobs_to_tests = Table('gany_jobs_to_tests', Base.metadata,
    Column('job_id', Integer, ForeignKey('gany_jobs.job_id')),
    Column('test_id', Integer, ForeignKey('gany_tests.test_id'))
)

class Job(Base) :
    __tablename__ = "gany_jobs"

    job_id = Column( Integer, primary_key=True )
    name = Column( Unicode, unique=True )
    repo = Column( Unicode )
    branch = Column( Unicode )
    env = Column( Unicode )
    exec_time = Column( Time )
    users = Column( Unicode )

    tests = relationship( "StoredTest", secondary = jobs_to_tests )

class Task(Base) :
    __tablename__ = "gany_tasks"

    task_id = Column( Integer, primary_key=True )
    job_id = Column( Unicode, ForeignKey("gany_jobs.job_id") )
    status = Column( Enum('waiting', 'running', 'success', 'fail'), nullable=False, default='waiting' )
    add_time = Column( DateTime )
    end_time = Column( DateTime )
    total_time = Column( Integer, default=-1 )
    log = Column( Unicode, nullable=False, default=u"" )
    result = Column( Unicode, nullable=False, default=u"[]" )
    artifacts = Column( Unicode, nullable=False, default=u"[]" )
    job = relationship("Job", backref=backref('gany_tasks'))

    def artifactsDir(self):
        return os.path.join( ganymede.settings.HEAP_PATH, "tasks", str(self.task_id), "artifacts" )

class StoredTest(Base) :
    __tablename__ = "gany_tests"

    test_id = Column( Integer, primary_key=True )
    code = Column( Unicode )
    status = Column( Enum('new', 'accepted'), nullable=False, default='new' )

import hashlib
import time

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    salt = Column(Unicode)
    email = Column(Unicode)
    role = Column(Unicode)
    allowed_databases = Column(Unicode)
    invited = Column(Integer)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def validate_password(self, password):
        return User.hash_password(password, self.salt) == self.password

    def email_hash(self):
        return hashlib.md5(self.email).hexdigest().encode('utf8')

    @staticmethod
    def hash_password(password, salt):
        return hashlib.sha1(hashlib.sha1(salt).hexdigest() + hashlib.sha1(unicode(password)).hexdigest()).hexdigest()

    @staticmethod
    def get_new_salt():
        return hashlib.sha1(str(time.time())).hexdigest()
