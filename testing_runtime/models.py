from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Unicode
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Job(Base) :
    __tablename__ = "gany_jobs"

    name = Column( Unicode, primary_key=True )
    repo = Column( String )
    branch = Column( String )
    env = Column( Unicode )
    tests = Column( Unicode )

class Task(Base) :
    __tablename__ = "gany_tasks"

    task_id = Column( Integer, primary_key=True )
    job_name = Column( Unicode, ForeignKey("gany_jobs.name") )
    status = Column( Enum('WAITING', 'RUNNING', 'SUCCESS', 'FAIL') )
    add_time = Column( DateTime )
    end_time = Column( DateTime )
    log = Column( Unicode )

    job = relationship("Job", backref=backref('gany_tasks'))

class StoredTest(Base) :
    __tablename__ = "gany_tests"

    test_id = Column( Integer, primary_key=True )
    code = Column( Unicode )
    status = Column( Enum('NEW', 'ACCEPTED') )
