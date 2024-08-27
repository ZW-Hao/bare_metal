from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey,Date,Text
from sqlalchemy.orm import relationship

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class BareMetal(Model):
    sn = Column(String(150), primary_key=True)
    ip = Column(String(150), unique = True)
    bmcip = Column(String(150))
    adress = Column(String(564))
    type = Column(String(150))
    restart = Column(Text)
    # BareMetalType = Column(String(150))

    def __repr__(self):
        return self.sn

class BareMetalProd(Model):
    sn = Column(String(150), primary_key=True)
    ip = Column(String(150), unique = True)
    bmcip = Column(String(150))
    adress = Column(String(564))
    type = Column(String(150))
    restart = Column(Text)
    # BareMetalType = Column(String(150))

    def __repr__(self):
        return self.sn