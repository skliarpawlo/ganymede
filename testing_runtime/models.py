from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Unicode
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
