import mongoengine as me
from Annotation import Annotation
from Room import Room
import xml.etree.ElementTree as ET


class Location(me.Document):
    name = me.StringField(max_length=50, unique=True, default='')
    room = me.ReferenceField(Room)
    isBeacon = me.BooleanField(default=False)
    isPlacement = me.BooleanField(default=False)
    annotation = me.EmbeddedDocumentField(Annotation)

    def to_xml(self):
        attribs = {x: self.__getattribute__(x) for x in self._fields}
        annot = attribs.pop('annotation')
        attribs.pop('id')
        attribs['room'] = attribs['room'].name #todo: room as reference?
        attribs = {x: str(attribs[x]) for x in attribs}
        root = ET.Element('LOCATION', attrib=attribs)
        root.append(annot.to_xml())
        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'unknown'
        return root