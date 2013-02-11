from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Job(Base) :
    __tablename__ = "gany_jobs"

    name = Column( String, primary_key=True )
    repo = Column( String )
    branch = Column( String )
    env = Column( String )
    tests = Column( String )

class Task(Base) :
    __tablename__ = "gany_tasks"

    id = Column( Integer, primary_key=True )
    job_name = Column( String, ForeignKey("gany_jobs.name") )
    status = Column( Enum('WAITING', 'RUNNING', 'ERROR', 'FINISHED') )
    add_time = Column( DateTime )
    end_time = Column( DateTime )
    log = Column( String )

    job = relationship("Job", backref=backref('gany_tasks'))
